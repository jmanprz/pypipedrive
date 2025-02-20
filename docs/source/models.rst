.. include:: _substitutions.rst


Models
==============


Defining Models
---------------

The :class:`~pypipedrive.orm.Model` class implements in an ORM-style the Pipedrive entities defined in :class:`~pypipedrive.models.*`.

.. code-block:: python

    from pypipedrive.models import Deals

    deal = Deals.all()