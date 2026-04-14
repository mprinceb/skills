# Implementation Playbook

## Goal

Deliver production-safe code changes driven by failing tests.

## Sequence

1. reproduce failure via tests
2. patch smallest responsible unit
3. verify pass
4. evaluate refactor opportunity
5. validate broader impacted scope

## Smallest Responsible Unit

Prefer changes in this order:

1. existing utility/service function
2. specific DocType controller method
3. hook handler function
4. schema/migration (only if necessary)

## Validation

Always include:

- targeted tests
- at least one integration-like flow check for critical doctypes
- runtime state/invariant checks if data side effects exist
