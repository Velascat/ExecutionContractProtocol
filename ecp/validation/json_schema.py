"""Compatibility shim. See `ecp.__init__` for details."""

from cxrp.validation.json_schema import (
    SCHEMA_FILE_MAP,
    SCHEMA_ROOT,
    load_payload_schema,
    load_schema,
    validate_contract,
    validate_payload,
)

__all__ = [
    "SCHEMA_FILE_MAP",
    "SCHEMA_ROOT",
    "load_payload_schema",
    "load_schema",
    "validate_contract",
    "validate_payload",
]
