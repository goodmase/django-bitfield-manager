=============================
bitfield_manager
=============================

.. image:: https://badge.fury.io/py/django-bitfield-manager.svg
    :target: https://badge.fury.io/py/django-bitfield-manager

.. image:: https://travis-ci.org/goodmase/django-bitfield-manager.svg?branch=master
    :target: https://travis-ci.org/goodmase/django-bitfield-manager

.. image:: https://codecov.io/gh/goodmase/django-bitfield-manager/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/goodmase/django-bitfield-manager

Your project description goes here


Quickstart
----------

Install bitfield_manager::

    pip install django-bitfield-manager

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'bitfield_manager.apps.BitfieldManagerConfig',
        ...
    )


Usage
--------
First you'll need a parent model with a status field
.. code-block::

    from django.db import models
    from bitfield_manager.models import ParentBitfieldModel


    class ParentExample(ParentBitfieldModel):
        status = models.BigIntegerField()

    def __str__(self):  # __unicode__ on Python 2
        return "status: %i" % self.status

Then for all models you want django-bitfield-manager to manage add the BitfieldMeta with a list of parent models
.. code-block::

    class ChildExample(models.Model):
        parent = models.ForeignKey('ParentExample', null=True)

        class BitfieldMeta:
            parent_models = [('parent', 'status', 0)]


The list of parent models takes in a tuple. The first field is the name of the field on the child model that the
bitfield-manager should use for modifying the status (should be a foreignkey, have not tested other relationships.) The
second is the name of the BigIntegerField or BitField (if using django-bitfield) that you want modified. The 3rd field
is the bitflag to use (i.e. 0 will be 1 << 0, 1 will be 1 << 1, etc.)


Features
--------

* Allows for automatic bitfield management for Django Models.
* Will update the status when models are added or deleted
* Supports multi-level relationships (use dot syntax)
* Supports django-bitfield

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
