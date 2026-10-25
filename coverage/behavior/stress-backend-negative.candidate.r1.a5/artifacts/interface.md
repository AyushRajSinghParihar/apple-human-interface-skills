# Queue retry policy

Runtime: Linux backend service. This policy is framework-neutral.

```json
{
  "maxAttempts": 3,
  "retryStatus": [408, 429, 500, 502, 503],
  "preserveJobId": true
}
```

- `maxAttempts` counts every execution, including the initial attempt: one initial attempt and at most two retries. Stop after the third failed attempt, even for a retryable failure.
- Retry only transient failures represented by the listed statuses: 408, 429, 500, 502, and 503. The status allowlist is necessary; a failure known to be permanent must not be retried even if its status is listed. Unlisted statuses and failures without a classified transient status are not retryable under this policy.
- Authentication and authorization failures (401 and 403) are terminal and must not be retried.
- Preserve the original job ID across every attempt. A retry must not create a new logical job or reset the attempt count.
- Stop on success. On a terminal failure or exhausted attempt budget, record the failed outcome using the original job ID.
