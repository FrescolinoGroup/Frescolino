#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    30.03.2016 00:30:19 CEST
# File:    create_python_package.py

import os
import sys

def create_package(full_name, import_name):
    existing_modules = os.listdir('../modules')

def main():
    if len(sys.argv) != 3:
        print('usage: python create_python_package.py FULL_NAME IMPORT_NAME')
    else:
        create_package(full_name=sys.argv[1], import_name=sys.argv[2])

if __name__ == "__main__":
    main()
