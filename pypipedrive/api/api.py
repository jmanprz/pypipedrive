import os
from requests.sessions import Session
from requests import Response
from typing import Dict


V1 = "v1"
V2 = "v2"
VERSIONS = {V1: "v1", V2: "api/v2"}


class Api:
    """
    Pipedrive API client for https://developers.pipedrive.com/docs/api/v1
    documentation.

    Supports the Piperive API V1 and V2 versions. By default, the ``Api``
    instance is initialized with the V2 version. When the Model doesn't
    support it, it fallbacks to the V1 version. However, it is possible to 
    force the usage of V1 version:

    >>> from pypipedrive.api import Api, V1
    >>> Api(version=V1)
    """

    if "PIPEDRIVE_API_TOKEN" not in os.environ:
        raise ValueError("PIPEDRIVE_API_TOKEN is not set in environment variables.")
    api_token = os.environ["PIPEDRIVE_API_TOKEN"]

    def __init__(self, version=V2) -> None:
        """
        Initialize the API client with the given version.

        Args:
            version (str, optional): API version. Defaults to V2.
        """
        assert version in VERSIONS, f"Invalid version: {version} (expected {VERSIONS.keys()})"
        self.session = Session()
        self.version = VERSIONS[version]
        self.endpoint_url = f"https://api.pipedrive.com/{self.version}/"
    
    def __repr__(self) -> str:
        return f"<pypipedrive.{self.__class__} version={self.version}>"
    
    def get(self, uri: str, params: Dict = {}) -> Response:
        """
        Make a GET request to the Pipedrive API.

        Args:
            uri (str): API endpoint
            params (Dict, optional): Query parameters. Defaults to {}.
        """
        params = {**params, "api_token": self.api_token}
        return self.session.request(
            method="GET",
            url=self.endpoint_url + uri,
            params=params
        )
    
    def post(self, uri: str, body: Dict) -> Response:
        """
        Make a POST request to the Pipedrive API.

        Args:
            uri (str): API endpoint
            body (Dict): Request body
        """
        return self.session.request(
            method="POST",
            url=self.endpoint_url + uri,
            params={"api_token": self.api_token},
            json=body
        )
    
    def patch(self, uri: str, body: Dict) -> Response:
        """
        Make a PATCH request to the Pipedrive API.

        Args:
            uri (str): API endpoint
            body (Dict): Request body
        """
        return self.session.request(
            method="PATCH",
            url=self.endpoint_url + uri,
            params={"api_token": self.api_token},
            json=body
        )

    def delete(self, uri: str) -> Response:
        """
        Make a DELETE request to the Pipedrive API.

        Args:
            uri (str): API endpoint
        """
        return self.session.request(
            method="DELETE",
            url=self.endpoint_url + uri,
            params={"api_token": self.api_token}
        )

    def batch_delete(self, uri: str, ids: str) -> Response:
        """
        Make a batch DELETE request to the Pipedrive API.

        Args:
            uri (str): API endpoint
            ids (str): Comma-separated string of integers
        """
        assert ids is not None, "ids cannot be None"
        assert isinstance(ids, str), "ids must be a comma-separated string of integers"
        assert all(map(lambda x: x.isdigit(), ids.split(","))), "ids must be a comma-separated string of integers"
        return self.session.request(
            method="DELETE",
            url=self.endpoint_url + uri,
            params={"api_token": self.api_token, "ids": ids}
        )