# Contributing to CxRP

CxRP is a **contract-only specification** defining the shared language exchanged between OperatorConsole, SwitchBoard, and OperationsCenter. It defines *what* systems say to each other, not *how* they run.

## Before You Start

- Check open issues to avoid duplicate work
- For any contract change (new field, enum value, schema revision), open an issue first to discuss the impact on downstream consumers
- All contributions must pass the test suite before merging

## Development Setup

```bash
git clone https://github.com/Velascat/CxRP.git
cd CxRP
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Requires `python3 >= 3.11`.

## Running Tests

```bash
PYTHONPATH=. .venv/bin/python -m pytest tests/ -v
```

## Project Structure

```
cxrp/contracts/      # Python contract models
cxrp/vocabulary/     # canonical enums (status, lane, artifact)
cxrp/validation/     # schema loading and validation helpers
cxrp/schemas/v0.2/   # JSON Schemas for the four canonical contracts (active)
cxrp/schemas/v0.1/   # frozen prior revision
examples/v0.2/       # minimal interoperable example payloads
docs/spec/           # versioned normative summaries
tests/               # contract + schema validation tests
```

## What Belongs Here

CxRP is the **contract layer only**. It must not contain:

- Execution logic (belongs in OperationsCenter)
- Routing or lane-selection logic (belongs in SwitchBoard)
- Scheduling, watchers, or subprocess execution
- Model/provider integrations or adapter implementations
- Queue systems or transport mechanisms

If unsure whether a change belongs here, open an issue first.

## Contract Change Rules

- **Additive within a version:** new optional fields and new enum values may be added to an existing schema version only if downstream consumers can ignore them safely.
- **Breaking changes require a new version:** renames, removals, type changes, and required-field additions must land under a new `schemas/vX.Y/` directory. The prior version stays frozen.
- Every contract carries `schema_version` and `contract_kind` — both are canonical discriminators and must not be repurposed.
- Update `docs/spec/` and `examples/` alongside any schema change.

## Pull Requests

- Keep PRs focused — one concern per PR
- Update or add tests for any contract or validation change
- Update relevant docs in `docs/spec/` if the change affects the normative spec
- Reference related issues in the PR description

## Commit Style

Use conventional commit prefixes:

| Prefix | Use for |
|--------|---------|
| `feat:` | new contract field, enum value, or schema revision |
| `fix:` | bug fix in models, validation, or schemas |
| `refactor:` | internal restructure, no contract change |
| `docs:` | documentation only |
| `test:` | test additions or fixes |
| `chore:` | tooling, CI, dependency updates |

## Code of Conduct

This project follows the [Contributor Covenant v2.1](CODE_OF_CONDUCT.md). By participating you agree to uphold its standards.
