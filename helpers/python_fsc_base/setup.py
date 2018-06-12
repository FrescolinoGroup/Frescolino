#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

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
    packages=['fsc'],
    author='C. Frescolino',
    description=description,
    long_description=readme,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
    ],
    install_requires=[
        'setuptools',
        'fsc.export',
        'fsc.formatting',
    ],
    extras_require={
        ':python_version >= "3"': [
            'fsc.iohelper',
            'fsc.locker',
            'fsc.hdf5-io',
        ],
        ':python_version >= "3.5"': [
            'fsc.async-tools',
        ],
    },
    license='Apache',
)
