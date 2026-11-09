# Medication reminder complication — revised interaction specification

This is a framework-agnostic watchOS design contract. The supplied `interface.md` describes full medication and patient names on a shared-visible face, tiny multiline instructions, a scrolling task list, and due/recorded/overdue states. No implementation or screenshot was supplied.

## Decisions and basis

1. **One status per glance.** Replace the task list with one selected reminder status. The whole complication is a single entry point; it neither scrolls nor records a dose. A tap opens the corresponding dose context, not generic app home. This applies [watchOS best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices) and [complication best practices](https://developer.apple.com/design/human-interface-guidelines/complications#Best-practices).
2. **Keep identity and instructions inside the app.** Never place patient identifiers, medication names, strengths, directions, or dose IDs in visible face content, spoken face labels, placeholders, or preview assets. Default face mode is Private: a neutral reminder glyph and “Reminder” where space permits. An explicit in-app preference may enable generic status and scheduled time on the active face; explain “Status and reminder times can be seen by other people.” This stricter default is a product decision based on shared visibility, supported by [privacy minimization](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices). It reduces exposure; it does not make the app's presence secret.
3. **Redact wrist-down content.** Even with status enabled, Always On, locked, or system privacy-redacted presentations show the neutral private variant, with neither status nor time. Redact before producing content; do not rely solely on dimming. In the companion app, wrist down preserves layout and context but replaces sensitive text with neutral blocks and makes controls unavailable in place. Wrist raise restores the same context when access is allowed. This follows [Always On guidance](https://developer.apple.com/design/human-interface-guidelines/always-on#Best-practices); exact hardware/runtime support remains unverified.
4. **Readable roles, no instruction compression.** Use the host family's system complication typography (SF Compact Rounded on watchOS), normal medium/semibold emphasis, and no custom tiny text. Instructions belong to a full-text app route. Use words plus distinct glyphs, never red/green alone. No progress ring: a dose status is neither a percentage nor a bounded measure. See [complication visual design](https://developer.apple.com/design/human-interface-guidelines/complications#Visual-design), [typography](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type), and [accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

## Surface and family contract

Planning assumption: modern watchOS 9+ complication families; the installed guide prefers WidgetKit families from watchOS 9. This is not an SDK choice or availability claim for an implementation. Older ClockKit support is outside this revision and would require separate template verification. Offer each variant only in slots the host supports.

| Family | Active face, status enabled | Private / wrist down | Tap |
|---|---|---|---|
| Circular | State glyph plus “Due”, “Late”, or “Done”; use “Next” before due | Neutral reminder glyph | Selected dose detail |
| Corner | Same short state word; omit time | Neutral reminder glyph | Selected dose detail |
| Inline | “Due 08:00”, “Overdue 08:00”, “Recorded 08:07”, or “Next 20:00” | “Reminder” | Selected dose detail |
| Rectangular | Primary “Dose due”, “Dose overdue”, “Dose recorded”, or “Next reminder”; secondary scheduled time, or recording time for recorded | Stable neutral glyph and “Reminder”; no secondary value | Selected dose detail |

Times use the person's locale and 12/24-hour preference. “Late” and “Done” are compact visual equivalents of overdue and recorded, not different states. If translated text cannot fit at the host's supported type treatment, use a recognizable glyph launcher and retain the relevant destination; never shrink to fit or add scrolling. No medication-specific glyph is required. No rotating carousel or animation.

Use family-specific static, neutral placeholders during initial load and in selection previews; they never assert that a real dose is due or recorded. Content artwork and placeholder assets are separate deliverables for a later implementation. Use host-provided layout bounds, not hand-inferred pixel dimensions. The local guide mixes modern families and legacy tables and flags conflicting legacy inline dimensions; do not reuse those disputed values for production art. Family tables and limitations: [Complications](https://developer.apple.com/design/human-interface-guidelines/complications).

## State, selection, freshness, and routing

Each occurrence has an opaque local ID, scheduled instant, configured overdue instant, optional durable recording event, schedule revision, and validity horizon. Overdue timing comes from the existing reminder plan; this design invents no medical grace period. Missing or inconsistent thresholds yield unavailable status. “Recorded” means the user logged an event, not that ingestion was independently verified.

```text
state(occurrence, now):
  if durable recording exists: RECORDED
  if now >= overdueAt: OVERDUE
  if now >= scheduledAt: DUE
  return UPCOMING

select(snapshot, now):
  if no authorized account: SETUP
  if missing data or now >= validUntil: UNAVAILABLE
  if unrecorded occurrences at/before now exist:
    return oldest scheduled occurrence (tie: stable opaque ID)
  if a recording occurred within the last 5 minutes:
    return most recently recorded occurrence
  if future occurrences exist: return earliest future occurrence
  return EMPTY

render(snapshot, family, context):
  selected = select(snapshot, context.now)
  destination = opaque route for selected occurrence, or reminders overview
  if private preference OR locked OR redacted OR wristDown:
    return neutral family variant + destination
  return family representation(selected) + destination

activate(route):
  enforce app access rules; resolve ID against current account and revision
  if occurrence remains available: open its current detail/status
  else: open reminders overview with “Reminder changed”
  never mutate a recording merely because the complication was tapped
```

The five-minute recorded display window is a proposed product choice, not Apple guidance. An outstanding occurrence takes precedence over that window so recording one dose cannot hide another due dose. Additional doses remain available in the app; the face does not imply that its selected item is the only one.

SETUP displays “Set up” (or neutral launcher); EMPTY displays “No reminders”; UNAVAILABLE displays “Open app” rather than a cached due/recorded assertion. Their tap opens setup or the reminder overview as appropriate. Private rendering still takes precedence over these labels. Offline operation may use a valid local schedule and durable local records; loss of connectivity alone does not establish that data is stale. At the validity horizon, stop asserting status. Show last verified time and refresh/recovery in the app. Exact validity horizons must be supplied by the data producer; absent one, treat the snapshot as unavailable.

Precompute useful timeline boundaries: scheduled time, overdue time, recorded-window end, and validity expiry. Request refresh after schedule/account/record changes, subject to the platform's budget. Never promise per-second updates, exact wall-clock refresh, or guaranteed delivery. On activation, re-resolve current data so a delayed face entry cannot cause an incorrect action. Keep old IDs scoped to their account; an account change clears cached content. No names or clinical data in route strings or diagnostic logs. [Timeline guidance](https://developer.apple.com/design/human-interface-guidelines/complications#Best-practices) supports bounded updates; the selection and recovery rules above are product decisions.

## Companion destination boundary

Dose detail shows the full medication name, scheduled date/time, current state, and existing directions after access is permitted. Preserve selection across interruption. It must remain useful from local data without requiring the phone for every glance. Full directions and other reminders are deeper app content, never face content. Recording is an explicit app action against that occurrence; only a successful durable write produces RECORDED. Pending or failed writes retain the prior state with visible recovery feedback. Repeated activation must not create duplicate records. This contract does not redesign the existing recording controls, prescribe medication behavior, or introduce a health-data integration.

The detail layout uses semantic title/body roles, growing containers, and full-text reflow. Start with watchOS body conventions (16 pt general default in the local guide; device-specific system styles vary), rather than applying the general 12 pt minimum as a target. Preserve access at 140% text enlargement and supported larger sizes/Bold Text. The fixed face slot uses its family's type treatment and full-text destination rather than promising app-style reflow within a complication. [Accessibility guidance](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision) supplies the watchOS scaling qualification.

## Data-purpose boundary

| Data | Need and exposure |
|---|---|
| Occurrence ID, state, schedule, validity | Local selection and routing; opaque ID is not displayed |
| Medication name and directions | Detail screen only, after app access checks |
| Patient identifier | Excluded from complication payload; no new collection |
| Face status preference | Local preference; defaults to private |

Adding this face surface requests no new sensor, contact, location, or health-store permission. If an actual backend later requires protected access, request only its needed scope at the invoked feature; this document is not evidence of an existing permission flow or secure storage. See [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission).

## Worked before/after

Illustrative fixture, not a clinical timing recommendation: occurrence A is scheduled at 08:00 with a supplied overdue boundary of 08:30; no other dose is outstanding.

**Before:** The proposed face shows the full medication name and patient identifier above tiny directions, with a scrollable task list. These are observed proposal choices; exact text, dimensions, contrast, and recording mechanics were not supplied.

**After:** At 08:05 the default private rectangular slot reads “Reminder.” With active-face status explicitly enabled it reads “Dose due / 08:00.” A tap opens occurrence A's detail, where identity and directions are readable. Wrist down shows “Reminder” again. At 08:30 an eligible timeline entry changes the active status to “Dose overdue / 08:00”; delayed host delivery remains possible. At 08:32 a successful app recording changes it to “Dose recorded / 08:32.” A failed save does not. At 08:37 the next scheduled occurrence is selected, or “No reminders” appears. If another dose is already due, that dose is selected immediately after A is recorded. No part of this flow scrolls or records on the watch face.

## Acceptance checks and evidence limits

**Passed — specification inspection only:** all three supplied dose states have explicit representations; face identity/instructions and scrolling are removed; private and wrist-down variants, relevant tap destinations, placeholders, no-data and stale handling, bounded timelines, and a worked transition are specified. The root skill, selected family routes, topic procedures, and local guides were explicitly read. No web browsing was performed; official links above identify the local guides' sources, not newly verified pages.

**Failed — supplied proposal against this revised contract:** shared-visible identity disclosure, tiny multiline directions, and scrolling task-list behavior. These are textual design findings, not measured rendering defects.

**Not executed — implementation acceptance gates:**

- For every offered family, test due/overdue/recorded/upcoming, private, unavailable, empty, setup, and placeholder variants on each supported watch/face size. Long localized text must trigger the specified fallback without tiny type or clipping.
- Test tinted, full-color, active, Always On, locked, and system-redacted contexts. Status must survive tint without color dependence; private fields must never appear in images, spoken face labels, previews, or transitions.
- Exercise 140% watchOS text scaling, larger supported sizes, Bold Text, and Increase Contrast. Measure actual contrast with a calculator under the guide's stated table scope; no contrast values have been measured here. Confirm comfortable reading on a moving wrist.
- Verify that the whole complication is one accessible activation target, with a meaningful privacy-matched label and current status value, and that supported assistive input reaches the correct detail. Test the complete detail/record/recovery task on supported assistive technologies; no VoiceOver or accessibility execution is claimed.
- Inject delayed reloads, expired validity, offline operation, schedule edits, deleted IDs, account switches, simultaneous doses, failed writes, and duplicate taps. Check deterministic selection, current-route resolution, no cross-account disclosure, and no duplicate recording.
- Verify host family availability, font rendering, asset/placeholder bounds, timeline budgets, wrist transitions, and preservation of app context on supported hardware/runtime before release.

Only a short textual brief and dated installed HIG-derived guidance were available. OS deployment target, SDK/API availability, storage/security implementation, notification behavior, physical geometry, haptics, energy use, GUI behavior, and device accessibility remain unverified. No SDK, simulator, device, or GUI was executed. The local guide's disputed legacy sizing is unresolved and outside the selected modern-family design; this specification does not certify medical safety, security, or accessibility conformance.
