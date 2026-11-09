# Delivery Live Activity audit

Decision: revise before implementation. The supplied iOS proposal conflicts with the local Live Activities guidance in five concrete ways. Rankings below are reviewer judgments about user impact, not Apple severity ratings.

## Evidence and route

Inspected [interface.md](interface.md), which contains a textual proposal, not a rendered interface. Read the installed [root procedure](.agents/skills/apple-hig/SKILL.md), then its selected [System experiences family procedure](.agents/skills/apple-hig/subskills/apple-hig-system-experiences/SKILL.md), searched the exact component in the [topic index](.agents/skills/apple-hig/references/topic-index.md), and read the routed [Live Activities source guide](.agents/skills/apple-hig/subskills/apple-hig-system-experiences/references/live-activities.md). The family routes directly to this article; it specifies no additional topic procedure. Paths resolve within this installed package.

Official links below identify the source sections represented by that local guide; they were not fetched. The guide identifies its snapshot as 2026-10-25.

## Ranked verified findings and decisions

| Rank | Observed proposal and effect | Source-backed guidance | Correction / decision |
|---|---|---|---|
| 1 — High | Shows the customer's full address on Lock Screen, exposing sensitive delivery information to bystanders. | Avoid exposed sensitive content; summarize or redact and offer app access/configuration. [Best practices](https://developer.apple.com/design/human-interface-guidelines/live-activities#Best-practices) | Remove the street address, unit and other identifying destination details from the activity payload and display. Use “Your delivery.” Open the relevant order in the app for address details, subject to the app's access controls. |
| 2 — High | Labels a 40-minute-old estimate “Now,” presenting old information as current and encouraging misplaced reliance. | Show immediately useful information; the family procedure explicitly requires state freshness and fallback behavior. [Best practices](https://developer.apple.com/design/human-interface-guidelines/live-activities#Best-practices) | Display “Estimate unavailable” and “Last updated 40 min ago.” Suppress countdowns based on stale estimates. Define a product freshness threshold and apply it consistently; HIG does not supply a numerical threshold here. |
| 3 — High | Starts automatically for promotional offers without an active delivery, occupying a persistent system surface without a bounded task. | Use tasks with clear starts/ends; exclude ads and promotions. Automatic starts may occur at expected moments, with an easy opt-out in the corresponding app view. [Best practices](https://developer.apple.com/design/human-interface-guidelines/live-activities#Best-practices), [Starting, updating, and ending](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity) | No activity for an offer. Start only for a real active delivery at an expected tracking moment. Provide an easy per-delivery opt-out in the order view. Automatic start itself is not the violation. |
| 4 — Medium | Displays “Delivered” forever, retaining an obsolete activity after the task ends. | End immediately when the task ends. Lock Screen may retain the ended summary for up to 4 hours; choose a shorter useful lifetime, commonly 15–30 minutes. [Starting, updating, and ending](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity) | End on confirmed delivery. Request a 20-minute final Lock Screen summary, then removal; earlier system/user dismissal is acceptable. End cancellation similarly with an appropriate brief summary. Twenty minutes is this design's choice, not a universal HIG requirement. |
| 5 — Medium | Includes a complete shopping catalog in expanded content, burying delivery status and turning tracking into browsing. | Show only immediately useful information, keeping details in the app; favor one essential direct action. [Best practices](https://developer.apple.com/design/human-interface-guidelines/live-activities#Best-practices), [Offering interactivity](https://developer.apple.com/design/human-interface-guidelines/live-activities#Offering-interactivity) | Remove the catalog from every activity presentation. Expanded content contains delivery stage, trustworthy ETA/freshness and a relevant order deep link. Catalog browsing remains in the app. |

## Corrected behavior specification

Framework-agnostic policy; lifecycle and scheduling adapters must later be verified against the target platform. No Apple API or SDK is assumed.

```text
Policy:
  staleAfter = 5 minutes       // proposed product policy; validate with delivery operations
  finalSummaryLifetime = 20 minutes

on delivery event:
  if event is promotion or there is no real active delivery:
    do not start an activity
    return
  if user opted out for this delivery:
    do not start or restart; end an existing activity if necessary
    return
  start/update only at an expected tracking moment
  use only changed content for updates

render active delivery at currentTime:
  age = currentTime - trustworthy estimate observation time
  if observation time is missing, invalid or in the future:
    etaText = "Estimate unavailable"
    freshnessText = "Update time unavailable"
  else if age > staleAfter or estimate arrival time has passed:
    etaText = "Estimate unavailable"
    freshnessText = localized "Last updated {age} ago"
  else:
    etaText = localized arrival time/range from current estimate
    freshnessText = localized "Updated {age} ago"
  show last confirmed delivery stage; do not infer progress from elapsed time
  never substitute "Now" for an old or absent estimate
  exclude address and catalog data from activity content
  expose a relevant order deep link
  reevaluate freshness when time crosses the threshold, even without a new delivery event

on confirmed delivered/cancelled:
  end the activity immediately
  request final summary until terminalEventTime + finalSummaryLifetime
  omit ETA; show confirmed terminal status and time
  never extend expiry through repeated terminal events
```

The freshness scheduler must not depend solely on receiving another network update. If the eventual platform cannot reliably refresh at the threshold, use a conservative timestamped fallback rather than leave a seemingly current ETA on screen. Network loss alone does not establish cancellation or delivery.

Use a distinct, compact task layout: “Your delivery,” last confirmed stage, then ETA or fallback and update age. Retain those meanings in expanded content. Support compact/minimal presentations with essential changing status and the same order destination. Use standard 14 pt Lock Screen margins, with tighter spacing only for grouping; verify legible text and contrast in both appearances and reduced-luminance Always On. These are implementation acceptance requirements, not observed visual failures. [Anatomy](https://developer.apple.com/design/human-interface-guidelines/live-activities#Anatomy), [Lock Screen presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Lock-Screen-presentation)

## Worked before / after

At 14:00, delivery D42 is active, its last confirmed stage is “On the way,” and its estimate was observed at 13:20. No newer estimate exists.

| Before: supplied behavior | After: specified behavior |
|---|---|
| Full customer street address | “Your delivery” |
| “Now” based on the 13:20 estimate | “On the way” / “Estimate unavailable” / “Last updated 40 min ago” |
| Complete catalog in expanded content | Same delivery summary, linking to D42 in the app |

At 14:07, a confirmed delivered event arrives. End immediately and show “Delivered at 14:07” as the final summary, requesting removal by 14:27. A repeated delivered event at 14:10 does not extend that deadline. If instead there is only a promotional offer and no delivery, show no Live Activity at all.

## Acceptance checks

These are proposed checks, not executed test results.

- Offer-only input with no active delivery produces no activity. An eligible active delivery can start at the expected moment; opting out ends it and prevents restart for that delivery.
- Inspect every activity payload and presentation: no full address, unit, identifying destination detail, catalog or promotional content is present. Activating its order link resolves to the correct order.
- At 14:00 with an observation timestamp of 13:20, output matches the worked example. Missing/invalid/future timestamps show an honest fallback. A past arrival estimate never becomes “Now.”
- With no network event, advance time beyond the proposed five-minute threshold: stale ETA disappears or a conservative timestamped fallback remains. A new trustworthy update restores the current estimate.
- A confirmed terminal event immediately ends the running activity and requests a final summary expiry 20 minutes from that event. Repeated events do not reset expiry; earlier system/user dismissal is accepted.
- On actual supported devices or suitable rendering tools, verify small screens, longer localized strings and larger text: status and freshness remain legible, with no clipping. Check Lock Screen margins and contrast in light/dark appearances and Always On, including dismiss-button visibility. Verify accessible reading order and meaningful link labeling with accessibility tooling.

## Evidence limits

Only the supplied sentence and installed instructions/source snapshot were audited. All five findings are verified against that textual proposal; their relative severity and the five-minute/20-minute policy values are review decisions. There is no screenshot, implementation, payload, delivery-service contract or rendering evidence. Contrast, typography, touch targets, accessibility behavior, actual deep links, timers, lifecycle execution and system dismissal were not tested. No device, SDK, GUI, simulator, accessibility or automated test execution occurred. This document specifies intended behavior; implementation feasibility and current platform behavior remain to be validated. No web browsing was performed, and current official guidance was not independently verified.
