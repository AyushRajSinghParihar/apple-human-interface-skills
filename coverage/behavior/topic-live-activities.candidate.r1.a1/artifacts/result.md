# Delivery Live Activity review

Reviewed `interface.md` as an iOS iPhone Lock Screen proposal. Decision: revise before implementation. All five findings below are verified against the supplied text; severity ranks are review judgments, not Apple classifications. No rendered interface or executable implementation was supplied.

## Ranked findings and decisions

| Rank | Observed evidence | Effect and source-backed decision | Corrected behavior |
|---|---|---|---|
| 1 — High | “shows the customer’s full address on Lock Screen” | Exposes personal destination information on a glanceable surface. Live Activities guidance says to avoid exposed sensitive content and summarize or redact. | Omit the address from the activity payload and every presentation. Show “Your delivery”; open the relevant order in the app for destination details, subject to the app’s authentication policy. |
| 2 — High | “starts automatically for promotional offers with no active delivery” | Has no bounded live task and uses the surface for promotion. Automatic initiation itself is not the defect: expected automatic starts for followed events are permitted. | Create an activity only for a real, active delivery the person expects to track, with an easy opt-out in that order’s app view. Keep offers in the app. |
| 3 — High | “labels a 40-minute-old estimate Now” | Misrepresents old information as current and undermines the central tracking task. The topic procedure explicitly fails misleading status; the guide requires immediately useful changing information. | Track estimate observation time and validity separately from arrival time. For this stale sample show “Arrival estimate unavailable · Last update 40 min ago.” Never infer arrival or delivery from elapsed time. |
| 4 — Medium | “keeps displaying Delivered forever” | Leaves an unbounded activity after the task ends. Guidance says end immediately; retained Lock Screen summaries are distinct from active tracking. | End on a confirmed terminal event. Request a short retained “Delivered” summary for 15 minutes, then removal. System/user removal may happen earlier; indefinite retention is disallowed. |
| 5 — Medium | “puts a complete shopping catalog inside expanded content” | Crowds out delivery progress and turns a glanceable task surface into an app screen. Guidance says show immediately useful information and keep details in the app. | Expanded content contains delivery identity, confirmed phase, trustworthy estimate or freshness fallback, and a relevant order deep link. Shopping stays in the app. |

Sources for ranks 1, 2, and 5: [Live Activities — Best practices](https://developer.apple.com/design/human-interface-guidelines/live-activities#Best-practices). Rank 3 also applies the installed Live Activities topic procedure’s misleading-status check and [Presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Presentation). Rank 4 and initiation/update decisions: [Starting, updating, and ending a Live Activity](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity). Data minimization is also supported by [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices).

## Framework-agnostic corrected contract

The following timing and copy choices are product decisions: a 5-minute estimate freshness budget and a 15-minute retained terminal summary. They are not mandatory HIG constants. Validate the freshness budget with the delivery data provider. The local guide recommends a shorter useful retained summary, commonly 15–30 minutes, within the system’s stated maximum of 4 hours; it describes bounded tasks ideally no longer than 8 hours, not an invented universal runtime guarantee.

```text
Inputs:
  deliveryId, accountId, expectedTracking, trackingAllowed
  event { revision, observedAt, phase, estimateWindow?, estimateValidUntil? }
  phase = preparing | enRoute | delivered | cancelled

Public presentation model:
  safeDeliveryLabel, confirmedPhase, estimateWindow?, observedAt,
  estimateValidUntil?, orderDestination
  // No street address, unit, access code, customer name, or catalog.

Start:
  if real delivery is active AND expectedTracking AND trackingAllowed:
    create one activity associated with this delivery
  otherwise: do not create
  promotions never create or update an activity

Receive event:
  verify association with delivery/account
  reject older or duplicate revisions
  accept confirmed phase from authoritative delivery events
  if delivered OR cancelled:
    publish safe terminal summary
    end active tracking immediately
    request retained summary expiry = terminal receipt time + 15 minutes
    reject later nonterminal events for this completed delivery
  else:
    update only changed content

Render estimate at current time:
  fresh = estimate exists
          AND 0 <= now - observedAt <= 5 minutes
          AND (estimateValidUntil absent OR now < estimateValidUntil)
  if fresh: show absolute arrival window and update age
  else: show "Arrival estimate unavailable" and last-update age
  missing or invalid timestamp: show "Update time unavailable"
  never show "Now" solely because an estimate time has passed

Navigation and exit:
  activity activation -> app's matching order details
  order view -> easy tracking opt-out
  opt-out -> end activity without a retained summary
  account change -> remove previous account's activity
  dismissal does not cancel the delivery or automatically recreate tracking
```

The data source must emit real phase changes, including terminal events. A timer cannot establish delivery. Estimate expiry needs a platform-supported stale-state mechanism or scheduled update strategy; unavailable delivery must produce conservative fallback content. This document does not establish that background updates or removal will execute reliably. On reconnect, reconcile the authoritative order state before presenting a fresh estimate. Terminal states cannot be reversed by a late en-route update.

Alert only for crucial changes, for example confirmed arrival when useful to receive the order. Do not also send a push for the same information. No alerts for unchanged data or estimate aging. This example is a product policy under [Live Activities lifecycle guidance](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity).

### Presentation and data decisions

| Surface/context | Required content and behavior |
|---|---|
| Lock Screen | “Your delivery,” confirmed phase, fresh arrival window or explicit stale fallback. Terminal summary replaces tracking after completion. Use only necessary height, standard 14 pt margins unless grouping justifies tighter spacing, and legible text generally medium weight or stronger. |
| Expanded | Preserve identity and relative status positions from compact; add freshness detail. No catalog. |
| Compact | Coherent leading delivery identity/phase and trailing fresh estimate or stale indicator; both halves open the same order. |
| Minimal / multiple activities | Recognizable delivery symbol plus changing phase or stale indicator; not a static logo alone. Distinguish simultaneous orders with safe labels when necessary. |
| Always On / appearances | Same privacy-safe content; verify foreground, background, and dismiss-control contrast in light, dark, and reduced luminance. Do not depend on animation to communicate status. |
| StandBy / propagated destinations | Verify scaled layout, margins and red Night Mode. Preserve essential status without controls for CarPlay; paired watch/Mac behavior needs separate execution checks if supported by the implementation. |

These are specifications, not verified layouts. See [Presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Presentation), [Lock Screen presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Lock-Screen-presentation), and [CarPlay](https://developer.apple.com/design/human-interface-guidelines/live-activities#CarPlay). The local guide’s sample iPhone Lock Screen sizes are 408×84–160 pt for a 430×932 pt screen and 371×84–160 pt for a 393×852 pt screen; these are contextual design guidance, not universal fixed dimensions.

No buttons, toggles, or other explicit controls are supplied in `interface.md`, so no existing control semantics or target sizes can be audited. The proposed activation destination is a deep link, not a new direct-action button. If a direct action is later added, review its owning component procedure; the guide favors one essential button or toggle rather than filling expanded content with controls: [Offering interactivity](https://developer.apple.com/design/human-interface-guidelines/live-activities#Offering-interactivity).

| Data | Purpose / exposure decision |
|---|---|
| Full destination address | Needed for fulfillment and order details; excluded from public activity content. No conclusion about existing collection, storage, or permissions is possible. |
| Phase, estimate, observation time | Minimum tracking information; display with explicit freshness semantics. |
| Internal order/account identifiers | Associate events and route to the correct order; do not render publicly. |
| Catalog and offers | No delivery-progress purpose; excluded from activity. |

No new location or other permission request is specified. Whether any permission flow needs revision is unknown because none was supplied.

## Worked before/after

Illustrative clock times below make the supplied 40-minute age concrete; they are not additional observations.

| Moment | Before from proposal | After under this contract |
|---|---|---|
| Offer received; no delivery | Promotional activity starts automatically. | No activity is created. Offer remains in app. |
| 13:55, actual order active | Full address appears publicly; expanded catalog is available. | “Your delivery · On the way · Estimated 14:20–14:30 · Updated just now.” Activation opens this order. |
| 14:35, no update since 13:55 | Estimate is labeled “Now.” | “Your delivery · On the way · Arrival estimate unavailable · Last update 40 min ago.” Phase is the last confirmed phase, not proof of current courier position. |
| 14:42, authoritative delivered event | “Delivered” remains forever. | End active tracking immediately; request safe “Delivered at 14:42” Lock Screen summary until 14:57. Dynamic Island removes the ended activity. |
| 14:57 | Still “Delivered.” | No retained activity requested; historical details remain in the order view. |

## Acceptance checks and current status

**Passed — static review only:** inspected all supplied interface text; tied each of its five claims to a ranked correction; read installed root → system-experiences family → Live Activities topic → guide, plus foundations → Privacy topic → guide; searched the topic index before finalizing routing. Corrected contract specifies start, freshness, terminal events, removal, destinations, privacy, and relevant presentations.

**Failed — supplied proposal by textual inspection:** all five ranked requirements: appropriate nonpromotional start, safe public content, truthful freshness, bounded completion, and task-focused expanded content. “Verified” means explicitly stated in the proposal, not observed on a device.

**Not executed — implementation acceptance:**

- No delivery + offer event creates zero activities; expected active delivery creates one; opt-out prevents recreation.
- Serialization and every presentation contain no full address or other excluded sensitive values, including when locked or Always On.
- A 40-minute-old estimate uses stale fallback; test missing timestamps, clock skew, expiration, reconnection, and late/duplicate revisions. Aging must invalidate the display without a new server event.
- A delivered/cancelled event ends active tracking immediately; retained summary expires under the chosen policy; late nonterminal events cannot revive it. Test user dismissal and account switching.
- Expanded content has only delivery essentials; compact halves open the same order; minimal remains informative with competing activities.
- Only changed content updates; crucial alerts have no duplicate push. Verify real event delivery and termination during app inactivity/network loss.
- Preview representative iPhone sizes, long localized labels, enlarged text, light/dark wallpaper, Always On and dismiss-control contrast; check reading order and meaningful spoken status with assistive technology. Check StandBy red mode and any propagated destinations. These are unresolved checks, not verified defects.

## Evidence limits

Only `interface.md` and installed local guidance were used; no web browsing occurred. Official links identify the source guidance and were not fetched. The local Live Activities guide records a 2026-10-25 snapshot; Privacy records retrieval on that date. Installed guidance is an independently authored HIG snapshot, not an SDK reference or proof of current API availability. No source conflict relevant to these decisions was found in the read passages.

There is no screenshot, layout, payload, backend event stream, SDK, build, GUI, device, or accessibility execution evidence. Therefore this audit cannot establish contrast, clipping, actual background delivery, dismissal timing, API feasibility, or assistive-technology behavior. The corrected artifact is a reviewable specification; it is not a tested implementation or security/privacy certification.
