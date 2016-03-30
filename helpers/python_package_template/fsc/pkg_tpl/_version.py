#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    30.03.2016 12:21:07 CEST
# File:    _version.py

import os

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'version.txt'), 'r') as f:
    __version__ = f.read().strip()
