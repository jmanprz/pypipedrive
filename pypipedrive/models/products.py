from typing import Any, List, Dict, Self, Union
from pypipedrive.api import V1, V2
from pypipedrive.api.api import ApiResponse
from pypipedrive.utils import (
    warn_endpoint_legacy,
    warn_endpoint_beta,
    build_multipart_file_tuple
)
from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F
from pypipedrive.orm.types import PriceDict, assert_typed_dict
from .item_search import ItemSearch
from .files import Files


class Products(Model):
    """
    Products are the goods or services you are dealing with. Each product can 
    have N different price points - firstly, each product can have a price in 
    N different currencies, and secondly, each product can have N variations 
    of itself, each having N prices in different currencies. Note that only one 
    price per variation per currency is supported. Products can be instantiated 
    to deals. In the context of instatiation, a custom price, quantity, duration 
    and discount can be applied.

    Pipedrive API reference: https://developers.pipedrive.com/docs/api/v1/Products

    Get all products.
    GET[Cost:20] v1/products DEPRECATED
    GET[Cost:10] v2/products

    Search products.
    GET[Cost:40] v1/products/search DEPRECATED
    GET[Cost:20] v2/products/search

    Get one product.
    GET[Cost:20] v1/products/{id} DEPRECATED
    GET[Cost:10] v2/products/{id}

    Get deals where a product is attached to
    GET[Cost:20] v1/products/{id}/deals

    List files attached to a product
    GET[Cost:20] v1/products/{id}/files

    List followers of a product
    GET[Cost:20] v1/products/{id}/followers DEPRECATED
    GET[Cost:10] v2/products/{id}/followers

    List permitted users
    GET[Cost:20] v1/products/{id}/permittedUsers

    List followers changelog of a product
    GET[Cost:10] v2/products/{id}/followers/changelog

    Get all product variations
    GET[Cost:10] v2/products/{id}/variations

    Get image of a product [BETA]
    GET[Cost:10] v2/products/{id}/images

    Add a product
    POST[Cost:10] v1/products DEPRECATED
    POST[Cost:5]  v2/products

    Add a follower to a product
    POST[Cost:10] v1/products/{id}/followers DEPRECATED
    POST[Cost:5]  v2/products/{id}/followers

    Duplicate a product
    POST[Cost:5] v2/products/{id}/duplicate

    Add a product variation
    POST[Cost:5] v2/products/{id}/variations

    Upload an image for a product [BETA]
    POST[Cost:5] v2/products/{id}/images

    Update a product
    PUT[Cost:10]  v1/products/{id} DEPRECATED
    PATCH[Cost:5] v2/products/{id}

    Update an image for a product [BETA]
    PUT[Cost:20] v2/products/{id}/images

    Delete a product.
    DELETE[Cost:6] v1/products/{id} DEPRECATED
    DELETE[Cost:3] v2/products/{id}

    Delete a follower from a product.
    DELETE[Cost:6] v1/products/{id}/followers/{follower_id} DEPRECATED
    DELETE[Cost:3] v2/products/{id}/followers/{follower_id}

    Delete a product variation
    DELETE[Cost:3] v2/products/{id}/variations/{product_variation_id}

    Delete the image of a product
    DELETE[Cost:6] v2/products/{id}/images
    """

    id                       = F.IntegerField("id", readonly=True)
    name                     = F.TextField("name")
    code                     = F.TextField("code")
    description              = F.TextField("description")
    unit                     = F.TextField("unit")
    tax                      = F.NumberField("tax")
    category                 = F.TextField("category")
    is_linkable              = F.BooleanField("is_linkable")
    is_deleted               = F.BooleanField("is_deleted", readonly=True)
    visible_to               = F.IntegerField("visible_to")
    owner_id                 = F.IntegerField("owner_id", readonly=True)
    add_time                 = F.DatetimeField("add_time", readonly=True)
    update_time              = F.DatetimeField("update_time", readonly=True)
    billing_frequency        = F.TextField("billing_frequency")
    billing_frequency_cycles = F.IntegerField("billing_frequency_cycles")
    prices                   = F.PricesField("prices")
    custom_fields            = F.CustomFieldsProductField("custom_fields")

    class Meta:
        entity_name = "products"
        version     = V2
    
    @classmethod
    def batch_delete(cls, *args, **kwargs) -> Any:
        raise NotImplementedError("Products.batch_delete() is not allowed.")

    @classmethod
    def search(cls, term: str = None, params: Dict = {}) -> List[ItemSearch]:
        """
        Searches all products by name, code and/or custom fields. This endpoint 
        is a wrapper of `/v1/itemSearch` with a narrower OAuth scope.

        Allowed query params:
            - term (str): The search term to look for.
            - fields (str): Comma-separated list of fields to search in.
            - exact_match (bool): full exact matches against the given term returned?
            - include_fields (str): optional fields to include (comma-separated).
            - limit (int): number of results to return (default: 10, max: 100).
            - cursor (str): cursor for pagination.

        Args:
            term: The search term to look for. Minimum 2 characters
                  (or 1 if using exact_match). Please note that the search 
                  term has to be URL encoded.
            params: Query params passed to the API (copied internally).
        Returns:
            List of ItemSearch objects.
        """
        return ItemSearch.search(term=term, item_types=["product"], params=params)

    @warn_endpoint_legacy
    def deals(self, status: str = None, params: Dict = {}) -> List[Dict]:
        """
        V1 endpoint. List deals attached to a product. Allowed query params:
            - limit (int): Amount of results to return. Default: 100. Max: 500.
            - cursor (str): For pagination, the marker (an opaque string value) 
                            representing the first item on the next page
            - status (str): Only fetch deals with a specific status. If omitted, 
                            all not deleted deals are returned. If set to deleted,
                            deals that have been deleted up to 30 days ago will 
                            be included. Default `all_not_deleted`.
                            Values: open, won, lost, deleted, all_not_deleted.

        Args:
            status (str): Filter deals by status.
            params: Query params passed to the API (copied internally).
        Returns:
            List of deals data.
        """
        ALLOWED_VALUES = ["open", "won", "lost", "deleted", "all_not_deleted"]
        if status not in [None, ""]:
            assert status in ALLOWED_VALUES, f"`status` must be one of: {', '.join(ALLOWED_VALUES)}"
            params.update({"status": status})

        uri = f"{self._get_meta('entity_name')}/{self.id}/deals"
        return self.get_api(version=V1).all(uri=uri, params=params).to_dict()

    @warn_endpoint_legacy
    def files(self, params: Dict = {}) -> List[Files]:
        """
        V1 endpoint. List files attached to a product. Allowed query params:
            - start (int): The starting offset of the page.
            - limit (int): Amount of results to return. Default: 100. Max: 500.
            - sort (str): Supported fields: `id`, `update_time`

        Args:
            params: Query params passed to the API (copied internally).
        Returns:
            A list of file objects.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/files"
        response: ApiResponse = self.get_api(version=V1).all(uri=uri, params=params)
        return [Files(**f) for f in response.data]

    def followers(self, params: Dict = {}) -> List[Dict]:
        """
        List followers of a product. Allowed query params:
            - limit (int): Amount of results to return. Default: 100. Max: 500.
            - cursor (str): For pagination, the marker (an opaque string value) 
                            representing the first item on the next page

        Args:
            params: Query params passed to the API (copied internally).
        Returns:
            A list of follower dictionaries.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/followers"
        return self.get_api(version=V2).all(uri=uri, params=params).to_dict()
    
    @warn_endpoint_legacy
    def permitted_users(self) -> List[Dict]:
        """
        V1 endpoint. List permitted users of a product.

        Returns:
            A list of permitted user dictionaries.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/permittedUsers"
        return self.get_api(version=V1).all(uri=uri).to_dict()

    def followers_changelog(self, params: Dict = {}) -> List[Dict]:
        """
        List followers changelog of a product. Allowed query params:
            - limit (int): Amount of results to return. Default: 100. Max: 500.
            - cursor (str): For pagination, the marker (an opaque string value) 
                            representing the first item on the next page

        Args:
            params: Query params passed to the API (copied internally).
        Returns:
            A list of follower changelog dictionaries.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/followers/changelog"
        return self.get_api(version=V2).all(uri=uri, params=params).to_dict()
    
    def variations(self, params: Dict = {}) -> List[Dict]:
        """
        Get all product variations. Allowed query params:
            - limit (int): Amount of results to return. Default: 100. Max: 500.
            - cursor (str): For pagination, the marker (an opaque string value) 
                            representing the first item on the next page

        Args:
            params: Query params passed to the API (copied internally).
        Returns:
            A list of product variation dictionaries.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/variations"
        return self.get_api(version=V2).all(uri=uri, params=params).to_dict()

    @warn_endpoint_beta
    def images(self) -> List[Dict]:
        """
        Get image of a product [BETA].

        Returns:
            A list of product image dictionaries.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/images"
        return self.get_api(version=V2).all(uri=uri).to_dict()

    @warn_endpoint_beta
    def add_image(
        self,
        data: bytes = None,
        file_name: str = None,
        content_type: str = None) -> Dict:
        """
        [BETA] Upload an image for a product.

        Args:
            data: One image supplied in the multipart/form-data encoding.
        Returns:
            The API response data as a dictionary.
        """
        files = {
            "data": build_multipart_file_tuple(
                data         = data,
                file_name    = file_name,
                content_type = content_type
            )
        }
        uri = f"{self._get_meta('entity_name')}/{self.id}/images"
        return self.get_api(version=V2).post(uri=uri, files=files).to_dict()

    @warn_endpoint_beta
    def update_image(
        self,
        data: bytes = None,
        file_name: str = None,
        content_type: str = None) -> Dict:
        """
        [BETA] Update an image for a product.

        Args:
            data: One image supplied in the multipart/form-data encoding.
            file_name: The name of the file.
            content_type: The MIME type of the file.
        Returns:
            The API response data as a dictionary.
        """
        files = self._build_multipart_files(
            data=data,
            file_name=file_name,
            content_type=content_type
        )
        uri = f"{self._get_meta('entity_name')}/{self.id}/images"
        return self.get_api(version=V2).put(uri=uri, files=files).to_dict()
    
    @warn_endpoint_beta
    def delete_image(self) -> Dict:
        """
        [BETA] Delete an image for a product.

        Returns:
            The API response data as a dictionary.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/images"
        return self.get_api(version=V2).delete(uri=uri).to_dict()

    def add_follower(self, user_id: int = None) -> Dict:
        """
        Add a follower to a product.

        Args:
            user_id: The ID of the user to add as a follower.
        Returns:
            The API response data as a dictionary.
        """
        assert user_id is not None, "`user_id` must be provided."
        assert isinstance(user_id, int), "`user_id` must be an integer."
        uri = f"{self._get_meta('entity_name')}/{self.id}/followers"
        body = {"user_id": user_id}
        return self.get_api(version=V2).post(uri=uri, json=body).to_dict()
    
    def delete_follower(self, follower_id: int = None) -> Dict:
        """
        Delete a follower from a product.

        Args:
            follower_id: The ID of the follower to delete.
        Returns:
            The API response as a dictionary.
        """
        assert isinstance(follower_id, int), "`follower_id` must be int."
        uri = f"{self._get_meta('entity_name')}/{self.id}/followers/{follower_id}"
        return self.get_api(version=V2).delete(uri=uri).to_dict()

    def duplicate(self) -> Self:
        """
        Duplicate a product.

        Returns:
            The newly created Product instance.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/duplicate"
        response = self.get_api(version=V2).post(uri=uri)
        return Products(**response.data)

    def add_variation(
        self,
        name: str = None,
        prices: List[Union[Dict, PriceDict]] = []) -> Dict:
        """
        Add a product variation.

        Args:
            name: The name of the product variation.
            prices: A list of price dictionaries/instances for the variation.
        """
        assert name not in [None, ""], "`name` must be provided."
        payload = []
        for price in prices:
            if isinstance(price, dict):
                assert_typed_dict(PriceDict, {**price, "product_id": self.id})
                payload.append({**price, "product_id": self.id})
            elif isinstance(price, PriceDict):
                price.product_id = self.id
                payload.append(price.model_dump())
            else:
                raise TypeError(
                    f"`prices` items must be of type `dict` or `PriceDict`, "
                    f"got: {type(price)}"
                )
        params = {"name": name, "prices": payload}
        uri = f"{self._get_meta('entity_name')}/{self.id}/variations"
        return self.get_api(version=V2).post(uri=uri, json=params).to_dict()
        
    def delete_variation(self, product_variation_id: int = None) -> Dict:
        """
        Delete a product variation.

        Args:
            product_variation_id: The ID of the product variation to delete.
        Returns:
            The API response as a dictionary.
        """
        assert isinstance(product_variation_id, int), "`product_variation_id` must be int."
        uri = f"{self._get_meta('entity_name')}/{self.id}/variations/{product_variation_id}"
        return self.get_api(version=V2).delete(uri=uri).to_dict()