import contextlib
import os
import socket
import sys
from functools import partial
from http.server import CGIHTTPRequestHandler
from http.server import SimpleHTTPRequestHandler
from http.server import ThreadingHTTPServer

from PyQt5.QtCore import QThread

"""Run an HTTP server on port 8000 (or the port argument).

Args:
    server_class (_type_, optional): Class of server. Defaults to DualStackServer.
    handler_class (_type_, optional): Class of handler. Defaults to SimpleHTTPRequestHandler.
    port (int, optional): Specify alternate port. Defaults to 8000.
    bind (str, optional): Specify alternate bind address. Defaults to '127.0.0.1'.
    cgi (bool, optional): Run as CGI Server. Defaults to False.
    directory (_type_, optional): Specify alternative directory. Defaults to os.getcwd().
"""


class DualStackServer(ThreadingHTTPServer):
    def server_bind(self):
        # suppress exception when protocol is IPv4
        with contextlib.suppress(Exception):
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        return super().server_bind()


class HttpServerThread(QThread):
    def __init__(self, server_class=DualStackServer, port=8000, bind='127.0.0.1', cgi=False, directory=os.getcwd()):
        super().__init__()
        self.server_class = server_class
        self.port = port
        self.bind = bind
        self.cgi = cgi
        self.directory = directory

    def run(self):
        handler_class = partial(SimpleHTTPRequestHandler, directory=self.directory)
        if self.cgi:
            handler_class = partial(CGIHTTPRequestHandler, directory=self.directory)

        with self.server_class((self.bind, self.port), handler_class) as httpd:
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                sys.exit(0)
