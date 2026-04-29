# Migration: ECP → CxRP

The project was renamed from **Execution Contract Protocol (ECP)** to **CxRP — Contract × Request Protocol** in 2026-04. This is a name-only refactor.

## What changed

| Item | Before | After |
|---|---|---|
| Project name | `execution-contract-protocol` | `cxrp` |
| Python package | `ecp/` | `cxrp/` |
| Primary import path | `from ecp.contracts import …` | `from cxrp.contracts import …` |
| Repository identity in docs | "ECP" | "CxRP" |
| Tagline | "Execution Contract Protocol" | "CxRP — Contract × Request Protocol for execution-bound workflows" |

## What did NOT change

The wire contract itself is unchanged. None of these moved:

- **Contract class names** — `TaskProposal`, `LaneDecision`, `ExecutionRequest`, `ExecutionResult`
- **Contract kinds** — `task_proposal`, `lane_decision`, `execution_request`, `execution_result`
- **Schema versions** — `0.1` (frozen) and `0.2` (active)
- **Schema filenames** — `*.schema.json` for the four canonical contracts
- **Per-lane payload schemas** — `coding_agent_input/v0.2`, `coding_agent_target/v0.2`
- **Vocabulary enums** — `LaneType`, `ExecutionStatus`, `ArtifactKind`
- **Validation helpers** — `validate_contract`, `validate_payload`, `load_schema`, `load_payload_schema`

Existing on-disk JSON payloads, audit logs, and tests against schema files continue to validate without modification.

## Compatibility

A temporary `ecp/` package remains and re-exports everything from `cxrp/`. It emits a `DeprecationWarning` on import:

```python
# Old import — still works during the transition window
from ecp.contracts import LaneDecision
# DeprecationWarning: The `ecp` package has been renamed to `cxrp`. ...
```

The shim does not duplicate any model definitions; it imports from `cxrp` and re-exports.

## How to update consumer code

```python
# Replace
from ecp.contracts import LaneDecision
from ecp.validation.json_schema import validate_contract
from ecp.vocabulary.lane import LaneType

# With
from cxrp.contracts import LaneDecision
from cxrp.validation.json_schema import validate_contract
from cxrp.vocabulary.lane import LaneType
```

A repo-wide find/replace of `ecp.` → `cxrp.` (with word-boundary checks) is sufficient for most consumers. Module names like `operations_center.contracts.ecp_mapper` and `switchboard.adapters.ecp_mapper` are consumer-side and may keep their existing names; they describe what the module *does* (maps to the wire contract), not the spec's identity.

## Removal timeline

The `ecp` shim will be removed in a future release once consumer repos (OperatorConsole, SwitchBoard, OperationsCenter) have migrated their imports to `cxrp`.
