# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 ProtocolWarden
import json
from dataclasses import fields
from pathlib import Path

import pytest
from jsonschema import ValidationError

from cxrp.contracts import (
    Artifact,
    ExecutionLimits,
    ExecutionRequest,
    ExecutionResult,
    LaneAlternative,
    LaneDecision,
    TaskProposal,
)
from cxrp.validation.json_schema import (
    SCHEMA_FILE_MAP,
    load_payload_schema,
    load_schema,
    validate_contract,
    validate_payload,
)
from cxrp.vocabulary.artifact import ArtifactKind
from cxrp.vocabulary.lane import LaneType
from cxrp.vocabulary.status import ExecutionStatus

EXAMPLES_DIR = Path("examples/v0.3")


def test_models_import_and_construct():
    from cxrp.contracts import BackendName, ExecutorName
    tp = TaskProposal(proposal_id="tp-1", title="T", objective="O")
    ld = LaneDecision(
        decision_id="ld-1",
        proposal_id="tp-1",
        lane=LaneType.CODING_AGENT,
        executor=ExecutorName.CLAUDE_CLI,
        backend=BackendName.TEAM_EXECUTOR,
        alternatives=[
            LaneAlternative(lane=LaneType.CODING_AGENT, executor=ExecutorName.CODEX_CLI, confidence=0.4)
        ],
    )
    erq = ExecutionRequest(
        request_id="erq-1",
        proposal_id="tp-1",
        lane_decision_id="ld-1",
        lane=LaneType.CODING_AGENT,
        scope="s",
        limits=ExecutionLimits(timeout_seconds=300),
    )
    ers = ExecutionResult(
        result_id="ers-1",
        request_id="erq-1",
        ok=True,
        status=ExecutionStatus.SUCCEEDED,
        artifacts=[Artifact(kind=ArtifactKind.OUTPUT.value, uri="file://out.txt")],
    )

    assert tp.contract_kind == "task_proposal"
    assert ld.contract_kind == "lane_decision"
    assert erq.contract_kind == "execution_request"
    assert ers.contract_kind == "execution_result"
    assert tp.schema_version == "0.3"


def test_examples_validate_against_json_schema():
    for path in EXAMPLES_DIR.glob("*.json"):
        payload = json.loads(path.read_text())
        validate_contract(payload["contract_kind"], payload)


def test_roundtrip_serialization_dict_shape():
    result = ExecutionResult(
        result_id="ers-9", request_id="erq-9", ok=False, status=ExecutionStatus.FAILED
    )
    payload = result.to_dict()

    assert payload["schema_version"] == "0.3"
    assert payload["contract_kind"] == "execution_result"
    assert payload["status"] == "failed"


def test_required_first_class_ids():
    contracts = {
        "task_proposal": "proposal_id",
        "lane_decision": "decision_id",
        "execution_request": "request_id",
        "execution_result": "result_id",
    }
    for contract_kind, id_field in contracts.items():
        schema = load_schema(contract_kind)
        assert id_field in schema["required"]


def test_lane_decision_confidence_bounds_enforced():
    payload = json.loads((EXAMPLES_DIR / "lane_decision.basic.json").read_text())

    payload["confidence"] = -0.01
    with pytest.raises(ValidationError):
        validate_contract("lane_decision", payload)

    payload["confidence"] = 1.01
    with pytest.raises(ValidationError):
        validate_contract("lane_decision", payload)


def test_lane_decision_confidence_model_validation():
    with pytest.raises(ValueError, match="confidence must be between 0.0 and 1.0"):
        LaneDecision(confidence=-0.01)
    with pytest.raises(ValueError, match="confidence must be between 0.0 and 1.0"):
        LaneDecision(confidence=1.01)
    assert LaneDecision(confidence=0.0).confidence == 0.0
    assert LaneDecision(confidence=1.0).confidence == 1.0


def test_lane_alternative_confidence_bounds_enforced():
    with pytest.raises(ValueError):
        LaneAlternative(lane=LaneType.CODING_AGENT, confidence=1.5)


def test_executor_and_backend_are_typed_enums_in_v0_3():
    """Schema 0.3 — closed-system simplification: backend/executor are
    typed enums on the wire. Unknown values fail at validation."""
    payload = json.loads((EXAMPLES_DIR / "lane_decision.basic.json").read_text())
    payload["executor"] = "some_future_tool_we_dont_know_yet"
    with pytest.raises(ValidationError):
        validate_contract("lane_decision", payload)
    payload["executor"] = "claude_cli"  # restore
    payload["backend"] = "some_future_dispatch_we_dont_know_yet"
    with pytest.raises(ValidationError):
        validate_contract("lane_decision", payload)


def test_artifact_kind_is_open_string_at_envelope_level():
    payload = json.loads((EXAMPLES_DIR / "execution_result.success.json").read_text())
    payload["artifacts"].append({"kind": "vendor_specific_kind", "uri": "file://x"})
    validate_contract("execution_result", payload)


def test_status_vocabulary_includes_full_set():
    schema = load_schema("execution_result")
    status_values = schema["properties"]["status"]["enum"]
    for required in ("succeeded", "failed", "cancelled", "timed_out", "rejected", "accepted"):
        assert required in status_values


def test_schema_filenames_follow_documented_convention():
    expected = {
        "task_proposal.schema.json",
        "lane_decision.schema.json",
        "execution_request.schema.json",
        "execution_result.schema.json",
    }
    found = {path.name for path in Path("cxrp/schemas/v0.2").glob("*.json")}
    assert found == expected
    assert set(SCHEMA_FILE_MAP.values()) == expected


def test_model_fields_and_schema_fields_cannot_drift():
    model_map = {
        "task_proposal": TaskProposal,
        "lane_decision": LaneDecision,
        "execution_request": ExecutionRequest,
        "execution_result": ExecutionResult,
    }
    for contract_kind, model in model_map.items():
        schema = load_schema(contract_kind)
        model_fields = {f.name for f in fields(model)}
        schema_fields = set(schema["properties"].keys())
        assert model_fields == schema_fields, contract_kind
        assert set(schema["required"]).issubset(schema_fields)


def test_payload_schema_loader_resolves_well_known_payloads():
    schema = load_payload_schema("coding_agent_input/v0.2")
    assert schema["title"] == "CodingAgentInput"


def test_coding_agent_input_payload_validates():
    request = json.loads((EXAMPLES_DIR / "execution_request.basic.json").read_text())
    validate_payload(request["input_payload_schema"], request["input_payload"])


def test_payload_schema_id_is_rejected_when_malformed():
    with pytest.raises(ValueError):
        load_payload_schema("not-a-valid-id")


def test_v01_schemas_are_frozen_and_still_present():
    v01 = Path("cxrp/schemas/v0.1")
    assert v01.is_dir(), "v0.1 schemas must remain frozen on disk"
    assert (v01 / "task_proposal.schema.json").exists()
