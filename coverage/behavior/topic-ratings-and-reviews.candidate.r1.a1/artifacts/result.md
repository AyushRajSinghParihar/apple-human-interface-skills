# Rating-request repair

Patched `interface.md` in place with an implementable iPhone flow, eligibility and persistence rules, migration behavior, system-owned outcomes, and acceptance scenarios.

## Decisions

- Replace the custom five-star demand with the standard system review request. Remove all rating dependencies from watering reminders and all decline-triggered retries.
- Ask only after saved watering activity at an idle care summary. Require 14 days and three care dates initially; thereafter require 90 days and three further care dates, with at most three candidate invocations per rolling year. These concrete thresholds are product choices; Apple advises demonstrated engagement and at least a week or two between candidates with further engagement.
- Count attempts regardless of display. Persist cadence through updates and prevent duplicate invocations. Never claim a rating was submitted or retry because the system displayed nothing.
- Preserve watering records and reminders, including during migration. Unknown legacy engagement starts a new observation period rather than an immediate ask.

The material sources are [Ratings and reviews — Best practices](https://developer.apple.com/design/human-interface-guidelines/ratings-and-reviews#Best-practices) and [Onboarding — Additional requests](https://developer.apple.com/design/human-interface-guidelines/onboarding#Additional-requests), read from the installed local snapshots, not fetched online. The standard prompt recommendation is a HIG preference; the stronger product contract here deliberately adopts it.

## Worked before / after

Before: On first launch, Maya tries to configure a fern's watering reminder. A custom demand for five stars blocks setup. Declining causes another request, and the app can claim submission without knowing whether system UI appeared.

After: Maya configures the reminder immediately, without a rating request. On day 15, she saves her third watering record on a third distinct date and returns to the care summary. The app records one candidate and invokes the system request mechanism. If the system suppresses it, the saved record and reminder remain available and no success message appears. The next day's watering cannot trigger another request. A later candidate requires both 90 elapsed days and three new care dates, and must fit the rolling-year budget. If a prompt appears and she dismisses it, the same continuation and cadence apply; the app does not infer her response.

## Acceptance checks and status

Passed — static specification review: the patched contract covers fresh users, engagement thresholds, an interrupted opportunity, recent requests, duplicate events, persistence, migration, opt-out/no-display, dismissal, and ordinary continuation. It removes the four supplied defects: first-launch asking, five-star coercion, reminder gating/repeated decline requests, and unverifiable success claims. The acceptance table in `interface.md` defines expected results for implementation.

Failed — the original supplied specification fails those four behavioral requirements. No executed implementation failures are asserted.

Not executed — native StoreKit invocation/presentation, SDK compilation or API availability, device flows, notification scheduling, persistence and clock-boundary tests, GUI rendering, or accessibility/assistive-technology checks. Implementation must test the acceptance table, including exact 14/90/365-day boundaries and duplicate callbacks; static review cannot establish these runtime outcomes.

## Evidence limits and route audit

Only the supplied one-paragraph interface and installed instructions were available. No app code, deployment target, SDK, telemetry, device, or account evidence establishes real engagement, prompt visibility, or submission. No web browsing occurred. System display remains outside the app's control; this work delivers a revised specification rather than an implemented or device-tested app.

Read the installed `apple-hig/SKILL.md`, searched `references/topic-index.md` for review concepts, then read `subskills/apple-hig-patterns/SKILL.md` and its `.topics/apple-hig-ratings-and-reviews/SKILL.md` before `references/ratings-and-reviews.md`. Followed the first-use route to `.topics/apple-hig-onboarding/SKILL.md` before `references/onboarding.md`. All paths resolve beneath `.agents/skills/apple-hig/`; each instruction/source read used one file per command. The local source snapshots are dated 2026-10-25 and are guidance summaries, not SDK documentation or proof of independent source review.
