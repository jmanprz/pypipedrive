# pypipedrive

![CI](https://github.com/jmanprz/pypipedrive/actions/workflows/ci_pipeline.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/pypipedrive-client.svg)](https://pypi.org/project/pypipedrive-client/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/pypipedrive-client.svg?label=downloads)](https://pypi.org/project/pypipedrive-client/)
[![Documentation Status](https://readthedocs.org/projects/pypipedrive/badge/?version=latest)](http://pypipedrive.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/jmanprz/pypipedrive/graph/badge.svg?token=8M4SGDOYGL)](https://codecov.io/gh/jmanprz/pypipedrive)

Python client for the Pipedrive V1/V2 API. Don't worry about which endpoint version to call, this SDK handles it for you.

## Pipedrive V1/V2 API SDK

[Pipedrive](https://pipedrive.com) is the developer-friendly CRM solution. Read its [Pipedrive API Reference](https://developers.pipedrive.com/docs/api/v1).

## Installation

```sh
% pip install pypipedrive-client
```

## Documentation

The full documentation can be found at [pypipedrive.readthedocs.io](https://pypipedrive.readthedocs.io).

## Contributing

Want to contribute or make a suggestion? Feel free. But don't forget to adhere to the guidelines and expectations set forth in the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

### Getting started

If it's your first time working on this library, clone the repo and make sure first that you can successfully run tests on your local machine. If that doesn't work out of the box, please check your local development environment before filing an issue.

Below command runs the test suite, code coverage and `/docs` build.

```sh
% make test
```

### Reporting a bug

[Submit an issue](https://github.com/jmanprz/pypipedrive/issues/new) to let the community know about bugs. The Pipedrive API evolves constantly, specially in their current V1 to V2 migration.

Make sure to follow these steps along the submission:

1. You're on the latest version of the library and you're able run the test suite locally.
2. Check [open issues](https://github.com/jmanprz/pypipedrive/issues) for a duplicate issue.
3. Provide context: expected vs. actual behavior, steps to reproduce, and runtime environment.
4. When possible, provide code to reproduce the problem that you can share in the issue summary.

For security vulnerabilities, share them _directly_ to the maintainers via email.

### Submitting a patch

You're welcome to [submit a pull request](https://github.com/jmanprz/pypipedrive/pulls) for a bug fix or a new feature.

We follow **Git Flow** branching strategy. See [CONTRIBUTING.rst](./CONTRIBUTING.rst) for branch naming conventions and workflow details.

All pull requests **must adhere** to the following guidelines:

1. Branch follows the naming conventions outlined above and created from the appropriate base branch.
2. Public functions/methods have docstrings and type annotations.
3. New functionality is accompanied by clear, descriptive unit tests.
4. Code passes ``make test``.
5. You have your [commits signed](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification).
6. No merge conflicts with the target branch.

Don't hesitate to [open a draft pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests#draft-pull-requests) when you're willing to discuss an idea you're working on but haven't yet finished all of the above. That's appreciated and part of the community sharing.

### License

This project is licensed under the [MIT License](https://opensource.org/license/MIT).

Built by [Juan Manuel M. Pérez](https://github.com/jmanprz), Pipedrive API expert from [© Magical Potion](https://magicalpotion.io?utm_source=pypipedrive&utm_medium=github&utm_campaign=open_source) for teams that need to enhance and customise their Pipedrive sales experience with custom integrations and automations.