# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 ProtocolWarden
"""ExecutionTargetEnvelope — Phase 2 wire-shape tests."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from cxrp.contracts import (
    ExecutionRequest, ExecutionTargetEnvelope, LaneDecision, RuntimeBinding,
)
from cxrp.validation.json_schema import validate_contract
from cxrp.vocabulary.lane import LaneType
from cxrp.vocabulary.runtime import RuntimeKind, SelectionMode


class TestEnvelopeShape:
    def test_constructs_with_lane_only(self):
        env = ExecutionTargetEnvelope(lane=LaneType.CODING_AGENT)
        assert env.backend is None
        assert env.executor is None
        assert env.runtime_binding is None

    def test_full_envelope(self):
        rb = RuntimeBinding(
            kind=RuntimeKind.CLI_SUBSCRIPTION,
            selection_mode=SelectionMode.EXPLICIT_REQUEST,
            provider="anthropic", model="opus",
        )
        env = ExecutionTargetEnvelope(
            lane=LaneType.CODING_AGENT, backend="team_executor", executor="claude_cli",
            runtime_binding=rb,
        )
        assert env.backend == "team_executor"
        assert env.executor == "claude_cli"
        assert env.runtime_binding.model == "opus"

    def test_backend_and_executor_are_open_strings(self):
        """The deliberate asymmetry — unknown backends/executors flow through."""
        env = ExecutionTargetEnvelope(
            lane=LaneType.CODING_AGENT,
            backend="some_future_backend_we_dont_know_yet",
            executor="some_future_executor_we_dont_know_yet",
        )
        assert env.backend.startswith("some_future")


class TestLaneDecisionAdditive:
    def test_decision_with_envelope_serializes(self):
        env = ExecutionTargetEnvelope(
            lane=LaneType.CODING_AGENT, backend="team_executor", executor="claude_cli",
        )
        ld = LaneDecision(
            decision_id="d", proposal_id="p",
            lane=LaneType.CODING_AGENT, executor="claude_cli", backend="team_executor",
            execution_target=env,
        )
        payload = ld.to_dict()
        assert payload["execution_target"]["backend"] == "team_executor"
        validate_contract("lane_decision", payload)

    def test_decision_without_envelope_still_validates(self):
        """Backward compat — pre-Phase 2 producers don't emit execution_target."""
        ld = LaneDecision(decision_id="d", proposal_id="p", lane=LaneType.CODING_AGENT)
        payload = ld.to_dict()
        # Older payloads serialize execution_target as None which is fine
        validate_contract("lane_decision", payload)

    def test_unknown_top_level_field_still_rejected(self):
        ld = LaneDecision(decision_id="d", proposal_id="p", lane=LaneType.CODING_AGENT)
        payload = ld.to_dict()
        payload["sneaky"] = "smuggled"
        with pytest.raises(ValidationError):
            validate_contract("lane_decision", payload)


class TestRequestAdditive:
    def test_request_with_envelope_validates(self):
        env = ExecutionTargetEnvelope(
            lane=LaneType.CODING_AGENT, backend="team_executor", executor="claude_cli",
        )
        req = ExecutionRequest(
            request_id="r", proposal_id="p", lane_decision_id="d",
            lane=LaneType.CODING_AGENT, scope="s",
            execution_target=env,
        )
        payload = req.to_dict()
        validate_contract("execution_request", payload)
        assert payload["execution_target"]["backend"] == "team_executor"

    def test_envelope_inside_request_keeps_legacy_fields_too(self):
        env = ExecutionTargetEnvelope(
            lane=LaneType.CODING_AGENT, backend="team_executor", executor="claude_cli",
        )
        req = ExecutionRequest(
            request_id="r", proposal_id="p", lane_decision_id="d",
            lane=LaneType.CODING_AGENT, scope="s",
            executor="claude_cli", backend="team_executor",
            execution_target=env,
        )
        # Both legacy fields and envelope coexist; consumer chooses
        assert req.executor == "claude_cli"
        assert req.execution_target.executor == "claude_cli"
