import traceback

from pyasynch import serialize_address
import logging

LOGGER = logging.getLogger(__name__)


class Node:

    def __init__(self, endpoint):
        self._endpoint = endpoint

    def _send(self, address, message, reply_to=None, error_to=None, session_id=None):
        self._endpoint.send(address, message, session_id=session_id, reply_to=reply_to, error_to=error_to)

    def _has(self, app_id):
        return hasattr(self, app_id)

    def _invoke(self,app_id:str,correlation_id:str,session_id:str,message:dict):
        func = getattr(self, app_id, None)
        if func is not None:
            message['_correlation_id'] = correlation_id
            message['_session_id'] = session_id
            result = func(**message)
            if result is None:
                return {}
            return result
        else:
            raise Exception("Function not found: "+app_id)



    def _perform(self, cluster_id: str, app_id: str, correlation_id: str, session_id: str, message: dict, reply_to=None,
                 error_to=None):
        func = getattr(self, app_id, None)
        current_address = serialize_address(self._endpoint.INBOUND_QUEUE, cluster_id, app_id)
        if func is not None:
            try:
                message['_correlation_id'] = correlation_id
                message['_session_id'] = session_id
                result = func(**message)
                if result is None:
                    return
                if type(result) is list:
                    for res in result:
                        if reply_to is not None:
                            LOGGER.info('Sending reply to {0}'.format(reply_to))
                            self._send(reply_to, res, session_id=session_id)
                        if current_address in self._endpoint._redirects:
                            for target in self._endpoint._redirects[current_address]:
                                LOGGER.info('Sending reply to {0}'.format(target))
                                self._send(target, res, session_id=session_id)
                elif type(result) is dict:
                    if reply_to is not None:
                        LOGGER.info('Sending reply to {0}'.format(reply_to))
                        self._send(reply_to, result, session_id=session_id)
                    if current_address in self._endpoint._redirects:
                        for target in self._endpoint._redirects[current_address]:
                            LOGGER.info('Sending reply to {0}'.format(target))
                            self._send(target, result, session_id=session_id)

            except Exception as e:
                if error_to is not None:
                    self._send(error_to, {'endpoint_id':self._endpoint.INBOUND_QUEUE,'app_id': app_id, 'node_id': cluster_id, 'message': str(e),
                                          'trace': traceback.format_exc()}, session_id=session_id)
                else:
                    error_address = serialize_address(self._endpoint.INBOUND_QUEUE,'system','error')
                    self._send(error_address,{'endpoint_id':self._endpoint.INBOUND_QUEUE,'app_id': app_id, 'node_id': cluster_id, 'message': str(e),
                                              'trace': traceback.format_exc()})
                LOGGER.error(
                    'Error performing {0} on {1} [{2}] : {3}\nDescription: {4}'.format(app_id, cluster_id,
                                                                                         correlation_id, str(e),
                                                                                         traceback.format_exc()))


class ErrorNode(Node):
    def receive(self,endpoint_id='', app_id='', node_id='', message='', trace='', **kwargs):
        LOGGER.error(
            'Error performing {0} on {1} [{2}] : {3}\nDescription: {4}'.format(app_id, node_id,
                                                                               endpoint_id, message,
                                                                               trace))


class SystemNode(Node):

    def status(self, **kwargs):
        return {'status': 'green'}

    def routes(self, **kwargs):
        return {'routes': self._endpoint.routes()}

    def error(self,endpoint_id='', app_id='', node_id='', message='', trace='', **kwargs):
        return {
            'endpoint_id':endpoint_id,
            'app_id':app_id,
            'node_id':node_id,
            'message':message,
            'trace':trace
        }
