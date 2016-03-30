#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    30.03.2016 00:29:06 CEST
# File:    setup.py


from setuptools import setup

modname = '{IMPORT_NAME}'
modname_qualified = 'fsc.' + modname

with open('doc/description.txt', 'r') as f:
    description = f.read()
try:
    with open('doc/README', 'r') as f:
        readme = f.read()
except IOError:
    readme = description

with open('version.txt', 'r') as f:
    version = f.read()

setup(
    name=modname_qualified,
    version=version,
    py_modules=[
        modname_qualified
    ],
    author='C. Frescolino',
    description=description,
    long_description=readme,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
    ],
    license='Apache',
)
