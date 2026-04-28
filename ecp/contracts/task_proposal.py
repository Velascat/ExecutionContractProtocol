from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ecp.contracts.common import BaseContract


@dataclass
class TaskProposal(BaseContract):
    contract_kind: str = "task_proposal"
    proposal_id: str = ""
    title: str = ""
    objective: str = ""
    constraints: list[str] = field(default_factory=list)
    requested_inputs: dict[str, Any] = field(default_factory=dict)
