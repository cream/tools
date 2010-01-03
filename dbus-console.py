#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import dbus
import code

BUS_NAME = sys.argv[1]
OBJECT_PATH = sys.argv[2]

bus = dbus.SessionBus()
obj = bus.get_object(BUS_NAME, OBJECT_PATH)

data = obj.Introspect()

methods = {}

for l in data.split('\n'):
    if l.strip().startswith('<method name="'):
        m = l.strip().split('"')[1]
        methods[m] = obj.__getattr__(m)

console = code.InteractiveConsole(methods)
console.interact('''\
DBus API Console

 » bus name:    {0}
 » object path: {1}

Running interactive console...\
'''.format(BUS_NAME, OBJECT_PATH))
