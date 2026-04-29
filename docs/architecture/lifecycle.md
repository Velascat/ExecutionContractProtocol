# Contract Lifecycle

Typical flow:

1. OperatorConsole emits `TaskProposal`.
2. SwitchBoard emits `LaneDecision`.
3. OperationsCenter builds `ExecutionRequest`.
4. Execution systems return `ExecutionResult`.

CxRP standardizes the payloads exchanged at each step; it does not define runtime control flow.
