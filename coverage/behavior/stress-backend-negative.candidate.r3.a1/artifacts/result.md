# Result

Updated `interface.md` in place with the concrete policy:

```json
{"maxAttempts":3,"retryStatus":[408,429,500,502,503],"preserveJobId":true}
```

## Decisions

- Three attempts means the initial execution plus at most two retries.
- Removed 401 and 403 from the existing retry allowlist; retained the supplied transient statuses without expanding the policy to other failures.
- Made termination, stable job identity, and durable attempt counting explicit. Unlisted statuses and statusless failures do not trigger automatic retries.
- No queue framework, retry delay, backoff, or scheduler implementation was selected; none was supplied.

## Acceptance checks

Local document checks passed: the JSON parses, `maxAttempts` is 3, the retry allowlist is exactly `[408,429,500,502,503]`, 401 and 403 are excluded, and `preserveJobId` is true. These checks validate the policy artifact, not a running service.

The backend implementation must demonstrate the following before runtime acceptance:

| Scenario | Required result |
| --- | --- |
| Success on any attempt | No further attempt |
| Each listed status on attempts 1 or 2 | Retry with the original job ID |
| Listed status on attempt 3 | Exhausted; no fourth attempt |
| 401 or 403 on any attempt | Terminal failure; no retry |
| Unlisted status or statusless failure | Terminal failure; no automatic retry |
| Retry scheduling or worker restart | Original job ID and consumed attempt count remain intact |

## Missing evidence

Only the policy document was supplied. There is no backend source, queue adapter, framework configuration, test suite, or execution log establishing that the service enforces this policy. Integration evidence is still needed for attempt accounting, terminal outcomes, identity persistence, and restart behavior. Retry timing, duplicate-delivery handling, and job side-effect idempotency are unspecified and unverified.

No device, SDK, GUI, or accessibility execution was performed or claimed. No Apple guidance or web sources were loaded.
