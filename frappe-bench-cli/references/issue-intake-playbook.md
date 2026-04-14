# Issue Intake Playbook (PDF/Error Reports)

## Goal

Convert unstructured error reports into an executable fix queue for Frappe benches.

## Input Types

- PDF bug report
- DOCX/notes export
- plain text error list
- mixed screenshots + text

## Intake Schema

Capture each issue as one row/object with:

- `issue_id`: stable identifier
- `source_page`: page/section in source doc
- `site`: site name (explicit or inferred)
- `app`: likely app/module
- `doctype`: target DocType (if present)
- `error_message`: normalized message
- `traceback_signature`: top frames + exception class
- `repro_steps`: concise reproduction path
- `expected_behavior`: expected outcome
- `severity`: critical/high/medium/low
- `status`: new/in-progress/fixed/blocked

## Extraction and Normalization

1. Extract text from source document.
2. Split by headings, traceback blocks, or numbered issue markers.
3. Normalize stack traces:
   - keep exception type
   - keep top relevant app frames
   - strip noisy worker/request wrappers
4. Infer ownership:
   - traceback path under `apps/<app>/...` => app owner
   - doctype path hints => doctype owner

## Triage Rules

Prioritize in this order:

1. Data corruption/loss risk
2. Financial/accounting correctness
3. Authentication/authorization/security
4. Blocking transaction workflows
5. Non-blocking UI/validation defects

## Execution Loop Per Issue

1. Reproduce on target site.
2. Confirm failing layer:
   - DocType controller, hook handler, API method, report query, client script, patch.
3. Implement smallest safe fix.
4. Run migration if needed.
5. Validate with tests + `bench execute` readback checks.
6. Record evidence:
   - command(s) run
   - before/after counts or behavior
   - files changed

## Recommended Bench Checks During Triage

```bash
bench --site <site> version
bench --site <site> list-apps
bench --site <site> migrate
bench --site <site> execute <app>.scripts.bench_tasks.<read_helper> --kwargs '{"dry_run":1}'
```

## Output Format for Agent Work

Keep a running table:

- `issue_id`
- `severity`
- `owner_layer`
- `root_cause`
- `fix_summary`
- `validation_summary`
- `status`

## Multi-Site Considerations

- Never assume one-site fixes apply everywhere.
- Validate on each impacted site if apps/config differ.
- Prefer site-explicit commands over implicit defaults.
