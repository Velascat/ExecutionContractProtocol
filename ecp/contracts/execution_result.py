from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ecp.contracts.common import BaseContract
from ecp.vocabulary.artifact import ArtifactType
from ecp.vocabulary.status import ExecutionStatus


@dataclass
class Artifact:
    artifact_type: ArtifactType
    uri: str
    description: str = ""


@dataclass
class ExecutionResult(BaseContract):
    contract_kind: str = "execution_result"
    result_id: str = ""
    request_id: str = ""
    ok: bool = False
    status: ExecutionStatus = ExecutionStatus.PENDING
    artifacts: list[Artifact] = field(default_factory=list)
    diagnostics: dict[str, Any] = field(default_factory=dict)
