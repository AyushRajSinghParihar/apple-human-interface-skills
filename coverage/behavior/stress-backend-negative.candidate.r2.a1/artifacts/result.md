# Result

Updated `interface.md` in place with this concrete policy:

```json
{"maxAttempts":3,"retryStatus":[408,429,500,502,503],"preserveJobId":true}
```

## Decisions

- Three attempts means one initial execution plus at most two retries.
- Removed 401 and 403 from retry eligibility. Retained the supplied transient-status candidates as an explicit allowlist; no additional statuses were inferred.
- Required success, nonretryable failure, and exhausted attempts to stop scheduling retries.
- Required the original job ID and accumulated attempt count to survive requeuing so retries cannot evade the cap.
- Unclassified failures are not automatically transient. Retry timing, backoff, and additional failure classification remain unspecified by the supplied requirements.

## Acceptance checks and evidence

- Local document check: the policy is valid JSON with `maxAttempts` equal to 3, the exact allowlist above, and `preserveJobId` equal to true.
- Specification coverage: `interface.md` defines checks for repeated transient failures, every allowed status, 401/403, other and unclassified failures, success, and identity/count retention through requeue.
- Only local document validation was performed. The behavioral acceptance checks are specified, not executed against a queue service.

## Missing evidence

The supplied project contains no backend implementation, queue adapter, test harness, or runtime logs. Implementation-level evidence is still needed that the service interprets the cap as total attempts, enforces the allowlist, retains identity and counts through requeue, and stops scheduling after success or terminal failure. Any crash recovery or concurrent-delivery guarantees also require implementation and runtime evidence.

No web sources or Apple UI guidance were used. No device, SDK, GUI, or accessibility execution was performed or claimed.
