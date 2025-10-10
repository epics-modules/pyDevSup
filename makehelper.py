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

from sysconfig import get_config_var, get_path, get_python_version

incdirs = [get_path("include")]
libdir = get_config_var('LIBDIR') or get_config_var('LIBDEST') or ''

have_np='NO'
try:
    from numpy import get_include
    numpy_dir = [get_include()]
    incdirs = numpy_dir+incdirs
    have_np='YES'
except ImportError:
    pass

print('TARGET_CFLAGS +=',get_config_var('BASECFLAGS') or '', file=out)
print('TARGET_CXXFLAGS +=',get_config_var('BASECFLAGS') or '', file=out)

print('PY_VER :=',get_python_version(), file=out)
ldver = get_config_var('LDVERSION')
if ldver is None:
    ldver = get_config_var('VERSION')
    if get_config_var('Py_DEBUG'):
        ldver = ldver+'_d'
print('PY_LD_VER :=',ldver, file=out)
print('PY_INCDIRS :=',' '.join(incdirs), file=out)
print('PY_LIBDIRS :=',libdir, file=out)
if sys.platform == 'win32':
    print('PY_LDLIBS :=', '-LIBPATH:' + os.path.join(sys.prefix, 'libs'), file=out)
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