# Reporting Patterns

Use this when the field-app work includes Desk visibility.

## Preferred Pattern

Do not create many near-duplicate reports when one report can support:
- `Detailed`
- `Branch Wise Summary`
- `Project Wise Summary`

Use:
- `view_type`
- `split_by_date`

That keeps audit rows and aggregate views on the same report surface.

## Engineering Reports In This Repo

- `Engineering Manpower Updates`
  Backed by `Manpower Daily Log` and `Manpower Daily Log Entry`
- `Construction Stage Updates`
  Backed by `Construction Sub Stage Progress Submission` and `Construction Sub Stage Progress Photo`

## Typical Filters

- `from_date`
- `to_date`
- `branch`
- `project`
- `unit_id`
- updater or submitter employee
- updater or submitter user
- milestone
- stage
- status or review status

## Aggregation Rules

- Apply filters first, then aggregate.
- `split_by_date = 1` means bucket by each date in range.
- `split_by_date = 0` means roll up across the whole filtered date range.
- Keep detailed rows available for audit/debugging even when summary modes exist.

## Verification

When a report changes:
- test the query shape in unit tests
- run the site test module
- clear cache so new filters appear
- verify any workspace link change if the user asked for app navigation updates

Minimum commands:

```bash
python3 -m py_compile <report python files>
/home/prince/frappe-bench/env/bin/python -m unittest vastu_vihar.tests.test_engineering_reports
bench --site <site> run-tests --app vastu_vihar --module vastu_vihar.tests.test_engineering_reports
bench --site <site> clear-cache
```
