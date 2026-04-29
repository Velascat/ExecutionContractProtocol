from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

SCHEMA_ROOT = Path(__file__).resolve().parent.parent / "schemas" / "v0.2"

SCHEMA_FILE_MAP = {
    "task_proposal": "task_proposal.schema.json",
    "lane_decision": "lane_decision.schema.json",
    "execution_request": "execution_request.schema.json",
    "execution_result": "execution_result.schema.json",
}


def load_schema(contract_kind: str) -> dict[str, Any]:
    schema_path = SCHEMA_ROOT / SCHEMA_FILE_MAP[contract_kind]
    return json.loads(schema_path.read_text())


def validate_contract(contract_kind: str, payload: dict[str, Any]) -> None:
    schema = load_schema(contract_kind)
    Draft202012Validator(schema).validate(payload)


def load_payload_schema(payload_schema_id: str) -> dict[str, Any]:
    """Load a per-lane payload schema by its `name/vX.Y` identifier.

    `coding_agent_input/v0.2` resolves to
    `schemas/v0.2/payloads/coding_agent_input.schema.json`.
    """
    name, _, version = payload_schema_id.partition("/")
    if not name or not version.startswith("v"):
        raise ValueError(f"invalid payload schema id: {payload_schema_id!r}")
    schema_path = SCHEMA_ROOT.parent / version / "payloads" / f"{name}.schema.json"
    return json.loads(schema_path.read_text())


def validate_payload(payload_schema_id: str, payload: dict[str, Any]) -> None:
    schema = load_payload_schema(payload_schema_id)
    Draft202012Validator(schema).validate(payload)
