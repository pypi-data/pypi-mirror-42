========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
.. |docs| image:: https://readthedocs.org/projects/pysqldict/badge/?style=flat
    :target: ttps://readthedocs.org/projects/pysqldict
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/charlee/pysqldict.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/charlee/pysqldict

.. end-badges

A library that allows python dictionaries to be stored in SQLite and provides a simple interface for read and write.

* Free software: MIT license

Installation
============

::

    pip install pysqldict

Documentation
=============


https://pysqldict.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
