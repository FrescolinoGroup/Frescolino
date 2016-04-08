#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    30.03.2016 12:36:11 CEST
# File:    __init__.py


import pkgutil as _pkgutil

__path__ = _pkgutil.extend_path(__path__, __name__)
