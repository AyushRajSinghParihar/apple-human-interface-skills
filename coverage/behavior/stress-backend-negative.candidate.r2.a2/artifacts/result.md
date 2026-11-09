# Result

Updated `interface.md` in place with a framework-neutral Linux backend queue policy:

```json
{"maxAttempts":3,"retryStatus":[408,429,500,502,503],"preserveJobId":true}
```

## Decisions

- Three attempts means the initial execution plus at most two retries.
- Removed 401 and 403. Retained only the supplied transient-status candidates: 408, 429, 500, 502, and 503. No additional statuses were introduced.
- Treat the status list as an explicit allowlist; unlisted statuses and failures without a listed status are terminal. Success also stops execution.
- Require the original job ID and consumed attempt count to survive retries, requeues, and restarts so these operations cannot reset the budget.
- Backoff, scheduling, and framework-specific configuration are outside the supplied policy and remain unspecified.

## Acceptance checks and evidence

- PASS: Parsed the JSON policy from the edited file using Python 3 and asserted the exact attempt limit, status allowlist, job ID preservation flag, and three expected keys. The first invocation using `python` failed because that executable was unavailable; the `python3` invocation succeeded.
- Specified behavioral acceptance cases in `interface.md`: repeated transient failure exhausts exactly three attempts; every allowlisted status is retryable only within budget; authentication and other non-allowlisted failures stop immediately; success stops retries; job identity and budget survive requeue/restart.
- Behavioral acceptance cases have not been executed. The supplied project contains only the policy document, with no queue implementation, adapter, test harness, or runtime traces.

## Evidence still missing

- Implementation or adapter evidence that `maxAttempts` counts all executions, rather than retries alone, and enforces the allowlist and terminal outcomes.
- Execution traces or integration tests demonstrating the behavioral acceptance cases, including persisted attempt counts and stable IDs across restarts/requeues.
- Service-specific evidence that the retained statuses represent retryable transient failures for its operations, and that retrying an operation is safe if an earlier attempt partially completed. A stable job ID alone does not prove idempotent effects.

Only local files and installed command-line tools were used. No web browsing, Apple guidance, device, SDK, GUI, or accessibility execution was performed.
