# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Velascat
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from cxrp.contracts.common import BaseContract
from cxrp.contracts.evidence import Evidence
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
    summary: str = ""
    artifacts: list[Artifact] = field(default_factory=list)
    diagnostics: dict[str, Any] = field(default_factory=dict)
    evidence: Evidence = field(default_factory=Evidence)
