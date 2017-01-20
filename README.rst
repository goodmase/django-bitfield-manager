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

Documentation
-------------

The full documentation is at https://django-bitfield-manager.readthedocs.io.

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


Features
--------

* Allows for automatic bitfield management for Django Models

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
