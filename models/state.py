"""Shared workflow state models."""

from dataclasses import dataclass, field


@dataclass
class ProcurementState:
    request: str = ""
    context: list[str] = field(default_factory=list)
    response: str = ""
