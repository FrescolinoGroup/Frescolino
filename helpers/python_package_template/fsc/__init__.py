#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    30.03.2016 00:29:31 CEST
# File:    __init__.py


import pkgutil

__path__ = pkgutil.extend_path(__path__, __name__)

from . import {PKGNAME} 
