from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from cxrp.contracts.common import BaseContract
from cxrp.vocabulary.lane import LaneType


@dataclass
class LaneAlternative:
    lane: LaneType
    executor: Optional[str] = None
    backend: Optional[str] = None
    confidence: float = 0.0
    reason: str = ""

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")


@dataclass
class LaneDecision(BaseContract):
    contract_kind: str = "lane_decision"
    decision_id: str = ""
    proposal_id: str = ""
    lane: LaneType = LaneType.CODING_AGENT
    executor: Optional[str] = None
    backend: Optional[str] = None
    rationale: str = ""
    confidence: float = 1.0
    alternatives: list[LaneAlternative] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
