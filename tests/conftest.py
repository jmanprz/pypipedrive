import pytest

from pypipedrive import Api
from pypipedrive.orm import fields as f
from pypipedrive.orm.model import Model


@pytest.fixture
def constants():
    return dict(
        API_token="API_TOKEN",
        VERSION_V1="v1",
        VERSION_V2="v2",
    )


@pytest.fixture()
def api_v1(constants) -> Api:
    return Api(api_token=constants["API_token"], version=constants["VERSION_V1"])


@pytest.fixture()
def api(constants) -> Api:
    return Api(api_token=constants["API_token"], version=constants["VERSION_V2"])


@pytest.fixture
def M() -> Model:
    class M(Model):
        name = f.Field("Name")

        class Meta:
            entity_name = "test"
            version     = "v1"
    return M