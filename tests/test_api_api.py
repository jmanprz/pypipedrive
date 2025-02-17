import pytest
from unittest import mock

from pypipedrive import Api


@pytest.fixture
def mock_bases_endpoint(api, requests_mock, sample_json):
    return requests_mock.get(api.urls.bases, json=sample_json("Bases"))


def test_repr(api):
    assert "Api" in api.__repr__()


def test_endpoint_url_v1(api: Api, constants):
    api = Api(version=constants["VERSION_V1"])
    assert api.endpoint_url == "https://api.pipedrive.com/v1/"


def test_endpoint_url_v2(api: Api):
    assert api.endpoint_url == "https://api.pipedrive.com/api/v2/"


def test_update_api_key(api):
    """
    Test that changing the access token also changes the default request headers.
    """
    api.api_key = "123"
    assert "123" in api.api_key