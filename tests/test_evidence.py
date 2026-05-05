# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Velascat
"""Tests for the Evidence sub-contract on ExecutionResult."""
from __future__ import annotations

import json
from dataclasses import asdict

import pytest
from jsonschema import ValidationError

from cxrp.contracts import Evidence, ExecutionResult
from cxrp.validation.json_schema import validate_contract
from cxrp.vocabulary.status import ExecutionStatus


def _result(**evidence_fields) -> dict:
    res = ExecutionResult(
        result_id="ers-1",
        request_id="erq-1",
        ok=True,
        status=ExecutionStatus.SUCCEEDED,
        evidence=Evidence(**evidence_fields) if evidence_fields else Evidence(),
    )
    return res.to_dict()


def test_evidence_default_is_empty_normalized_shape():
    res = ExecutionResult(result_id="r", request_id="q")
    assert res.evidence.files_changed == []
    assert res.evidence.commands_run == []
    assert res.evidence.tests_run == []
    assert res.evidence.artifacts_created == []
    assert res.evidence.failure_reason is None
    assert res.evidence.extensions == {}


def test_evidence_serializes_to_dict_under_result():
    payload = _result(
        files_changed=["src/a.py", "src/b.py"],
        commands_run=["pytest"],
        failure_reason=None,
    )
    assert payload["evidence"]["files_changed"] == ["src/a.py", "src/b.py"]
    assert payload["evidence"]["commands_run"] == ["pytest"]
    assert payload["evidence"]["failure_reason"] is None
    assert payload["evidence"]["extensions"] == {}


def test_evidence_extensions_is_open_dict():
    payload = _result(extensions={"archon_workflow_id": "wf-42", "internal_trace": [1, 2]})
    assert payload["evidence"]["extensions"]["archon_workflow_id"] == "wf-42"
    assert payload["evidence"]["extensions"]["internal_trace"] == [1, 2]
    validate_contract("execution_result", payload)


def test_evidence_rejects_unknown_top_level_field():
    payload = _result()
    payload["evidence"]["definitely_not_a_real_field"] = "smuggled"
    with pytest.raises(ValidationError):
        validate_contract("execution_result", payload)


def test_extension_data_belongs_under_extensions_not_at_top_level():
    """Backend-specific data goes under evidence.extensions, never at the
    top of evidence (additionalProperties=false enforces this)."""
    payload = _result()
    payload["evidence"]["custom_backend_field"] = "leaked"
    with pytest.raises(ValidationError):
        validate_contract("execution_result", payload)

    # Same data, correctly placed under extensions, validates.
    payload = _result(extensions={"custom_backend_field": "leaked"})
    validate_contract("execution_result", payload)


def test_evidence_omitted_entirely_is_valid():
    """evidence is not in required[], so legacy producers without it pass."""
    payload = ExecutionResult(
        result_id="r", request_id="q", ok=True, status=ExecutionStatus.SUCCEEDED
    ).to_dict()
    payload.pop("evidence")
    validate_contract("execution_result", payload)


def test_failure_reason_accepts_string_or_null():
    payload = _result(failure_reason="adapter timed out")
    validate_contract("execution_result", payload)
    payload = _result(failure_reason=None)
    validate_contract("execution_result", payload)


def test_summary_field_present_and_optional():
    res = ExecutionResult(result_id="r", request_id="q")
    assert res.summary == ""
    payload = res.to_dict()
    assert payload["summary"] == ""
