# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Velascat
"""CapabilitySet — coarse permission classes for executor backends.

Capabilities answer "may?" — they are coarse permission categories.
Quantifiers (size limits, allowed paths, max diffs, strictness) belong
in policy, not capability names. See README "Contract Evolution Policy"
and OperationsCenter/docs/architecture/backend_control_audit.md
(Phase 0.4) for the rule.

Naming guardrails (enforced by ``test_capability_naming.py``):
  - no numeric suffixes      (repo_patch_500 ❌)
  - no size words            (small / medium / large ❌)
  - no degree words          (safe / strict / loose / limited / max / min ❌)

Capability removals require a deprecation cycle (one release window
marked deprecated, then removal in the next).
"""
from __future__ import annotations

from enum import Enum


class CapabilitySet(str, Enum):
    """Initial coarse capability set. Keep small; resist growth.

    Add a new capability only when an existing one cannot describe the
    permission class. Quantifiers (limits, paths, sizes) live in policy.
    """

    REPO_READ      = "repo_read"
    REPO_PATCH     = "repo_patch"
    TEST_RUN       = "test_run"
    SHELL_READ     = "shell_read"
    SHELL_WRITE    = "shell_write"
    NETWORK_ACCESS = "network_access"
    HUMAN_REVIEW   = "human_review"


# Banned tokens enforced by the guardrail test. These reject capability
# names that smuggle policy/quantifier semantics into the permission class.
_BANNED_DEGREE_TOKENS = frozenset({
    "safe", "strict", "loose", "limited", "max", "min",
})
_BANNED_SIZE_TOKENS = frozenset({
    "small", "medium", "large",
})
