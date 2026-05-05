# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Velascat
"""RuntimeBinding — what powers an executor for a given request.

Distinct from `executor` (the system that performs the work) and from
`lane` (the work category). RuntimeBinding answers *what powers it*:
CLI subscription, local model server, hosted API, container, human, or
backend default.

Validation runs on construction:
  - `kind × selection_mode` must be in the validity table
  - optional fields (model, provider, endpoint, config_ref) must be
    valid for the chosen kind

See cxrp/vocabulary/runtime.py for the tables and
OperationsCenter/docs/architecture/backend_control_audit.md (Phase 0.5–0.7).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from cxrp.vocabulary.runtime import (
    RuntimeKind,
    SelectionMode,
    field_allowed_for_kind,
    is_valid_kind_selection_mode,
)


@dataclass
class RuntimeBinding:
    kind: RuntimeKind = RuntimeKind.BACKEND_DEFAULT
    selection_mode: SelectionMode = SelectionMode.BACKEND_DEFAULT
    model: Optional[str] = None
    provider: Optional[str] = None
    endpoint: Optional[str] = None
    config_ref: Optional[str] = None

    def __post_init__(self) -> None:
        kind_value = self.kind.value if isinstance(self.kind, RuntimeKind) else str(self.kind)
        sel_value = (
            self.selection_mode.value
            if isinstance(self.selection_mode, SelectionMode)
            else str(self.selection_mode)
        )
        if not is_valid_kind_selection_mode(kind_value, sel_value):
            raise ValueError(
                f"invalid RuntimeBinding: kind={kind_value!r} cannot pair with "
                f"selection_mode={sel_value!r}"
            )
        for field_name in ("model", "provider", "endpoint", "config_ref"):
            value = getattr(self, field_name)
            if value is None:
                continue
            if not field_allowed_for_kind(field_name, kind_value):
                raise ValueError(
                    f"invalid RuntimeBinding: field {field_name!r} is not "
                    f"allowed for kind={kind_value!r}"
                )
