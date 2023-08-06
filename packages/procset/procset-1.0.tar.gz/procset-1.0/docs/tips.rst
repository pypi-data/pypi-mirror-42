Tips & Tricks
=============

Scaling a :class:`~procset.ProcSet`
-----------------------------------

Assuming a :class:`~procset.ProcSet` represents a set of processors with many
cores, one may create the set of cores with the following snippet:

.. code:: python

   def upscale(pset, factor):
       return procset.ProcSet(
           *map(
               lambda itv: (itv.inf * factor, (itv.sup + 1) * factor - 1),
               pset.intervals()
           )
       )


Dumping to JSON
---------------

The :class:`~procset.ProcSet` object does not provide a JSON serialization
method.
The main reason for this is that the canonical string representation is enough
to store all the information, and allows for portability of the serialization.

The following snippet might come handy to export a :class:`~procset.ProcSet` to
JSON.

.. code:: python

   import json
   import procset


   class ProcSetJSONEncoder(json.JSONEncoder):
       def default(self, obj):
           if isinstance(obj, procset.ProcSet):
               return str(obj)  # use canonical string representation
           return json.JSONEncoder.default(self, obj)


   json.dumps({'alloc': procset.ProcSet((0, 3))}, cls=ProcSetJSONEncoder)


For more advanced usages, see the standard module :mod:`json`, or the
third-party package `jsonpickle <https://jsonpickle.rtfd.io>`_.
