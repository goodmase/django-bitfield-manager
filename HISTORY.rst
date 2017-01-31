.. :changelog:

History
-------
0.3.0 (2017-01-31)
++++++++++++++++++
* Added example
* Changed the parent_models models tuple from ('parent', 'child', 0) to ('parent.child', 0)
* additional unit tests
* bug fixes

0.2.0 (2017-01-27)
++++++++++++++++++

* Added django-bitfield support
* No longer uses signals
* Added mixin for child models (ChildBitfieldModelMixin)
* Added support for one-to-one and limited support for m2m fields
* Added support for models multiple levels deep (using dot syntax)


0.1.0 (2017-01-18)
++++++++++++++++++

* First release on PyPI.
