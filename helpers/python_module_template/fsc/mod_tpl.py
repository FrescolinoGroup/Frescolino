#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  C. Frescolino, D. Gresch
# Date:    30.03.2016 12:23:23 CEST
# File:    {IMPORT_NAME}.py

import os

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../version.txt'), 'r') as f:
    __version__ = f.read().strip()
