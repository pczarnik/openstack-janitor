"""Tests for openstack_janitor.connection."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from openstack_janitor.connection import get_connection


def test_get_connection_passes_cloud_through() -> None:
    with patch("openstack_janitor.connection.openstack.connect") as mock_connect:
        mock_connect.return_value = MagicMock()
        result = get_connection(cloud="my-cloud")

    mock_connect.assert_called_once_with(cloud="my-cloud")
    assert result is mock_connect.return_value


def test_get_connection_none_calls_connect_with_no_cloud_kwarg() -> None:
    with patch("openstack_janitor.connection.openstack.connect") as mock_connect:
        mock_connect.return_value = MagicMock()
        result = get_connection()

    mock_connect.assert_called_once_with()
    assert result is mock_connect.return_value
