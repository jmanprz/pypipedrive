import pytest

from pypipedrive.orm import types
import pydantic


class DummyType(pydantic.BaseModel):
    x1: int
    x2: str


def test_assert_typed_dict_accepts_valid_dict():
    data = {"x1": 123, "x2": "abc"}
    inst = types.assert_typed_dict(cls=DummyType, obj=data)
    assert isinstance(inst, DummyType)
    assert inst.x1 == 123
    assert inst.x2 == "abc"


@pytest.mark.parametrize(
    "obj",
    [123, True, "not-a-dict", [1, 2, 3], None]
)
def test_assert_typed_dict_raises_typeerror_on_non_dict(obj):
    """Test that assert_typed_dict raises TypeError when input is not a dict."""
    with pytest.raises(TypeError) as exc:
        types.assert_typed_dict(cls=DummyType, obj=obj)
    assert "expected dict" in str(exc.value)


def test_assert_typed_dict_raises_validation_error_on_invalid_contents():
    """Test that assert_typed_dict raises ValidationError when dict contents are invalid."""
    # trigger a pydantic.ValidationError
    bad = {"x1": "not-a-number", "x2": "abc"}
    with pytest.raises(pydantic.ValidationError):
        types.assert_typed_dict(cls=DummyType, obj=bad)


def test_assert_typed_obj_accepts_instance_and_returns_model():
    """
    Test that assert_typed_obj accepts an instance of the given class
    and returns it (or a new instance with same data).
    """
    obj = DummyType(x1=123, x2="abc")
    out = types.assert_typed_obj(cls=DummyType, obj=obj)
    # The function returns cls(obj) which for pydantic models will create a
    # new model instance; ensure returned is a model and has same data.
    assert isinstance(out, DummyType)
    assert out.x1 == 123
    assert out.x2 == "abc"


@pytest.mark.parametrize(
    "obj",
    [123, True, "not-a-model", [1, 2, 3], None, {"x1": 123, "x2": "abc"}]
)
def test_assert_typed_obj_raises_when_wrong_type(obj):
    with pytest.raises(TypeError) as exc:
        types.assert_typed_obj(cls=DummyType, obj=obj)
    assert "expected DummyType" in str(exc.value)