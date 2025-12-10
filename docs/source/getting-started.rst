.. include:: _warn_latest.rst

Getting Started
===============

Installation
------------

.. code-block:: shell

    $ pip install pypipedrive-client

API token
-------------

To use the Pipedrive API you need an API token. If you do not have one yet, see the Pipedrive guide to find your `api token <https://pipedrive.readme.io/docs/how-to-find-the-api-token>`__.

This library will not persist your access token anywhere. Your access token should be securely stored.
A common method is to store it as an environment variable and load it using ``os.environ``.

Make sure to set the environment variable ``PIPEDRIVE_API_TOKEN`` with your API token value before using the library while working directly with the :class:`~pypipedrive.orm.Model` entities. :class:`~pypipedrive.Api` class also accepts the API token as a parameter.

.. note::

    You can only have one active API token per account at any time.

Quickstart
----------

This library provides two main interfaces to interact with the Pipedrive API.

- The :class:`~pypipedrive.Api` class represents the low-level Api interface to Pipedrive API. It allows you to make direct requests to any endpoint of the Pipedrive API while handling authentication, response parsing, and error handling.

.. code-block:: python

    >>> import os
    >>> from pypipedrive import Api
    >>> api = Api(api_token=os.environ["PIPEDRIVE_API_TOKEN"])
    >>> deal_id = 1 # define your deal identifier
    >>> api.get(uri="deals/1")
    ApiResponse(
        success=True,
        data={'id': 1, 'title': '...', '...'},
        additional_data={},
        related_objects={}
    )

The :class:`~pypipedrive.Api` exposes the methods ``get()``, ``post()``, ``put()`` (v1), ``patch()`` (v2) and ``delete()`` to interact with any endpoint of the Pipedrive API.

- The :class:`~pypipedrive.orm.Model` class is the parent class of the Pipedrive entities for retrieving, creating, and modifying any records in Pipedrive.

.. code-block:: python

    >>> from pypipedrive.models import Deals
    >>> deal = Deals.get(id=1)
    <Deals id=1>
    >>> deal.to_record()
    {
        'entity': 'deals',
        'created_at': '2025-11-15T12:00:00.000Z',
        'id': 1,
        'fields': {
            'id': 1,
            'title': 'Deal Title', 
        }
    }

See :doc:`models` for more details on how to get and set data in Pipedrive.