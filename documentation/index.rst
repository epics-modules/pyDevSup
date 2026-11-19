.. devsup documentation master file, created by
   sphinx-quickstart on Sun Mar 31 19:28:10 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pydevsup documentation
======================

*pyDevSup* is a means of writing EPICS device support code in Python.

It currently supports EPICS >=3.14.12 and python versions >=3.6
The numpy package is also required.

It is not possible to use the module with a static build configuration.
The code will build, but it will not work.
The reason is that EPICS database defintions are created in two modules:
1. The _dbapi module creates the defintion of 'Python Device'.
2. The softIocPy module implements device types such as longin that use 'Python Device'.
   In a static build, these are held in seperate EPICS databases.
   Consequently the softIocPy module does not know what a 'Python Device' is.
   In a shared library build there is ony one database, held by the underlying EPICS base library.

The source can be found at https://github.com/epics-modules/pyDevSup

File releases are available at https://github.com/epics-modules/pyDevSup/releases

Contents:

.. toctree::
   :maxdepth: 4

   gettingstarted
   environment
   devsup
   interfaces
   ptable

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

