"""Compatibility shim. See `ecp.__init__` for details."""

from cxrp.contracts import (
    Artifact,
    ExecutionLimits,
    ExecutionRequest,
    ExecutionResult,
    LaneAlternative,
    LaneDecision,
    TaskProposal,
)

__all__ = [
    "Artifact",
    "ExecutionLimits",
    "ExecutionRequest",
    "ExecutionResult",
    "LaneAlternative",
    "LaneDecision",
    "TaskProposal",
]
