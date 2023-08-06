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

.. |travis| image:: https://travis-ci.org/sagersmith8/journal_software_engineering.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/sagersmith8/journal_software_engineering

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/sagersmith8/journal_software_engineering?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/sagersmith8/journal_software_engineering

.. |requires| image:: https://requires.io/github/sagersmith8/journal_software_engineering/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/sagersmith8/journal_software_engineering/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/sagersmith8/journal_software_engineering/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/sagersmith8/journal_software_engineering

.. |version| image:: https://img.shields.io/pypi/v/journal-software-engineering.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/journal-software-engineering

.. |commits-since| image:: https://img.shields.io/github/commits-since/sagersmith8/journal_software_engineering/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/sagersmith8/journal_software_engineering/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/journal-software-engineering.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/journal-software-engineering

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/journal-software-engineering.svg
    :alt: Supported versions
    :target: https://pypi.org/project/journal-software-engineering

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/journal-software-engineering.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/journal-software-engineering


.. end-badges

journal_software_engineering

* Free software: Apache Software License 2.0

Installation
============

.. code-block:: bash
    pip install journal-software-engineering

Documentation
=============


To use the project:

.. code-block:: python

    import journal_software_engineering
    journal_software_engineering -h


.. code-block:: bash

    usage: journal [-h] [-t] [-d] [-n] [-c] [-s] [-j] [-b BEFORE] [-a AFTER]
                   [entry]

            journal makes commits to repos in the following locations:
                journal location: /Users/sagesmith/.journal
                notes location: /Users/sagesmith/.journal/.notes
                ticket location: /Users/sagesmith/.journal/.ticket
                todo location: /Users/sagesmith/.journal/.todo

    positional arguments:
      entry                 entry to enter in journal

    optional arguments:
      -h, --help            show this help message and exit
      -t, --ticket          specifies ticket journal
      -d, --do              specifies todo journal
      -n, --note            specifies note journal
      -s, --standup         prints stand up
      -j, --journal         specifies entire journal
      -b BEFORE, --before BEFORE
                            specifies to grab standup logs before entered date
      -a AFTER, --after AFTER
                            specifies to grab standup logs after entered date

    made by sage smith



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
