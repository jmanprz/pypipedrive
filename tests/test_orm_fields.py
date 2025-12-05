import pytest
import datetime
import operator

from pypipedrive.orm import fields as f
from pypipedrive.orm import types as t
from pypipedrive.orm.model import Model


DATE_S = "2025-01-01"
DATE_V = datetime.date(2025, 1, 1)
DATETIME_S = "2025-01-01T09:30:00.000Z"
DATETIME_V = datetime.datetime(2025, 1, 1, 9, 30, 0, tzinfo=datetime.timezone.utc)


def test_field(M: Model):
    m = M()
    m.name = "x"
    assert m.name == "x"
    assert m.__dict__["_fields"]["name"] == "x"

    with pytest.raises(AttributeError):
        del m.name


def test_description(M: Model):
    M.other = f.Field("Other")
    assert M.name._description == "M.name"
    assert M.other._description == "'Other' field"


@pytest.mark.parametrize(
    "instance,expected",
    [
        (
            f.Field("Name"),
            "Field('Name', readonly=False, validate_type=True)",
        ),
        (
            f.Field("Name", readonly=True, validate_type=False),
            "Field('Name', readonly=True, validate_type=False)",
        ),
        (
            f.TextField("Name"),
            "TextField('Name', readonly=False, validate_type=True)",
        ),
        (
            f.BytesField("Name"),
            "BytesField('Name', readonly=False, validate_type=True)",
        ),
        (
            f.FloatField("Name"),
            "FloatField('Name', readonly=False, validate_type=True)",
        ),
        (
            f.IntegerField("Name"),
            "IntegerField('Name', readonly=False, validate_type=True)",
        ),
        (
            f.BooleanField("Name"),
            "BooleanField('Name', readonly=False, validate_type=True)",
        ),
        (
            f.DatetimeField("Name"),
            "DatetimeField('Name', readonly=False, validate_type=True)",
        ),
        (
            f.DateField("Name"),
            "DateField('Name', readonly=False, validate_type=True)",
        ),
        (
            f.TimeField("Name"),
            "TimeField('Name', readonly=False, validate_type=True)",
        ),
        (
            f.DurationField("Name"),
            "DurationField('Name', readonly=False, validate_type=True)",
        ),
        (
            f._DictField("Name"),
            "_DictField('Name', readonly=False, validate_type=True)",
        ),
        (
            f.AddressField("Name"),
            "AddressField('Name', readonly=False, validate_type=True)",
        ),
        (
            f.MonetaryField("Name"),
            "MonetaryField('Name', readonly=False, validate_type=True)",
        ),
        (
            f._ListField("Name"),
            "_ListField('Name', readonly=False, validate_type=True)",
        ),
        (
            f._ValidatingListField("Name"),
            "_ValidatingListField('Name', readonly=False, validate_type=True)",
        ),
        (
            f.PhonesField("Name"),
            "PhonesField('Name', readonly=False, validate_type=True)",
        ),
        (
            f.ImField("Name"),
            "ImField('Name', readonly=False, validate_type=True)",
        ),
        (
            f.LabelIdsField("Name"),
            "LabelIdsField('Name', readonly=False, validate_type=True)",
        ),
        (
            f.ParticipantField("Name"),
            "ParticipantField('Name', readonly=False, validate_type=True)",
        ),
        (
            f.AttendeeField("Name"),
            "AttendeeField('Name', readonly=False, validate_type=True)",
        ),
        (
            f.AttendeeField("Name"),
            "AttendeeField('Name', readonly=False, validate_type=True)",
        ),
        (
            f.ItemSearchDealField("Name"),
            "ItemSearchDealField('Name', readonly=False, validate_type=True)",
        ),
        (
            f.ItemSearchPersonField("Name"),
            "ItemSearchPersonField('Name', readonly=False, validate_type=True)",
        ),
        (
            f.OptionsField("Name"),
            "OptionsField('Name', readonly=False, validate_type=True)",
        )
    ]
)
def test_repr(instance, expected):
    assert repr(instance) == expected


@pytest.mark.parametrize(
    argnames=("field_type", "default_value"),
    argvalues=[
        (f.Field, None),
        (f.TextField, None),
        (f.BytesField, None),
        (f.NumberField, None),
        (f.FloatField, None),
        (f.IntegerField, None),
        (f.BooleanField, None),
        (f.DatetimeField, None),
        (f.DateField, None),
        (f.TimeField, None),
        (f.DurationField, None),
        (f._DictField, {}),
        (f.AddressField, {}),
        (f.MonetaryField, {}),
        (f._ListField, []),
        (f._ValidatingListField, []),
        (f.PhonesField, []),
        (f.EmailsField, []),
        (f.ImField, []),
        (f.LabelIdsField, []),
        (f.ParticipantField, []),
        (f.AttendeeField, []),
        (f.ItemSearchDealField, []),
        (f.ItemSearchPersonField, []),
        (f.OptionsField, []),
    ],
)
def test_orm_missing_values(field_type, default_value):
    class M(Model):
        field = field_type("Field Name")
        class Meta:
            entity_name = "test"
            version     = "v1"

    m = M()
    assert m.field == default_value


# Mapping from types to a test value for that type.
TYPE_VALIDATION_TEST_VALUES = {
    str: "some value",
    bool: False,
    bytes: b"some bytes",
    list: [],
    dict: {},
    int: 1,
    float: 1.0,
    datetime.date: datetime.date.today(),
    datetime.datetime: datetime.datetime.now(),
    datetime.time: datetime.time(12, 0, 0),
    datetime.timedelta: datetime.timedelta(seconds=1),
    t.AddressDict: t.AddressDict(),
    t.MonetaryDict: t.MonetaryDict(),
}


@pytest.mark.parametrize(
    argnames=("test_case"),
    argvalues=[
        (f.Field, tuple(TYPE_VALIDATION_TEST_VALUES), None),
        (f.TextField, str, None),
        (f.BytesField, bytes, None),
        (f.NumberField, (int, float), None),
        (f.FloatField, float, None),
        (f.IntegerField, int, None),
        (f.BooleanField, bool, None),
        (f.DatetimeField, (datetime.datetime), None),
        (f.DateField, datetime.date, None),
        (f.TimeField, datetime.time, None),
        (f.DurationField, datetime.timedelta, None),
        (f._DictField, dict, None),
        (f.AddressField, (t.AddressDict, dict), None),
        (f.MonetaryField, (t.MonetaryDict, dict), None),
        (f._ListField, list, [t for t in TYPE_VALIDATION_TEST_VALUES if t != list]),
        (f._ValidatingListField, list, None),
        (f.PhonesField, list, None),
        (f.EmailsField, list, None),
        (f.ImField, list, None),
        (f.LabelIdsField, list, None),
        (f.ParticipantField, list, None),
        (f.AttendeeField, list, None),
        (f.ItemSearchDealField, list, None),
        (f.ItemSearchPersonField, list, None),
        (f.OptionsField, list, None),
    ],
    ids=operator.itemgetter(0),
)
def test_type_validation(test_case):
    """
    Test that attempting to assign the wrong type of value to a field
    will throw TypeError, but the right kind of value will work.
    """
    field_type, valid_types, unvalid_types = test_case
    if isinstance(valid_types, type):
        valid_types = [valid_types]

    class M(Model):
        field = field_type("Field Name")
        unvalidated_field = field_type("Unvalidated", validate_type=False)

        class Meta:
            entity_name = "test"
            version     = "v1"

    m = M()

    for testing_type, test_value in TYPE_VALIDATION_TEST_VALUES.items():
        # This statement should not raise an exception, no matter what.
        if unvalid_types:
            if testing_type in unvalid_types:
                with pytest.raises(TypeError):
                    m.unvalidated_field = test_value

        if testing_type in valid_types:
            m.field = test_value
        else:
            with pytest.raises(TypeError):
                m.field = test_value
                pytest.fail(
                    f"{field_type.__name__} = {test_value!r} "
                    f"{testing_type} did not raised TypeError"
                )


def test_readonly_fields():
    """
    Test that a readonly field cannot be overwritten.
    """
    class M(Model):
        field = f.Field(field_name="Field Name", readonly=True)
        class Meta:
            entity_name = "test"
            version     = "v1"

    m = M.from_record(**{"Field Name": "read only value"})
    with pytest.raises(AttributeError):
        m.field = "new value"
    assert m.field == "read only value"


def test_writable_fields():
    """
    Test that a writable field can be overwritten.
    """
    class M(Model):
        field = f.Field(field_name="Field Name", readonly=False)
        class Meta:
            entity_name = "test"
            version     = "v1"

    m = M.from_record(**{"Field Name": "writable value"})
    m.field = "new value"
    assert m.field == "new value"


def test_field_validate_callable():
    """Test that a field's validate callable is invoked on set."""
    calls = []

    def validator(val: str) -> str:
        calls.append(val)
        return f"validated:{val}"

    class M(Model):
        field = f.TextField("Field Name", validate=validator)

        class Meta:
            entity_name = "test"
            version     = "v1"

    m = M()
    m.field = "abc"
    assert calls == ["abc"]
    assert m.field == "validated:abc"


def test_field_validate_list():
    """Test that a field's validate list is invoked in order on set."""
    calls = []

    def v1(val: str) -> str:
        """Validator n°1: strip whitespace."""
        calls.append(("v1", val))
        return val.strip()

    def v2(val: str) -> str:
        """Validator n°2: uppercase the value."""
        calls.append(("v2", val))
        return val.upper()

    class M(Model):
        field = f.TextField("Field Name", validate=[v1, v2])

        class Meta:
            entity_name = "test"
            version     = "v1"

    m = M()
    m.field = "  abc "
    assert m.field == "ABC"
    assert calls == [("v1", "  abc "), ("v2", "abc")]