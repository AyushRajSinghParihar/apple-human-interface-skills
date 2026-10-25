# Queue retry policy

Runtime: Linux backend service. This policy is framework-neutral.

```json
{
  "maxAttempts": 3,
  "retryStatus": [408, 429, 500, 502, 503],
  "preserveJobId": true
}
```

## Required behavior

- `maxAttempts` counts every execution, including the initial attempt: one initial attempt and at most two retries. Stop after success or the third failed attempt.
- Retry only failures with a status in `retryStatus`, and only while fewer than three attempts have run. This list is the policy's transient-failure allowlist; it does not permit retries for every server error.
- Authentication and authorization failures (`401` and `403`) are terminal and must never trigger a retry. Other statuses and failures without a listed status are also terminal under this policy.
- Preserve the original job ID across all attempts. Scheduling a retry must not reset its attempt count or create a new logical job ID.

## Acceptance cases

| Attempt outcomes | Expected executions | Expected result |
| --- | --- | --- |
| Success | 1 | Complete; no retry |
| `408`, then success | 2 | Complete |
| `429`, `502`, then success | 3 | Complete |
| `503`, `503`, `503` | 3 | Terminal failure; no fourth attempt |
| `401` or `403` | 1 | Terminal failure; no retry |
| `500`, then `401` or `403` | 2 | Terminal failure; no further retry |
| Unlisted status or failure without a listed status | 1 | Terminal failure; no retry |

Each of `408`, `429`, `500`, `502`, and `503` must independently qualify for a retry when the attempt budget remains. For every case with retries, all executions must retain the original job ID and advance the same attempt counter.
