"""Connection helper: the single seam between openstack-janitor and openstacksdk.

Kept intentionally tiny so tests and the CLI have one place to mock instead of
reaching into openstacksdk internals.
"""

from __future__ import annotations

import openstack
from openstack.connection import Connection


def get_connection(cloud: str | None = None) -> Connection:
    """Return an authenticated openstacksdk Connection.

    Resolution order follows openstacksdk's own rules:

    1. If ``cloud`` is given, it is looked up by name in ``clouds.yaml``
       (searched in the current directory, ``~/.config/openstack/`` and
       ``/etc/openstack/``), optionally layered with ``secure.yaml``.
    2. If ``cloud`` is ``None``, ``openstack.connect()`` is called with no
       arguments and openstacksdk resolves the cloud itself: the ``OS_CLOUD``
       environment variable (which behaves like passing ``cloud=...``), or
       else the standard ``OS_*`` environment variables (``OS_AUTH_URL``,
       ``OS_USERNAME``, ``OS_PASSWORD``, ``OS_PROJECT_NAME``, etc.).

    No connection is made here -- openstacksdk connections are lazy, so this
    only builds the ``Connection`` object.
    """
    if cloud is None:
        return openstack.connect()
    return openstack.connect(cloud=cloud)
