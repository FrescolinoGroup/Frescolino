#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    29.03.2016 10:09:09 CEST
# File:    __init__.py

import pip as _pip
import pkgutil as _pkgutil
import importlib as _importlib

__path__ = _pkgutil.extend_path(__path__, __name__)

# get all modules
_submodules = [mod.key for mod in _pip.get_installed_distributions()]
# filter out those which belong to fsc
_submodules = [name.split('fsc', 1)[1]
               for name in _submodules if name.startswith('fsc.')]
for _modname in _submodules:
    _importlib.import_module(_modname.replace("-", "_"), package='fsc')

__all__ = [name.lstrip('.') for name in _submodules]
