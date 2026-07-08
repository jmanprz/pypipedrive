# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`pypipedrive` (published to PyPI as `pypipedrive-client`) is a Python SDK for the Pipedrive CRM **V1 and V2** REST API. Its central value proposition is that callers don't choose the endpoint version — each entity declares its version in `Meta` and the SDK routes to the correct v1/v2 endpoint and HTTP verb transparently.

## Commands

Testing runs through `tox` (default env `py312`), which sets `PIPEDRIVE_API_TOKEN=api_token` and `PYTHONDONTWRITEBYTECODE=1` for the session. All API calls in tests are mocked with `requests_mock` — no live network.

```sh
make test                 # tox: runs py312 tests + coverage + docs build
tox                       # same as above
tox -e py312              # unit tests only
tox -e coverage           # coverage report (fails under 60%)
tox -e docs               # build Sphinx docs into docs/build
make coverage             # coverage + open htmlcov/index.html
```

Running a **single test** directly needs the API token env var (tox normally injects it):

```sh
PIPEDRIVE_API_TOKEN=api_token python -m pytest tests/test_orm_fields.py -v
PIPEDRIVE_API_TOKEN=api_token python -m pytest tests/test_api_api.py::test_repr -v
# or via tox (token injected automatically):
tox -e py312 -- tests/test_api_api.py::test_repr
```

Build & publish (maintainer only; uses `.pypirc`):

```sh
make build                # python -m build
make testpypi             # build + twine upload to TestPyPI
make pypi                 # build + twine upload to PyPI
```

Formatting target is Black, `line-length = 80`, `py312` (config in `pyproject.toml`).

## Architecture

Three layers, bottom to top:

### 1. `pypipedrive/api/` — HTTP transport
- `Api` (in `api.py`) wraps a `requests.Session`, holding the API token as a query param and a version-specific base URL. `V1` → `https://api.pipedrive.com/v1/`, `V2` → `https://api.pipedrive.com/api/v2/`. HTTP verbs are `partialmethod`s (`get`/`put`/`post`/`patch`/`delete`).
- `update_method()` returns `patch` for V2 and `put` for V1 — the core of version-transparent updates.
- `iterator()` transparently handles both pagination schemes: **V2 cursor-based** (`next_cursor`) and **V1 start/limit** (`more_items_in_collection`). `all()` drains the iterator and merges `data` + `related_objects`.
- All responses become `ApiResponse` (pydantic: `success`, `data`, `additional_data`, `related_objects`). Non-OK responses go through `exceptions.raise_from_error_response`, which maps HTTP status codes to typed exceptions (`BadRequestException`, `NotFoundException`, …) that normalize the differing V1/V2 error payload shapes.

### 2. `pypipedrive/orm/` — the ORM framework
This is the heart of the library and where most complexity lives.
- **`Model` (`model.py`)** — base class for every entity. Instances store values in `self._fields` (keyed by attribute name) and track modifications in `self._changed`. Classmethods `all()`, `get()`, `iterator()` read; `save()`, `delete()`, `batch_delete()` write.
  - `save()` creates when there is no id, otherwise updates **only changed fields** (pass `force=True` to send everything) and returns a `SaveResult`. It picks PATCH vs PUT via `Api.update_method()`, with a hardcoded exception: `leads` and `leadLabels` use PATCH even though they are V1 endpoints.
  - `from_record()` / `to_record()` translate between the Pipedrive JSON shape and internal values, including extracting/repacking the `custom_fields` dict.
  - Class validity is enforced at subclass-creation time via `__init_subclass__` → `_validate_class()`: `Meta.entity_name` and `Meta.version` are required, and field attribute names may not clash with `Model` methods (except an allowlist: `all`, `iterator`, `get`, `save`, `update`, `delete`, `batch_delete`, `files`, `changelog`).
- **`Field` descriptors (`fields.py`)** — every model attribute is a `Field` (descriptor). `Field.__get__`/`__set__` mediate all attribute access: type validation, optional `validate` callables, `readonly` enforcement, `to_internal_value`/`to_record_value` conversion, and marking the field dirty in `_changed`. Key distinction: a field's **`field_name` is the Pipedrive API key**, while the **Python attribute name is what code uses** — `Model` builds bidirectional maps between them (`_field_name_to_attribute_map`, `_attribute_to_field_name_map`, etc.).
  - Scalar fields: `TextField`, `IntegerField`, `NumberField`, `BooleanField`, `DatetimeField`, `DateField`, `TimeField`, `DurationField` (datetime types convert to/from ISO 8601 strings via `utils`).
  - `_DictField` subclasses (e.g. `AddressField`, `MonetaryField`) validate against a schema type; `_ListField`/`_ValidatingListField` subclasses (e.g. `PhonesField`, `EmailsField`, `ItemsField`) hold validated lists.
- **`types.py`** — the `TypedDict`/pydantic schemas (`AddressDict`, `MonetaryDict`, `ItemSearchDict`, …) that the dict/list fields validate against, plus `assert_typed_dict`/`assert_typed_obj` helpers.

### 3. `pypipedrive/models/` — one module per Pipedrive entity
Each entity (`Deals`, `Persons`, `Organizations`, `Leads`, `Products`, `Activities`, `Goals`, the `*Fields` metadata entities, etc.) subclasses `Model`, declares its columns as `Field` instances, and sets an inner `Meta`:

```python
class Deals(Model):
    id    = F.IntegerField("id", readonly=True)
    title = F.TextField("title")
    value = F.NumberField("value")
    custom_fields = F.CustomFieldsField("custom_fields")

    class Meta:
        entity_name = "deals"   # URI segment
        version     = V2        # default API version for this entity
```

Conventions to follow when adding or editing an entity:
- **`Meta.entity_name`** is the API URI segment; **`Meta.version`** (`V1`/`V2`) is the default version. `Meta.field_id` optionally overrides which attribute holds the record id.
- Entity-specific endpoints beyond CRUD are added as methods that build a URI from `self._get_meta('entity_name')` and call `self.get_api(version=...)` explicitly (many entities are V2 by default but expose some endpoints only available on V1).
- **Custom fields**: attributes prefixed `custom_` map into the record's `custom_fields` dict rather than being top-level keys.
- Decorate methods hitting soon-to-be-removed v1 endpoints with `@warn_endpoint_legacy` and beta v2 endpoints with `@warn_endpoint_beta` (both in `utils.py`).
- To forbid an inherited operation, override it to `raise NotImplementedError` (see `ItemSearch`, and `Deals.batch_delete`).
- New entities must be exported from `pypipedrive/models/__init__.py` (`import` + `__all__`).

`utils.py` holds the ISO 8601 date/time/duration converters, the multipart file-upload tuple builder, and the two warning decorators.

## Runtime requirements

`PIPEDRIVE_API_TOKEN` must be set in the environment; `Model.get_api()` reads it (and is `lru_cache`d, so token changes mid-process won't take effect). A local `.env` holds it for development (gitignored).

## Conventions

- **Git Flow branching** (enforced on PRs by `.github/workflows` branch-name check): branches must be `feature/`, `bugfix/`, `hotfix/`, `docs/`, `chore/`, `refactor/`, or `test/`. Base off `develop` (off `main` for `hotfix/`).
- Public functions/methods carry docstrings and type annotations; new functionality ships with tests; `make test` must pass.
- Bump the version in a single place: `pypipedrive/__init__.py` (`__version__`) — `setup.cfg` reads it via `attr:`.
- `scripts/`, `check_models.py`, `*.json` dumps, `DEPLOYMENT.md`, `README-OLD.md`, and sample media are **gitignored** local helpers, not part of the shipped package.
