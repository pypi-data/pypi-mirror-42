import logging
import sys
import json
from pyasynch.endpoint import Endpoint
from pyasynch.option import PassThroughOptionParser
logger = logging.getLogger(__name__)


class Environment:

    def __init__(self):
        argv = sys.argv[1:]
        parser = PassThroughOptionParser()
        parser.add_option('-c', '--config', dest='configpath', nargs=1)
        parser.add_option('-r', '--routes', dest='routespath', nargs=1)
        parser.add_option('-p', '--port', dest='webport', nargs=1)
        (opts, args) = parser.parse_args(argv)
        configpath = opts.configpath
        routespath = opts.routespath
        self.port = int(opts.webport)

        with open(configpath) as fp:
            self.config = json.load(fp)


        with open(routespath) as fp:
            self.routes = json.load(fp).get('routes',{})

        LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
                      '-35s %(lineno) -5d: %(message)s')
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

        config_endpoint = self.config['endpoint']

        amqp = config_endpoint['amqp']
        id = config_endpoint['id']
        threaded = config_endpoint.get('threaded', True)

        self.endpoint = Endpoint(url=amqp, inbound=id, threaded=threaded,port=self.port)


        for source in self.routes:
            for target in self.routes[source]:
                self.endpoint.redirect(source, target)

    def register_node(self,node_id,node_reference):
        self.endpoint.register_node(node_id,node_reference)

    def _prerun(self):
        for route in self.endpoint.routes():
            logger.info("Registered route: {0}".format(route))

    def _postrun(self):
        pass

    def run(self):
        self._prerun()
        self.endpoint.run()
        self._postrun()

    def stop(self):
        self.endpoint.stop()
