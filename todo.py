#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

import os
import sys
import re

EXPR = re.compile(r'.*TODO.*')

def scan(path):

    path = os.path.abspath(path)
    files = os.listdir(path)
    res = []

    for file in files:
        if os.path.isdir(os.path.join(path, file)):
            res.extend(scan(os.path.join(path, file)))
        else:
            if file.endswith('.py'):
                res.append(os.path.join(path, file))

    return res

res = scan(sys.argv[1])

for i in res:
    fh = open(i)
    ln = 1

    header_printed = False
    for l in fh.readlines():
        if EXPR.match(l):
            if not header_printed:
                header_printed = True
                print "\nFile: {0}:".format(i)
            print "{0}: {1}".format(ln, l.strip())
        ln += 1
