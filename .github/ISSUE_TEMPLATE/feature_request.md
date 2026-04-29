---
name: Feature Request
about: Propose a new field, enum value, contract, or schema revision
labels: enhancement
assignees: ''
---

## Summary

A one-sentence description of the proposal.

## Problem It Solves

What can downstream systems (OperatorConsole / SwitchBoard / OperationsCenter) not currently express or validate?

## Proposed Change

What you want added or changed. Include a sketch:

```json
{
  "schema_version": "0.1",
  "contract_kind": "...",
  "...": "..."
}
```

## Change Class

- [ ] New optional field (additive within current version)
- [ ] New enum value (additive within current version)
- [ ] New contract kind
- [ ] Breaking change — requires new `schemas/vX.Y/`

## Downstream Consumers

Which systems need this, and how will they use it?

- OperatorConsole: 
- SwitchBoard: 
- OperationsCenter: 

## Alternatives Considered

Other shapes you thought about and why you ruled them out.

## Scope Check

Confirm this belongs in CxRP (contract layer) rather than:

- [ ] OperationsCenter (planning / execution / adapters)
- [ ] SwitchBoard (routing / lane selection logic)
- [ ] OperatorConsole (operator UX)

## Additional Context

Prior discussion links, related issues, or use-case background.
