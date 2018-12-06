ftpservercontext
================

You need a temporary ftp server in your python unittests?

This small library provides you the class called `FTPServerContext`.

Usage
-----

        temp_dir = tempfile.mkdtemp()
        with FTPServerContext(temp_dir) as ftp_context:
            # now you have these variables for your test your ftp client code:
            ftp_context.ip_address
            ftp_context.test_user_name
            ftp_context.test_user_password
            ftp_context.port


Internals
---------

With subprocess.Popen() a script called `serve_directory_via_ftp` gets called.

You provide `FTPServerContext` a directory and the ftp server serves this directory via ftp running on '127.0.0.1' and a matching
open port.


You can see a working example in the unittest: https://github.com/tbz-pariv/ftpservercontext/blob/master/ftpservercontext/tests/test_ftpservercontext.py


Feedback
--------

Feedback is welcome. Just open an issue at github, even if you just want to say "thank you".

