# Flow Output Template

## Doctype Note Template

```md
# <DocType>

## Scope
- app:
- module:
- bench/site:
- question:

## Structural Ownership
- schema:
- controller:
- client script:
- child tables:
- incoming links:

## Entry Points
- hook:
- API:
- button/client action:
- scheduler/background:

## Write Paths
- function:
- trigger:
- mutation:
- downstream side effects:

## Reports, Prints, and Workflow
- report refs:
- print refs:
- workflow refs:

## Open Questions
- ...
```

## Process Note Template

```md
# <Process Name>

## Trigger
- actor:
- entrypoint:

## Happy Path
1. ...
2. ...
3. ...

## Branches
- ...

## Side Effects
- document updates:
- events/jobs:
- integrations:

## Risks
- permissions:
- financial/state correctness:
- unclear ownership:
```

## Mermaid Templates

### Structural Impact Map

```mermaid
flowchart TD
    Trigger[Trigger] --> Controller[Controller method]
    Controller --> Service[Shared service]
    Service --> Target[Target DocType]
    Target --> Downstream[Downstream DocType or event]
```

### Request To Side Effect

```mermaid
sequenceDiagram
    actor User
    participant UI as Client or Hook
    participant API as API or Controller
    participant Service as Service
    participant DB as Frappe DB
    participant SideEffect as Event or Job

    User->>UI: Trigger action
    UI->>API: Call endpoint or save doc
    API->>Service: Validate and orchestrate
    Service->>DB: Create or mutate records
    Service-->>SideEffect: Emit side effect
    API-->>UI: Return updated outcome
```

### State Transition View

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Submitted: submit
    Submitted --> Cancelled: cancel
```

## Merge Discipline

- keep diagram names stable so later hunts can replace or extend them
- prefer one diagram per question instead of one giant app diagram
- keep unresolved edges in notes beneath the diagram instead of drawing speculative arrows
