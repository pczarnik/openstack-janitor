"""Tests for the `janitor audit` command."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from openstack.exceptions import SDKException
from typer.testing import CliRunner

from openstack_janitor.cli import app
from openstack_janitor.detectors.base import Finding

runner = CliRunner()


class FakeDetector:
    def __init__(self, name: str, findings: list[Finding] | None = None) -> None:
        self.name = name
        self.description = f"fake detector {name}"
        self._findings = findings or []

    def detect(self, conn) -> list[Finding]:
        return self._findings


def test_audit_no_findings_exits_zero() -> None:
    with (
        patch("openstack_janitor.cli.get_connection", return_value=MagicMock()),
        patch(
            "openstack_janitor.cli.get_detectors",
            return_value=[FakeDetector("unattached-volumes")],
        ),
    ):
        result = runner.invoke(app, ["audit"])

    assert result.exit_code == 0
    assert "No findings" in result.stdout


def test_audit_with_findings_exits_one_and_shows_table() -> None:
    finding = Finding(
        resource_type="volume",
        resource_id="vol-123",
        resource_name="orphan",
        project_id="proj-1",
        reason="volume is unattached (status=available)",
    )
    with (
        patch("openstack_janitor.cli.get_connection", return_value=MagicMock()),
        patch(
            "openstack_janitor.cli.get_detectors",
            return_value=[FakeDetector("unattached-volumes", [finding])],
        ),
    ):
        result = runner.invoke(app, ["audit"])

    assert result.exit_code == 1
    assert "vol-123" in result.stdout
    assert "orphan" in result.stdout


def test_audit_unknown_detector_exits_two() -> None:
    with (
        patch("openstack_janitor.cli.get_connection", return_value=MagicMock()),
        patch(
            "openstack_janitor.cli.get_detectors",
            return_value=[FakeDetector("unattached-volumes")],
        ),
    ):
        result = runner.invoke(app, ["audit", "--detector", "does-not-exist"])

    assert result.exit_code == 2


def test_audit_sdk_exception_exits_three() -> None:
    with (
        patch("openstack_janitor.cli.get_connection", side_effect=SDKException("auth failed")),
        patch(
            "openstack_janitor.cli.get_detectors",
            return_value=[FakeDetector("unattached-volumes")],
        ),
    ):
        result = runner.invoke(app, ["audit"])

    assert result.exit_code == 3
