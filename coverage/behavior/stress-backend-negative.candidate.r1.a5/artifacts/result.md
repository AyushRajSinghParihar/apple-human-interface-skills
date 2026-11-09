# Result

Updated `interface.md` in place with a framework-neutral policy for the Linux backend:

```json
{
  "maxAttempts": 3,
  "retryStatus": [408, 429, 500, 502, 503],
  "preserveJobId": true
}
```

## Decisions

- Three attempts means the initial execution plus at most two retries, not three retries.
- Removed 401 and 403 from the retry allowlist because authentication and authorization failures are terminal.
- Retained the supplied transient status candidates; did not add new statuses. Known permanent failures are excluded even when their status is listed. Unclassified failures do not receive retries by default.
- Preserved logical job identity and attempt accounting across retries; success ends execution and terminal failures retain the original ID.
- No retry timing, backoff, persistence mechanism, or queue framework was selected because the supplied file provides no requirements or implementation for them.

## Acceptance checks

Local document checks: PASS. Parsed the JSON policy from `interface.md` and verified that `maxAttempts` is 3, `retryStatus` is exactly `[408, 429, 500, 502, 503]`, neither 401 nor 403 is allowed, and `preserveJobId` is true. Checked that the document explicitly includes the initial attempt in the limit and prohibits resetting the attempt count on retry.

Runtime acceptance scenarios (specified, not executed):

| Scenario | Required outcome |
| --- | --- |
| Three consecutive transient failures | Exactly three executions; no fourth attempt; final failure retains original job ID. |
| 401 or 403 on the first attempt | One execution; terminal failure; no retry. |
| Each allowed status on the first attempt, classified transient | A retry is eligible within the remaining attempt budget. |
| Unlisted status, unclassified failure, or known permanent failure | Terminal failure; no retry. |
| Success on any attempt | No further executions. |
| A job retries | Original job ID and cumulative attempt count are retained. |

## Missing evidence

Only `interface.md` was supplied as project content. There is no queue implementation, adapter configuration, test suite, or execution trace to establish runtime enforcement. Integration evidence is still needed for attempt accounting, transient classification, terminal outcomes, and job ID preservation, including behavior across worker restarts or redelivery. Job ID preservation alone does not establish idempotent side effects or exactly-once processing.

Validation was limited to local document checks. No backend service, device, SDK, GUI, or accessibility execution was performed. No web sources or Apple UI guidance were used.
