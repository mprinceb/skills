# Canonical Workflow Doc Template

Use this template for major workflow docs.

```md
# <Title>

## Scope And Assumptions

- Scope:
- Assumptions:
- Evidence layers used:

## Ownership Graph

| Surface | Owner | Key files or artifacts | Evidence |
| --- | --- | --- | --- |

```mermaid
flowchart TD
    A[Trigger] --> B[Controller or Hook]
    B --> C[Downstream DocType]
```

## Write Paths And Side Effects

- Function or event:
  - writes:
  - downstream effects:
  - evidence:

## Reconstructed Flow

```mermaid
sequenceDiagram
    participant U as User or Trigger
    participant A as App Layer
    participant D as DocType or Service
    participant X as Downstream Effect
    U->>A: action
    A->>D: validate and mutate
    D->>X: side effect
```

## Reports, Print Formats, Dashboards, Workflows

- Reports:
- Print formats:
- Dashboards:
- Live workflow states:

## Unresolved Gaps And Next Probes

- Gap:
- Next probe:
```

## Metadata Files

For `_meta` files, keep the structure compact and machine-oriented when possible.

- `baseline.md`: short human-readable snapshot
- `baseline.json`: stable machine-readable contract
- `legacy-doc-map.md`: replacement ledger
