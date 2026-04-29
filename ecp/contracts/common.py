from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class BaseContract:
    schema_version: str = "0.2"
    contract_kind: str = ""
    created_at: Optional[datetime] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if self.created_at is not None:
            data["created_at"] = self.created_at.astimezone(timezone.utc).isoformat()
        return data


@dataclass
class ExecutionLimits:
    max_changed_files: Optional[int] = None
    timeout_seconds: Optional[int] = None
    require_clean_validation: Optional[bool] = None
