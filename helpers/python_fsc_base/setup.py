#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    20.10.2014 11:27:40 CEST
# File:    setup.py

import sys

try:
    import xmlrpclib
except ImportError:
    import xmlrpc.client as xmlrpclib

from setuptools import setup

pypi_proxy = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')
fsc_packages = [pack for pack in pypi_proxy.list_packages() if pack.startswith('fsc.')]

valid_packages = []
for pack in fsc_packages:
    for pkg_version in pypi_proxy.package_releases(pack):
        all_classifiers = pypi_proxy.release_data(pack, pkg_version)['classifiers']
        python_classifiers = (cl for cl in all_classifiers if cl.startswith('Programming Language :: Python ::'))
        py_versions = [tuple(int(x) for x in cl.split('::')[-1].strip().split('.')) for cl in python_classifiers]
        
        if any(sys.version_info >= py_version for py_version in py_versions):
            valid_packages.append(pack + '==' + pkg_version)
            break

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
    install_requires=valid_packages,
    license='Apache',
)
