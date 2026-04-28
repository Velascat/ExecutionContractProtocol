from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ecp.contracts.common import BaseContract
from ecp.vocabulary.lane import LaneType


@dataclass
class ExecutionRequest(BaseContract):
    contract_kind: str = "execution_request"
    request_id: str = ""
    proposal_id: str = ""
    lane_decision_id: str = ""
    lane: LaneType = LaneType.CODING_AGENT
    scope: str = ""
    input_payload: dict[str, Any] = field(default_factory=dict)
    constraints: list[str] = field(default_factory=list)
