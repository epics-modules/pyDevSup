#!/usr/bin/env python
"""
Set some python derived Makefile variables.

Emits something like the following

PY_OK := YES  # indicates success of this script
HAVE_NUMPY := YES/NO
PY_VER := 2.6
PY_INCDIRS := /path ...
PY_LIBDIRS := /path ...
"""

from __future__ import print_function

import sys
import errno
import os

if len(sys.argv)<2:
    out = sys.stdout
else:
    try:
        os.makedirs(os.path.dirname(sys.argv[1]))
    except OSError:
        pass
    out = open(sys.argv[1], 'w')

"""
3.2      sysconfig
3.10     sysconfig.get_path
3.10.13  distutils is deprecated.
3.12     distutils was removed.
"""
if sys.version_info >= (3,10,):
    from sysconfig import get_config_var, get_path
    incdirs = [get_path("include")]
else:
    from distutils.sysconfig import get_config_var, get_python_inc
    incdirs = [get_python_inc()]

libdir = get_config_var('LIBDIR') or ''

have_np='NO'

"""
numpy 1.18, numpy.get_include()
"""
try:
    from numpy import get_include
    numpy_dir = [get_include()]
    incdirs = numpy_dir+incdirs
    have_np='YES'
except ImportError:
    pass

print('TARGET_CFLAGS +=',get_config_var('BASECFLAGS'), file=out)
print('TARGET_CXXFLAGS +=',get_config_var('BASECFLAGS'), file=out)

print('PY_VER :=',get_config_var('VERSION'), file=out)
ldver = get_config_var('LDVERSION')
if ldver is None:
    ldver = get_config_var('VERSION')
    if get_config_var('Py_DEBUG'):
        ldver = ldver+'_d'
print('PY_LD_VER :=',ldver, file=out)
print('PY_INCDIRS :=',' '.join(incdirs), file=out)
print('PY_LIBDIRS :=',libdir, file=out)
print('HAVE_NUMPY :=',have_np, file=out)

try:
    import asyncio
except ImportError:
    print('HAVE_ASYNCIO := NO', file=out)
else:
    print('HAVE_ASYNCIO := YES', file=out)

try:
    import cothread
except ImportError:
    print('HAVE_COTHREAD := NO', file=out)
else:
    print('HAVE_COTHREAD := YES', file=out)

print('PY_OK := YES', file=out)

out.close()
