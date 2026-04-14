# Migration-Safe Changes

## When to Use Migration/Patch

Use patches when:

- field semantics change
- data backfill is required
- relation cleanup is needed
- hook path refactor requires state transition support

## Checklist

1. backup posture for target site
2. patch idempotency check
3. run `bench --site <site> migrate`
4. run post-migrate invariants/tests
5. log changed record counts
