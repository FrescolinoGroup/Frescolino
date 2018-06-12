#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    29.03.2016 10:09:09 CEST
# File:    __init__.py

import sys as _sys
import pkgutil as _pkgutil
import importlib as _importlib
import pkg_resources as _pkg_resources

__path__ = _pkgutil.extend_path(__path__, __name__)

# update working_set
for _path in _sys.path:
    _pkg_resources.working_set.add_entry(_path)
# get all modules
_submodules = [_mod.key for _mod in _pkg_resources.working_set]
# filter out those which belong to fsc
_submodules = [_name.split('fsc', 1)[1]
               for _name in _submodules if _name.startswith('fsc.')]
for _modname in _submodules:
    _importlib.import_module(_modname.replace("-", "_"), package='fsc')

__all__ = [_name.lstrip('.') for _name in _submodules]
