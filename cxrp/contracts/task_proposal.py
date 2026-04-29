from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from cxrp.contracts.common import BaseContract


@dataclass
class TaskProposal(BaseContract):
    contract_kind: str = "task_proposal"
    proposal_id: str = ""
    title: str = ""
    objective: str = ""
    task_type: Optional[str] = None
    execution_mode: Optional[str] = None
    priority: Optional[str] = None
    risk_level: Optional[str] = None
    target: Optional[dict[str, Any]] = None
    constraints: list[str] = field(default_factory=list)
    requested_inputs: dict[str, Any] = field(default_factory=dict)
