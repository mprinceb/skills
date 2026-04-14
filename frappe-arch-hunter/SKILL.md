---
name: frappe-arch-hunter
description: Architecture and process discovery for Frappe and ERPNext apps. Use when Codex needs to trace a DocType or business workflow across DocType JSON, controllers, client scripts, hooks, reports, print formats, patches, workflows, whitelisted methods, and linked doctypes; identify functions that create, mutate, submit, cancel, or read that DocType; and turn the evidence into reusable flow notes or Mermaid diagrams for onboarding and knowledge capture.
---

# Frappe Arch Hunter

## Overview

Map a Frappe DocType or business process into an evidence-backed architecture packet. Start with static repo evidence, confirm bench and site context only when runtime truth matters, and leave behind reusable notes that can be extended instead of rediscovered.

## Hunt Modes

- `doctype-impact`: start with one DocType and map schema, controller methods, hooks, linked doctypes, write paths, reports, print formats, workflows, and patches.
- `process-trace`: start with a user action, button, API, scheduler task, or hook and trace the downstream DocTypes and side effects.
- `knowledge-pack`: combine multiple traces into onboarding material for one module or app.

## Workflow

1. Lock context.
   - Identify bench root, site, app, module, environment, target DocType, and the business question.
   - Reuse the cautious bench habits from `frappe-bench-cli`: prefer explicit site scope and read-only validation first.
2. Build a structural inventory.
   - Find the DocType JSON, controller, client script, related child tables, hooks, patches, workflows, reports, print formats, fixtures, overrides, and whitelisted methods.
   - Run `scripts/doctype_arch_hunt.py` for the first pass, then expand with the targeted search patterns in `references/doctype-hunt-playbook.md`.
3. Build the ownership graph.
   - Reuse the `frappe-staff-engineer` mindset: map `doctype -> controller -> lifecycle methods -> hooks -> utilities/services -> downstream doctypes/events`.
   - Keep every edge tied to a file and line or a concrete runtime observation.
4. Hunt effectful code paths.
   - Prioritize functions that create, save, submit, cancel, amend, rename, delete, enqueue, notify, or perform direct DB writes.
   - Separate read paths from write paths. Keep ambiguous helpers marked as unconfirmed until verified.
5. Reconstruct flows.
   - Convert references into ordered business flows: trigger, permission gate, validation, mutation, downstream side effects, and user-visible outcome.
   - Keep separate flows separate until their branching conditions are clear.
6. Validate runtime truth when static evidence is not enough.
   - Use `bench --site <site> execute ...` read helpers or safe inspection commands.
   - Do not mutate data unless the task explicitly changes into a repair or implementation task.
7. Synthesize reusable knowledge material.
   - Produce a compact summary, open questions, and at least one Mermaid diagram.
   - Update an existing flow note if one already exists; otherwise create a new doctype or process note.

## Search Priorities

Start in this order:

1. DocType schema, controller, and client script
2. `hooks.py` doc_events, overrides, fixtures, scheduler events, and whitelisted method registrations
3. service or utility modules imported by controllers and hooks
4. reports, print formats, workflows, notifications, and integration adapters
5. patches and migrations that rewrite the DocType or related records
6. frontend calls that trigger server behavior

Use `references/doctype-hunt-playbook.md` for concrete `rg` patterns and output rules.

## Output Contract

Return results in this order:

1. scope and assumptions
2. ownership graph
3. write paths and side effects
4. reconstructed flows
5. Mermaid diagram or diagrams
6. unresolved gaps and next probes

Keep outputs evidence-backed and easy to extend. Prefer small tables or bullets over long prose.

## Mermaid Rules

- Use `flowchart TD` for structural impact maps.
- Use `sequenceDiagram` for request-to-side-effect flows.
- Use `stateDiagram-v2` only when the DocType has explicit state transitions worth modeling.
- Keep node labels short and move nuance into notes below the diagram.

Use `references/flow-output-template.md` for ready-to-fill templates.

## Escalation Rules

- Stay read-only by default.
- If the hunt reveals a likely bug or needed refactor, switch to `frappe-staff-engineer` for planning and `frappe-developer` for implementation instead of mixing the work into the analysis pass.
- If runtime truth requires a live bench, use explicit site scope and record the exact commands run.

## Resources

- `scripts/doctype_arch_hunt.py`: run a first-pass evidence sweep for one DocType across a Frappe app or package path.
- `references/doctype-hunt-playbook.md`: use targeted search patterns, ownership graph rules, and runtime validation prompts.
- `references/flow-output-template.md`: use reusable templates for doctype notes, process notes, and Mermaid diagrams.
