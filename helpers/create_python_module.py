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

def create_module(full_name, import_name):
    existing_modules = os.listdir('../modules')
    for name in [full_name, import_name]:
        if name in existing_modules:
            raise ValueError('A fsc module with name {} exists already'.format(name))

    mod_dest = '../modules/' + full_name
    shutil.copytree('python_package_template', mod_dest)
    shutil.move(
        os.path.join(mod_dest, 'fsc', 'pkg_tpl'),
        os.path.join(mod_dest, 'fsc', import_name)
    )

    shutil.copytree('python_doc_template', os.path.join(mod_dest, 'doc'))

    for path, _, filenames in os.walk(mod_dest):
        for filename in filenames:
            abspath = os.path.join(path, filename)
            with open(abspath, 'r') as f:
                text = f.read()
            with open(abspath, 'w') as f:
                f.write(text.replace('{IMPORT_NAME}', import_name).replace('{FULL_NAME}', full_name))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(dest='full_name', type=str)
    parser.add_argument(dest='import_name', type=str)
    args = parser.parse_args(sys.argv[1:])

    create_module(args.full_name, args.import_name)
