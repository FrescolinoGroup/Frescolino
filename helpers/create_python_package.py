#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    30.03.2016 00:30:19 CEST
# File:    create_python_package.py

import os
import sys
import shutil

def create_package(full_name, import_name):
    existing_modules = os.listdir('../modules')
    for name in [full_name, import_name]:
        if name in existing_modules:
            raise ValueError('A module with name {} exists already'.format(name))

    module_dest = '../modules/' + full_name
    shutil.copytree('./python_package_template', module_dest)
    shutil.move(
        os.path.join(module_dest, 'fsc', 'pkg_tpl'),
        os.path.join(module_dest, 'fsc', import_name)
    )

    for path, _, filenames in os.walk(module_dest):
        for filename in filenames:
            abspath = os.path.join(path, filename)
            with open(abspath, 'r') as f:
                text = f.read()
            with open(abspath, 'w') as f:
                f.write(text.replace('{PKGNAME}', import_name))

def main():
    if len(sys.argv) != 3:
        print('usage: python create_python_package.py FULL_NAME IMPORT_NAME')
    else:
        create_package(full_name=sys.argv[1], import_name=sys.argv[2])

if __name__ == "__main__":
    main()
