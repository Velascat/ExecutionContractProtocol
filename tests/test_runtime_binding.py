# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Velascat
"""RuntimeBinding tests — validity table + optional-field allow-list."""
from __future__ import annotations

import json

import pytest
from jsonschema import ValidationError as JsonValidationError

from cxrp.contracts import ExecutionRequest, RuntimeBinding
from cxrp.validation.json_schema import validate_contract
from cxrp.vocabulary.lane import LaneType
from cxrp.vocabulary.runtime import (
    RuntimeKind,
    SelectionMode,
    field_allowed_for_kind,
    is_valid_kind_selection_mode,
)


# ── kind × selection_mode validity table ────────────────────────────────────


class TestValidityTable:
    def test_backend_default_pairs_with_backend_default_only(self):
        assert is_valid_kind_selection_mode("backend_default", "backend_default")
        assert not is_valid_kind_selection_mode("backend_default", "explicit_request")
        assert not is_valid_kind_selection_mode("backend_default", "policy_selected")

    def test_cli_subscription_accepts_all_three_modes(self):
        for mode in ("backend_default", "policy_selected", "explicit_request"):
            assert is_valid_kind_selection_mode("cli_subscription", mode)

    def test_human_rejects_backend_default(self):
        assert not is_valid_kind_selection_mode("human", "backend_default")
        assert is_valid_kind_selection_mode("human", "policy_selected")
        assert is_valid_kind_selection_mode("human", "explicit_request")

    def test_construction_rejects_invalid_pair(self):
        with pytest.raises(ValueError, match="cannot pair"):
            RuntimeBinding(
                kind=RuntimeKind.HUMAN,
                selection_mode=SelectionMode.BACKEND_DEFAULT,
            )
        with pytest.raises(ValueError, match="cannot pair"):
            RuntimeBinding(
                kind=RuntimeKind.BACKEND_DEFAULT,
                selection_mode=SelectionMode.EXPLICIT_REQUEST,
            )

    def test_construction_accepts_valid_pair(self):
        rb = RuntimeBinding(
            kind=RuntimeKind.CLI_SUBSCRIPTION,
            selection_mode=SelectionMode.EXPLICIT_REQUEST,
        )
        assert rb.kind == RuntimeKind.CLI_SUBSCRIPTION
        assert rb.selection_mode == SelectionMode.EXPLICIT_REQUEST


# ── optional-field allow-list ───────────────────────────────────────────────


class TestOptionalFieldAllowList:
    def test_model_allowed_for_cli_subscription_local_hosted(self):
        for kind in ("cli_subscription", "local_model_server", "hosted_api"):
            assert field_allowed_for_kind("model", kind)

    def test_model_forbidden_for_human_and_backend_default(self):
        assert not field_allowed_for_kind("model", "human")
        assert not field_allowed_for_kind("model", "backend_default")

    def test_provider_only_for_cli_and_hosted(self):
        assert field_allowed_for_kind("provider", "cli_subscription")
        assert field_allowed_for_kind("provider", "hosted_api")
        assert not field_allowed_for_kind("provider", "local_model_server")
        assert not field_allowed_for_kind("provider", "human")

    def test_endpoint_only_for_local_and_hosted(self):
        assert field_allowed_for_kind("endpoint", "local_model_server")
        assert field_allowed_for_kind("endpoint", "hosted_api")
        assert not field_allowed_for_kind("endpoint", "cli_subscription")
        assert not field_allowed_for_kind("endpoint", "human")

    def test_config_ref_for_all_runtime_kinds_except_human_and_default(self):
        assert field_allowed_for_kind("config_ref", "cli_subscription")
        assert field_allowed_for_kind("config_ref", "local_model_server")
        assert field_allowed_for_kind("config_ref", "hosted_api")
        assert field_allowed_for_kind("config_ref", "containerized_runtime")
        assert not field_allowed_for_kind("config_ref", "human")
        assert not field_allowed_for_kind("config_ref", "backend_default")

    def test_human_runtime_rejects_model(self):
        with pytest.raises(ValueError, match="model"):
            RuntimeBinding(
                kind=RuntimeKind.HUMAN,
                selection_mode=SelectionMode.EXPLICIT_REQUEST,
                model="opus",
            )

    def test_human_runtime_rejects_endpoint(self):
        with pytest.raises(ValueError, match="endpoint"):
            RuntimeBinding(
                kind=RuntimeKind.HUMAN,
                selection_mode=SelectionMode.EXPLICIT_REQUEST,
                endpoint="https://example.com/review",
            )

    def test_cli_subscription_accepts_model_and_provider(self):
        rb = RuntimeBinding(
            kind=RuntimeKind.CLI_SUBSCRIPTION,
            selection_mode=SelectionMode.EXPLICIT_REQUEST,
            provider="anthropic",
            model="opus",
        )
        assert rb.model == "opus"
        assert rb.provider == "anthropic"

    def test_cli_subscription_rejects_endpoint(self):
        with pytest.raises(ValueError, match="endpoint"):
            RuntimeBinding(
                kind=RuntimeKind.CLI_SUBSCRIPTION,
                selection_mode=SelectionMode.EXPLICIT_REQUEST,
                endpoint="https://localhost:1234",
            )


# ── ExecutionRequest integration ────────────────────────────────────────────


class TestRequestIntegration:
    def test_request_default_has_no_runtime_binding(self):
        req = ExecutionRequest(request_id="r", proposal_id="p", lane_decision_id="d")
        assert req.runtime_binding is None

    def test_request_with_binding_serializes(self):
        req = ExecutionRequest(
            request_id="r", proposal_id="p", lane_decision_id="d",
            lane=LaneType.CODING_AGENT,
            scope="s",
            runtime_binding=RuntimeBinding(
                kind=RuntimeKind.CLI_SUBSCRIPTION,
                selection_mode=SelectionMode.EXPLICIT_REQUEST,
                provider="anthropic",
                model="opus",
            ),
        )
        payload = req.to_dict()
        assert payload["runtime_binding"]["kind"] == "cli_subscription"
        assert payload["runtime_binding"]["selection_mode"] == "explicit_request"
        assert payload["runtime_binding"]["provider"] == "anthropic"
        assert payload["runtime_binding"]["model"] == "opus"
        validate_contract("execution_request", payload)

    def test_request_without_binding_still_validates(self):
        req = ExecutionRequest(
            request_id="r", proposal_id="p", lane_decision_id="d",
            lane=LaneType.CODING_AGENT, scope="s",
        )
        payload = req.to_dict()
        validate_contract("execution_request", payload)

    def test_schema_rejects_unknown_runtime_kind(self):
        req = ExecutionRequest(
            request_id="r", proposal_id="p", lane_decision_id="d",
            lane=LaneType.CODING_AGENT, scope="s",
            runtime_binding=RuntimeBinding(
                kind=RuntimeKind.CLI_SUBSCRIPTION,
                selection_mode=SelectionMode.EXPLICIT_REQUEST,
            ),
        )
        payload = req.to_dict()
        payload["runtime_binding"]["kind"] = "made_up_kind"
        with pytest.raises(JsonValidationError):
            validate_contract("execution_request", payload)

    def test_schema_rejects_extra_runtime_field(self):
        req = ExecutionRequest(
            request_id="r", proposal_id="p", lane_decision_id="d",
            lane=LaneType.CODING_AGENT, scope="s",
            runtime_binding=RuntimeBinding(
                kind=RuntimeKind.CLI_SUBSCRIPTION,
                selection_mode=SelectionMode.EXPLICIT_REQUEST,
            ),
        )
        payload = req.to_dict()
        payload["runtime_binding"]["sneaky_field"] = "smuggled"
        with pytest.raises(JsonValidationError):
            validate_contract("execution_request", payload)


# ── architect-via-CLI use case ──────────────────────────────────────────────


def test_architect_role_via_claude_cli_opus_constructs():
    """The special use case from the spec: architecture_design lane,
    Claude CLI subscription, Opus model. Must construct cleanly."""
    binding = RuntimeBinding(
        kind=RuntimeKind.CLI_SUBSCRIPTION,
        selection_mode=SelectionMode.EXPLICIT_REQUEST,
        provider="anthropic",
        model="opus",
    )
    req = ExecutionRequest(
        request_id="erq-arch-1",
        proposal_id="tp-arch-1",
        lane_decision_id="ld-arch-1",
        lane=LaneType.CODING_AGENT,
        executor="kodo",
        scope="design auth subsystem",
        runtime_binding=binding,
    )
    payload = req.to_dict()
    validate_contract("execution_request", payload)
    assert payload["runtime_binding"]["model"] == "opus"
