Runtime: Linux backend only. This policy is framework-neutral.

Queue policy:

```json
{"maxAttempts":3,"retryStatus":[408,429,500,502,503],"preserveJobId":true}
```

Required behavior:

- `maxAttempts` counts every execution, including the initial attempt: at most three attempts total (one initial attempt and up to two retries).
- Retry only failures with status 408, 429, 500, 502, or 503, and only while attempts remain. This is an explicit allowlist; unlisted statuses and failures without a status are not eligible under this policy.
- Authentication and authorization failures (401 and 403) are terminal and must not be retried.
- Stop after success or any non-retryable failure. If the third attempt fails, mark the job failed without scheduling another attempt.
- Preserve the original job ID across every attempt. A retry must not create a new logical job or reset its attempt count. The attempt limit applies across worker restarts and redelivery as well.

Acceptance cases:

| Outcomes by attempt | Expected result |
| --- | --- |
| Success | One attempt; complete |
| 401 or 403 | One attempt; failed; no retry |
| Any other unlisted status, or failure without a status | One attempt; failed; no retry |
| Each allowed status followed by success | Two attempts; complete |
| 503, 503, success | Three attempts; complete |
| 503, 503, 503 | Three attempts; failed; no fourth attempt |
| Retry after worker restart or redelivery | Same job ID and retained attempt count; three-attempt limit still applies |

These are required semantics, not evidence that a queue implementation has executed them. Queue adapter configuration, durable attempt accounting, and runtime verification remain implementation responsibilities.
