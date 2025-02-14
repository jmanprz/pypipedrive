## Pipedrive API SDK

[Pipedrive](https://pipedrive.com) is the developer-friendly CRM solution.

## Package setup

See [dev.to](https://dev.to/abdellahhallou/create-and-release-a-private-python-package-on-github-2oae) thread.

### Installation

```sh
pip install git+https://{{ your access token }}@github.com/gildastone/pypipedrive.git@{{ tag/version }}#egg=pypipedrive
```

### Building the package

```sh
python -m build
```

### Releasing a new release

```sh
git tag 0.0.1 -m "Initial release"
git push origin 0.0.1
```