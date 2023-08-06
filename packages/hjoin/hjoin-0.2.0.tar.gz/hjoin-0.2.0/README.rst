=====
hjoin
=====


.. image:: https://img.shields.io/pypi/v/hjoin.svg
        :target: https://pypi.python.org/pypi/hjoin

.. image:: https://img.shields.io/travis/jonathaneunice/hjoin.svg
        :target: https://travis-ci.org/jonathaneunice/hjoin

.. image:: https://pyup.io/repos/github/jonathaneunice/hjoin/shield.svg
     :target: https://pyup.io/repos/github/jonathaneunice/hjoin/
     :alt: Updates

Early-stage code for horizontal text joining. That means obeying
the line breaks and implicit columns in the given strings,
rather than simply appending them linearly.

.. code-block:: python

    from hjoin import *
    from colors import *

    r = red('this perhaps\nand\nthat')
    b = blue('and\none\nmore\nthing')
    g = green('yet\nanother\n')
    print(hjoin([r, b, g]))

Notes
-----

* This module is **not** ready for prime time. It's currently
  published solely to enable distributed testing (CI pipeline).
  You shouldn't use it, depend on it, or expect anything
  specific from it. Especially don't expect its API will remain
  constant.
