# Evidence And Labeling Rules

## Evidence Labels

Use these labels consistently:

- `repo-confirmed`
  Claim is backed by files in the app repo.
- `site-confirmed`
  Claim is backed by live site metadata or read-only bench output.
- `erpnext-core`
  Claim is backed by upstream ERPNext or Frappe code.
- `legacy-note`
  Claim came from an old repo doc and has not yet been re-verified.

Do not present `legacy-note` content as confirmed behavior.

## Required Sections Per Canonical Doc

Every major workflow doc should contain:

1. Scope and assumptions
2. Ownership graph
3. Write paths and side effects
4. Reconstructed flows
5. Mermaid diagrams
6. Reports, print formats, dashboards, and workflow states when relevant
7. Unresolved gaps and next probes

## Ownership Graph Guidance

Map at least:

- trigger surface
- controller or hook owner
- shared services or utilities
- downstream doctypes
- reports or prints exposing the outcome

Keep each edge tied to a file path, function name, or site artifact.

## Mermaid Rules

- Use `flowchart TD` for structural maps.
- Use `sequenceDiagram` for request-to-side-effect flows.
- Use `stateDiagram-v2` for workflow states, document statuses, or approval gates.
- Prefer short node labels.
- Put nuance in notes below the diagram, not inside large node text.

## Legacy Note Handling

- If an old note matches current code, absorb it and drop the legacy label.
- If it conflicts, keep the current source as canonical and record the conflict in the unresolved appendix or replacement map.
- If it covers a still-unverified edge, keep it as `legacy-note` until the edge is confirmed.
