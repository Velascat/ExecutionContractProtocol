# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 ProtocolWarden
"""ExecutorName + BackendName — typed executor/backend vocabulary.

Schema 0.3 (introduced 2026-05-05) replaces v0.2's open-string
``executor``/``backend`` envelope fields with typed enums. v0.2 stays
frozen on disk for historical interop; new producers target v0.3.

Adding a new executor or backend now requires bumping CxRP minor
version + a coordinated rollout to every consumer. In a closed-system
deployment (all consumers under one org), this is a one-commit
coordination cost; in exchange, typo'd backend/executor names die at
the wire boundary instead of at the OC binding step.
"""
from __future__ import annotations

from enum import Enum


class ExecutorName(str, Enum):
    """Canonical executor names. Producers must use one of these."""

    CLAUDE_CLI       = "claude_cli"
    CODEX_CLI        = "codex_cli"
    AIDER_LOCAL      = "aider_local"
    TEAM_EXECUTOR    = "team_executor"
    DAG_EXECUTOR     = "dag_executor"
    CRITIQUE_EXECUTOR = "critique_executor"


class BackendName(str, Enum):
    """Canonical backend names. Producers must use one of these."""

    DIRECT_LOCAL      = "direct_local"
    AIDER_LOCAL       = "aider_local"
    OPENCLAW          = "openclaw"
    TEAM_EXECUTOR     = "team_executor"
    DAG_EXECUTOR      = "dag_executor"
    CRITIQUE_EXECUTOR = "critique_executor"
