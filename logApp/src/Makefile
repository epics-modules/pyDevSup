TOP=../..

include $(TOP)/configure/CONFIG

#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

LOADABLE_LIBRARY_HOST_Linux = _inotifyy

_inotifyy_SRCS += inotify_wrap.c

PY += inotifyy.py
PY += logwatch/__init__.py
PY += logwatch/caputlog.py

#===========================

include $(TOP)/configure/RULES

#----------------------------------------
#  ADD RULES AFTER THIS LINE
