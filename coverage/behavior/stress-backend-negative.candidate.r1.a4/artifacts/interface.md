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

- `maxAttempts` counts the initial execution: one initial attempt and at most two retries. Never start a fourth attempt.
- Retry only a failed attempt whose status is in `retryStatus`, and only while the total attempt count is below three. These statuses are the transient-failure allowlist for this policy; other statuses and failures without a status are not automatically retryable.
- Authentication and authorization failures (`401` and `403`) are terminal and must not be retried.
- Stop immediately on success. When a failure is not retryable or the attempt limit is reached, record a terminal failure.
- Keep the original job ID for every attempt; a retry must not create a new logical job or reset its attempt count.

## Integration requirements

The backend adapter must map its failure classifications to this allowlist and translate the total-attempt limit if its queue library configures retries instead (two retries). Persist the attempt count with the job and enforce it across worker restarts and redelivery. Preserving the ID does not by itself guarantee idempotent side effects or exactly-once execution.

Retry delay, backoff, concurrency, and side-effect deduplication are outside the supplied policy and require separate integration decisions.
