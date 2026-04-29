# Compatibility

All top-level contracts use `schema_version` and `contract_kind` as stable discriminators.

Consumers should validate payloads against `cxrp/schemas/v0.1/*.schema.json` before processing.
