# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| `main`  | ✅ Yes     |

Only the current `main` branch receives security fixes. Contract revisions are tracked under `schemas/vX.Y/`; older revisions are frozen and not patched.

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Report security issues privately by emailing **coding.projects.1642@proton.me**.

Include:
- A description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested mitigations (optional)

You will receive an acknowledgment within 72 hours. We aim to release a fix within 14 days of a confirmed report, depending on severity and complexity.

## Scope

CxRP is a **contract-only specification**. It defines schemas, vocabulary enums, and validation helpers — it does not execute work, route requests, or run subprocesses. The relevant security surface is therefore narrow:

- Schema-level ambiguities or under-constrained fields that allow unsafe payloads to validate
- Validation helper bugs that cause valid-looking but malformed contracts to pass
- Vocabulary enum gaps that permit unintended lanes, statuses, or artifact kinds
- Example payloads that demonstrate or encourage unsafe usage patterns

## Out of Scope

- Vulnerabilities in downstream consumers (OperatorConsole, SwitchBoard, OperationsCenter) — report those to the respective project
- Vulnerabilities in `jsonschema` or other upstream dependencies — report upstream
- Misuse of CxRP contracts by an implementing system (e.g., trusting unvalidated input)
