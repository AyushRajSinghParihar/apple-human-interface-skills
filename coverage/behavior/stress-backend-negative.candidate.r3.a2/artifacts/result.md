# Result

Updated `interface.md` in place with this framework-neutral Linux backend policy:

```json
{"maxAttempts":3,"retryStatus":[408,429,500,502,503],"preserveJobId":true}
```

## Decisions

- Three attempts means the initial execution plus at most two retries.
- Retained the supplied transient-status list after removing 401 and 403. Retry eligibility is an explicit allowlist; no additional status or statusless failure was assumed transient.
- Success, non-retryable failures, and exhaustion terminate processing. Retries retain the original job ID and attempt count, including across restart or redelivery.
- No framework, scheduling delay, backoff, or jitter setting was invented from the limited input.

## Acceptance checks

- Static policy validation passed: valid JSON, `maxAttempts` equals 3, retry statuses equal `[408,429,500,502,503]`, 401/403 excluded, and `preserveJobId` equals true.
- Specification review: acceptance cases cover immediate success, authentication/authorization failure, unlisted or statusless failure, every allowed retry status, success on the third attempt, exhaustion without a fourth attempt, and restart/redelivery identity and accounting.

## Missing evidence

Only a policy document was supplied. No queue implementation, adapter, runtime configuration, test suite, or execution logs were available. The acceptance cases are specified but have not been executed against a backend. Durable attempt accounting, job ID preservation, actual retry filtering, and enforcement under restart/redelivery still require implementation-level tests and logs. No device, SDK, GUI, or accessibility execution was performed or claimed.
