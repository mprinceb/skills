# Refactor and Code Splitting Checklist

## Smell Signals

- Large file or module: repeatedly edited file with high complexity.
- Mixed concerns: one module owns UI logic, data fetching, orchestration, and state transitions.
- Cyclic imports or deep coupling chains across folders.
- Duplicate business rules with divergent behavior.
- Feature flags/toggles spread without a single owner boundary.

## JavaScript / TypeScript Signals

- React component files that exceed ~300 lines or contain multiple unrelated effects/hook clusters.
- Utility hooks or helpers with cross-cutting usage and no clear owning domain.
- Monorepo barrel/export files that re-export large unstable surfaces.
- Import fan-in/fan-out that creates brittle coupling between `pages`, `services`, `components`, and `shared`.
- Repeated API/data-shape transformations duplicated across components or services.
- Route handlers/controllers where validation, permission checks, and business logic are all colocated.

## Python Signals

- Modules >~800 LOC with mixed concerns (`api`, `models`, `persistence`, `parsing`) in a single file.
- Import cycles across package layers (model <-> service <-> utils).
- Repeated parsing/normalization logic copied between command, task, and worker modules.
- Django/Flask/FastAPI endpoints that handle request parsing, authorization, business rules, and persistence together.
- Service modules that directly import low-level infrastructure and UI/CLI concerns.

## Candidate Priority

1. Critical
- Cyclic imports blocking independent builds.
- Monolithic module where multiple teams touch unrelated concerns.
- Repeated runtime failure or test brittleness from hidden coupling.

2. High
- Overloaded shared utilities touched by many unrelated domains.
- Large, frequently changed files that represent multiple responsibilities.
- Route or command handlers with >20% shared setup code.

3. Medium
- Files with repeated helper logic that can be consolidated.
- Stable helper clusters duplicated in sibling modules.
- Feature code that repeatedly branches on the same mode or flags.

4. Low
- Cosmetic naming or placement cleanup with low risk reduction.

## Split Design Heuristics

- Define one ownership boundary per package/folder.
- Export minimal public surface; keep internal APIs private by default.
- Preserve invariants before moving files (data model, error semantics, auth).
- Add temporary adapter layers for backward compatibility when public contracts change.
- Prioritize extracting by behavior: `input parsing`, `core logic`, `side effects`.
- Keep language-specific split boundaries semantically stable:
  - JS/TS: split by feature slice (UI, state, API client, domain helpers) before horizontal utility extraction.
  - Python: split by transport vs application domain vs infra adapters before micro-optimizations.
- Verify that each split preserves import direction (`ui -> domain -> infra`) and avoids cycle creation.

## Output Must Include

- exact file names as evidence
- why split is safer than leaving as-is
- migration path and rollback point
- validation checks before and after the change (tests, linters, integration checks)
- a dedicated section for mixed-language interactions (if both JS/TS and Python boundaries are edited together)
