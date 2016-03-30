#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    20.10.2014 11:27:40 CEST
# File:    setup.py

try:
    import xmlrpclib
except ImportError:
    import xmlrpc.client as xmlrpclib

from setuptools import setup

pypi_proxy = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')
fsc_packages = [pack for pack in pypi_proxy.list_packages() if pack.startswith('fsc.')]

with open('doc/description.txt', 'r') as f:
    description = f.read()
try:
    with open('doc/README', 'r') as f:
        readme = f.read()
except IOError:
    readme = description

with open('version.txt', 'r') as f:
    version = f.read().strip()

setup(
    name='fsc',
    version=version,
    packages=[
        'fsc'
    ],
    author='C. Frescolino',
    description=description,
    long_description=readme,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
    ],
    install_requires=fsc_packages,
    license='Apache',
)
