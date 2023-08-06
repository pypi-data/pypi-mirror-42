========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/cookiecutterJSROBIN888/badge/?style=flat
    :target: https://readthedocs.org/projects/cookiecutterJSROBIN888
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/jsrobin888/cookiecutterJSROBIN888.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/jsrobin888/cookiecutterJSROBIN888

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/jsrobin888/cookiecutterJSROBIN888?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/jsrobin888/cookiecutterJSROBIN888

.. |requires| image:: https://requires.io/github/jsrobin888/cookiecutterJSROBIN888/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/jsrobin888/cookiecutterJSROBIN888/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/jsrobin888/cookiecutterJSROBIN888/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/jsrobin888/cookiecutterJSROBIN888

.. |version| image:: https://img.shields.io/pypi/v/cookiecutterJSROBIN888.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/cookiecutterJSROBIN888

.. |commits-since| image:: https://img.shields.io/github/commits-since/jsrobin888/cookiecutterJSROBIN888/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/jsrobin888/cookiecutterJSROBIN888/compare/v0.0.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/cookiecutterJSROBIN888.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/cookiecutterJSROBIN888

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/cookiecutterJSROBIN888.svg
    :alt: Supported versions
    :target: https://pypi.org/project/cookiecutterJSROBIN888

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/cookiecutterJSROBIN888.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/cookiecutterJSROBIN888


.. end-badges

An example package. Generated with cookiecutter-pylibrary.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install cookiecutterJSROBIN888

Documentation
=============


https://cookiecutterJSROBIN888.readthedocs.io/


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
