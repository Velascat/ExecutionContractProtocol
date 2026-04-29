from enum import Enum


class ExecutionStatus(str, Enum):
    """Canonical execution status vocabulary for CxRP contracts."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    TIMED_OUT = "timed_out"
