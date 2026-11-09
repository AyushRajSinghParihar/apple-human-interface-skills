# Result

Updated `interface.md` in place with a framework-neutral Linux backend queue policy:

```json
{"maxAttempts":3,"retryStatus":[408,429,500,502,503],"preserveJobId":true}
```

## Decisions

- Interpret three attempts as one initial execution plus at most two retries.
- Retain the supplied transient-status candidates; remove 401 and 403. Use an explicit allowlist rather than retrying all errors or all server errors.
- Preserve the original job ID and consumed attempt count across retries, restarts, and redelivery; stop on success, nonretryable failure, or exhaustion.
- Leave timing/backoff unspecified because the supplied file provides no requirements for them.

## Acceptance checks

Local document checks passed: the policy parses as JSON, has exactly the three supplied keys, sets `maxAttempts` to 3, contains exactly statuses 408/429/500/502/503, excludes 401/403, and sets `preserveJobId` to true. The document explicitly counts the initial attempt toward the limit.

Required backend behavior checks, not executed:

| Scenario | Expected result |
| --- | --- |
| Repeated allowlisted failures | Three total executions, then failed/exhausted; no fourth execution |
| 401 or 403 | Stop after the first failure |
| Unlisted status or unclassified failure | No retry |
| Success initially or on a retry | Stop immediately |
| Any retry | Original job ID retained; attempt count increases |
| Restart or redelivery | Persisted ID/count retained; total attempt limit still enforced |

## Missing evidence

Only `interface.md` was supplied; no queue implementation, framework configuration, automated backend tests, or runtime logs were available. Consequently, enforcement of the policy, durable attempt accounting, and job ID preservation have not been demonstrated. Service-specific evidence that each allowlisted status represents a transient failure is also missing. Retry scheduling and side-effect idempotency need separate requirements and validation. No device, SDK, GUI, or accessibility execution was performed or claimed.
