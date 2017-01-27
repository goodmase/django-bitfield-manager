=============================
bitfield_manager
=============================

.. image:: https://badge.fury.io/py/django-bitfield-manager.svg
    :target: https://badge.fury.io/py/django-bitfield-manager

.. image:: https://travis-ci.org/goodmase/django-bitfield-manager.svg?branch=master
    :target: https://travis-ci.org/goodmase/django-bitfield-manager

.. image:: https://codecov.io/gh/goodmase/django-bitfield-manager/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/goodmase/django-bitfield-manager

.. image:: https://readthedocs.org/projects/django-bitfield-manager/badge/?version=latest
    :target: http://django-bitfield-manager.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Automatic bitfield management for Django Models. 


Quickstart
----------

Install bitfield_manager::

    pip install django-bitfield-manager

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'bitfield_manager',
        ...
    )


Usage
--------
First you'll need a parent model with a status field

.. code-block:: python

    from django.db import models
    from bitfield_manager.models import ParentBitfieldModel, ChildBitfieldModelMixin


    class ParentExample(ParentBitfieldModel):
        status = models.BigIntegerField()

    def __str__(self):  # __unicode__ on Python 2
        return "status: %i" % self.status

Then for all models you want django-bitfield-manager to manage add the BitfieldMeta with a list of parent models.
The list of parent models takes in a tuple. The first field is the name of the field on the child model that the
bitfield-manager should use for modifying the status (should be a foreignkey, have not tested other relationships.) The
second is the name of the BigIntegerField or BitField (if using django-bitfield) that you want modified. The 3rd field
is the bitflag to use (i.e. 0 will be 1 << 0, 1 will be 1 << 1, etc.)

.. code-block:: python

    class ChildExample1(ChildBitfieldModelMixin, models.Model):
        parent = models.ForeignKey('ParentExample', null=True)

        class BitfieldMeta:
            parent_models = [('parent', 'status', 0)]

    class ChildExample2(ChildBitfieldModelMixin, models.Model):
        parent = models.ForeignKey('ParentExample', null=True)

        class BitfieldMeta:
            parent_models = [('parent', 'status', 1)]

Now when creating/deleting child models the parent status should update

.. code-block:: python

    # create the model
    p = ParentExample.objects.create(status=0)
    p2 = ParentExample.objects.create(status=0)
    # add a child p.status is now 1
    c1 = ChildExample1.objects.create(parent=p)

    # add the other child. p.status is now 3
    c2 = ChildExample2.objects.create(parent=p)

    # deleting a child will refresh the status. p.status is now 2
    c1.delete()

    # updates or mass deletes will require manual refresh
    # p.status will be 2 and p2.status will be 0
    ChildExample2.objects.filter(parent=p).update(parent=p2)

    # trigger a manual refresh. p.status is now correct with a status of 0
    p.force_status_refresh()

    # if you know the related models modified you can specify them
    # p2.status is now 2
    p2.force_status_refresh(related_models=[ChildExample2])

    # force status refresh will work with models multiple levels deep. Specify the search_depth to search
    # more than 1 level deep
    p2.force_status_refresh(search_depth=2)



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
