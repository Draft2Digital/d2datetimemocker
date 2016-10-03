==============
datetimemocker
==============

.. image:: https://travis-ci.org/Draft2Digital/d2datetimemocker.png?branch=master
    :target: https://travis-ci.org/Draft2Digital/d2datetimemocker


.. code-block:: python

    with DateTimeMocker():
        # datetime is mocked everywhere.

For examples, see the unittests at `/datetimemocker/test/test_datetimemocker.py`


Installation
------------

1. Install the package:

    .. code-block:: bash

        $ pip install datetimemocker

2. Import ``datetime`` and ``DateTimeMocker`` in your test file.

    .. code-block:: python

        # test.py
        from datetimemocker import DateTimeMocker
        import datetime

3. Define the ``datetime`` or ``date`` instance you wish to use as your mock value.

    .. code-block:: python

        def test():
            datetime_to_use = datetime.datetime(2016, 7, 8, 16, 0, 0)


4. Using the ``with`` context manager, pass the datetime instance you wish as your mock value.

    .. code-block:: python

            with DateTimeMocker(datetime_to_use=datetime_to_use):
                assert(...)

* Or pass a ``date`` instance to ``date_to_use``:

   .. code-block:: python

            date_to_use = datetime.date(2016, 7, 8)
            with DateTimeMocker(date_to_use=date_to_use):
                assert(...)



API
---

The ``datetime`` module implements all of the following backend functions:

* ``instance_check()``
* ``make_mock_date_time()``
* ``make_mock_date()``
* ``make_mock_date_time_module()``

``DateTimeMocker`` implements all of the following backend methods.

* ``__init__()``
* ``__add_mocking_to_module()``
* ``__enter__()``
* ``__exit__()``


How to use the DateTimeMocker keyword arguments to customize the mocked values.
-------------------------------------------------------------------------------

``DateTimeMocker.__init__(self, datetime_to_use=None, date_to_use=None, modules=None, search_for_modules=True)**:``

Passing in a ``datetime`` instance to the ``datetime_to_use`` argument will set
the ``datetime`` instance as the return value of ``datetime.now()``.

For example, with datetime_to_use set to ``datetime(2016, 7, 8, 13, 0, 5, 72, tzinfo=pytz.UTC)``:

``datetime.now()`` returns ``2016-07-08 13:00:05.000072+00:00``
``datetime.date.today()`` returns ``2016-07-08``

Likewise, pasing in a ``date`` instance to the ``date_to_use`` argument will set
the ``date`` instance as the return value of ``datetime.today()``.

For example, with ``date_to_use`` set to ``datetime.date(2016, 7, 8)``:
``datetime.now()`` returns ``2016-07-08 03:07:59.330384+00:00``
``datetime.date.today()`` returns ``2016-07-08``

Notice, however that the times are different in the two examples. When passing in a
``datetime`` instance, the time value of the ``datetime`` instance is applied to the
mock as well. When passing in a ``date`` instance, however, the time portion of the
``datetime`` instance returned by ``datetime.now()`` is inherited from an newly-created
instance, and so the time value is "now" (the time on the server) on the mocked date.

By default, the DateTimeMocker will mock all loaded modules with references to datetime.
However, if you wish to restrict the mock to specific modules, you may pass them in as
an iterable to the ``modules`` argument.

For example:
``with DateTimeMocker(datetime_to_use=datetime_to_use, modules=(module1, module2)):``

This will only apply the mock to these two modules.

The ``search_for_modules`` argument is ``True`` by default. If ``True`` the ``DateTimeMocker``
will iterate through all modules loaded in the environment and apply the mock, except for the
``datetime`` modules and the current module.


How it works
------------

Using the ``with`` context manager, instantiating a ``DateTimeMocker`` class will
create mock ``datetime`` and ``date`` classes and a mock ``datetime`` module.
Then the DateTimeMocker instance will iterate over a list of modules and mock all
references to ``datetime`` or ``date`` with the mock module and classes.
Upon exiting the context (un-indenting), the mocks will be stopped gracefully.