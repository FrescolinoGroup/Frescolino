#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    29.03.2016 10:09:09 CEST
# File:    __init__.py

import pkgutil
import importlib

__path__ = pkgutil.extend_path(__path__, __name__)

# TODO: automate
module_names = ['testmod1', 'testmod2', 'testmod3']

for modname in module_names:
    importlib.import_module('.' + modname, package='fsc') 
