# OperationsCenter Integration

OperationsCenter is the primary CxRP consumer — it sees every contract type
across the orchestration lifecycle.

## Types consumed

| Direction | Contract | Where |
|---|---|---|
| Inbound (from operator/agents) | `TaskProposal` | `console run`, autonomy loop, intake watcher |
| Inbound (from SwitchBoard) | `LaneDecision` | `LaneSelector.select()` over HTTP |
| Outbound (to CoreRunner) | `ExecutionRequest` | `ExecutionCoordinator.execute()` |
| Outbound (return) | `ExecutionResult` | retained as `ExecutionRecord` |

## Mapping pattern

OC keeps internal Pydantic mirrors of CxRP types under
`src/operations_center/contracts/` (legacy reasons — they predate CxRP
extraction). The mirror is bridged via `src/operations_center/contracts/cxrp_mapper.py`,
which converts between OC's internal types and the canonical CxRP dataclasses.

```python
from cxrp.contracts import TaskProposal as CxrpTaskProposal
from operations_center.contracts import TaskProposal as OcTaskProposal
from operations_center.contracts.cxrp_mapper import to_cxrp_proposal, from_cxrp_proposal
```

New code should:
- Read CxRP types directly from `cxrp.contracts` when at a boundary
  (e.g. SwitchBoard HTTP, persisted run artifacts).
- Use OC's internal Pydantic types within the OC service layer.
- Round-trip through the mapper when crossing the boundary.

## Schema version

OC pins `cxrp >= 0.2.0` in `pyproject.toml`. Schema bumps require a
matching mapper update; v0.1 → v0.2 was handled in the schema-symmetry pass
on 2026-05-05.

## Related

- [boundary_rules](../architecture/boundary_rules.md) — what belongs in CxRP vs. consumers
- [compatibility](../architecture/compatibility.md) — schema_version policy
- [lifecycle](../architecture/lifecycle.md) — full TaskProposal → ExecutionResult flow
