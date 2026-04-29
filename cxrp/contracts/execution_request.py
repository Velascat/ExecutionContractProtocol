from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from cxrp.contracts.common import BaseContract, ExecutionLimits
from cxrp.vocabulary.lane import LaneType


@dataclass
class ExecutionRequest(BaseContract):
    contract_kind: str = "execution_request"
    request_id: str = ""
    proposal_id: str = ""
    lane_decision_id: str = ""
    lane: LaneType = LaneType.CODING_AGENT
    executor: Optional[str] = None
    backend: Optional[str] = None
    scope: str = ""
    input_payload: dict[str, Any] = field(default_factory=dict)
    input_payload_schema: Optional[str] = None
    constraints: list[str] = field(default_factory=list)
    limits: Optional[ExecutionLimits] = None
