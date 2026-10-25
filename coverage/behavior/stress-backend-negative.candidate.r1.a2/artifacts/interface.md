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

- `maxAttempts` counts all executions, including the initial execution: at most one initial attempt and two retries. After the third failed attempt, stop retrying and mark the job as failed.
- Retry only failures with a status in `retryStatus`, treated as transient by this policy, and only while attempts remain. The allowlist is exhaustive; failures without a listed status do not retry.
- Authentication and authorization failures (`401` and `403`) are terminal and must not retry.
- A successful attempt completes the job and schedules no further attempts.
- Preserve the original job ID across every retry. Retrying must not create a new logical job or reset its attempt count.

The backend adapter must enforce the total-attempt limit even if its queue library counts retries separately (in that case, configure at most two retries). Persist the job ID and attempt count across retry scheduling and worker restarts so restarts cannot reset the budget. This document defines policy; enforcement in a running service requires implementation evidence.
