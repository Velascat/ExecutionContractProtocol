# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Velascat
"""Runtime vocabulary — kinds and selection modes for RuntimeBinding.

A RuntimeBinding answers *what powers the executor* — CLI subscription,
local model server, hosted API, container, human, or backend default.
The kind is orthogonal to the executor (`kodo`, `archon`) and to the
lane (`coding_agent`, etc.).

`selection_mode` records *who decided* the runtime — the backend's
default, OC's policy layer, or an explicit field on the request. This
makes routing decisions auditable.

See OperationsCenter/docs/architecture/backend_control_audit.md
(Phase 0.5–0.7) for the validity table and optional-field allow-list.
"""
from __future__ import annotations

from enum import Enum


class RuntimeKind(str, Enum):
    BACKEND_DEFAULT       = "backend_default"
    CLI_SUBSCRIPTION      = "cli_subscription"
    LOCAL_MODEL_SERVER    = "local_model_server"
    HOSTED_API            = "hosted_api"
    CONTAINERIZED_RUNTIME = "containerized_runtime"
    HUMAN                 = "human"


class SelectionMode(str, Enum):
    BACKEND_DEFAULT  = "backend_default"
    POLICY_SELECTED  = "policy_selected"
    EXPLICIT_REQUEST = "explicit_request"


# kind × selection_mode validity table.
# Rule: if `kind` is `backend_default`, selection_mode must be
# `backend_default` (a backend default chosen by anyone other than the
# backend is incoherent). If `kind` is `human`, selection_mode must be
# `policy_selected` or `explicit_request` (humans aren't a backend default).
_VALID_KIND_SELECTION_MODE: frozenset[tuple[str, str]] = frozenset({
    (RuntimeKind.BACKEND_DEFAULT.value,       SelectionMode.BACKEND_DEFAULT.value),
    (RuntimeKind.CLI_SUBSCRIPTION.value,      SelectionMode.BACKEND_DEFAULT.value),
    (RuntimeKind.CLI_SUBSCRIPTION.value,      SelectionMode.POLICY_SELECTED.value),
    (RuntimeKind.CLI_SUBSCRIPTION.value,      SelectionMode.EXPLICIT_REQUEST.value),
    (RuntimeKind.LOCAL_MODEL_SERVER.value,    SelectionMode.BACKEND_DEFAULT.value),
    (RuntimeKind.LOCAL_MODEL_SERVER.value,    SelectionMode.POLICY_SELECTED.value),
    (RuntimeKind.LOCAL_MODEL_SERVER.value,    SelectionMode.EXPLICIT_REQUEST.value),
    (RuntimeKind.HOSTED_API.value,            SelectionMode.BACKEND_DEFAULT.value),
    (RuntimeKind.HOSTED_API.value,            SelectionMode.POLICY_SELECTED.value),
    (RuntimeKind.HOSTED_API.value,            SelectionMode.EXPLICIT_REQUEST.value),
    (RuntimeKind.CONTAINERIZED_RUNTIME.value, SelectionMode.BACKEND_DEFAULT.value),
    (RuntimeKind.CONTAINERIZED_RUNTIME.value, SelectionMode.POLICY_SELECTED.value),
    (RuntimeKind.CONTAINERIZED_RUNTIME.value, SelectionMode.EXPLICIT_REQUEST.value),
    (RuntimeKind.HUMAN.value,                 SelectionMode.POLICY_SELECTED.value),
    (RuntimeKind.HUMAN.value,                 SelectionMode.EXPLICIT_REQUEST.value),
})


# Optional-field allow-list per kind. Each entry maps an optional
# RuntimeBinding field to the kinds that may carry it. `human` and
# `backend_default` carry none of these — bindings that name them must
# leave optional fields unset.
_OPTIONAL_FIELD_ALLOWED_KINDS: dict[str, frozenset[str]] = {
    "model": frozenset({
        RuntimeKind.CLI_SUBSCRIPTION.value,
        RuntimeKind.LOCAL_MODEL_SERVER.value,
        RuntimeKind.HOSTED_API.value,
    }),
    "provider": frozenset({
        RuntimeKind.CLI_SUBSCRIPTION.value,
        RuntimeKind.HOSTED_API.value,
    }),
    "endpoint": frozenset({
        RuntimeKind.LOCAL_MODEL_SERVER.value,
        RuntimeKind.HOSTED_API.value,
    }),
    "config_ref": frozenset({
        RuntimeKind.CLI_SUBSCRIPTION.value,
        RuntimeKind.LOCAL_MODEL_SERVER.value,
        RuntimeKind.HOSTED_API.value,
        RuntimeKind.CONTAINERIZED_RUNTIME.value,
    }),
}


def is_valid_kind_selection_mode(kind: str, selection_mode: str) -> bool:
    return (kind, selection_mode) in _VALID_KIND_SELECTION_MODE


def field_allowed_for_kind(field_name: str, kind: str) -> bool:
    allowed = _OPTIONAL_FIELD_ALLOWED_KINDS.get(field_name)
    if allowed is None:
        return True  # field has no kind restriction
    return kind in allowed
