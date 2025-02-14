import os
from requests.sessions import Session
from requests import Response
from typing import Dict


V1 = "v1"
V2 = "v2"
VERSIONS = {V1: "v1", V2: "api/v2/"}


class Api:
    """
    Pipedrive API client for https://developers.pipedrive.com/docs/api/v1
    documentation.

    Supports only the Piperive API V2 version.
    """

    if "PIPEDRIVE_API_TOKEN" not in os.environ:
        raise ValueError("PIPEDRIVE_API_TOKEN is not set in environment variables.")
    api_token = os.environ["PIPEDRIVE_API_TOKEN"]

    def __init__(self, version=V2) -> None:
        assert version in VERSIONS, f"Invalid version: {version} (expected {VERSIONS})"
        self.session = Session()
        self.version = VERSIONS[version]
        self.endpoint_url = f"https://api.pipedrive.com/{self.version}/"
    
    def __repr__(self) -> str:
        return "<pipedrive.Api>"
    
    def get(self, uri: str, params: Dict = {}) -> Response:
        params = {**params, "api_token": self.api_token}
        return self.session.request(
            method="GET",
            url=self.endpoint_url + uri,
            params=params
        )
    
    def post(self, uri: str, body: Dict) -> Response:
        return self.session.request(
            method="POST",
            url=self.endpoint_url + uri,
            params={"api_token": self.api_token},
            json=body
        )
    
    def patch(self, uri: str, body: Dict) -> Response:
        return self.session.request(
            method="PATCH",
            url=self.endpoint_url + uri,
            params={"api_token": self.api_token},
            json=body
        )

    def delete(self, uri: str) -> Response:
        return self.session.request(
            method="DELETE",
            url=self.endpoint_url + uri,
            params={"api_token": self.api_token}
        )

    def batch_delete(self, uri: str, ids: str) -> Response:
        assert ids is not None, "ids cannot be None"
        assert isinstance(ids, str), "ids must be a comma-separated string of integers"
        assert all(map(lambda x: x.isdigit(), ids.split(","))), "ids must be a comma-separated string of integers"
        return self.session.request(
            method="DELETE",
            url=self.endpoint_url + uri,
            params={"api_token": self.api_token, "ids": ids}
        )