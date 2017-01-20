=====
Usage
=====

To use bitfield_manager in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'bitfield_manager.apps.BitfieldManagerConfig',
        ...
    )

Add bitfield_manager's URL patterns:

.. code-block:: python

    from bitfield_manager import urls as bitfield_manager_urls


    urlpatterns = [
        ...
        url(r'^', include(bitfield_manager_urls)),
        ...
    ]
