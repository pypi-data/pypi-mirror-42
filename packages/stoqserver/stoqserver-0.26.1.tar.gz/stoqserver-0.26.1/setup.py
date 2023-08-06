# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2015 Async Open Source <http://www.async.com.br>
## All rights reserved
##
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU Lesser General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., or visit: http://www.gnu.org/.
##
## Author(s): Stoq Team <stoq-devel@async.com.br>
##

import os
import platform
import sys

from kiwi.dist import setup, listpackages, listfiles

import stoqserver


PACKAGE = 'stoqserver'

scripts = [
    'bin/stoqserver',
]

data_files = [
    ('$datadir/webrtc',
     [os.path.join('data', 'webrtc', 'package.json'),
      os.path.join('data', 'webrtc', 'start.sh')] +
     listfiles('data', 'webrtc', '*.js')),
    ('$datadir/scripts', listfiles('data', 'scripts', '*.py')),
    ('$datadir/htsql', listfiles('data', 'htsql', '*.yml')),
]
if 'bdist_egg' not in sys.argv and platform.system() != "Windows":
    data_files.extend([
        ('/etc/sudoers.d',
         [os.path.join('data', 'sudoers.d', 'stoqserver')]),
        ('/etc/supervisor/conf.d',
         [os.path.join('data', 'supervisor', 'stoqserver.conf')]),
    ])

with open('requirements.txt') as f:
    install_requires = [l.strip() for l in f.readlines() if
                        l.strip() and not l.startswith('#')]

setup(
    name=PACKAGE,
    author="Stoq Team",
    author_email="stoq-devel@async.com.br",
    description="Stoq server",
    url="http://www.stoq.com.br",
    license="GNU LGPL 2.1 (see COPYING)",
    long_description=("Service that provides a bridge between Stoq and "
                      "stoq.link, along with other usefullnesses."),
    version=stoqserver.version_str,
    packages=listpackages('stoqserver'),
    data_files=data_files,
    install_requires=install_requires,
    scripts=scripts,
    zip_safe=True,
)
