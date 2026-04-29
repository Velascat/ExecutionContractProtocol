# Execution Contract Protocol (ECP)

Execution Contract Protocol is a **contract-only specification** that defines the shared language exchanged between:

- **OperatorConsole** (entrypoint)
- **SwitchBoard** (lane selection boundary)
- **OperationsCenter** (planning boundary, execution boundary, policy enforcement, and adapter dispatch)

ECP defines **what systems say to each other**, not how they run.

## What ECP Is

- Versioned contract models.
- Canonical vocabulary enums.
- JSON Schemas for validation.
- Example payloads for interoperable integration.

## What ECP Is Not

ECP excludes implementation logic, including:

- execution logic
- routing logic
- scheduling/watchers
- subprocess execution
- model/provider integrations
- adapters
- queue systems

## Core Contracts (v0.2)

1. `TaskProposal` — expresses requested work intent.
2. `LaneDecision` — records chosen lane/executor/backend by SwitchBoard.
3. `ExecutionRequest` — defines bounded work unit for execution; carries lane-specific `input_payload` validated against a named payload schema.
4. `ExecutionResult` — reports normalized outcome (`ok`, `status`, optional `artifacts`, optional `diagnostics`).

### Layered vocabulary

`lane` is an abstract category (`coding_agent`, `review_agent`, ...). `executor` (e.g. `claude_cli`) and `backend` (e.g. `kodo`) are open strings at the envelope level — consuming systems layer their own typed constraints internally.

## Repository Layout

- `ecp/contracts/`: Python contract models.
- `ecp/vocabulary/`: canonical enums (`status`, `lane`, `artifact`).
- `ecp/validation/`: schema loading and validation helper.
- `schemas/v0.2/`: JSON Schemas for the four canonical contracts.
  - `task_proposal.schema.json`
  - `lane_decision.schema.json`
  - `execution_request.schema.json`
  - `execution_result.schema.json`
  - `payloads/`: per-lane payload schemas (e.g. `coding_agent_input.schema.json`).
- `schemas/v0.1/`: frozen prior revision, retained for historical interop.
- `examples/v0.2/`: minimal interoperable examples.
- `docs/spec/v0.2.md`: versioned normative summary.

## Inter-system Relationship

- OperatorConsole emits or captures `TaskProposal` and `ExecutionResult`-shaped data.
- SwitchBoard consumes `TaskProposal` and emits `LaneDecision` only.
- OperationsCenter consumes `TaskProposal` + `LaneDecision`, builds `ExecutionRequest`, and consumes `ExecutionResult`.

## Versioning

All contracts include `schema_version = "0.2"` and `contract_kind` as canonical discriminators. v0.1 is frozen; breaking changes land under a new `schemas/vX.Y/`.
