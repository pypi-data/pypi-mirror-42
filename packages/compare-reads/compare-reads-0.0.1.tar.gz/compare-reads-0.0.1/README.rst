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
        | |coveralls|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/pysam-compare-reads/badge/?style=flat
    :target: https://readthedocs.org/projects/pysam-compare-reads
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/mvdbeek/pysam-compare-reads.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/mvdbeek/pysam-compare-reads

.. |coveralls| image:: https://coveralls.io/repos/mvdbeek/pysam-compare-reads/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/mvdbeek/pysam-compare-reads

.. |version| image:: https://img.shields.io/pypi/v/compare-reads.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/compare-reads

.. |commits-since| image:: https://img.shields.io/github/commits-since/mvdbeek/pysam-compare-reads/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/mvdbeek/pysam-compare-reads/compare/v0.0.1...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/compare-reads.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/compare-reads

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/compare-reads.svg
    :alt: Supported versions
    :target: https://pypi.org/project/compare-reads

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/compare-reads.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/compare-reads


.. end-badges

cythonized function to compare reads by name

* Free software: MIT license

Installation
============

::

    pip install compare-reads

Documentation
=============


https://pysam-compare-reads.readthedocs.io/


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
