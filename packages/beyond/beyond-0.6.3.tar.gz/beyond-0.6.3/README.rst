Beyond
======

.. image:: http://readthedocs.org/projects/beyond/badge/?version=latest
    :alt: Documentation Status
    :target: http://beyond.readthedocs.io/en/latest/?badge=latest

.. image:: https://travis-ci.org/galactics/beyond.svg?branch=master
    :alt: Tests
    :target: https://travis-ci.org/galactics/beyond

.. image:: https://coveralls.io/repos/github/galactics/beyond/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://coveralls.io/github/galactics/beyond?branch=master

.. image:: https://img.shields.io/pypi/v/beyond.svg
    :alt: PyPi version
    :target: https://pypi.python.org/pypi/beyond

.. image:: https://img.shields.io/pypi/pyversions/beyond.svg
    :alt: Python versions
    :target: https://pypi.python.org/pypi/beyond

This library was started to better understand how Flight Dynamics works. It
has no intent of efficiency nor performance at the moment, and the goal is
mainly to develop a simple API for space observations.

The sources of this library can be found at `github <https://github.com/galactics/beyond>`__ and
are under the MIT license.

Installation
------------

Beyond requires Python 3.5+, numpy and `sgp4 <https://github.com/brandon-rhodes/python-sgp4>`__.
To install the library and its dependencies use pip

.. code-block:: shell

    pip install beyond

Documentation
-------------

  * `Last release <http://beyond.readthedocs.io/en/stable/>`__ (stable)
  * `Dev <http://beyond.readthedocs.io/en/latest/>`__ (latest)

Usage
-----

This library is used as basis for the `Space-Command <https://github.com/galactics/space-command>`__ utility.

Commons usages for this library are:

  * `Predicting of satellite visibility <http://beyond.readthedocs.io/en/stable//examples.html#station-pointings>`__
  * `Computing satellite ground track <http://beyond.readthedocs.io/en/stable//examples.html#ground-track>`__
  * `Computing planets visibility <http://beyond.readthedocs.io/en/stable//examples.html#jupiter-and-its-moons>`__

References
----------

A lot of the formulas and flight dynamic algorithm are based on Vallado's
*Fundamentals of Astrodynamic and Applications* 4th ed.
