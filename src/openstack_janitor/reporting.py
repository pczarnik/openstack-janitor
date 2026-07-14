"""Rendering findings to the terminal, JSON, or HTML."""

from __future__ import annotations

import dataclasses
import html
import json

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


def render_json(findings: list[Finding]) -> str:
    """Render findings as an indented JSON array, for reports/piping."""
    return json.dumps([dataclasses.asdict(f) for f in findings], indent=2, sort_keys=True)


def render_html(findings: list[Finding]) -> str:
    """Render findings as a fully self-contained HTML document.

    Every dynamic value is passed through ``html.escape`` -- findings come
    from cloud-controlled resource names, which must never be trusted enough
    to interpolate into HTML unescaped.
    """
    summary = f"{len(findings)} finding{'s' if len(findings) != 1 else ''}"

    if not findings:
        body = "<p>No findings — cloud looks clean.</p>"
    else:
        rows = []
        for finding in findings:
            extra = ", ".join(f"{k}={v}" for k, v in finding.extra.items())
            cells = [
                finding.resource_type,
                finding.resource_id,
                finding.resource_name,
                finding.project_id,
                finding.reason,
                extra,
            ]
            row = "".join(f"<td>{html.escape(cell)}</td>" for cell in cells)
            rows.append(f"<tr>{row}</tr>")
        body = (
            "<table>\n"
            "<tr><th>Type</th><th>ID</th><th>Name</th><th>Project</th>"
            "<th>Reason</th><th>Extra</th></tr>\n" + "\n".join(rows) + "\n</table>"
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>openstack-janitor report</title>
<style>
body {{ font-family: sans-serif; margin: 2rem; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ccc; padding: 0.4rem 0.6rem; text-align: left; }}
th {{ background: #eee; }}
</style>
</head>
<body>
<h1>openstack-janitor report</h1>
<p>{html.escape(summary)}</p>
{body}
</body>
</html>
"""
