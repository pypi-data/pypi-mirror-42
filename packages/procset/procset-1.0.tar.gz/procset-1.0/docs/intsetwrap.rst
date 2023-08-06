Migrating :mod:`interval_set`
=============================

The module :mod:`interval_set` provided a crude API to manipulate interval
sets.
To ease the transition, the :mod:`intsetwrap` module is provided as a drop in
wrapper of the new :mod:`procset` API.

.. note::
   The focus of the wrapper is to keep the same semantic.
   As every call transforms the interval set to a ProcSet before converting it
   back, the performances may drastically drop.


As a first migration step, it's as simple as replacing ``import interval_set``
by ``import intsetwrap as interval_set``.

The following table shows how :mod:`procset` API may be used when migrating.
``pset`` represents a :class:`~procset.ProcSet` object.

+------------------------------------+---------------------------------+
| :mod:`interval_set` API            | :mod:`procset` API              |
+====================================+=================================+
| ``aggregate(itvs)``                | ``pset.aggregate()``            |
+------------------------------------+---------------------------------+
| ``difference(itvs1, itvs2)``       | ``pset1 - pset2``               |
+------------------------------------+---------------------------------+
| ``equals(itvs1, itvs2)``           | ``pset1 == pset2``              |
+------------------------------------+---------------------------------+
| ``id_list_to_iterval_set(idlist)`` | ``ProcSet(*idlist)``            |
+------------------------------------+---------------------------------+
| ``intersection(itvs1, itvs2)``     | ``pset1 & pset2``               |
+------------------------------------+---------------------------------+
| ``interval_set_to_id_list(itvs)``  | ``list(pset)``                  |
+------------------------------------+---------------------------------+
| ``interval_set_to_set(itvs)``      | ``set(pset)``                   |
+------------------------------------+---------------------------------+
| ``interval_set_to_string(itvs)``   | ``str(pset)``, ``format(pset)`` |
+------------------------------------+---------------------------------+
| ``set_to_interval_set(idset)``     | ``ProcSet(*idset)``             |
+------------------------------------+---------------------------------+
| ``string_to_interval_set(string)`` | ``ProcSet.from_str(string)``    |
+------------------------------------+---------------------------------+
| ``total(itvs)``                    | ``len(pset)``                   |
+------------------------------------+---------------------------------+
| ``union(itvs1, itvs2)``            | ``pset1 | pset2``               |
+------------------------------------+---------------------------------+
