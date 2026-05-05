# Log

_Chronological continuity log. Decisions, stop points, what changed and why._
_Not a task tracker — that's backlog.md. Keep entries concise and dated._

## Stop Points

- Phase 0 of Backend Control Audit framework landed (2026-05-05, on `main`): All 8 sub-items of the contract foundation. **0.1** Contract evolution policy added to README (additive non-breaking; renames/removals require schema_version bump; capability removals require deprecation cycle; `evidence.extensions` is the sole sanctioned extension slot). **0.2 + 0.8** New `Evidence` dataclass at `cxrp/contracts/evidence.py` carrying `files_changed`, `commands_run`, `tests_run`, `artifacts_created`, `failure_reason`, `extensions` — wired into `ExecutionResult` as `evidence` field plus a `summary` field; JSON schema updated to enforce `additionalProperties: false` at the evidence level (extensions go under `extensions`, not at the top). **0.3** `cxrp/vocabulary/capability.py` with `CapabilitySet` enum (7 coarse capabilities: repo_read, repo_patch, test_run, shell_read, shell_write, network_access, human_review). **0.4** Naming guardrail tests reject digits, size words (small/medium/large), and degree words (safe/strict/loose/limited/max/min) in capability names; soft cap of 8 to discourage bloat. **0.5–0.7** `cxrp/vocabulary/runtime.py` (RuntimeKind, SelectionMode enums, validity table, optional-field allow-list) + `cxrp/contracts/runtime_binding.py` with `__post_init__` validation rejecting invalid kind×selection_mode pairs and forbidden optional-fields-per-kind (e.g. `human` with `model=opus` → ValueError). RuntimeBinding wired into ExecutionRequest as optional field; schema updated. Architect-via-Claude-CLI-Opus use case has a dedicated test confirming construction + serialization + schema validation. 16 → 51 tests pass.

## Recent Decisions

| Decision | Rationale | Date |
|----------|-----------|------|
| CxrpExecutionResult typed deserialization | parse_execution_result(payload) validates and returns typed object; summarize_execution_result() now takes typed object not raw dict; T2 exclusion removed since tests now have real assertions | 2026-05-02 |
| C16 encoding fix in json_schema.py | 2× schema_path.read_text() missing encoding= keyword; Custodian C16 finding resolved | 2026-05-02 |

## Stop Points

_(none)_

## Notes

_Free-form scratch. Clear periodically._
