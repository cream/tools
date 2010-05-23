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

import sys
import dbus
import code
try:
    import readline
    import rlcompleter
    import __main__
    readline.parse_and_bind("tab: complete")
except ImportError:
    # no readline support on Windoze
    readline = None


def dbus_object_get_methods(obj):
    methods = dict()
    data = obj.Introspect()
    for line in data.split('\n'):
        if line.strip().startswith('<method name="'):
            method = line.strip().split('"')[1]
            methods[method] = getattr(obj, method)
    return methods


if __name__ == '__main__':
    try:
        BUS_NAME = sys.argv[1]
        OBJECT_PATH = sys.argv[2]
    except IndexError:
        print 'USAGE:  %s  bus_name object_path' % sys.argv[0]
        exit(1)

    bus = dbus.SessionBus()
    obj = bus.get_object(BUS_NAME, OBJECT_PATH)
    obj_methods = dbus_object_get_methods(obj)

    if readline is not None:
        readline.set_completer(rlcompleter.Completer(obj_methods).complete)

    console = code.InteractiveConsole(obj_methods)
    console.interact('''\
    DBus API Console

     » bus name:    {0}
     » object path: {1}

    Running interactive console...\
    '''.format(BUS_NAME, OBJECT_PATH))
