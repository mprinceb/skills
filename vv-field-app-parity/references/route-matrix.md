# Route Matrix

Use this as the first ownership map before reading code.

## Discovery and Targets

| Route | Frappe Method | Primary Code | Primary Tests | Notes |
| --- | --- | --- | --- | --- |
| `/api/townships` | `vastu_vihar.api.field_bridge.get_townships` | `vastu_vihar/api/field_bridge.py` | `vastu_vihar/tests/test_field_api_contract_compat.py` | Project + CST summary read |
| `/api/townships/:projectName/units` | `vastu_vihar.api.field_bridge.get_township_units` | `vastu_vihar/api/field_bridge.py` | `vastu_vihar/tests/test_field_api_contract_compat.py` | Branch-scope and current phase label logic live here |
| `/api/my-targets` | `vastu_vihar.api.field_bridge.get_my_targets` | `vastu_vihar/api/field_bridge.py` | `vastu_vihar/tests/test_field_status_and_targets.py` | Reads from execution milestones, not old target helpers |

## Project, Status, and Stage Updates

| Route | Frappe Method | Primary Code | Primary Tests | Notes |
| --- | --- | --- | --- | --- |
| `/api/project-milestones` | `vastu_vihar.vastu_vihar.api.field_app_engineering.get_project_milestones` | `vastu_vihar/api/field_app_engineering.py` | `vastu_vihar/tests/test_field_api_contract_compat.py`, `vastu_vihar/tests/test_field_status_and_targets.py` | GET must not create execution docs |
| `/api/construction-status` | `vastu_vihar.vastu_vihar.api.field_app_engineering.get_construction_status` | `vastu_vihar/api/field_app_engineering.py` | `vastu_vihar/tests/test_field_api_contract_compat.py` | Project-wide CST + execution snapshot |
| `/api/construction-status/:unitId` | `vastu_vihar.vastu_vihar.api.field_app_engineering.get_unit_construction_status` | `vastu_vihar/api/field_app_engineering.py` | `vastu_vihar/tests/test_field_status_and_targets.py` | Milestone state derives from sub-stage + latest submission review |
| `/api/construction-status/:unitId/init` | `vastu_vihar.vastu_vihar.api.field_app_engineering.init_construction_status` | `vastu_vihar/api/field_app_engineering.py` | `vastu_vihar/tests/test_field_api_contract_compat.py` | Explicit bootstrap path for execution docs |
| `/api/stage-updates` `POST` | `vastu_vihar.vastu_vihar.api.field_app_engineering.submit_stage_update` | `vastu_vihar/api/field_app_engineering.py` | `vastu_vihar/tests/test_field_status_and_targets.py` | One mutable submission per sub-stage, photos append |
| `/api/stage-updates` `GET` | `vastu_vihar.vastu_vihar.api.field_app_engineering.get_stage_updates` | `vastu_vihar/api/field_app_engineering.py` | `vastu_vihar/tests/test_field_api_contract_compat.py` | Review current submission surface and param compatibility |
| `/api/stage-updates/:id/photos` | `vastu_vihar.vastu_vihar.api.field_app_engineering.get_stage_update_photos` | `vastu_vihar/api/field_app_engineering.py` | `vastu_vihar/tests/test_field_api_contract_compat.py` | Photo evidence lives on child rows, not separate legacy queues |

## Manpower

| Route | Frappe Method | Primary Code | Primary Tests | Notes |
| --- | --- | --- | --- | --- |
| `/api/unit-manpower` `POST` | `vastu_vihar.vastu_vihar.api.field_app_engineering.upsert_unit_manpower` | `vastu_vihar/api/field_app_engineering.py` | `vastu_vihar/tests/test_field_status_and_targets.py`, `vastu_vihar/tests/test_field_api_contract_compat.py` | Shared by `project_name + log_date`; actor is audit metadata |
| `/api/unit-manpower` `GET` | `vastu_vihar.vastu_vihar.api.field_app_engineering.get_unit_manpower_logs` | `vastu_vihar/api/field_app_engineering.py` | `vastu_vihar/tests/test_field_api_contract_compat.py` | Reads must not filter shared data by updater |
| `/api/unit-manpower/today` | `vastu_vihar.vastu_vihar.api.field_app_engineering.get_today_unit_manpower` | `vastu_vihar/api/field_app_engineering.py` | `vastu_vihar/tests/test_field_api_contract_compat.py` | Supports explicit `date` override |
| `/api/unit-manpower/summary` | `vastu_vihar.vastu_vihar.api.field_app_engineering.get_unit_manpower_summary` | `vastu_vihar/api/field_app_engineering.py` | `vastu_vihar/tests/test_field_api_contract_compat.py` | Verify `days` vs `since` precedence |
| `/api/admin-panel/engineering/manpower-summary` | `vastu_vihar.vastu_vihar.api.field_app_engineering.get_admin_manpower_summary` | `vastu_vihar/api/field_app_engineering.py` | `vastu_vihar/tests/test_field_api_contract_compat.py` | Cloudflare admin-role boundary matters here |

## Admin Review

| Route | Frappe Method | Primary Code | Primary Tests | Notes |
| --- | --- | --- | --- | --- |
| `/api/admin-panel/stage-updates/pending` | `vastu_vihar.vastu_vihar.api.field_app_engineering.get_pending_stage_updates` | `vastu_vihar/api/field_app_engineering.py` | `vastu_vihar/tests/test_field_status_and_targets.py` | Must require forwarded admin role |
| `/api/admin-panel/stage-updates/:id/approve` | `vastu_vihar.vastu_vihar.api.field_app_engineering.approve_stage_update` | `vastu_vihar/api/field_app_engineering.py` | `vastu_vihar/tests/test_field_status_and_targets.py` | Must reject already-processed submissions |
| `/api/admin-panel/stage-updates/:id/reject` | `vastu_vihar.vastu_vihar.api.field_app_engineering.reject_stage_update` | `vastu_vihar/api/field_app_engineering.py` | `vastu_vihar/tests/test_field_api_contract_compat.py` | Same auth and transition boundary as approve |

## Supporting Artifacts

Use these when the route family changes:
- contract source: `engineering-frappe-api-contract.md`
- route exposure or hooks: `vastu_vihar/hooks.py`
- reports: `vastu_vihar/vastu_vihar/report/engineering_manpower_updates/`, `vastu_vihar/vastu_vihar/report/construction_stage_updates/`
- report tests: `vastu_vihar/tests/test_engineering_reports.py`

If a route seems correct in the controller but still mismatched at runtime, inspect:
- bridge wrappers
- hook registrations
- report/workspace sync
- migration or patch side effects
