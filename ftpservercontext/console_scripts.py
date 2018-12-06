# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import socket

# noinspection PyUnresolvedReferences
from ftpservercontext import FTPServerContext

logger = logging.getLogger(__name__)
del (logging)

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def serve_directory_via_ftp():
    # https://pyftpdlib.readthedocs.io/en/latest/tutorial.html
    authorizer = DummyAuthorizer()
    authorizer.add_user(FTPServerContext.test_user_name, FTPServerContext.test_user_password, '.', perm='elradfmwMT')
    handler = FTPHandler
    handler.authorizer = authorizer

    port = FTPServerContext.start_port
    while port < FTPServerContext.max_port:
        address = (
            FTPServerContext.ip_address,
            port)  # do not use "localhost", otherwise old server might run on IPv6 and client on IPv4.
        try:
            server = FTPServer(address, handler)
        except socket.error as exc:
            # https://github.com/giampaolo/pyftpdlib/issues/479
            if '[Errno 98]' in str(exc):  # Address already in use
                port += 1
                continue
            raise
        break
    else:
        raise Exception('Tried all ports from %s..%s. Found no open port for the temporary ftp server' % (
            FTPServerContext.start_port,
            FTPServerContext.max_port))
    server.serve_forever()
