from typing import List
from typing_extensions import Self
from pypipedrive.api import V1
from pypipedrive.utils import warn_endpoint_legacy
from pypipedrive.orm.model import Model, SaveResult
from pypipedrive.orm import fields as F


class OrganizationRelationships(Model):
    """
    Organization relationships represent how different organizations are related 
    to each other. The relationship can be hierarchical (parent-child companies) 
    or lateral as defined by the type `field` - either `parent` or `related`.

    See `OrganizationRelationships API reference <https://developers.pipedrive.com/docs/api/v1/OrganizationRelationships>`_.

    Get all relationships for organization.

      * GET[Cost:20] ``v1/organizationRelationships``

    Get one organization relationship.
      * GET[Cost:2] ``v1/organizationRelationships/{id}``

    Create an organization relationship.

      * POST[Cost:10] ``v1/organizationRelationships``

    Update an organization relationship.

      * PUT[Cost:10] ``v1/organizationRelationships/{id}``

    Delete an organization relationship.

      * DELETE[Cost:6] ``v1/organizationRelationships/{id}``
    """

    id                        = F.IntegerField("id")
    type                      = F.TextField("type")
    related_organization_name = F.TextField("related_organization_name")
    calculated_type           = F.TextField("calculated_type")
    calculated_related_org_id = F.IntegerField("calculated_related_org_id")
    rel_owner_org_id          = F.IntegerField("rel_owner_org_id")
    rel_linked_org_id         = F.IntegerField("rel_linked_org_id")
    add_time                  = F.DatetimeField("add_time")
    update_time               = F.DatetimeField("update_time")
    active_flag               = F.BooleanField("active_flag")

    class Meta:
        entity_name = "organizationRelationships"
        version     = V1

    @warn_endpoint_legacy
    @classmethod
    def get(cls, id: int, org_id: int = None) -> Self:
        """
        Finds and returns an organization relationship from its ID.

        Args:
            id: The ID of the organization relationship.
            org_id: The ID of the base org for the returned calculated values.
        Returns:
            An OrganizationRelationships instance.
        """
        params = None
        assert isinstance(id, int), "`id` must be an integer"
        if org_id is not None:
            assert isinstance(org_id, int), "`org_id` must be an integer"
            params = {"org_id": org_id}
        return super().get(id=id, params=params)

    @warn_endpoint_legacy
    @classmethod
    def all(cls, org_id: int) -> List[Self]:
        """
        Gets all of the relationships for a supplied organization ID.

        Args:
            org_id: The ID of the organization to get relationships for.
        Returns:
            A list of OrganizationRelationships instances.
        """
        assert isinstance(org_id, int), "`org_id` must be an integer"
        return super().all(params={"org_id": org_id})

    @warn_endpoint_legacy
    def save(self, force: bool = False) -> SaveResult:
        """
        Updates and returns an organization relationship.

        Allowed query parameters:

            - ``org_id`` (int): The ID of the base organization for the 
              returned calculated values.
            - ``type`` (str):   The type of relationship (`parent` or `related`).
            - ``rel_owner_org_id`` (int): The owner of this relationship. If 
              type is parent, then the owner is the parent and the linked 
              organization is the daughter.
            - ``rel_linked_org_id`` (int): The linked organization in this 
              relationship. If type is parent, then the linked organization is 
              the daughter.

        To create a new organization relationship, ``type``, 
        ``rel_owner_org_id`` and ``rel_linked_org_id`` must be provided.

        Args:
            force: Whether to force the save operation.
        Returns:
            A SaveResult object containing the result of the save operation.
        """
        return super().save(force=force)

    @warn_endpoint_legacy
    def delete(self, *args, **kwargs) -> bool:
        """
        Deletes an organization relationship and returns the deleted ID.

        Returns:
            A boolean indicating whether the deletion was successful.
        """
        return super().delete(*args, **kwargs)

    @warn_endpoint_legacy
    @classmethod
    def batch_delete(cls, *args, **kwargs):
        raise NotImplementedError("OrganizationRelationships.batch_delete() is not allowed.")