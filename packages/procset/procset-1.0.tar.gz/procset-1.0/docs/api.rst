ProcSet API
===========

.. currentmodule:: procset


.. autoclass:: ProcSet

   >>> ProcSet()  # empty set
   ProcSet()
   >>> ProcSet(1)
   ProcSet(1)
   >>> ProcSet(ProcInt(0, 1))
   ProcSet((0, 1))
   >>> ProcSet(ProcInt(0, 1), ProcInt(2, 3))
   ProcSet((0, 3))
   >>> ProcSet((0, 1), [2, 3])  # identical to previous call
   ProcSet((0, 3))
   >>> ProcSet(ProcInt(0, 1), *[0, 3])  # mixing ProcInt and lists
   ProcSet((0, 1), 3)

   **Implementation detail:**
   A ProcSet is implemented as a sorted list of :class:`ProcInt`.
   The memory complexity is hence linear in the number of disjoint intervals
   contained in the set.

   .. versionchanged:: 1.0
      The constructor now supports ProcSet objects.


   .. automethod:: from_str

      >>> ProcSet.from_str('1-3 5 7')
      ProcSet((1, 3), 5, 7)
      >>> ProcSet.from_str('5 2-2 7 1-3')
      ProcSet((1, 3), 5, 7)
      >>> ProcSet.from_str('1:3,5,7', insep=':', outsep=',')
      ProcSet((1, 3), 5, 7)

      .. note::
         :meth:`from_str` only supports single character strings for ``insep``
         and ``outsep`` delimiters.

      .. seealso::
         :ref:`string-representation`


   .. describe:: str(pset)
                 format(pset[, format_spec])

      Return the canonical :ref:`string representation <string-representation>`
      of *pset*.

      When using :func:`str` or :func:`format` without *format_spec*, the
      default delimiters are used (default inner delimiter is ``-``, default
      outer delimiter is  ``␣``).

      When using :func:`format`, the parameter *format_spec* may be used to
      change the delimiters.
      The format specification is a length-2 string, where the first character
      encodes the inner delimiter, and the second character encodes the outer
      delimiter.

      >>> pset = ProcSet((1, 3), 5, 7)
      >>> str(pset)
      '1-3 5 7'
      >>> format(pset)
      '1-3 5 7'
      >>> format(pset, ':,')
      '1:3,5,7'


   .. describe:: i in pset

      Test whether processor ``i`` is in *pset*.

      >>> 3 in ProcSet((0, 7))
      True
      >>> 8 in ProcSet((0, 7))
      False


   .. describe:: len(pset)

      Return the number of processors contained in *pset*.


   .. automethod:: count

      >>> pset = ProcSet((1, 3), 5, 7)
      >>> len(pset)  # 5 processors
      5
      >>> pset.count()  # 3 disjoint intervals
      3


   .. describe:: iter(pset)
                 reversed(pset)

      Iterate over the processors in *pset*.

      >>> pset = ProcSet((1, 3), 5, 7)
      >>> list(iter(pset))
      [1, 2, 3, 5, 7]
      >>> list(reversed(pset))
      [7, 5, 3, 2, 1]


   .. describe:: pset[i]
                 pset[i:j]
                 pset[i:j:k]

      Access processors of *pset* by position.
      ProcSet supports element index lookup, slicing and negative indices.

      The semantic of the ``[]`` operator is defined to behave the same as if
      *pset* was a list of integers.

      When used with an :class:`int` ``i``, ``pset[i]`` returns the processor
      at the i-th position.

      When used with a :class:`slice`, ``pset[i:j:k]`` returns the
      corresponding list of processors (see also :meth:`iter_slice`).

      >>> pset = ProcSet(ProcInt(0), ProcInt(2, 5), ProcInt(7, 13))
      >>> pset[0], pset[2], pset[-1]
      (0, 3, 13)
      >>> pset[1:5]
      [2, 3, 4, 5]
      >>> pset[:-3]
      [0, 2, 3, 4, 5, 7, 8, 9, 10]
      >>> pset[::2]
      [0, 3, 5, 8, 10, 12]
      >>> pset[3::3]
      [4, 8, 11]
      >>> pset[3::-3]
      [4, 0]


   .. automethod:: iter_slice

      This method iterate over the same set of processors as
      ``pset[start:stop:step]``.
      In contrast to using ``[]``, we do not build the list of processors: the
      memory complexity is hence constant rather than linear in the number of
      iterated processors.

      >>> pset = ProcSet(ProcInt(0), ProcInt(2, 5), ProcInt(7, 13))
      >>> pset.iter_slice()
      <generator object ProcSet.iter_slice at 0x7f0dd6afb8b8>
      >>> list(pset.iter_slice())
      [0, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13]


   .. automethod:: isdisjoint


   .. method:: issubset(other)
               pset <= other

      Test whether every element in the ProcSet is in *other*.


   .. method:: pset < other

      Test whether the ProcSet is a proper subset of *other*, that is
      ``pset <= other`` and ``pset != other``.


   .. method:: issuperset(other)
               pset >= other

      Test whether every element in *other* is in the ProcSet.


   .. method:: pset > other

      Test whether the ProcSet is a proper superset of *other*, that is
      ``pset >= other`` and ``pset != other``.


   .. method:: union(*others)
               pset | other | ...

      Return a new ProcSet with elements from the ProcSet and all others.


   .. method:: intersection(*others)
               pset & other & ...

      Return a new ProcSet with elements common to the ProcSet and all others.


   .. method:: difference(*others)
               pset - other - ...

      Return a new ProcSet with elements in the ProcSet that are not in the
      others.


   .. method:: symmetric_difference(other)
               pset ^ other

      Return a new ProcSet with elements in either the ProcSet or *other*, but
      not in both.


   .. automethod:: copy


   .. note::
      The non-operator versions of :meth:`union`, :meth:`intersection`,
      :meth:`difference`, :meth:`symmetric_difference` methods accept as
      argument any combination of objects that may be used to initialize a
      ProcSet.

      In contrast, their operator based counterparts require their arguments to
      be ProcSet.
      This avoid error-prone constructions, and favors readability.


   .. method:: update(*others)
               insert(*others)
               pset |= other | ...

      Update the ProcSet, adding elements from all others.


   .. method:: intersection_update(*others)
               pset &= other & ...

      Update the ProcSet, keeping only elements found in the ProcSet and all
      others.


   .. method:: difference_update(*others)
               discard(*others)
               pset -= other | ...

      Update the ProcSet, removing elements found in others.


   .. method:: symmetric_difference_update(other)
               pset ^= other

      Update the ProcSet, keeping only elements found in either the ProcSet or
      *other*, but not in both.


   .. automethod:: clear


   .. note::
      The non-operator versions of :meth:`update`, :meth:`intersection_update`,
      :meth:`difference_update`, :meth:`symmetric_difference_update` methods
      accept as argument any combination of objects that may be used to
      initialize a ProcSet.

      In contrast, their operator based counterparts require their arguments to
      be ProcSet.
      This avoid error-prone constructions, and favors readability.


   .. automethod:: iscontiguous

      >>> ProcSet().iscontiguous()
      True
      >>> ProcSet((1, 3)).iscontiguous()
      True
      >>> ProcSet((1, 3), 4).iscontiguous()
      True
      >>> ProcSet((1, 3), 5, 7).iscontiguous()
      False


   .. automethod:: aggregate

      >>> ProcSet().aggregate()
      ProcSet()
      >>> ProcSet((1, 3), 5, 7).aggregate()
      ProcSet((1, 7))


   .. automethod:: intervals

      >>> pset = ProcSet((1, 3), 5)
      >>> list(pset.intervals())
      [ProcInt(inf=1, sup=3), ProcInt(inf=5, sup=5)]


   .. autoattribute:: min


   .. autoattribute:: max
