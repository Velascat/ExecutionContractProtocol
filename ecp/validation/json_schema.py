from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

SCHEMA_ROOT = Path(__file__).resolve().parents[2] / "schemas" / "v0.1"
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
