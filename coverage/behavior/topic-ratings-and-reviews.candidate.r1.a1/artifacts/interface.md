# Plant-care app: App Store review requests

Platform: iOS on iPhone. This specification replaces the custom first-launch five-star demand and its reminder gate.

## User flow

- First launch and onboarding contain no review request. People can add a plant, record watering, and configure watering reminders without rating the app.
- Remove the custom rating prompt, star selector, five-star demand, and decline/retry loop. Use the standard system App Store review prompt through the supported StoreKit review-request mechanism for the project's iOS deployment target. Verify the exact API and scene requirements against the SDK during implementation.
- Consider a request only after a watering record is successfully saved and the person returns to the care summary, with no edit, permission dialog, onboarding, or other task in progress. Save the record and update the summary before evaluating eligibility. Do not request while someone is setting a reminder or responding to one.
- No sentiment survey, positive-answer filter, reward, feature gate, or request for a particular star count precedes the system prompt. All eligible users follow the same rules.
- If another task starts, the app backgrounds, or the summary is no longer the active screen before invocation, discard that opportunity. Reevaluate only at a later completed watering task; do not queue a delayed interruption.

## Eligibility and cadence

These thresholds are product decisions, not Apple-mandated engagement counts:

1. At least 14 elapsed days since first use and at least three successfully saved watering records on three distinct local calendar dates. Opening the app alone does not count as completed care.
2. After a previous candidate request, at least 90 elapsed days and three additional watering records on distinct local dates must pass before another candidate is allowed.
3. Allow at most three app-initiated candidate requests in any rolling 365-day period. This conservative app budget is separate from the system's display limit; it counts invocations even if nothing appears.
4. Persist first-use time, completed-care dates, candidate timestamps, and the care-progress checkpoint at each candidate across launches and app updates. Serialize evaluation and record the candidate/checkpoint immediately before invoking the system mechanism so duplicate completion events cannot cause duplicate requests. If required history is missing, begin collecting it without making an immediate request. If time moves backward, suppress until eligibility can be established.

Never infer a decline, rating, or review from returning to the app, elapsed time, or a request invocation. Do not retry because no prompt appears. No release-version change resets the app's cadence history.

## System-owned outcome and continuation

The app requests presentation; the system decides whether to display UI, including based on prior feedback, global opt-out, and its own frequency rules. The local HIG snapshot describes a system display maximum of three times per app in 365 days; this is not an entitlement to three presentations.

Whether the prompt is shown, dismissed, completed, or suppressed, retain the saved watering record, current summary, and reminder configuration. All plant-care features remain available. Show no app-owned loading state, substitute prompt, success toast, or “rating submitted” message. A candidate invocation is not proof of visibility or submission. If instrumented, name the event `review_request_attempted`; never report it as a displayed prompt or submitted rating.

Existing reminder schedules must survive this migration. Remove the rating prerequisite from reminder entry and scheduling; do not request notification permission merely to solicit a review. Discard legacy decline/retry state without turning it into a new immediate request. Existing users without reliable engagement history start collecting the new history.

## Acceptance contract

| Scenario | Required result |
|---|---|
| Fresh install / onboarding | No rating UI or request invocation; plant care and reminder setup available. |
| Fewer than 14 days or fewer than three care dates | No candidate request. |
| Eligible completion at the care summary | Save first, invoke the standard mechanism once, preserve summary state. |
| Editing, reminder setup, permission UI, backgrounding, or navigating away | No request at that opportunity and no delayed replay. |
| Duplicate completion event / relaunch / app update | Persisted history prevents a duplicate candidate. |
| Less than 90 days or insufficient new care since candidate | No request, even when the previous invocation showed nothing. |
| Three candidates within rolling 365 days | Suppress another candidate. |
| System opt-out, suppression, dismissal, or completion | Care and reminders continue; no submission claim or replacement prompt. |
| Upgrade from old rating-gated flow | Existing reminders remain configured; no rating prerequisite or decline loop. |

## Guidance basis

[Apple HIG: Ratings and reviews — Best practices](https://developer.apple.com/design/human-interface-guidelines/ratings-and-reviews#Best-practices) supports demonstrated use, natural stopping points, spacing candidates by at least a week or two with further engagement, and preferring the standard prompt on iOS. This specification chooses a longer 90-day interval.

[Apple HIG: Onboarding — Additional requests](https://developer.apple.com/design/human-interface-guidelines/onboarding#Additional-requests) supports letting people experience value before requesting a rating. These links identify the official articles; the supplied installed snapshots were used without web access.
