from __future__ import annotations

from dataclasses import dataclass, field

from ecp.contracts.common import BaseContract
from ecp.vocabulary.lane import LaneType


@dataclass
class LaneDecision(BaseContract):
    contract_kind: str = "lane_decision"
    decision_id: str = ""
    proposal_id: str = ""
    lane: LaneType = LaneType.CODING_AGENT
    rationale: str = ""
    confidence: float = 1.0
    alternatives: list[LaneType] = field(default_factory=list)
