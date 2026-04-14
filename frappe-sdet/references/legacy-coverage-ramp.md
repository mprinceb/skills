# Legacy Coverage Ramp

## Goal

Increase confidence quickly in old Frappe apps without brittle over-testing.

## 3 Waves

1. Wave 1 (critical):
   - top 3 transactional doctypes
   - bug regressions currently observed
2. Wave 2 (high):
   - hook-heavy doctypes
   - override code paths
3. Wave 3 (medium):
   - utility modules and edge validations

## Progress Metrics

Track:

- critical scenarios covered
- number of regressions codified
- flaky tests count
- time to reproduce/verify bugs

Coverage percentage is secondary to risk closure.
