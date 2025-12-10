Models
======

Defining Models
---------------

The :class:`~pypipedrive.orm.Model` class implements in an ORM-style the Pipedrive entities defined in :class:`~pypipedrive.models.*`. Each entity class inherits from the :class:`~pypipedrive.orm.Model` class and defines its fields using class :class:`~pypipedrive.orm.fields.Field`, relationships, and behaviors.

The basic definition of a model looks like this:

.. code-block:: python

    from pypipedrive.orm import Model
    from pypipedrive.api import V2
    from pypipedrive.orm import fields as F

    class Entity(Model):

        id   = F.IntegerField("id", readonly=True)
        name = F.TextField("subject")
        
        class Meta:
            entity_name = "entity"
            version     = V2

The ``Meta`` class inside the model definition specifies the entity name as defined in the Pipedrive API and the API version to use (V1 or V2). The ``entity_name`` is used to build the API endpoints for the model.

.. note::

    All entities are already defined in the :mod:`~pypipedrive.models` module. You can directly import and use them without redefining.

CRUD Operations
---------------

The :class:`~pypipedrive.orm.Model` class provides class methods and instance methods to perform CRUD operations on the Pipedrive entities.

- **Create**: To create a new record, instantiate the model and call the ``save()`` method.

.. code-block:: python

    from pypipedrive.models import Deals

    new_deal = Deals(title="New Deal", ...)
    new_deal.save()
    print(new_deal.id)  # The ID is assigned after saving

- **Update**: To update an existing record, modify its attributes and call the ``save()`` method.

.. code-block:: python

    deal = Deals.get(id=1)
    deal.title = "Updated Deal Title"
    deal.save()

- **Retrieve**: To retrieve a record by its ID, use the ``get()`` class method.

.. code-block:: python

    deal = Deals.get(id=1)
    print(deal.title)

- **List**: To list records with optional filtering, use the ``all()`` class method.

.. code-block:: python

    deals = Deals.all(params={...})
    for deal in deals:
        print(deal.id, deal.title)

- **Delete**: To delete a record, call the ``delete()`` method on the instance.

.. code-block:: python

    deal = Deals.get(id=1)
    deal.delete()

- **Batch delete**: To delete multiple records at once, use the ``batch_delete()`` class method.

.. code-block:: python

    Deals.batch_delete(ids=[1, 2, 3])

These methods handle the necessary API calls and data serialization/deserialization automatically.

Other :class:`~pypipedrive.orm.Model` methods include:

- **Fetch**: Refresh the instance data from the API.

.. code-block:: python

    deal = Deals.get(id=1)
    deal.fetch()

- **Exists**: Check if a record exists by its ID.

.. code-block:: python

    exists: bool = Deals.exists(id=1)

- **To record**: Convert the instance to its dictionary representation using Pipedrive field names.

.. code-block:: python

    deal = Deals.get(id=1)
    record_dict = deal.to_record()

- **From record**: Create an instance from a dictionary representation.

.. code-block:: python

    record = {...}
    deal = Deals.from_record(record)