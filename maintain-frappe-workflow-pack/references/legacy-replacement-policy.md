# Legacy Replacement Policy

## Goal

Move from scattered workflow notes to one canonical `business-workflow/` pack without losing track of what was replaced.

## Replacement Rule

Delete a legacy doc only when all of these are true:

1. the replacement canonical doc already exists
2. the canonical doc covers the same business slice at equal or better fidelity
3. any still-useful unmatched details were carried over or explicitly recorded as unresolved
4. `business-workflow/_meta/legacy-doc-map.md` records the replacement

## Replacement Map Format

Record at least:

- legacy path
- canonical replacement path
- replacement status: `replaced`, `merged`, `retired-without-replacement`
- notes on stale or conflicting claims

## Recommended Slice Strategy

- replace sales-related legacy docs when the sales pack lands
- replace construction legacy docs when the construction pack lands
- replace accounting and buying legacy docs when those packs land

Do not delete unrelated legacy docs early just because one new domain doc exists.

## Conflicts

If a legacy doc conflicts with current code or live site behavior:

- keep the current source as canonical
- record the conflict in the replacement map or unresolved appendix
- do not preserve the stale statement verbatim
