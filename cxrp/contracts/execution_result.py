from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from cxrp.contracts.common import BaseContract
from cxrp.vocabulary.status import ExecutionStatus


@dataclass
class Artifact:
    kind: str = ""
    uri: str = ""
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionResult(BaseContract):
    contract_kind: str = "execution_result"
    result_id: str = ""
    request_id: str = ""
    ok: bool = False
    status: ExecutionStatus = ExecutionStatus.PENDING
    artifacts: list[Artifact] = field(default_factory=list)
    diagnostics: dict[str, Any] = field(default_factory=dict)
