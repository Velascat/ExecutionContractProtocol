# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Velascat
"""CapabilitySet tests + naming guardrails.

The guardrail test rejects capability names that smuggle quantifier or
degree semantics into the permission class. Capabilities are coarse;
policy carries the limits. See cxrp/vocabulary/capability.py.
"""
from __future__ import annotations

import re

import pytest

from cxrp.vocabulary.capability import (
    _BANNED_DEGREE_TOKENS,
    _BANNED_SIZE_TOKENS,
    CapabilitySet,
)


def test_capability_set_initial_members():
    assert CapabilitySet.REPO_READ.value      == "repo_read"
    assert CapabilitySet.REPO_PATCH.value     == "repo_patch"
    assert CapabilitySet.TEST_RUN.value       == "test_run"
    assert CapabilitySet.SHELL_READ.value     == "shell_read"
    assert CapabilitySet.SHELL_WRITE.value    == "shell_write"
    assert CapabilitySet.NETWORK_ACCESS.value == "network_access"
    assert CapabilitySet.HUMAN_REVIEW.value   == "human_review"


def test_capability_values_are_lowercase_snake_case():
    for cap in CapabilitySet:
        assert re.fullmatch(r"[a-z][a-z_]*[a-z]", cap.value), cap.value


def test_capability_names_have_no_numeric_suffix():
    """repo_patch_500, max_diff_100 etc. — quantifiers leaking in."""
    for cap in CapabilitySet:
        assert not re.search(r"\d", cap.value), (
            f"{cap.value!r} contains a digit — quantifiers belong in policy, not capabilities"
        )


def test_capability_names_have_no_size_words():
    """small / medium / large — size class leaking in."""
    for cap in CapabilitySet:
        tokens = set(cap.value.split("_"))
        leaked = tokens & _BANNED_SIZE_TOKENS
        assert not leaked, (
            f"{cap.value!r} contains size tokens {leaked} — size belongs in policy"
        )


def test_capability_names_have_no_degree_words():
    """safe / strict / loose / limited / max / min — degree leaking in."""
    for cap in CapabilitySet:
        tokens = set(cap.value.split("_"))
        leaked = tokens & _BANNED_DEGREE_TOKENS
        assert not leaked, (
            f"{cap.value!r} contains degree tokens {leaked} — degree belongs in policy"
        )


def test_guardrails_catch_hypothetical_violations():
    """Sanity: the same checks correctly reject names we'd never accept."""
    bad_names = [
        "repo_patch_500",
        "repo_patch_safe",
        "repo_patch_small",
        "repo_patch_max",
        "shell_write_limited",
    ]
    for name in bad_names:
        tokens = set(name.split("_"))
        has_digit = bool(re.search(r"\d", name))
        has_size = bool(tokens & _BANNED_SIZE_TOKENS)
        has_degree = bool(tokens & _BANNED_DEGREE_TOKENS)
        assert has_digit or has_size or has_degree, (
            f"guardrail tokens missed {name!r}"
        )


def test_capability_set_is_kept_small():
    """Resist enum bloat. Bumping this number requires deliberation."""
    assert len(CapabilitySet) <= 8, (
        "CapabilitySet exceeded the soft cap. Confirm the new capability is "
        "a genuine permission class and not a policy-quantifier in disguise."
    )
