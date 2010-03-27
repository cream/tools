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
import gtk

import cream.gui.builder
import cream.util

META_TEMPLATE = """<?xml version="1.0" ?>
<meta>
    <name>{name}</name>
    <comment>{comment}</comment>
    <type>module</type>
    <hash>{hash}</hash>
    <author>{author}</author>
    <license>GPLv3</license>
    <homepage>{homepage}</homepage>
    <mail>{mail}</mail>
</meta>
"""

MODULE_TEMPLATE = """#! /usr/bin/env python
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

import cream

class {class_name}(cream.Module):

    def __init__(self):

        cream.Module.__init__(self)


if __name__ == '__main__':
    {instance_name} = {class_name}()
    {instance_name}.main()
"""


class ModuleCreator:
    
    def __init__(self):
        
        self.interface = cream.gui.builder.GtkBuilderInterface('create-module.ui')
        res = self.interface.dialog.run()
        if res == 0:
            sys.exit()
            
        name = self.interface.entry_name.get_text()
        comment = self.interface.entry_description.get_text()
        author = self.interface.entry_author.get_text()
        mail = self.interface.entry_mail.get_text()
        homepage = self.interface.entry_homepage.get_text()
        
        dir = '/tmp/{0}'.format(name.replace(' ', '-').lower())
        os.mkdir(dir)
        
        meta_file = open(os.path.join(dir, 'meta.xml'), 'w')
        meta_file.write(META_TEMPLATE.format(
                name=name,
                comment=comment,
                author=author,
                mail=mail,
                homepage=homepage,
                hash=cream.util.random_hash()
                ))
        meta_file.close()
        
        class_name = ''.join([i.capitalize() for i in name.split(' ')])
        instance_name = name.replace(' ', '_').lower()
        
        module_file = open(os.path.join(dir, name.replace(' ', '-').lower()) + '.py', 'w')
        module_file.write(MODULE_TEMPLATE.format(
                class_name=class_name,
                instance_name=instance_name
                ))
        module_file.close()


if __name__ == '__main__':
    ModuleCreator()
