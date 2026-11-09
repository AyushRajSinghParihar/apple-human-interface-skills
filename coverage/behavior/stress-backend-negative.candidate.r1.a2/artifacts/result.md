# Result

Updated `interface.md` in place with the corrected framework-neutral policy:

```json
{"maxAttempts":3,"retryStatus":[408,429,500,502,503],"preserveJobId":true}
```

## Decisions

- Three attempts means the initial execution plus at most two retries.
- Removed `401` and `403` from the retry allowlist. Retained the supplied transient status set: `408`, `429`, `500`, `502`, and `503`. Unlisted or missing statuses do not retry.
- Preserved job identity and required the attempt budget to survive retries and worker restarts.
- Specified terminal behavior for success, nonretryable failures, and exhausted attempts.
- Kept this change to a Linux backend policy. No Apple guidance was loaded and no web sources were used.

## Acceptance checks

Document checks performed locally:

- The JSON policy parses and exactly matches the corrected values above.
- The attempt limit is an integer of three, the authentication statuses are absent, and job ID preservation is enabled.
- The document explicitly defines initial-attempt counting, exhaustive retry eligibility, terminal behavior, and persistence of identity and attempt count.

Required runtime acceptance checks (not executed):

| Scenario | Expected result |
| --- | --- |
| Repeated failure for each listed status | Exactly three total executions, then terminal failure; same job ID throughout |
| `401` or `403` on the initial attempt | One execution, terminal failure, no retry |
| Unlisted status or failure without a status | One execution, terminal failure, no retry |
| Immediate success | One execution, completed job, no retry |
| Listed transient failure followed by success | Two executions, completed job, no third execution; same job ID |
| Worker restart between attempts | Original job ID and consumed attempt count retained; total remains at most three |

## Missing evidence

Only the policy document was supplied. There is no service implementation, queue adapter, framework configuration, test suite, execution trace, or persistence evidence to establish runtime enforcement. In particular, mapping the total-attempt limit to the actual queue library and preserving the budget across restarts remain unverified. No device, SDK, GUI, or accessibility execution was performed or claimed.
