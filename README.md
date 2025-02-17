# pyPipedrive

![CI](https://github.com/gildastone/pypipedrive/actions/workflows/test_lint_deploy.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/pypipedrive-client.svg)](https://pypi.org/project/pypipedrive-client/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/pypipedrive-client.svg?label=downloads)](https://pypi.org/project/pypipedrive-client/)
[![Documentation Status](https://readthedocs.org/projects/pypipedrive/badge/?version=latest)](http://pypipedrive.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/gildastone/pypipedrive/branch/main/graph/badge.svg?token=askmZgmMoV)](https://codecov.io/gh/gildastone/pypipedrive)

## Pipedrive API SDK

[Pipedrive](https://pipedrive.com) is the developer-friendly CRM solution.

## Package setup

See [dev.to](https://dev.to/abdellahhallou/create-and-release-a-private-python-package-on-github-2oae) thread.

### Installation

```sh
pip install git+https://{{ your access token }}@github.com/gildastone/pypipedrive.git@{{ tag/version }}#egg=pypipedrive
```

### Limitations

- Unable to upate the `custom_fields`.
- Only for Pipedrive V2 API

### Building the package

```sh
python -m build
```

### Installing the Revitron theme

```
pip install https://github.com/revitron/revitron-sphinx-theme/archive/master.zip
```

### Building the docs

The [Sphinx](https://www.sphinx-doc.org/) is used to generate the docs. `builder` is one of the supported builders, e.g. html, latex or linkcheck.

```
make builder
```

To render the documentation as HTML for the first time:

```
sphinx-build -M html docs/source/ docs/build/
```

### Releasing a new release

```sh
git tag 0.0.1 -m "Initial release"
git push origin 0.0.1
```