"""Base types shared by all detectors."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar

from openstack.connection import Connection


@dataclass(frozen=True)
class Finding:
    """A single flagged resource."""

    resource_type: str
    resource_id: str
    resource_name: str
    project_id: str
    reason: str
    extra: dict[str, str] = field(default_factory=dict)


class Detector(ABC):
    """A check that scans a cloud for one category of orphaned/wasteful resource."""

    name: ClassVar[str]
    """Kebab-case identifier, e.g. "unattached-volumes"."""

    description: ClassVar[str]
    """Short human-readable description of what this detector looks for."""

    @abstractmethod
    def detect(self, conn: Connection) -> list[Finding]:
        """Scan the cloud reachable via ``conn`` and return any findings."""
        raise NotImplementedError
