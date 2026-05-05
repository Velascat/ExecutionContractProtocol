# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Velascat
"""Evidence — normalized result detail returned by an executor.

Carries the structured fields every backend must populate (files_changed,
commands_run, tests_run, artifacts_created, failure_reason) plus a single
``extensions`` slot for backend-specific data that does not fit the
normalized shape. ``extensions`` is the only place backend-specific
fields may appear; anything else outside the schema is a contract
violation.

See README "Contract Evolution Policy" and
``OperationsCenter/docs/architecture/backend_control_audit.md`` for the
boundary rules.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Evidence:
    files_changed: list[str] = field(default_factory=list)
    commands_run: list[str] = field(default_factory=list)
    tests_run: list[str] = field(default_factory=list)
    artifacts_created: list[str] = field(default_factory=list)
    failure_reason: Optional[str] = None
    extensions: dict[str, Any] = field(default_factory=dict)
