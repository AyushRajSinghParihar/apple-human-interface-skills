# Delivery Live Activity review

Decision: revise before implementation. The five findings below are verified against the written proposal in `interface.md`, not against a running interface. Ranking reflects privacy exposure and harm to delivery decisions, followed by lifecycle and scope. This is an iOS iPhone Lock Screen review; no framework or Apple SDK is assumed.

## Ranked findings and decisions

| Rank | Verified proposal | Effect and source-backed finding | Corrected behavior |
|---|---|---|---|
| 1 — High | Shows the customer’s full address on Lock Screen. | Exposes sensitive destination information to nearby people. Live Activities guidance says to avoid exposing sensitive content and summarize or redact it. | Omit the full address from every activity presentation and its display payload. Show “Your delivery”; open the corresponding order in the app for private destination details. |
| 2 — High | Labels a 40-minute-old estimate “Now.” | Presents an old prediction as current, misleading a person deciding whether to meet the courier. The topic procedure explicitly fails misleading status; the guide calls for immediately useful, changing information. | Show “Estimate unavailable · Updated 40 min ago”; retain the last confirmed delivery phase with its age. Never infer arrival from an elapsed estimate. |
| 3 — High | Starts automatically for promotional offers with no active delivery. | There is no bounded delivery task, and promotion is explicitly excluded from Live Activities. Automatic initiation itself is not the defect: expected automatic starts for followed events are allowed. | Start only for a real, active delivery at an expected moment, with an easy opt-out in that order’s app view. Keep offers outside this surface. |
| 4 — Medium | Keeps displaying “Delivered” forever. | An ended task must end immediately; indefinite retention defeats the bounded lifecycle. | End on confirmed delivery, remove from active presentations, and request a short Lock Screen completion summary, then removal. Choose 15 minutes as this product’s retention policy. |
| 5 — Medium | Puts a complete shopping catalog inside expanded content. | Displaces delivery status with nonessential app content. The guide calls for immediately useful information with details in the app. A catalog need not be advertising to be inappropriate here. | Expanded content shows delivery identity, confirmed phase, current estimate or stale-data explanation, and update age. Activity activation opens that order; catalog browsing remains in the app. |

Source for findings 1, 3, and 5: [Live Activities — Best practices](https://developer.apple.com/design/human-interface-guidelines/live-activities#Best-practices). Sources for finding 2: the installed Live Activities topic procedure and [Compact presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Compact-presentation). Source for finding 4 and expected initiation: [Starting, updating, and ending a Live Activity](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity). These are links supplied by local guidance; no website was accessed.

## Corrected contract

The following thresholds and wording are product decisions, not Apple-mandated values. Choose a conservative five-minute estimate freshness limit until the delivery service supplies a validated expiry. Honor any earlier service expiry. Do not promise a delivery update cadence that has not been established.

```text
state = absent | active | ended
input = orderId, eventVersion, confirmedPhase, observedAt,
        estimateWindow?, estimateObservedAt?, serviceValidUntil?, terminalAt?

on delivery event:
  accept only an event for this order with a newer authoritative version
  if confirmedPhase is delivered or cancelled:
    end activity immediately, once
    request safe final summary removal at terminalAt + 15 minutes
    discard later nonterminal events for this delivery
  else if delivery is active and tracking is allowed and not opted out:
    start at the expected order-tracking moment, or update changed content
  else:
    do not create an activity

render(now):
  never include address, catalog, offers, or other private order details
  if ended: show "Delivered" or "Delivery cancelled" with terminal time
  if active:
    show last confirmed phase and the age of that confirmation
    estimateExpiry = min(estimateObservedAt + 5 minutes,
                         serviceValidUntil if supplied)
    if estimate exists and now < estimateExpiry and window has not passed:
      show "Estimated arrival <window>" and estimate update age
    else:
      show "Estimate unavailable" and last estimate update age if known
  never map an expired estimate to "Now" or "Delivered"
  if timestamps are absent or invalid: show "Update time unavailable"

on activation:
  open corresponding order tracking in app, subject to normal access controls
on opt-out in order view:
  end activity and suppress automatic restart for this delivery
```

Recompute freshness when time crosses the expiry even without another delivery event. The eventual implementation must arrange supported expiry/rendering behavior; this pseudocode alone does not prove that a remotely displayed estimate will change on time. If expiry cannot be reliably represented, omit the estimate rather than retain a claim of current arrival. On termination, request the end and removal immediately even if an event arrives late; do not start a new 15-minute window from late receipt. System dismissal can remove the summary earlier.

Update only changed information. Alert only for crucial changes, such as a confirmed arrival requiring attention; do not send a duplicate push for the same update. Backend event delivery, ordering, and terminal signals remain implementation dependencies.

### Presentation and destination decisions

| Presentation | Essential content and behavior |
|---|---|
| Lock Screen | “Your delivery,” last confirmed phase, estimate or freshness explanation. Brief completion summary after ending. Distinct task layout; standard 14 pt margins from the local guide, adjusting only for justified grouping. |
| Expanded | Same identity and relative positions as smaller presentations, with room for update ages. No catalog. |
| Compact | Delivery symbol/identity and short changing estimate or stale-status indicator. Both halves open the same order. |
| Minimal / multiple activities | Recognizable delivery symbol plus meaningful current state, such as a stale indicator; never a static logo alone. |

No explicit buttons, toggles, catalog controls, or interaction mechanics were supplied, so none can be declared defective. Use the activity’s relevant-order deep link; no new direct-action control is necessary for this correction. These compact/minimal provisions cover related iPhone presentations without claiming rendered support.

For eventual destination coverage, check StandBy scaling and red Night Mode, watch status, and CarPlay status with controls disabled; paired Mac activation follows the local guide’s iPhone Mirroring model. No separate destination implementation is claimed here. Sources: [Presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Presentation), [Offering interactivity](https://developer.apple.com/design/human-interface-guidelines/live-activities#Offering-interactivity), and [CarPlay](https://developer.apple.com/design/human-interface-guidelines/live-activities#CarPlay).

### Data-purpose and privacy decisions

| Data | Purpose | Activity exposure |
|---|---|---|
| Internal order identifier | Route to the correct order and reject unrelated events | Routing metadata; no customer-identifying display required |
| Phase, estimate, observation time | Delivery progress and truthful freshness | Show only necessary status |
| Full address | Fulfillment and private order details | Exclude from activity display payload; access within the app |
| Catalog and promotional offers | Shopping | Exclude from activity |

No extra permission request is specified: the brief supplies no collection or authorization flow to audit. Retain existing authorized fulfillment data handling; this review does not establish that consent, storage, transfers, authentication, or privacy disclosures are correct. Data minimization is supported by [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices); Lock Screen exposure is addressed directly by Live Activities guidance.

## Worked before/after

Illustrative fixture, not production data: at 12:40 a delivery remains last confirmed “On the way.” Its estimate was observed at 12:00 and predicted 12:05–12:15.

| Moment | Proposed behavior | Corrected behavior |
|---|---|---|
| Promotional offer, no delivery | Activity starts. | No activity. Offer stays outside the delivery surface. |
| Active delivery at 12:40 | Full address, “Now,” expanded catalog. | “Your delivery · On the way (last confirmed 40 min ago) · Estimate unavailable · Estimate updated 40 min ago.” No address or catalog. Activation opens this order. |
| Authoritative delivery event at 12:43 | “Delivered” persists forever. | End at 12:43. Lock Screen may retain “Delivered at 12:43” until requested removal at 12:58; active Dynamic Island presentation is removed. |
| Late “On the way” event after 12:43 | Unspecified. | Ignore older/nonterminal event; do not reopen the completed activity. |

## Acceptance checks and evidence status

**Passed — static audit only:** read the supplied proposal; identified five explicit behaviors and tied each to a correction; corrected specification excludes private destination text and shopping content and defines freshness, termination, and relevant-order routing. The worked example satisfies the written contract by inspection. No pseudocode was executed.

**Failed — supplied proposal by textual inspection:** all five ranked findings. These are specification failures, not observed runtime failures.

**Not executed — implementation acceptance checks:**

- A promotion without an active delivery creates nothing; an expected active-delivery start honors opt-out. Repeated events do not create duplicate activities or restart opted-out tracking.
- A fresh estimate is labeled estimated; at the earlier expiry boundary it becomes unavailable. At 40 minutes old it never says “Now.” Missing times, passed windows, loss of updates, and invalid timestamps cannot produce false arrival or completion.
- Confirmed delivery/cancellation ends immediately. A summary requests removal at terminal time plus 15 minutes, including late terminal events. Older updates cannot reverse completion.
- Every presentation excludes the full address, catalog, and offers; relevant-order activation respects app access controls. Inspect payloads and redacted states, including account changes.
- Changed-content updates and crucial alerts avoid duplicate push alerts; verify actual delivery and offline/reconnection behavior.
- Render on representative iPhones with and without Dynamic Island, multiple activities, long/localized text, and larger text settings. Check clipping, identity continuity, and meaningful minimal content. Test light/dark wallpaper contrast, Always On including dismiss control, and StandBy red mode. No contrast, typography, accessibility, or geometry defect is inferred from this text-only brief.
- Where destinations are delivered, verify watch/CarPlay status without required controls and paired Mac routing. Device, native rendering, assistive-technology behavior, SDK compilation, and server update delivery require actual execution evidence.

## Evidence limits and route record

Only `interface.md` and installed instructions/guides were used. No screenshots, source implementation, device, GUI, SDK, backend trace, or accessibility execution was available. The proposal omits actual update sources, timestamps, opt-out behavior, supported device/OS matrix, layouts, permission flow, and service guarantees. These omissions are open implementation questions, not additional verified violations.

Read sequence: installed `apple-hig/SKILL.md`; System experiences family; relevant rows of `references/topic-index.md`; Live Activities topic procedure; Foundations family; Privacy topic procedure; then the Live Activities and Privacy source guides. All paths resolved under `.agents/skills/apple-hig/`; each file was read with a separate `cat` or `rg` command. This routes the lifecycle, surface, and explicit privacy concerns without treating collection-permission guidance as proof of a Lock Screen authorization defect.

The installed guides identify a 2026-10-25 snapshot/retrieval date and are independent, derived guidance. Official links above are attribution, not live verification. No source conflict was encountered. The local guide says “ideally no more than 8 hours,” allows up to four hours of retained completion on specified surfaces, and recommends a shorter useful summary, commonly 15–30 minutes. These qualifications do not authorize indefinite display; this design selects 15 minutes without inventing an SDK limit or universal HIG requirement.
