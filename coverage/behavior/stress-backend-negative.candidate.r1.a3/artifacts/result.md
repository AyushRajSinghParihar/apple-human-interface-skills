# Result

Updated `interface.md` in place with a concrete, framework-neutral Linux backend queue policy:

```json
{"maxAttempts":3,"retryStatus":[408,429,500,502,503],"preserveJobId":true}
```

## Decisions

- Three attempts means three total executions, including the initial attempt, with at most two retries.
- Removed `401` and `403` from the supplied retry list. Retained the supplied transient statuses; did not add new ones.
- Made retry eligibility an explicit allowlist. Unlisted statuses and failures without a listed status are terminal.
- Required stable job identity and a continuing attempt count across retries.
- Success and terminal failures stop execution immediately, even if attempt budget remains.

## Acceptance checks

- Static document checks passed: the JSON sets the three required policy values, excludes authentication failures, and retains exactly the five supplied transient statuses.
- `interface.md` includes acceptance cases for immediate success, transient recovery, exhaustion after three attempts, immediate authentication failure, authentication failure after a retry, and unlisted failures.
- The policy explicitly requires each allowed status to qualify independently and job identity and attempt count to persist across retries.

## Missing evidence

Only the supplied policy document was available; no queue implementation, framework adapter, runtime configuration, tests, or execution logs were supplied. The acceptance cases are specifications, not executed backend tests. Actual enforcement of the attempt limit, status classification, and ID/counter persistence remains unverified, including across worker restarts or redelivery. Framework-specific mapping of total attempts versus retry counts also remains unverified.

No device, SDK, GUI, or accessibility execution was performed or claimed. No web sources or Apple UI guidance were used.
