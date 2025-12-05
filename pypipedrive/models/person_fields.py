from typing import Dict, List
from typing_extensions import Self
from pypipedrive.api import V1, V2
from pypipedrive.api.api import ApiResponse
from pypipedrive.utils import warn_endpoint_legacy
from pypipedrive.orm.model import Model, SaveResult
from pypipedrive.orm import fields as F


class PersonFields(Model):
    """
    Person fields represent the near-complete schema for a person in the 
    context of the company of the authorized user. Each company can have a 
    different schema for their persons, with various custom fields. In the 
    context of using person fields as a schema for defining the data fields of 
    a person, it must be kept in mind that some types of custom fields can have 
    additional data fields which are not separate person fields per se. Such 
    is the case with monetary, daterange and timerange fields - each of these 
    fields will have one additional data field in addition to the one presented 
    in the context of person fields. For example, if there is a monetary field 
    with the key `ffk9s9` stored on the account, `ffk9s9` would hold the numeric 
    value of the field, and `ffk9s9_currency` would hold the ISO currency code 
    that goes along with the numeric value. To find out which data fields are 
    available, fetch one person and list its keys.

    Pipedrive API reference: https://developers.pipedrive.com/docs/api/v1/DealFields

    Get all person fields
    GET[Cost:20] v1/personFields DEPRECATED
    GET[Cost:10] v2/personFields

    Get one person field
    GET[Cost:2] v1/personFields/{id} DEPRECATED
    GET[Cost:1] v2/personFields/{field_code}

    Add a new person field
    POST[Cost:10] v1/personFields DEPRECATED
    POST[Cost:5]  v2/personFields

    Add person field options in bulk
    POST[Cost:5] v2/personFields/{field_code}/options

    Update a person field
    PUT[Cost:10]  v1/personFields/{id} DEPRECATED
    PATCH[Cost:5] v2/personFields/{field_code}

    Update person field options in bulk
    PATCH[Cost:5] v2/personFields/{field_code}/options
    
    Delete multiple person fields in bulk
    DELETE[Cost:10] v1/personFields

    Delete a person field
    DELETE[Cost:6] v1/personFields/{id} DEPRECATED
    DELETE[Cost:3] v2/personFields/{field_code}

    Delete person field options in bulk
    DELETE[Cost:3] v2/personFields/{field_code}/options
    """

    id                         = F.TextField("id")  # Used for compatibility
    field_name                 = F.TextField("field_name")
    field_code                 = F.TextField("field_code")
    field_type                 = F.TextField("field_type")
    options                    = F.OptionsField("options")
    subfields                  = F.SubfieldField("subfields")
    is_custom_field            = F.BooleanField("is_custom_field")
    is_optional_response_field = F.BooleanField("is_optional_response_field")

    class Meta:
        entity_name = "personFields"
        version     = V2
        field_id    = "field_code"  # Indicates field used as the object id
    
    @classmethod
    def get(cls, id: str, params: Dict = {}) -> Self:
        """
        Returns metadata about a specific person field. Allowed query params:
            - include_fields (str): Optional comma separated string array of 
                                    additional data namespaces to include in 
                                    response. Values: `ui_visibility`, 
                                    `important_fields`, `required_fields`.
        
        Args:
            id: The code of the person field to retrieve.
            params: Additional query parameters.
        Returns:
            An instance of PersonFields representing the person field.
        """
        assert isinstance(id, str), "`id` must be a string"
        return super().get(id=id, params=params)

    def add_options(self, option_labels: List[Dict[str, str]]) -> Dict:
        """
        Adds new options to a person custom field that supports options (enum 
        or set field types). This operation is atomic - all options are added 
        or none are added. Returns only the newly added options.

        Args:
            option_labels: A list of option dictionaries to add. Each item must 
                           contain a label. At least one option is required.
        Returns:
            A dictionary containing the newly added options.
        """
        if self.field_type not in ["enum", "set"]:
            raise ValueError(
                "`PersonFields.add_options()` is only supported for "
                "'enum' and 'set' field types."
            )
        assert isinstance(self.field_code, str), "`field_code` must be a string"
        assert isinstance(option_labels, list), "`option_labels` must be a list"
        for option in option_labels:
            assert isinstance(option, dict), "each `option` must be a dict"
            assert list(option.keys()) == ["label"], \
                "each `option` must contain only the `label` key"
            assert isinstance(option.get("label"), str), \
                "`label` value must be a string"
        uri = f"{self._get_meta('entity_name')}/{self.field_code}/options"
        response = self.get_api(version=V2).post(uri=uri, json=option_labels)
        self.fetch()  # Refresh the model data after adding options
        return response.to_dict()

    def update_options(self, options: List[Dict]) -> Dict:
        """
        Updates existing options for a person custom field. This operation is 
        atomic and fails if any of the specified option IDs do not exist. 
        Returns only the updated options.

        Args:
            options: A list of option dictionaries to update. Each item must 
                     contain an id and label.
        Returns:
            A dictionary containing the updated options.
        """
        if self.field_type not in ["enum", "set"]:
            raise ValueError(
                "`PersonFields.update_options()` is only supported for "
                "'enum' and 'set' field types."
            )
        assert isinstance(self.field_code, str), "`field_code` must be a string"
        assert isinstance(options, list), "`options` must be a list"
        for option in options:
            assert isinstance(option, dict), "each `option` must be a dict"
            assert set(option.keys()) == {"id", "label"}, \
                "each `option` must contain only the `id` and `label` keys"
            assert isinstance(option.get("id"), int), "`id` value must be an integer"
            assert isinstance(option.get("label"), str), "`label` value must be a string"
        uri = f"{self._get_meta('entity_name')}/{self.field_code}/options"
        response = self.get_api(version=V2).patch(uri=uri, json=options)
        self.fetch()  # Refresh the model data after updating options
        return response.to_dict()

    def delete_options(self, option_ids: List[str]) -> Dict:
        """
        Removes existing options from a person custom field. This operation is 
        atomic and fails if any of the specified option IDs do not exist. 
        Returns only the deleted options.

        Args:
            option_ids: A list of option IDs to delete.
        Returns:
            A dictionary containing the deleted options.
        """
        if self.field_type not in ["enum", "set"]:
            raise ValueError(
                "`PersonFields.add_options()` is only supported for "
                "'enum' and 'set' field types."
            )
        assert isinstance(self.field_code, str), "`field_code` must be a string"
        assert isinstance(option_ids, list), "`option_ids` must be a list"
        for option in option_ids:
            assert isinstance(option, dict), "each `option` must be a dict"
            assert list(option.keys()) == ["id"], \
                "each `option` must contain only the `id` key"
            assert isinstance(option.get("id"), int), \
                "`id` value must be an integer"
        uri = f"{self._get_meta('entity_name')}/{self.field_code}/options"
        response = self.get_api(version=V2).delete(uri=uri, json=option_ids)
        self.fetch()  # Refresh the model data after deleting options
        return response.to_dict()

    @warn_endpoint_legacy
    @classmethod
    def batch_delete(cls, ids: List[str]) -> Dict:
        """
        Marks multiple fields as deleted.

        Args:
            ids: A list of field codes to delete.
        Returns:
            A dictionary containing the result of the batch delete operation.
        """
        return super().batch_delete(ids=ids, version=V1).to_dict()