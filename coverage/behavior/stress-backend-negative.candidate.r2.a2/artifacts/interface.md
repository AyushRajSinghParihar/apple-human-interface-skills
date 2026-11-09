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

- `maxAttempts` counts the initial execution and every retry: at most three executions per job (one initial attempt and at most two retries). Persist the attempt count across requeues and service restarts; do not reset it on retry.
- Retry a failed attempt only when its status is in `retryStatus` and fewer than three attempts have executed. This list is the policy's transient-failure allowlist.
- Authentication and authorization failures, including 401 and 403, are terminal and must not be retried. Other statuses and failures without a listed status are also terminal under this policy.
- A successful attempt completes the job without a retry. A terminal failure or an exhausted attempt budget marks the job failed without another enqueue.
- Preserve the original job ID on every attempt and requeue. Do not create a new job identity to reset the attempt budget.

## Acceptance checks

1. A job that always returns 503 executes exactly three times, with the same job ID each time, then fails with no further retry.
2. For each of 408, 429, 500, 502, and 503, a failure on the first attempt permits a second attempt; a failure on the third attempt permits none.
3. Each of 401, 403, an unlisted status (for example 400), and a failure without a status terminates after the first attempt with no retry.
4. A successful first attempt executes once. A transient failure followed by success executes twice and stops, preserving the ID.
5. Restarting the service or requeuing the job after two failed attempts retains the original ID and consumed attempt count, allowing at most one further attempt.
