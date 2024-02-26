#!/usr/bin/python3

import logging
import pkipplib3 as pkipplib
from gevent.server import StreamServer
import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s:%(name)s:%(message)s'))

logger = colorlog.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class PrintServer(object):

    def __init__(self):
        pass

    def log_request_attributes(self, request):
        if hasattr(request, 'operation'):
            for attribute, value in request.operation.items():
                logger.debug(f'Operation attribute: {attribute}, value: {value}')
        if hasattr(request, 'job'):
            for attribute, value in request.job.items():
                logger.debug(f'Job attribute: {attribute}, value: {value}')
        if hasattr(request, 'printer'):
            for attribute, value in request.printer.items():
                logger.debug(f'Printer attribute: {attribute}, value: {value}')

    def handle(self, sock, address):
        logger.debug(f'Handling connection from {address}')
    
        # Receiving data
        data = sock.recv(8192)
        logger.debug(f'Received data: {repr(data)}')
        
        # Processing request
        try:
            body = data.split(b'\r\n\r\n', 1)[1]
            logger.debug('Extracted request body')
        except IndexError:
            body = data
            logger.warning('No separate request body found, using entire data as body')
            
        # Parsing request
        request = pkipplib.IPPRequest(body)
        request.parse()
        logger.info(f'Received request: {request}')
        
        # Log detailed request attributes if needed
        self.log_request_attributes(request)
        
        # Sending response
        response_data = self.prepare_response(request)
        sock.send(response_data)
        logger.info('Response sent to the client')

    def prepare_response(self, request):
        response_request = pkipplib.IPPRequest(operation_id=pkipplib.CUPS_GET_DEFAULT)
        response_request.operation["attributes-charset"] = ("charset", "utf-8")
        response_request.operation["attributes-natural-language"] = ("naturalLanguage", "en-us")
        return response_request.dump()

    def get_server(self, host, port):
        connection = (host, port)
        server = StreamServer(connection, self.handle)
        logger.info(f'LPR server started on: {connection}')
        return server

if __name__ == "__main__":
    ps = PrintServer()
    print_server = ps.get_server("0.0.0.0", 9100)
    print_server.serve_forever()
