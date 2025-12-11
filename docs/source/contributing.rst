Contributing
============

Want to contribute or make a suggestion? Feel free. But don't forget to adhere to the guidelines and expectations set forth in the `Contributor Covenant <https://www.contributor-covenant.org/version/2/1/code_of_conduct/>`_.

We follow **Git Flow** branching strategy to maintain a clean and organized development workflow. Post your questions at the project's `Github Page <http://www.github.com/jmanprz/pypipedrive>`_. Remember: there are no stupid questions, only stupid silences.

Getting started
---------------

If it's your first time working on this library, clone the repo and make sure first that you can successfully run tests on your local machine. If that doesn't work out of the box, please check your local development environment before filing an issue.

.. code-block:: shell

    $ git clone https://github.com/jmanprz/pypipedrive.git
    $ cd pypipedrive
    $ make test

Or use ``tox`` for multi-environment testing:

.. code-block:: shell

    $ tox

Git Flow Branching Strategy
---------------------------

We follow `Git Flow <https://nvie.com/posts/a-successful-git-branching-model/>`_ for our branching model. This ensures a clean history and organized releases.

**Branch Types:**

| **Type** | **Purpose** | **Base Branch** | **Naming** |
|---|---|---|---|
| Feature | New feature development | ``develop`` | ``feature/<name>`` |
| Bugfix | Bug fixes | ``develop`` | ``bugfix/<name>`` |
| Hotfix | Production fixes | ``main`` | ``hotfix/<name>`` |
| Docs | Documentation updates | ``develop`` | ``docs/<topic>`` |
| Chore | Maintenance, dependencies | ``develop`` | ``chore/<desc>`` |
| Refactor | Code refactoring | ``develop`` | ``refactor/<area>`` |
| Test | Test improvements | ``develop`` | ``test/<area>`` |

**Workflow:**

1. Create a branch from the appropriate base branch
2. Make your changes and commit with signed commits
3. Push your branch and open a Pull Request targeting the base branch
4. Request review and ensure all checks pass
5. Merge once approved

**Examples:**

- ``feature/add-entity-mailbox`` — New mailbox entity
- ``bugfix/fix-entity-mailbox-attributes`` — Contact update issue
- ``hotfix/security-patch-v1.0.3`` — Production security fix
- ``docs/update-getting-started`` — Documentation update
- ``refactor/deprecate-v1-api-client`` — Code improvement

Reporting a bug
---------------

`Submit an issue <https://github.com/jmanprz/pypipedrive/issues/new>`_ to let the community know about bugs. The Pipedrive API evolves constantly, specially in their current V1 to V2 migration.

Make sure to follow these steps along the submission:

1. You're on the latest version of the library and you're able run the test suite locally.
2. Check `open issues <https://github.com/jmanprz/pypipedrive/issues>`_ for a duplicate issue.
3. Provide context: expected vs. actual behavior, steps to reproduce, and runtime environment.
4. When possible, provide code to reproduce the problem that you can share in the issue summary.

For security vulnerabilities, share them _directly_ to the maintainers via email.

Submitting a patch
------------------

You're welcome to `submit a pull request <https://github.com/jmanprz/pypipedrive/pulls>`_ for a bug fix or a new feature.

All pull requests **must adhere** to the following guidelines:

1. Branch follows the naming conventions outlined above and created from the appropriate base branch.
2. Public functions/methods have docstrings and type annotations.
3. New functionality is accompanied by clear, descriptive unit tests.
4. Code passes ``make test``.
5. You have your `commits signed <https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification>`_.
6. No merge conflicts with the target branch.

Don't hesitate to `open a draft pull request <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests#draft-pull-requests>`_ when you're willing to discuss an idea you're working on but haven't yet finished all of the above. That's appreciated and part of the community sharing.

License
-------

This project is licensed under the `MIT License <https://opensource.org/licenses/MIT>`_.

Built by `Juan Manuel M. Pérez <https://github.com/jmanprz>`_, Pipedrive API expert from `© Magical Potion <https://magicalpotion.io?utm_source=pypipedrive&utm_medium=docs&utm_campaign=open_source>`_ for teams that need to enhance and customise their Pipedrive sales experience with custom integrations and automations.