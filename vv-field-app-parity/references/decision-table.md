# Data Ownership Decision Table

Use this before changing any DocType or endpoint.

| Situation | Action | Reason | Repo Example |
| --- | --- | --- | --- |
| Contract mismatch is only method path, arg naming, or passthrough kwargs | Reuse existing API and harden compatibility | No lifecycle change is needed | Wrong contract method paths and Cloudflare passthrough args |
| New field belongs to the same record lifecycle | Extend existing DocType | Keeps the right grain and avoids unnecessary models | Target fields on milestone summary/execution parent where grain is unchanged |
| Requirement introduces sub-stages, criteria, repeated evidence, approvals, or daily event history | Introduce or use execution-layer DocTypes | Summary child rows are the wrong place for event history | `Engineering Sub Stage`, `Construction Sub Stage Progress Submission`, `Manpower Daily Log` |
| Summary DocType is carrying operational data just because it already exists | Refactor away from summary row ownership | Prevents CST/CSD overload and child-table limitations | Moving sub-stage state and evidence out of `Construction Status Detail` |
| Temporary compatibility surface exists and deployment state is explicitly safe | Remove | Avoids carrying dead architecture | Legacy daily report / project log / legacy milestone queue removal |
| Temporary compatibility surface exists but deployment state is unknown | Keep for now, ask first | Prevents destructive cleanup based on assumption | Any bridge or legacy API slated for removal before staging/prod confirmation |
| GET route creates execution docs or updates naming series | Refactor to synthesize read state | GET must be non-mutating and concurrency-safe | `get_project_milestones` read-side bootstrap removal |
| Shared operational data is being filtered by actor identity | Keep shared data and store actor as audit metadata | Consumer decides visibility; storage remains global | Manpower logs read behavior after actor-filter removal |

## Non-Negotiable Ownership Rules

- `Construction Status Tracker` and `Construction Status Detail` are summary-only.
- Execution docs own sub-stage state, criteria, evidence, and review history.
- Daily manpower logs are transactional docs, not embedded summary state.
- Progress photos append to the current submission record for the sub-stage.

## Removal Gate

Before removing any compatibility layer, confirm one of these:
- the user explicitly says nothing is in staging or production
- release context proves the surface is not deployed

If neither is true, do not remove by default.
