# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 ProtocolWarden
"""AgentTopology — execution coordination pattern vocabulary.

Topologies describe HOW agents coordinate to accomplish a goal. They are
structural patterns, not capability levels. Quantifiers, quality thresholds,
and configuration belong in the executor's runtime config, not here.

Naming guardrails (enforced by tests):
  - no numeric suffixes      (team_3 ❌)
  - no size words            (small / medium / large ❌)
  - no degree words          (safe / strict / loose / limited / max / min ❌)

Topology removals require a deprecation cycle.
"""
from __future__ import annotations

from enum import Enum


class AgentTopology(str, Enum):
    """Canonical agent coordination topologies.

    Add a new topology only when no existing pattern can describe the
    coordination structure. Executor configuration (team size, cycle
    limits, model selection) lives in executor settings, not here.
    """

    SINGLE_AGENT = "single_agent"
    SEQUENTIAL   = "sequential"   # linear DAG subtype — chain-shaped graph
    TEAM         = "team"         # coordinator + role pool + verify/reject cycles
    DAG          = "dag"          # node graph with explicit depends_on edges
    ADVERSARIAL  = "adversarial"  # proposer + critic loop until consensus
    REFLEXION    = "reflexion"    # single agent + independent self-critic loop


# Banned tokens enforced by the guardrail test.
_BANNED_DEGREE_TOKENS = frozenset({
    "safe", "strict", "loose", "limited", "max", "min",
})
_BANNED_SIZE_TOKENS = frozenset({
    "small", "medium", "large",
})
