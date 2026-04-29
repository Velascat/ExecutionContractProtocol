# CxRP — Contract × Request Protocol

> CxRP is a contract-only protocol for defining and executing structured work — describing AI/workflow request lifecycles across planning, lane selection, execution requests, and execution results.

CxRP defines the shared language exchanged between:

- **OperatorConsole** (entrypoint)
- **SwitchBoard** (lane selection boundary)
- **OperationsCenter** (planning boundary, execution boundary, policy enforcement, and adapter dispatch)

CxRP defines **what systems say to each other**, not how they run.

## What CxRP Is

- Versioned contract models.
- Canonical vocabulary enums.
- JSON Schemas for validation.
- Example payloads for interoperable integration.

## What CxRP Is Not

CxRP excludes implementation logic, including:

- execution logic
- routing logic
- scheduling/watchers
- subprocess execution
- model/provider integrations
- adapters
- queue systems
- transport machinery (gRPC, FastAPI, Temporal, etc.)

## Status

Current revision: **v0.2** (active). Frozen prior revision: **v0.1** (retained on disk for historical interop).

## Core Contracts (v0.2)

1. `TaskProposal` — expresses requested work intent.
2. `LaneDecision` — records chosen lane/executor/backend by SwitchBoard.
3. `ExecutionRequest` — defines bounded work unit for execution; carries lane-specific `input_payload` validated against a named payload schema.
4. `ExecutionResult` — reports normalized outcome (`ok`, `status`, optional `artifacts`, optional `diagnostics`).

### Layered vocabulary

`lane` is an abstract category (`coding_agent`, `review_agent`, ...). `executor` (e.g. `claude_cli`) and `backend` (e.g. `kodo`) are open strings at the envelope level — consuming systems layer their own typed constraints internally.

## Repository Layout

- `cxrp/contracts/`: Python contract models.
- `cxrp/vocabulary/`: canonical enums (`status`, `lane`, `artifact`).
- `cxrp/validation/`: schema loading and validation helper.
- `cxrp/schemas/v0.2/`: JSON Schemas for the four canonical contracts (shipped inside the installable package).
  - `task_proposal.schema.json`
  - `lane_decision.schema.json`
  - `execution_request.schema.json`
  - `execution_result.schema.json`
  - `payloads/`: per-lane payload schemas (e.g. `coding_agent_input.schema.json`).
- `cxrp/schemas/v0.1/`: frozen prior revision, retained for historical interop.
- `examples/v0.2/`: minimal interoperable examples.
- `docs/spec/v0.2.md`: versioned normative summary.

## Inter-system Relationship

- OperatorConsole emits or captures `TaskProposal` and `ExecutionResult`-shaped data via `operator_console.ecp_capture`.
- SwitchBoard consumes `TaskProposal` and emits `LaneDecision` only; the wire shape is produced by `switchboard.adapters.ecp_mapper`.
- OperationsCenter consumes `TaskProposal` + `LaneDecision`, builds `ExecutionRequest`, and consumes `ExecutionResult`. OC has its own internal Pydantic subtype with stricter narrowing — `operations_center.contracts.cxrp_mapper` translates between OC's subtype and the CxRP envelope at the boundary.

### Subtype pattern

CxRP defines the **envelope**: identities, abstract `lane: LaneType` category, open-string `executor`/`backend`, free-form `input_payload` keyed by a lane-specific payload schema. Consumer repos (notably OC) layer their own typed `Literal`/Pydantic constraints internally without changing the wire contract. Cross-repo communication uses CxRP shape; intra-repo code is free to use richer types as long as it maps to/from CxRP at the wire.

## Versioning

All contracts include `schema_version = "0.2"` and `contract_kind` as canonical discriminators. v0.1 is frozen; breaking changes land under a new `cxrp/schemas/vX.Y/`.

Contract kinds and schema filenames are **stable** across versions:

```
task_proposal       lane_decision       execution_request       execution_result
```
