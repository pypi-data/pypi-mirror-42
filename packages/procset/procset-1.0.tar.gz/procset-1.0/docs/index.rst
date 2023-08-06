Overview
========

.. toctree::
   :hidden:
   :titlesonly:

   Overview <self>
   ProcSet API <api>
   tips
   intsetwrap


.. currentmodule:: procset


This package implements for Python a memory-efficient representation of
closed-interval sets.


The package provides two modules: :mod:`procset` and :mod:`intsetwrap`:
  - :mod:`procset` is an implementation aiming at providing a pythonic
    experience: it should be the preferred module for any new project.
  - :mod:`intsetwrap` is a wrapper around :mod:`procset` providing the old API
    of :mod:`interval_set`: do not use in any new project.


A :class:`ProcSet` is an hybrid between a :class:`set` and a :class:`list` of
indexes.
More precisely, a :class:`ProcSet` object is an ordered collection of
unique non-negative :class:`int`.
It supports most of :class:`set` operations: notably membership testing,
mathematical operations such as intersection, union, and (symmetric)
difference; with the additional ability to access its elements by position.

The :class:`ProcSet` type is mutable, as its content can be modified using
methods such as :meth:`~ProcSet.insert()`.
Since it is mutable, it has no hash value and cannot be used as either a
dictionary key or as an element of another set.


Example use
-----------

You can get the library directly from PyPI:

.. code:: bash

   pip install procset


What does it look like to use ``procset``?  Here is a simple example program:

.. code:: python

   from procset import ProcSet


   free_cores = ProcSet((0, 7))  # I have 8 cores to work with

   job_cores = ProcSet((2, 5))  # let's use some cores for a job
   free_cores -= job_cores

   print('remaining cores:', str(free_cores))


And it looks like this when run:

.. code:: bash

   $ python example.py
   remaining cores: 0-1 6-7


.. _string-representation:

String representation of interval sets
--------------------------------------

In the scheduling community, interval sets often are encoded as strings where
the string ``'a-b'`` (middle symbol is a dash, ascii ``0x2d``) represents the
integer interval :math:`[a, b]`, with the convention that the string ``a``
represents the degenerate case of the singleton :math:`\{a\}`.
An interval set with many disjoint intervals is encoded by joining interval
representations with a space (ascii ``0x20``): for example ``a-b c d-e``
represents :math:`[a, b] \cup \{c\} \cup [d, e]`.

.. warning::
   There are many different strings representing the same interval set.
   For the description of a canonical representation, please refer to the
   `documentation of Batsim <https://batsim.readthedocs.io/en/latest/interval-set.html#canonical-string-representation>`_.
