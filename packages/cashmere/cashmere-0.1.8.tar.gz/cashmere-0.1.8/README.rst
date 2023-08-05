========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-cashmere/badge/?style=flat
    :target: https://readthedocs.org/projects/python-cashmere
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/githubuser/python-cashmere.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/githubuser/python-cashmere

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/githubuser/python-cashmere?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/githubuser/python-cashmere

.. |version| image:: https://img.shields.io/pypi/v/cashmere.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/cashmere

.. |commits-since| image:: https://img.shields.io/github/commits-since/githubuser/python-cashmere/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/githubuser/python-cashmere/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/cashmere.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/cashmere

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/cashmere.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/cashmere

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/cashmere.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/cashmere


.. end-badges

Caching function calls.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install cashmere

Documentation
=============


https://python-cashmere.readthedocs.io/


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
