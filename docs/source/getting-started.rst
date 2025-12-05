.. include:: _warn_latest.rst
.. include:: _substitutions.rst


Getting Started
===============

Installation
------------

Add the `pypipedrive <https://pypi.org/project/pypipedrive>`_ library to your project just as you would any other:

.. code-block:: shell

    $ pip install pypipedrive


API token
-------------

To begin, you will need an API token. If you do not have one yet, see the Pipedrive guide to find your `api token <https://pipedrive.readme.io/docs/how-to-find-the-api-token>`__.

This library will not persist your access token anywhere. Your access token should be securely stored.
A common method is to store it as an environment variable and load it using ``os.environ``.

.. note::

    You can only have one active API token per account at any time.


Quickstart
----------

The :class:`~pypipedrive.Api` class represents the low-level Api interface to Pipedrive API while the
:class:`~pypipedrive.orm.Model` class is the parent class of the Pipedrive entities for retrieving, creating, and modifying
records in Pipedrive:

.. code-block:: python

    >>> import os
    >>> from pypipedrive import Api
    >>> os.environ['PIPEDRIVE_API_TOKEN'] = 'your_api_token'
    >>> api = Api() # default to v2
    >>> deal_id = 1 # define your deal identifier
    >>> api.get(uri=f'deals/{deal_id}')
    {
        "success": true,
        "data": {
            "id": 1,
            "title": "Sample Deal",
            ...
        }
    }
    >>> api.get(uri='deals', params={'owner_id': '1'})
    {
        "success": true,
        "data": [
            {
                "id": 1,
                "title": "Sample Deal",
                ...
            },
            ...
        ]
    }
    >>> api.post(uri='deals', body={'title': 'New Deal'})
    {
        "success": true,
        "data": {
            "id": 2,
            "title": "New Deal",
            ...
        }
    }
    >>> api.patch(uri=f'deals/{deal_id}', body={'title': 'Updated Deal'})
    {
        "success": true,
        "data": {
            "id": 1,
            "title": "Updated Deal",
            ...
        }
    }
    >>> api.delete(uri=f'deals/{deal_id}')
    {
        "success": true,
        "data": {
            "id": 1,
            "deleted": true
        }
    }

See :doc:`models` for more details on how to get and set data in Airtable.