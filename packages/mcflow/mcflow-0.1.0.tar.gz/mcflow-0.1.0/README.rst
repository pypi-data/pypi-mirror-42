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

.. |docs| image:: https://readthedocs.org/projects/python-mcflow/badge/?style=flat
    :target: https://readthedocs.org/projects/python-mcflow
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/githubuser/python-mcflow.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/githubuser/python-mcflow

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/githubuser/python-mcflow?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/githubuser/python-mcflow

.. |version| image:: https://img.shields.io/pypi/v/mcflow.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/mcflow

.. |commits-since| image:: https://img.shields.io/github/commits-since/githubuser/python-mcflow/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/githubuser/python-mcflow/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/mcflow.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/mcflow

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/mcflow.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/mcflow

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/mcflow.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/mcflow


.. end-badges

An example package. Generated with cookiecutter-pylibrary.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install mcflow

Documentation
=============


https://python-mcflow.readthedocs.io/


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
