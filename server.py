# Copyright (C) 2013  Lukas Rist <glaslos@gmail.com>
# Copyright (C) 2024  James Brine <james@jamesbrine.com.au>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

#!/usr/bin/python3

import logging
from pkipplib import pkipplib
from gevent.server import StreamServer
import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s:%(name)s:%(message)s'))

logger = colorlog.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class PrintServer(object):

    def __init__(self):
        pass

    def handle(self, sock, address):
        logger.info(f'Connection from {address}')
        data = sock.recv(8192)
        logger.debug(f'Received data: {repr(data)}')

        try:
            body = data.split(b'\r\n\r\n', 1)[1]
        except IndexError:
            body = data
        request = pkipplib.IPPRequest(body)
        request.parse()
        logger.info(f'Received request: {request}')
        
        if hasattr(request, 'operation'):
            for attribute, value in request.operation.items():
                logger.debug(f'Request operation attribute: {attribute}, value: {value}')
        if hasattr(request, 'job'):
            for attribute, value in request.job.items():
                logger.debug(f'Request job attribute: {attribute}, value: {value}')
        if hasattr(request, 'printer'):
            for attribute, value in request.printer.items():
                logger.debug(f'Request printer attribute: {attribute}, value: {value}')

        request = pkipplib.IPPRequest(operation_id=pkipplib.CUPS_GET_DEFAULT)
        request.operation["attributes-charset"] = ("charset", "utf-8")
        request.operation["attributes-natural-language"] = ("naturalLanguage", "en-us")
        response_data = request.dump().encode('utf-8')
        sock.send(response_data)
        logger.info('Response sent to the client')

    def get_server(self, host, port):
        connection = (host, port)
        server = StreamServer(connection, self.handle)
        logger.info(f'LPR server started on: {connection}')
        return server

if __name__ == "__main__":
    ps = PrintServer()
    print_server = ps.get_server("localhost", 9100)
    print_server.serve_forever()
