===============
DOE2-SIM-Parser
===============

.. image:: https://img.shields.io/pypi/v/doe2-sim-parser.svg
   :target: https://pypi.python.org/pypi/doe2-sim-parser
   :alt: PyPI Version

.. image:: https://img.shields.io/badge/wheel-yes-brightgreen.svg
   :target: https://pypi.python.org/pypi/doe2-sim-parser
   :alt: Wheel Status

.. image:: https://readthedocs.org/projects/doe2-sim-parser/badge/?version=latest
   :target: https://doe2-sim-parser.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://travis-ci.org/grammy-jiang/doe2-sim-parser.svg
   :target: https://travis-ci.org/grammy-jiang/doe2-sim-parser
   :alt: Travis Status

.. image:: https://codecov.io/gh/grammy-jiang/doe2-sim-parser/branch/draft/graph/badge.svg
   :target: https://codecov.io/gh/grammy-jiang/doe2-sim-parser
   :alt: Coverage Report

.. image:: https://api.codacy.com/project/badge/Grade/a5740e303e2b456f9d74d0baf0776071
   :target: https://www.codacy.com/app/grammy-jiang/doe2-sim-parser?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=grammy-jiang/doe2-sim-parser&amp;utm_campaign=Badge_Grade
   :alt: Codacy Report

.. image:: https://pyup.io/repos/github/grammy-jiang/doe2-sim-parser/shield.svg
   :target: https://pyup.io/repos/github/grammy-jiang/doe2-sim-parser/
   :alt: pyup

.. image:: https://pyup.io/repos/github/grammy-jiang/doe2-sim-parser/python-3-shield.svg
   :target: https://pyup.io/repos/github/grammy-jiang/doe2-sim-parser/
   :alt: Python 3

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0
   :alt: GNU General Public License v3.0


Overview
========

This project provides the DOE2 sim report splitting and parsing:

* split the sim report into pieces by the reports' names
* parse the sim report from pure text to csv file (comma-separated values),
  based on the requirement (configuration)
* upload the parsed sim reports to Google Spreadsheet

Requirements
============

* Python 3.6+
* Fully tested on Linux, but it should works on Windows, Mac OSX, BSD

Installation
============

The quick way:

   pip install doe2-sim-parser

For more details see the installation section in the documentation:
https://doe2-sim-parser.readthedocs.io/en/latest/installation.html

Documentation
=============

Documentation is available online at
https://doe2-sim-parser.readthedocs.io/en/latest/ and in the ``docs`` directory.

TODO
====

* [ ] Add Microsoft Office 365 support for parsed sim reports uploading
* [ ] Trigger Google Apps Script to do post-process after uploading the parsed
  sim reports
