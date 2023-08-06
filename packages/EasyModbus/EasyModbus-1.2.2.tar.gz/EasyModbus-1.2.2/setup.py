#!/usr/bin/env python3

from distutils.core import setup

#To upload to pypi: call setup.py with the parameters sdist upload
#Copy .pypirc into home directory (Benutzer/srossmann....)

setup(
    name='EasyModbus',
    packages = ['easymodbus'],
    version      = '1.2.2',
    license      = 'GPLv3',
    author       = 'Stefan Rossmann',
    author_email = 'info@rossmann-engineering.de',
    url          = 'http://www.easymodbustcp.net',#'https://github.com/rossmann-engineering/EasyModbusTCP.PY',
    long_description='Visit www.EayModbusTCP.net for more informations and Codesamples',
    description='THE standard library for Modbus RTU and Modbus TCP - See www.EasyModbusTCP.NET for documentation',
    install_requires=[
          'pyserial'
      ],
    keywords='easymodbus modbus serial RTU TCP EasyModbusTCP',
    classifiers=[
       'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ]
)