# -*- coding: utf-8 -*-
# Copyright (c) 2014 Raphaël Barrois
# This code is distributed under the two-clause BSD License.


from __future__ import unicode_literals

import sys

"""Python 2 backwards compatibility layer."""

if sys.version_info[0] == 2:
    PY2 = True
else:
    PY2 = False
