#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    29.03.2016 10:09:09 CEST
# File:    __init__.py

import pip
import pkgutil
import importlib

__path__ = pkgutil.extend_path(__path__, __name__)

# get all modules
submodules = [mod.key for mod in pip.get_installed_distributions()]
# filter out those which belong to fsc
submodules = [name.lstrip('fsc') for name in submodules if name.startswith('fsc.')]
for modname in submodules:
    importlib.import_module(modname, package='fsc') 
