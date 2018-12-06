# -*- coding: utf-8 -*-
import setuptools


setuptools.setup(
    name='ftpservercontext',
    version='2018.1.0',
    license='commercial',
    long_description=open('README.txt').read(),
    packages=setuptools.find_packages(),
    zip_safe = False,
    # https://www.tbz-pariv.lan/index.html/doku.php?id=python_packages#requirementstxt_vs_install_requires
    # All reusable libraries use install_requires.
    # Projects (containing only config) can use requirements.txt
    install_requires=[
        'pyftpdlib',
    ],

    include_package_data=True,

    entry_points={
        'console_scripts': [
             'serve_directory_via_ftp=ftpservercontext.console_scripts:serve_directory_via_ftp',
        ],
    }
)
