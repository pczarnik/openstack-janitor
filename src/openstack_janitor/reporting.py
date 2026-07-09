"""Rendering findings to the terminal.

JSON/HTML output formats are planned for a later batch; this module only
knows how to print a rich table (or a "clean" message) to the console.
"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from openstack_janitor.detectors.base import Finding


def render_table(findings: list[Finding]) -> Table:
    """Build a rich Table summarizing the given findings."""
    table = Table(title="openstack-janitor findings")
    table.add_column("Type", style="cyan")
    table.add_column("ID", style="dim")
    table.add_column("Name")
    table.add_column("Project")
    table.add_column("Reason")

    for finding in findings:
        table.add_row(
            finding.resource_type,
            finding.resource_id,
            finding.resource_name,
            finding.project_id,
            finding.reason,
        )
    return table


def print_findings(findings: list[Finding], console: Console) -> None:
    """Print findings as a table, or a clean-cloud message if there are none."""
    if not findings:
        console.print("[green]No findings — cloud looks clean.[/green]")
        return
    console.print(render_table(findings))
