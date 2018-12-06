# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
import io
import re
import subprocess
import tempfile
import time


class FTPServerContext(object):
    start_port = 2121
    max_port = 2300
    wait_seconds = 12
    detect_running_string = 'passive ports:'
    ip_address = '127.0.0.1'
    test_user_name = 'testuser-ftp'
    test_user_password = 'testuser-ftp-pwd'

    def __init__(self, directory_to_serve):
        self.directory_to_serve = directory_to_serve

    def __enter__(self):
        cmd = ['serve_directory_via_ftp']
        self.temp_file = tempfile.NamedTemporaryFile(prefix=self.__class__.__name__)
        try:
            self.pipe = subprocess.Popen(cmd, cwd=self.directory_to_serve, stderr=subprocess.STDOUT,
                                         stdout=self.temp_file)
        except OSError as exc:
            raise OSError('cmd failed: %s. This scripts should get created via pip or "setup.py develop". %s' % (
                cmd, exc))
        start = datetime.datetime.now()
        max_wait = datetime.timedelta(seconds=self.wait_seconds)
        while start + max_wait > datetime.datetime.now():
            if self.is_ftp_server_running():
                return self
            time.sleep(0.1)
        raise Exception('Timeout reached. FTP server did not start: %s' % self.ftp_server_output)

    def __exit__(self, *args):
        self.pipe.kill()
        self.temp_file.close()

    @property
    def ftp_server_output(self):
        return io.open(self.temp_file.name, 'rt').read()

    def is_ftp_server_running(self):
        ftp_server_output = self.ftp_server_output
        if 'Traceback' in ftp_server_output:
            raise Exception(ftp_server_output)
        alive = bool(self.detect_running_string in ftp_server_output)
        if not alive:
            return False
        match = re.search('starting FTP server on \S+:(\d+)', ftp_server_output, re.MULTILINE)
        assert match, ftp_server_output
        self.port = int(match.group(1))
        return True
