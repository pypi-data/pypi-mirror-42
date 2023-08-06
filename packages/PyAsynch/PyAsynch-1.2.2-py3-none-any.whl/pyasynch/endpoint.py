import json
from queue import Queue
from threading import Thread
from uuid import uuid4
import logging
import tornado.escape

import tornado
import tornado.web
from tornado.options import options, define
import tornado.httpserver
import tornado.ioloop
import  pika.adapters.tornado_connection

from pyasynch.encoder import Encoder, decoder

LOGGER = logging.getLogger(__name__)

import pika
import pika.adapters

from pyasynch import deserialize_address, serialize_address
from pyasynch.node import SystemNode


class WebHandler(tornado.web.RequestHandler):

    def prepare(self):
        super(WebHandler, self).prepare()
        self.json_data = None
        if self.request.body:
            try:
                self.json_data = tornado.escape.json_decode(self.request.body)
            except ValueError:
                # TODO: handle the error
                pass

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'PUT,POST, GET, OPTIONS, DELETE')
        self.set_header("Access-Control-Allow-Headers","*")
        self.set_header("Access-Control-Allow-Headers", "access-control-allow-origin,authorization,content-type")
        self.set_header('Access-Control-Allow-Credentials','true')
        self.set_header('Access-Control-Expose-Headers', "true")



    def get_argument(self, name, default=object(), strip=True):
        # TODO: there's more arguments in the default get_argument() call
        # TODO: handle other method types
        if self.request.method in ['POST', 'PUT'] and self.json_data:
            return self.json_data.get(name, default)
        else:
            return super(WebHandler, self).get_argument(name, default, strip=strip)

    @tornado.web.asynchronous
    def post(self, method):
        try:
            headers = self.request.headers
            ip = self.request.remote_ip
            url = self.request.path
            request = self.json_data
            additionals = {'ip':ip}
            req = {**request,**additionals}
            data = self.invoke(method, headers, req)
            response = {"route": url, "payload": data}
            self.write(json.dumps(response, cls=Encoder))
            self.finish()
        except Exception as e:
            self.error(500, str(e))

    def error(self, code, message):
        self.clear()
        self.set_status(code)
        self.write(json.dumps({"error": message}, cls=Encoder))
        self.finish()

    @tornado.web.asynchronous
    def options(self,method):
        # no body
        self.set_status(204)
        self.finish()

    @tornado.web.asynchronous
    def get(self, method):
        try:
            headers = self.request.headers
            ip = self.request.remote_ip
            url = self.request.path
            request = self.json_data
            additionals = {'ip':ip}
            req = {**request,**additionals}
            data = self.invoke(method, headers, req)
            response = {"route": url, "payload": data}
            self.write(json.dumps(response, cls=Encoder))
            self.finish()
        except Exception as e:
            self.error(500, str(e))

    def invoke(self, method, headers, message, **kwargs):
        parts = method.split('/')
        cluster_id = parts[0]
        app_id = parts[1]
        correlation_id = headers.get('correlation_id', None)
        session_id = headers.get('correlation_id', None)
        return self.application.endpoint.invoke(cluster_id, app_id, correlation_id, session_id, message)


class WebServer(tornado.web.Application):
    ' Tornado Webserver Application...'

    def __init__(self, endpoint):
        # Url to its handler mapping.
        self.endpoint = endpoint
        handlers = [
            (r"/(?P<method>\S+)", WebHandler)
        ]

        # Other Basic Settings..
        settings = dict(
            # cookie_secret = options.cookie_secret,
            # login_url="/signin",
            # template_path = os.path.join(os.path.dirname(__file__),"templates"),
            # static_path = os.path.join(os.path.dirname(__file__),"static"),
            # xsrf_cookies=True,
            debug=True

        )

        # Initialize Base class also.
        tornado.web.Application.__init__(self, handlers, **settings)


class Endpoint(object):
    """This is an example consumer that will handle unexpected interactions
    with RabbitMQ such as channel and connection closures.

    If RabbitMQ closes the connection, it will reopen it. You should
    look at the output, as there are limited reasons why the connection may
    be closed, which usually are tied to permission related issues or
    socket timeouts.

    If the channel is closed, it will indicate a problem with one of the
    commands that were issued and that should surface in the output as well.

    """
    EXCHANGE = 'message'
    EXCHANGE_TYPE = 'topic'

    def __init__(self, url, inbound, publish_interval=0.1, threaded=False, port=8081):
        """Create a new instance of the consumer class, passing in the AMQP
        URL used to connect to RabbitMQ.

        :param str url: The AMQP url to connect with

        """
        self._threaded = threaded
        self._connection = None
        self._channel = None
        self._acked = 0
        self._nacked = 0
        self._deliveries = []
        self._closing = False
        self._consumer_tag = None
        self._message_number = 0
        self._stopping = False
        self._url = url
        self.INBOUND_QUEUE = inbound
        self._outbounds = []
        self.PUBLISH_INTERVAL = publish_interval
        self.INBOUND_ROUTING_KEY = self.INBOUND_QUEUE
        self.inputs = Queue()
        self._outputs = Queue()
        self._nodes = {}
        self._enabled_delivery = False
        self._nodes['system'] = SystemNode(self)
        self._redirects = {}
        self._port = port

    def send(self, address, message, reply_to=None, error_to=None, session_id=None):
        """Sends a message to a specified address

        :address: pin://endpoint_id/cluster_id/app_id
        :message: json message dict to be sent
        :reply_to: Optional reply pin:// address
        :error_to: Optional error pin:// address
        :session_id: Optional conversational session id

        :rtype: str
        """
        endpoint_id, cluster_id, app_id = deserialize_address(address)

        if endpoint_id in self._outbounds:
            correlation_id = str(uuid4())
            self._outputs.put(
                [endpoint_id, cluster_id, app_id, correlation_id, session_id, message, reply_to, error_to])
            return correlation_id
        return None

    def routes(self):
        """Returns a full list of the available inbound endpoints"""
        ret = []
        for cluster_id in self._nodes:
            method_list = [app_id for app_id in dir(self._nodes[cluster_id]) if
                           callable(getattr(self._nodes[cluster_id], app_id))]
            for app_id in method_list:
                if not app_id.startswith('_'):
                    ret.append(serialize_address(self.INBOUND_QUEUE, cluster_id, app_id))
        return ret

    def redirect(self, source, target):
        '''
        Redirects an output of an endpoint to another endpoint
        :param source:
        :param target:
        :return:
        '''
        if deserialize_address(source)[0] != self.INBOUND_QUEUE:
            return
        if source not in self._redirects:
            self._redirects[source] = []
        if target not in self._redirects[source]:
            target_id = deserialize_address(target)[0]
            if target_id not in self._outbounds:
                self._outbounds.append(target_id)
            self._redirects[source].append(target)

    def register_node(self, node_id, node_reference):
        """This method adds a new application to the current consumer part, by specification
        :cluster_id: the Cluster id string
        :cluster_reference: The Cluster class reference

        """
        if node_id == 'system':
            raise Exception('Cluster with name "system" cannot be registered')
        if node_id not in self._nodes:
            LOGGER.info('Registering cluster: {0}'.format(node_id))
            self._nodes[node_id] = node_reference

    def connect(self):
        """This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method
        will be invoked by pika.

        :rtype: pika.SelectConnection

        """
        LOGGER.info('Connecting to %s', self._url)

        return pika.adapters.tornado_connection.TornadoConnection(pika.URLParameters(self._url),
                                                                  self.on_connection_open,
                                                                  stop_ioloop_on_close=False)
        #return pika.SelectConnection(pika.URLParameters(self._url),
        #                             self.on_connection_open,
        #                             stop_ioloop_on_close=False)

    def close_connection(self):
        """This method closes the connection to RabbitMQ."""
        LOGGER.info('Closing connection')
        self._closing = True
        self._connection.close()

    def add_on_connection_close_callback(self):
        """This method adds an on close callback that will be invoked by pika
        when RabbitMQ closes the connection to the publisher unexpectedly.

        """
        LOGGER.info('Adding connection close callback')
        self._connection.add_on_close_callback(self.on_connection_closed)

    def on_connection_closed(self, connection, reply_code, reply_text):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.

        :param pika.connection.Connection connection: The closed connection obj
        :param int reply_code: The server provided reply_code if given
        :param str reply_text: The server provided reply_text if given

        """
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            LOGGER.warning('Connection closed, reopening in 5 seconds: (%s) %s',
                           reply_code, reply_text)
            self._connection.add_timeout(5, self.reconnect)

    def on_connection_open(self, unused_connection):
        """This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.

        :type unused_connection: pika.SelectConnection

        """
        LOGGER.info('Connection opened')
        self.add_on_connection_close_callback()
        self.open_channel()

    def reconnect(self):
        """Will be invoked by the IOLoop timer if the connection is
        closed. See the on_connection_closed method.

        """
        # This is the old connection IOLoop instance, stop its ioloop
        self._connection.ioloop.stop()

        if not self._closing:
            # Create a new connection
            self._connection = self.connect()

            # There is now a new connection, needs a new ioloop to run
            self._connection.ioloop.start()

    def add_on_channel_close_callback(self):
        """This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.

        """
        LOGGER.info('Adding channel close callback')
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_text):
        """Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.

        :param pika.channel.Channel: The closed channel
        :param int reply_code: The numeric reason the channel was closed
        :param str reply_text: The text reason the channel was closed

        """
        LOGGER.warning('Channel %i was closed: (%s) %s',
                       channel, reply_code, reply_text)
        if not self._closing:
            self._connection.close()

    def on_channel_open(self, channel):
        """This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.

        Since the channel is now open, we'll declare the exchange to use.

        :param pika.channel.Channel channel: The channel object

        """
        LOGGER.info('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.EXCHANGE)

    def setup_exchange(self, exchange_name):
        """Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declareok method will
        be invoked by pika.

        :param str|unicode exchange_name: The name of the exchange to declare

        """
        LOGGER.info('Declaring exchange %s', exchange_name)
        self._channel.exchange_declare(self.on_exchange_declareok,
                                       exchange_name,
                                       self.EXCHANGE_TYPE)

    def on_exchange_declareok(self, unused_frame):
        """Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC
        command.

        :param pika.Frame.Method unused_frame: Exchange.DeclareOk response frame

        """
        LOGGER.info('Exchange declared')
        self.setup_inbound_queue(self.INBOUND_QUEUE)
        for outbound in self._outbounds:
            self.setup_outbound_queue(outbound)

    def setup_inbound_queue(self, queue_name):
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.

        :param str|unicode queue_name: The name of the queue to declare.

        """
        LOGGER.info('Declaring queue %s', queue_name)
        self._channel.queue_declare(self.on_inbound_queue_declareok, queue_name)

    def setup_outbound_queue(self, queue_name):
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.

        :param str|unicode queue_name: The name of the queue to declare.

        """
        LOGGER.info('Declaring queue %s', queue_name)
        self._channel.queue_declare(self.on_outbound_queue_declareok, queue_name)

    def on_inbound_queue_declareok(self, method_frame):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.

        :param pika.frame.Method method_frame: The Queue.DeclareOk frame

        """
        LOGGER.info('Binding %s to %s with %s',
                    self.EXCHANGE, self.INBOUND_QUEUE, self.INBOUND_ROUTING_KEY)
        self._channel.queue_bind(self.on_inbound_bindok, self.INBOUND_QUEUE,
                                 self.EXCHANGE, self.INBOUND_ROUTING_KEY)

    def on_outbound_queue_declareok(self, method_frame):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.

        :param pika.frame.Method method_frame: The Queue.DeclareOk frame

        """
        queue = method_frame.method.queue
        LOGGER.info('Binding %s to %s with %s',
                    self.EXCHANGE, queue, queue)
        self._channel.queue_bind(self.on_outbound_bindok, queue,
                                 self.EXCHANGE, queue)

    def on_delivery_confirmation(self, method_frame):
        """Invoked by pika when RabbitMQ responds to a Basic.Publish RPC
        command, passing in either a Basic.Ack or Basic.Nack frame with
        the delivery tag of the message that was published. The delivery tag
        is an integer counter indicating the message number that was sent
        on the channel via Basic.Publish. Here we're just doing house keeping
        to keep track of stats and remove message numbers that we expect
        a delivery confirmation of from the list used to keep track of messages
        that are pending confirmation.

        :param pika.frame.Method method_frame: Basic.Ack or Basic.Nack frame

        """
        confirmation_type = method_frame.method.NAME.split('.')[1].lower()
        LOGGER.info('Received %s for delivery tag: %i',
                    confirmation_type,
                    method_frame.method.delivery_tag)
        if confirmation_type == 'ack':
            self._acked += 1
        elif confirmation_type == 'nack':
            self._nacked += 1
        self._deliveries.remove(method_frame.method.delivery_tag)
        LOGGER.info('Published %i messages, %i have yet to be confirmed, '
                    '%i were acked and %i were nacked',
                    self._message_number, len(self._deliveries),
                    self._acked, self._nacked)

    def enable_delivery_confirmations(self):
        """Send the Confirm.Select RPC method to RabbitMQ to enable delivery
        confirmations on the channel. The only way to turn this off is to close
        the channel and create a new one.

        When the message is confirmed from RabbitMQ, the
        on_delivery_confirmation method will be invoked passing in a Basic.Ack
        or Basic.Nack method from RabbitMQ that will indicate which messages it
        is confirming or rejecting.

        """
        LOGGER.info('Issuing Confirm.Select RPC command')
        if not self._enabled_delivery:
            self._channel.confirm_delivery(self.on_delivery_confirmation)
            self._enabled_delivery = True

    def publish_message(self):
        """If the class is not stopping, publish a message to RabbitMQ,
        appending a list of deliveries with the message number that was sent.
        This list will be used to check for delivery confirmations in the
        on_delivery_confirmations method.

        Once the message has been sent, schedule another message to be sent.
        The main reason I put scheduling in was just so you can get a good idea
        of how the process is flowing by slowing down and speeding up the
        delivery intervals by changing the PUBLISH_INTERVAL constant in the
        class.

        """
        if self._stopping:
            return

        if not self._outputs.empty():
            queue, cluster_id, app_id, correlation_id, session_id, message, reply_to, error_to = self._outputs.get()

            # message = {u'مفتاح': u' قيمة',
            #           u'键': u'值',
            #           u'キー': u'値'}
            LOGGER.info('OUTCOMING: {0}'.format(serialize_address(queue, cluster_id, app_id)))
            LOGGER.info('Publishing message to {0} : {1}'.format(cluster_id, app_id))
            properties = pika.BasicProperties(correlation_id=correlation_id,
                                              reply_to=reply_to,
                                              content_type='application/json',
                                              headers={'session_id': session_id,
                                                       'error_to': error_to,
                                                       'cluster_id': cluster_id,
                                                       'app_id': app_id})

            self._channel.basic_publish(self.EXCHANGE, queue,
                                        json.dumps(message, ensure_ascii=False, cls=Encoder),
                                        properties)
            self._message_number += 1
            self._deliveries.append(self._message_number)
            LOGGER.info('Published message # %i', self._message_number)
        self.schedule_next_message()

    def schedule_next_message(self):
        """If we are not closing our connection to RabbitMQ, schedule another
        message to be delivered in PUBLISH_INTERVAL seconds.

        """
        if self._stopping:
            return
        LOGGER.debug('Scheduling next message for %0.1f seconds',
                     self.PUBLISH_INTERVAL)
        self._connection.add_timeout(self.PUBLISH_INTERVAL,
                                     self.publish_message)

    def start_publishing(self):
        """This method will enable delivery confirmations and schedule the
        first message to be sent to RabbitMQ

        """
        LOGGER.info('Issuing consumer related RPC commands')
        self.enable_delivery_confirmations()
        self.schedule_next_message()

    def on_outbound_bindok(self, unused_frame):
        """This method is invoked by pika when it receives the Queue.BindOk
        response from RabbitMQ. Since we know we're now setup and bound, it's
        time to start publishing."""
        LOGGER.info('Queue bound')
        self.start_publishing()

    def add_on_cancel_callback(self):
        """Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.

        """
        LOGGER.info('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        """Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.

        :param pika.frame.Method method_frame: The Basic.Cancel frame

        """
        LOGGER.info('Consumer was cancelled remotely, shutting down: %r',
                    method_frame)
        if self._channel:
            self._channel.close()

    def acknowledge_message(self, delivery_tag):
        """Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.

        :param int delivery_tag: The delivery tag from the Basic.Deliver frame

        """
        LOGGER.info('Acknowledging message %s', delivery_tag)
        self._channel.basic_ack(delivery_tag)

    def on_message(self, unused_channel, basic_deliver, properties, body):
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.

        :param pika.channel.Channel unused_channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param str|unicode body: The message body

        """

        message = json.loads(body, object_hook=decoder)
        cluster_id = properties.headers.get('cluster_id', None)
        correlation_id = properties.correlation_id
        session_id = properties.headers.get('session_id', None)
        app_id = properties.headers.get('app_id', None)
        reply_to = getattr(properties, 'reply_to', None)
        error_to = None
        if 'error_to' in properties.headers:
            error_to = properties.headers['error_to']
        if message is None:
            message = {}
        LOGGER.info('INCOMING: {0}'.format(serialize_address(self.INBOUND_QUEUE, cluster_id, app_id)))

        LOGGER.info('Received message # %s from %s: %s',
                    basic_deliver.delivery_tag, app_id, str(list(message.keys())))

        if cluster_id in self._nodes:
            if self._nodes[cluster_id]._has(app_id):
                if self._threaded:
                    thread = Thread(target=self._nodes[cluster_id]._perform,
                                    args=(cluster_id, app_id, correlation_id, session_id, message, reply_to, error_to))
                    thread.setDaemon(False)
                    thread.start()
                else:
                    self._nodes[cluster_id]._perform(cluster_id, app_id, correlation_id, session_id, message,
                                                     reply_to, error_to)
            else:
                LOGGER.warning('Cannot send message since cluster is not registered: {0}'.format(cluster_id))

        self.acknowledge_message(basic_deliver.delivery_tag)

    def invoke(self, cluster_id, app_id, correlation_id, session_id, message):
        LOGGER.info('Invoking: {0}/{1}'.format(cluster_id,app_id))
        if cluster_id in self._nodes:
            if self._nodes[cluster_id]._has(app_id):
                return self._nodes[cluster_id]._invoke(app_id, correlation_id, session_id, message)
            else:
                LOGGER.warning('Cannot send message since cluster is not registered: {0}'.format(cluster_id))
                raise Exception("Endpoint cannot be found: {0}".format(cluster_id))

    def on_cancelok(self, unused_frame):
        """This method is invoked by pika when RabbitMQ acknowledges the
        cancellation of a consumer. At this point we will close the channel.
        This will invoke the on_channel_closed method once the channel has been
        closed, which will in-turn close the connection.

        :param pika.frame.Method unused_frame: The Basic.CancelOk frame

        """
        LOGGER.info('RabbitMQ acknowledged the cancellation of the consumer')
        self.close_channel()

    def stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.

        """
        if self._channel:
            LOGGER.info('Sending a Basic.Cancel RPC command to RabbitMQ')
            if not self._stopping:
                self._channel.basic_cancel(self.on_cancelok, self._consumer_tag)

    def start_consuming(self):
        """This method sets up the consumer by first calling
        add_on_cancel_callback so that the object is notified if RabbitMQ
        cancels the consumer. It then issues the Basic.Consume RPC command
        which returns the consumer tag that is used to uniquely identify the
        consumer with RabbitMQ. We keep the value to use it when we want to
        cancel consuming. The on_message method is passed in as a callback pika
        will invoke when a message is fully received.

        """
        LOGGER.info('Issuing consumer related RPC commands')
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self.on_message,
                                                         self.INBOUND_QUEUE)

    def on_inbound_bindok(self, unused_frame):
        """Invoked by pika when the Queue.Bind method has completed. At this
        point we will start consuming messages by calling start_consuming
        which will invoke the needed RPC commands to start the process.

        :param pika.frame.Method unused_frame: The Queue.BindOk response frame

        """
        LOGGER.info('Queue bound')
        self.start_consuming()

    def close_channel(self):
        """Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.

        """
        LOGGER.info('Closing the channel')
        if self._channel:
            self._channel.close()

    def open_channel(self):
        """Open a new channel with RabbitMQ by issuing the Channel.Open RPC
        command. When RabbitMQ responds that the channel is open, the
        on_channel_open callback will be invoked by pika.

        """
        LOGGER.info('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def run(self):
        """Run the example consumer by connecting to RabbitMQ and then
        starting the IOLoop to block and allow the SelectConnection to operate.

        """

        self._application = WebServer(self)
        self._webserver = tornado.httpserver.HTTPServer(self._application)
        self._webserver.listen(self._port)
        self._connection = self.connect()
        self._connection.ioloop.start()


    def stop(self):
        """Cleanly shutdown the connection to RabbitMQ by stopping the consumer
        with RabbitMQ. When RabbitMQ confirms the cancellation, on_cancelok
        will be invoked by pika, which will then closing the channel and
        connection. The IOLoop is started again because this method is invoked
        when CTRL-C is pressed raising a KeyboardInterrupt exception. This
        exception stops the IOLoop which needs to be running for pika to
        communicate with RabbitMQ. All of the commands issued prior to starting
        the IOLoop will be buffered but not processed.

        """
        LOGGER.info('Stopping')
        self._stopping = True
        self._closing = True
        self.stop_consuming()
        self.close_channel()
        self.close_connection()
        self._connection.ioloop.start()
        LOGGER.info('Stopped')
