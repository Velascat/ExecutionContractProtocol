# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 ProtocolWarden
"""AgentTopology tests + naming guardrails.

Mirrors the CapabilitySet guardrail pattern — topology names must be
structural descriptors, not quantifiers or degree words.
"""
from __future__ import annotations

import re

import pytest

from cxrp.vocabulary.agent_topology import (
    _BANNED_DEGREE_TOKENS,
    _BANNED_SIZE_TOKENS,
    AgentTopology,
)


def test_all_members_present():
    members = {m.name for m in AgentTopology}
    assert members == {
        "SINGLE_AGENT",
        "SEQUENTIAL",
        "TEAM",
        "DAG",
        "ADVERSARIAL",
        "REFLEXION",
    }


def test_member_values():
    assert AgentTopology.SINGLE_AGENT.value == "single_agent"
    assert AgentTopology.SEQUENTIAL.value   == "sequential"
    assert AgentTopology.TEAM.value         == "team"
    assert AgentTopology.DAG.value          == "dag"
    assert AgentTopology.ADVERSARIAL.value  == "adversarial"
    assert AgentTopology.REFLEXION.value    == "reflexion"


def test_values_are_lowercase_snake_case():
    for topo in AgentTopology:
        assert re.fullmatch(r"[a-z][a-z_]*[a-z]|[a-z]+", topo.value), topo.value


def test_names_have_no_numeric_suffix():
    for topo in AgentTopology:
        assert not re.search(r"\d", topo.value), (
            f"{topo.value!r} contains a digit — quantifiers belong in executor config"
        )


def test_names_have_no_size_words():
    for topo in AgentTopology:
        tokens = set(topo.value.split("_"))
        leaked = tokens & _BANNED_SIZE_TOKENS
        assert not leaked, (
            f"{topo.value!r} contains size tokens {leaked} — size belongs in executor config"
        )


def test_names_have_no_degree_words():
    for topo in AgentTopology:
        tokens = set(topo.value.split("_"))
        leaked = tokens & _BANNED_DEGREE_TOKENS
        assert not leaked, (
            f"{topo.value!r} contains degree tokens {leaked} — degree belongs in executor config"
        )


def test_guardrails_catch_hypothetical_violations():
    bad_names = [
        "team_3",
        "dag_safe",
        "team_small",
        "reflexion_strict",
        "adversarial_max",
    ]
    for name in bad_names:
        tokens = set(name.split("_"))
        has_digit = bool(re.search(r"\d", name))
        has_size = bool(tokens & _BANNED_SIZE_TOKENS)
        has_degree = bool(tokens & _BANNED_DEGREE_TOKENS)
        assert has_digit or has_size or has_degree, (
            f"guardrail tokens missed {name!r}"
        )


def test_round_trip_from_string():
    for topo in AgentTopology:
        assert AgentTopology(topo.value) is topo


def test_is_str_subclass():
    for topo in AgentTopology:
        assert isinstance(topo, str)


def test_invalid_value_raises():
    with pytest.raises(ValueError):
        AgentTopology("swarm_parallel")


def test_topology_count_soft_cap():
    """Resist enum bloat. Bumping this requires deliberation."""
    assert len(AgentTopology) <= 8, (
        "AgentTopology exceeded the soft cap. Confirm the new topology is a "
        "genuine coordination pattern and not a configuration variant in disguise."
    )
