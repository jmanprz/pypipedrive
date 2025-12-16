import os
import pytest
from requests_mock import Mocker

from pypipedrive import Api
from pypipedrive.api.api import ApiResponse


def test_repr(api):
    api_repr = api.__repr__()
    assert "<pypipedrive.Api" in api_repr
    assert f"version=" in api_repr


def test_pipedrive_api_token_unset():
    os.environ.pop("PIPEDRIVE_API_TOKEN", None)
    with pytest.raises(ValueError):
        Api()


def test_endpoint_url_v1(api_v1: Api):
    assert api_v1.endpoint_url == f"https://api.pipedrive.com/v1/"


def test_endpoint_url_v2(api: Api):
    assert api.endpoint_url == f"https://api.pipedrive.com/api/v2/"


def test_endpoint_url_version_unallowed():
    with pytest.raises(ValueError):
        Api(api_token="apiToken", version="v3")


def test_api_build_url():
    url = Api("v2").build_url("entityTest")
    assert url == "https://api.pipedrive.com/api/v2/entityTest"


def test_update_api_token(api: Api):
    """
    Test that changing the access token also changes the default request headers.
    """
    assert api.api_token != "ApiToken_123"
    api.api_token = "ApiToken_123"
    assert "ApiToken_123" == api.api_token


@pytest.mark.parametrize("method", ["get", "post", "patch", "delete"])
def test_api_method(method: str, api: Api, requests_mock: Mocker):
    uri = "entityName/1"
    url = api.build_url(uri)
    # Register the mock response for the URL
    payload = {"success": True, "data": {"id": 1}}
    getattr(requests_mock, method)(url, json=payload, status_code=200)
    response = getattr(api, method)(uri)

    assert requests_mock.called
    assert requests_mock.call_count == 1
    req = requests_mock.request_history[0]
    assert req.method == method.upper()
    assert req.qs == {"api_token": [api.api_token]}

    assert response.success
    assert response.data == {"id": 1}


def test_api_batch_delete(api: Api, requests_mock: Mocker):
    uri = "entityName"
    url = api.build_url(uri)

    payload = {"success": True, "data": {"ids": [1, 2, 3]}} 
    requests_mock.delete(url, json=payload, status_code=200)
    response: ApiResponse = api.delete(uri, json={"ids": [1, 2, 3]})

    assert requests_mock.called
    assert requests_mock.call_count == 1
    req = requests_mock.request_history[0]
    assert req.method == "DELETE"
    assert req.qs == {"api_token": [api.api_token]}
    assert req.json() == {"ids": [1, 2, 3]}

    assert response.success
    assert response.data == {"ids": [1, 2, 3]}