#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    30.03.2016 00:30:19 CEST
# File:    create_python_module.py

import os
import sys
import shutil
import argparse

def create_module(full_name, import_name, single_file=True):
    existing_modules = os.listdir('../modules')
    for name in [full_name, import_name]:
        if name in existing_modules:
            raise ValueError('A fsc module with name {} exists already'.format(name))

    mod_dest = '../modules/' + full_name
    if single_file:
        shutil.copytree('./python_module_template', mod_dest)
        shutil.move(
            os.path.join(mod_dest, 'fsc', 'mod_tpl.py'),
            os.path.join(mod_dest, 'fsc', import_name + '.py')
        )
    else:
        shutil.copytree('./python_package_template', mod_dest)
        shutil.move(
            os.path.join(mod_dest, 'fsc', 'pkg_tpl'),
            os.path.join(mod_dest, 'fsc', import_name)
        )
        

    for path, _, filenames in os.walk(mod_dest):
        for filename in filenames:
            abspath = os.path.join(path, filename)
            with open(abspath, 'r') as f:
                text = f.read()
            with open(abspath, 'w') as f:
                f.write(text.replace('{IMPORT_NAME}', import_name).replace('{FULL_NAME}', full_name))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--module', dest='module', action='store_true', help='Create a single-file module.')
    parser.add_argument('-p', '--package', dest='package', action='store_true', help='Create a package directory.')

    parser.add_argument(dest='full_name', type=str)
    parser.add_argument(dest='import_name', type=str)
    args = parser.parse_args(sys.argv[1:])

    if args.module and args.package:
        print('Cannot create both a module and a package. Choose either -m or -p.')
    elif args.module:
        print('Creating a single-file module.')
        create_module(args.full_name, args.import_name, single_file=True)
    elif args.package:
        print('Creating a package directory.')
        create_module(args.full_name, args.import_name, single_file=False)
    else:
        print('Choose between creating single-file module [-m] and a package directory [-p] by setting the appropriate flag.')
