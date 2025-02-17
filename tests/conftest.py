import pytest

from pypipedrive import Api


@pytest.fixture
def constants():
    return dict(
        API_KEY="API_KEY",
        VERSION_V1="v1",
        VERSION_V2="v2",
    )


@pytest.fixture()
def api_v1(constants) -> Api:
    return Api(version=constants["VERSION_V1"])


@pytest.fixture()
def api(constants) -> Api:
    return Api(version=constants["VERSION_V2"])


