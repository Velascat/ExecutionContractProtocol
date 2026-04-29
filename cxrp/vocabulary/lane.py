from enum import Enum


class LaneType(str, Enum):
    """Canonical lane/backend vocabulary for CxRP contracts."""

    CODING_AGENT = "coding_agent"
    REVIEW_AGENT = "review_agent"
    LOCAL_MODEL = "local_model"
    HOSTED_MODEL = "hosted_model"
