# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import ftplib
import os
import tempfile
import unittest

import ftputil
from ftpservercontext import FTPServerContext


class SessionOnPort(ftplib.FTP):

    def __init__(self, host, userid, password, port):
        if not port:
            port = 0
        ftplib.FTP.__init__(self)
        self.connect(host, int(port))
        self.login(userid, password)


class Test(unittest.TestCase):
    binary_data = b'\x00\xaa\xff'

    def test_execute_job_and_create_log__ftp(self):
        temp_dir = tempfile.mkdtemp()
        with FTPServerContext(temp_dir) as ftp_context:
            with ftputil.FTPHost(ftp_context.ip_address, ftp_context.test_user_name, ftp_context.test_user_password,
                                 port=ftp_context.port, session_factory=SessionOnPort) as host:
                host.makedirs('a/b/c')
                self.assertTrue(os.path.exists(os.path.join(temp_dir, 'a', 'b', 'c')))
                with host.open('out.bin', 'wb') as fd:
                    fd.write(self.binary_data)
                self.assertEqual(self.binary_data, open(os.path.join(temp_dir, 'out.bin'), 'rb').read())
            self.assertTrue(host.closed)
