import json
from dataclasses import fields
from pathlib import Path

import pytest
from jsonschema import ValidationError

from ecp.contracts import ExecutionRequest, ExecutionResult, LaneDecision, TaskProposal
from ecp.contracts.execution_result import Artifact
from ecp.validation.json_schema import SCHEMA_FILE_MAP, load_schema, validate_contract
from ecp.vocabulary.artifact import ArtifactType
from ecp.vocabulary.lane import LaneType
from ecp.vocabulary.status import ExecutionStatus


def test_models_import_and_construct():
    tp = TaskProposal(proposal_id="tp-1", title="T", objective="O")
    ld = LaneDecision(decision_id="ld-1", proposal_id="tp-1", lane=LaneType.CODING_AGENT)
    erq = ExecutionRequest(
        request_id="erq-1",
        proposal_id="tp-1",
        lane_decision_id="ld-1",
        lane=LaneType.CODING_AGENT,
        scope="s",
    )
    ers = ExecutionResult(
        result_id="ers-1",
        request_id="erq-1",
        ok=True,
        status=ExecutionStatus.SUCCEEDED,
        artifacts=[Artifact(artifact_type=ArtifactType.OUTPUT, uri="file://out.txt")],
    )

    assert tp.contract_kind == "task_proposal"
    assert ld.contract_kind == "lane_decision"
    assert erq.contract_kind == "execution_request"
    assert ers.contract_kind == "execution_result"


def test_examples_validate_against_json_schema():
    for path in Path("examples/v0.1").glob("*.json"):
        payload = json.loads(path.read_text())
        validate_contract(payload["contract_kind"], payload)


def test_roundtrip_serialization_dict_shape():
    result = ExecutionResult(result_id="ers-9", request_id="erq-9", ok=False, status=ExecutionStatus.FAILED)
    payload = result.to_dict()

    assert payload["schema_version"] == "0.1"
    assert payload["contract_kind"] == "execution_result"
    assert payload["result_id"] == "ers-9"
    assert payload["status"] == "failed"


def test_required_first_class_ids_and_no_metadata_id_requirement():
    contracts = {
        "task_proposal": "proposal_id",
        "lane_decision": "decision_id",
        "execution_request": "request_id",
        "execution_result": "result_id",
    }
    for contract_kind, id_field in contracts.items():
        schema = load_schema(contract_kind)
        assert id_field in schema["required"]

    payload = json.loads(Path("examples/v0.1/task_proposal.basic.json").read_text())
    payload["metadata"] = {}
    validate_contract("task_proposal", payload)


def test_execution_request_includes_lane_and_status_vocabulary_expanded():
    request_schema = load_schema("execution_request")
    assert "lane" in request_schema["required"]

    result_schema = load_schema("execution_result")
    status_values = result_schema["properties"]["status"]["enum"]
    assert "accepted" in status_values
    assert "rejected" in status_values
    assert "timed_out" in status_values


def test_lane_decision_confidence_bounds_enforced():
    payload = json.loads(Path("examples/v0.1/lane_decision.basic.json").read_text())

    payload["confidence"] = -0.01
    with pytest.raises(ValidationError):
        validate_contract("lane_decision", payload)

    payload["confidence"] = 1.01
    with pytest.raises(ValidationError):
        validate_contract("lane_decision", payload)


def test_schema_filenames_follow_documented_convention():
    expected = {
        "task_proposal.schema.json",
        "lane_decision.schema.json",
        "execution_request.schema.json",
        "execution_result.schema.json",
    }
    found = {path.name for path in Path("schemas/v0.1").glob("*.json")}
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
        assert model_fields == schema_fields
        assert set(schema["required"]).issubset(schema_fields)
