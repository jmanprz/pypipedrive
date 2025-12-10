.. include:: _warn_latest.rst

V2 Migration
============

As Pipedrive is currently migrating from API V1 to V2, some endpoints and behaviors may change.

Even though this library abstracts the necessity of knowing the underlying API version, some differences may still affect how you interact with the library.

In that particular case, you may need to adjust your code accordingly using the low-level :class:`~pypipedrive.api.api.Api` interface while a patch is submitted to support the new behavior in the ORM-style :class:`~pypipedrive.orm.Model` interface.

Refer to the official `Pipedrive API V2 migration guide <https://pipedrive.readme.io/docs/pipedrive-api-v2-migration-guide>`__ for more information.