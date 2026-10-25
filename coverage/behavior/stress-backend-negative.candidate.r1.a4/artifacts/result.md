# Result

Updated `interface.md` in place with this concrete policy:

```json
{"maxAttempts":3,"retryStatus":[408,429,500,502,503],"preserveJobId":true}
```

## Decisions

- Three attempts means the initial execution plus at most two retries.
- Retained the supplied transient status list, removing authentication/authorization statuses 401 and 403. No additional retry categories were inferred.
- Unlisted statuses and failures without a status are terminal unless a separate policy explicitly classifies them.
- Success stops execution; retry exhaustion ends in terminal failure.
- Job identity and attempt count must survive retries, restarts, and redelivery. Queue adapters that count retries must configure two retries.
- Left timing, backoff, concurrency, and deduplication unspecified because the supplied file provides no requirements for them.

## Acceptance checks

Executed local document checks: the JSON in `interface.md` parses and exactly matches the policy above; the attempt cap is 3, 401/403 are absent, and identity preservation is enabled. These are document checks, not service execution.

The following behavioral acceptance cases are specified but remain unexecuted:

| Case | Required result |
| --- | --- |
| First attempt succeeds | One execution, no retry |
| 408, 429, 500, 502, or 503 fails repeatedly | Three total attempts, then terminal failure |
| Transient failure then success | Stop at success, at most three attempts |
| 401 or 403 | One attempt, terminal failure |
| Unlisted status or failure without status | No automatic retry |
| Any retry | Original job ID and cumulative attempt count retained |
| Restart or redelivery | Persisted count enforced; no fourth attempt |

## Missing evidence

Only `interface.md` was supplied as task input. No backend implementation, queue adapter, dependency configuration, persistence schema, test harness, or runtime logs were supplied. Service-level enforcement, restart/redelivery handling, status mapping, and side-effect idempotency therefore remain unverified. No device, SDK, GUI, or accessibility execution was performed or claimed. No web sources or Apple UI guidance were used.
