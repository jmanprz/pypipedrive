import logging
import requests
import pydantic
from typing import Any, Dict, Iterator, List, Optional, Union
from functools import partialmethod
from .exceptions import raise_from_error_response


V1 = "v1"
V2 = "v2"
VERSIONS = {V1: "v1", V2: "api/v2"}


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# ApiResponse.data type
T_DATA = Union[Dict[str, Any], List[Union[int, str]], List[Dict[str, Any]]]
T_ADDITIONAL_DATA = Union[Dict[str, Any], List[Union[int, str]], List[Dict[str, Any]]]
T_RELATED_OBJECTS = Union[Dict[str, Any], List[Dict[str, Any]]]


class ApiResponse(pydantic.BaseModel):
    success:         Optional[bool] = None
    data:            Optional[T_DATA] = None
    additional_data: Optional[T_ADDITIONAL_DATA] = {}
    related_objects: Optional[T_RELATED_OBJECTS] = {}

    def to_dict(self):
        return self.model_dump(include={"data", "related_objects"})


class Api:
    """
    Pipedrive API client for https://pipedrive.readme.io/docs/
    documentation.

    Supports the Piperive API V1 and V2 versions. By default, the ``Api``
    instance is initialized with the V2 version. When the Model doesn't
    support it, it fallbacks to the V1 version. However, it is possible to 
    force the usage of V1 version:

    >>> from pypipedrive.api import Api, V1
    >>> Api(version=V1)
    """

    def __init__(self, api_token: str = None, version=V2) -> None:
        """
        Initialize the API client with the given version.

        Args:
            api_token: Pipedrive API token. If not provided, it will be read
                       from the ``PIPEDRIVE_API_TOKEN`` environment variable.
            version: API version. Defaults to V2.
        """
        if version not in VERSIONS:
            raise ValueError(f"Invalid version: {version} (expected {list(VERSIONS.keys())})")

        if api_token is None:
            raise ValueError("`api_token` must be provided")
            
        self.session = requests.Session()
        self.api_token = api_token
        self.version = VERSIONS[version]
        self.endpoint_url = f"https://api.pipedrive.com/{self.version}/"
    
    @property
    def api_token(self) -> str:
        """
        Pipedrive API token used in all calls.
        """
        return self._api_token

    @api_token.setter
    def api_token(self, value: str) -> None:
        self.session.params.update({"api_token": value})
        self._api_token = value

    def __repr__(self) -> str:
        return f"<pypipedrive.{self.__class__.__name__} version={self.version}>"

    def update_method(self) -> partialmethod:
        """
        Determine the appropriate HTTP method for updating resources based
        on the API version.

        Returns:
            The appropriate partialmethod for updating resources.
        """
        if self.version == VERSIONS[V2]:
            return self.patch
        else:
            return self.put

    def build_url(self, uri: str) -> str:
        """
        Build the full URL for the given endpoint parts.

        Args:
            uri: The endpoint URI.
        Returns:
            Full URL
        """
        return self.endpoint_url + uri

    def process_response(self, response: requests.Response) -> ApiResponse:
        """
        Process the HTTP response from the Pipedrive API.

        Args:
            response: The HTTP response object.
        Returns:
            The processed response data.
        Raises:
            Appropriate exceptions based on the response status code.
        """
        payload = {}  # Set the payload variable
        try:
            payload = response.json()
        except requests.exceptions.JSONDecodeError:  # Response not JSON
            payload = {"data": {"content": response.content}}
        except Exception as exc:
            raise requests.exceptions.HTTPError(
                f"API request failed. Status code: {response.status_code}. "
                f"Reason: {response.reason}. Response content: {response.text}. "
                f"Exception: {exc}"
            )
        
        # Return ApiResponse or raise exception
        if response.ok:
            return ApiResponse(**payload)
        else:
            raise_from_error_response(
                code=response.status_code,
                version=self.version,
                error_response=payload
            )
        # try:
        #     payload = response.json()
        #     if response.ok:
        #         return ApiResponse(**payload)
        #     raise_from_error_response(
        #         code           = response.status_code,
        #         version        = self.version,
        #         error_response = payload
        #     )
        # except requests.exceptions.JSONDecodeError as exc:  # Response not JSON
        #     payload = {"data": {"content": response.content}}
        #     if response.ok:
        #         return ApiResponse(**payload)
        #     raise_from_error_response(
        #         code           = response.status_code,
        #         version        = self.version,
        #         error_response = payload
        #     )
        # except Exception as exc:
        #     raise requests.exceptions.HTTPError(
        #         f"API request failed. Status code: {response.status_code}. "
        #         f"Reason: {response.reason}. Response content: {response.text}. "
        #         f"Exception: {exc}"
        #     )

    def request(
        self,
        method: str,
        uri: str,
        headers: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None) -> ApiResponse:
        """
        Make a request to the Pipedrive API.

        Args:
            method: HTTP method to use.
            uri: The URI we're attempting to call.
            params: Additional query params to append to the URL as-is.
            json: The JSON payload for a POST/PUT/PATCH/DELETE request.
            files: Files to upload.
        """
        response = self.session.request(
            method=method,
            url=self.build_url(uri),
            headers=headers,
            params={**(params or {})},
            json=json,
            data=data,
            files=files,
        )
        logger.info(msg=f"{method}:{response.status_code} {uri}")
        return self.process_response(response)

    # By using partialmethod, we avoid repeating the "GET", "PUT", "POST", 
    # "PATCH" and "DELETE" strings each time the request is made (code cleaner)
    get = partialmethod(request, "GET")
    put = partialmethod(request, "PUT")  # V1 endpoints only
    post = partialmethod(request, "POST")
    patch = partialmethod(request, "PATCH")  # V2 endpoints only
    delete = partialmethod(request, "DELETE")

    def batch_delete(
        self,
        uri: str = None,
        ids: List[Union[int, str]] = []) -> ApiResponse:
        """
        Make a batch DELETE request to the Pipedrive API using `ids`.

        Args:
            uri: API endpoint
            ids: List of IDs to delete.
        Returns:
            The API response.
        """
        assert uri not in [None, ""], "`uri` must be provided."
        assert ids is not None, "`ids` cannot be None."
        assert isinstance(ids, list), "`ids` must be a list of integers or strings."
        assert all(isinstance(x, (int, str)) for x in ids), \
            "`ids` must be a list of integers or strings."
        return self.delete(uri=uri, params={"ids": ",".join(map(str, ids))})

    def iterator(
        self,
        uri: str = None,
        params: Optional[Dict[str, Any]] = None) -> Iterator[ApiResponse]:
        """
        Yield API responses for a paginated endpoint.

        Args:
            uri: Endpoint URI to call.
            params: Initial query parameters (copied internally).
        Yields:
            Each `requests.Response` returned by the API until pagination ends.
        """
        if uri is None:
            raise ValueError("`uri` must be provided")

        qparams: Dict[str, Any] = dict(params or {})
        while True:
            response: ApiResponse = self.get(uri=uri, params=qparams)
            if not response.success:
                break
            yield response

            # Safe guard: if no additional_data, stop pagination
            if not response.additional_data:
                break
            pagination = response.additional_data.get("pagination") or {}

            # V2 cursor-based pagination
            next_cursor = response.additional_data.get("next_cursor") or {}
            if next_cursor:
                qparams["cursor"] = next_cursor
                qparams.pop("start", None)
                continue

            # V1 start/limit pagination
            more = pagination.get("more_items_in_collection")
            if more:
                used_limit = qparams.get("limit") or pagination.get("limit") or 100
                try:
                    start = int(qparams.get("start", 0))
                except Exception:
                    start = 0
                qparams["start"] = start + int(used_limit)
                continue

            break  # No more pages

    def all(
        self,
        uri: str,
        params: Optional[Dict[str, Any]] = None) -> ApiResponse:
        """
        Make a GET request to retrieve all items from a paginated endpoint.

        Args:
            uri: Endpoint URI to call.
            params: Initial query parameters (copied internally).
        Returns:
            A list of all items retrieved from the paginated endpoint.
        """
        data: Union[T_DATA] = []
        success: bool = True
        related_objects: List[T_RELATED_OBJECTS] = []
        for response in self.iterator(uri=uri, params=params):
            success = success and response.success
            # Merge data, additional_data and related_objects for processing
            values = (
                ("data", response.data, data),
                ("related_objects", response.related_objects, related_objects),
            )
            for _, value, items in values:
                if value in [None, "", [], {}]:
                    continue
                elif isinstance(value, list):
                    items.extend(value)
                else:
                    items.append(value)

        return ApiResponse(
            success=success,
            data=data,
            related_objects=related_objects if related_objects else None
        )