# Pickup summary and delivery tracking design

Design specification based on `interface.md` and the installed local apple-hig snapshot, dated 2026-10-25. No web sources were fetched. Official links below identify the source guidance, not independently verified current API availability.

## Result and corrections

Use a household-safe periodic pickup widget and a personal Live Activity for the bounded 80-minute delivery. On Watch, choose the delivery Live Activity in Smart Stack for active tracking; offer an optional pickup complication for recurring pickup checks. These answer different questions and do not require the person to install both.

The supplied proposal fails three static design checks: every-second widget refresh assumes an unavailable continuous refresh budget; the shared face exposes an address and access secret; and an inline accessory draws three independent targets despite having one target. Replace them as specified below. The supplied last update is 35 minutes old: current status, pickup readiness, ETA and connectivity are unknown. Do not invent them.

The shared Apple HomeView Modular face is a household surface, distinct from an Apple Watch Modular watch face. The local widgets guide explicitly supports system-small widgets on HomeView; this is snapshot support, with shipping device/OS and SDK availability still to verify. [Widgets: Apple HomeView](https://developer.apple.com/design/human-interface-guidelines/widgets#Apple-HomeView)

## Household pickup widget

Glance question: “Does this household have a pickup to handle?” This is periodic summary information, not an animated delivery tracker.

| Surface / family | Concrete hierarchy | Activation |
|---|---|---|
| iPhone Home Screen / system small | `Household pickups`; large confirmed ready count or `Status unavailable`; freshness line | Open household pickup list filtered to the configured household |
| Shared HomeView Modular / system small | Same hierarchy, larger glanceable count; removable background; no person-specific detail | Open the safe household pickup summary in the available app context; never launch directly into private parcel details |
| iPhone Lock Screen / accessory inline | `Pickups: check status` for supplied stale data; `Pickups: 1 ready` only after confirmation | One whole-widget target to the household pickup list; remove Accept, Cancel and Details drawings |

An illustrative confirmed-data small layout is:

```
Household pickups
1 ready
Updated 2 min ago
```

For the actual supplied data, show:

```
Household pickups
Check status
Updated 35 min ago
```

“1 ready” is simulated preview data only. A parcel record alone is not evidence of readiness. Do not display a numeric zero without a successful, complete empty response. Use the inline label `Pickups: check status` when space cannot fit age; the destination must prominently show the last-confirmed time. Consider an optional rectangular Lock Screen variant only if user testing demonstrates that age needs to be readable before tapping; it is not required for this release.

Configure household explicitly. Before enabling shared display, explain: “Show pickup counts to everyone in this household. Names, addresses and access codes stay private.” Sharing is off until the account owner chooses it. Without configured sharing, show `Set up household pickups`, with a setup destination. Do not automatically reuse the connected phone owner's private parcel feed. Gallery description: `Check household pickups.` Use explicitly simulated safe preview content and static skeleton placeholders; never use real secrets as preview data. [Widgets: purpose, interaction, previews](https://developer.apple.com/design/human-interface-guidelines/widgets#Best-practices)

## Private delivery Live Activity

Glance question: “What is happening with my current delivery?” The 80-minute event fits a bounded activity, with meaningful state changes rather than per-second widget polling. It belongs to the signed-in recipient's personal devices; never publish it to the household widget feed. “Private” means personal account scope and minimized out-of-app content, not a guarantee that a visible screen is secret. [Live Activities: best practices](https://developer.apple.com/design/human-interface-guidelines/live-activities#Best-practices)

| Presentation | Fresh confirmed example (simulated) | Supplied 35-minute-old data |
|---|---|---|
| Lock Screen | `Delivery` / `On the way` / `Expected 14:20–14:35` / `Updated 2 min ago` | `Delivery` / `Update delayed` / `Last update 35 min ago` / `Open for details` |
| Expanded Dynamic Island | Parcel glyph leading, status central, estimate trailing; freshness below | Same identity and relative positions; `Update delayed`, last-confirmed time; omit ETA |
| Compact | Parcel glyph plus motion/status badge leading; short confirmed estimate trailing | Parcel glyph with warning badge leading; `Old` trailing; accessible text says update delayed |
| Minimal / competing activities | Parcel glyph with meaningful changing status badge; no static logo alone | Parcel glyph plus warning badge; tap opens this delivery |
| Watch Smart Stack | `Delivery` / `On the way · 14:20–14:35` / freshness where space permits | `Delivery` / `Update delayed` / `35 min since update` |

Both compact halves and the entire other presentations open the exact delivery detail, preserving its identifier through authentication and interruption. Expanded and Lock Screen include one clearly labeled `Details` link. No Accept or Cancel action is justified by this brief. Those terms have unspecified business consequences; keep any future transactional action in the authenticated app until its semantics and confirmation/recovery behavior are defined. No controls are needed for tracking.

Do not compute a delivery percentage from elapsed time or count down an old ETA. Retain an explicitly labeled last-known stage in app detail if one exists. The supplied record does not establish a stage or estimated arrival.

Start when the server confirms delivery has begun for a followed parcel, or when the user enables tracking for an already active delivery. Offer “Stop showing live tracking” in that delivery's app view; stopping display does not cancel delivery. If Live Activities are disabled or unsupported, tracking remains available in app detail and periodic safe widgets; do not repeatedly solicit authorization.

Lifecycle: `not started → active → delivered / cancelled / failed → ended`. Freshness and connectivity are independent flags on active state. End immediately on a confirmed terminal event; remove Dynamic Island presence and retain a safe `Delivered`, `Cancelled`, or `Delivery ended` summary for 15 minutes where the system permits retained content, then dismiss. A person dismissing the activity does not alter the logistics event. Do not restart a dismissed activity on routine updates.

The stated 80 minutes is expected duration, not proof of completion. At start, record an absolute tracking cutoff of start + 120 minutes (product choice: 40-minute delay allowance). At cutoff, end with `Tracking ended · Check delivery` if no terminal signal arrived; never declare delivery complete merely because time elapsed. App detail continues tracking. An explicit resumed tracking session requires a newly confirmed bounded window. Actual termination delivery under suspended/offline conditions requires implementation evidence; an absolute freshness deadline must prevent retained old content looking live. Updates use changed server state or revised ETA, not a polling animation. Only a crucial arrival/terminal update may alert; avoid duplicate notification alerts. [Live Activities: lifecycle and presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity)

## Freshness, offline and account contract

These thresholds are proposed product rules, not Apple refresh guarantees. Record server observation time separately from device receipt time; receiving an old cached response must not reset freshness. Use server version/event sequence to reject out-of-order updates and prevent resurrection after terminal events.

| State | Widget | Delivery activity / recovery |
|---|---|---|
| Fresh | Successful complete summary, observed within 15 min | Last observation within 5 min: show confirmed stage and still-valid estimate |
| Refresh in progress | Keep available content and its timestamp | Keep content; never substitute an indefinite spinner |
| Stale | Older than 15 min: `Check status`, last-confirmed age; suppress authoritative ready count | Older than 5 min or estimate expired: `Update delayed`, last-confirmed age; suppress ETA/countdown |
| Known offline | `Offline · Check status`, age if available | `Offline · Last update …`; reconnect and fetch newest version before restoring live claims |
| No cached data | `Status unavailable`; tap for retry in app | `Status unavailable`; no invented stage or estimate |
| Confirmed empty | `No pickups ready`, freshness | No active event means no new activity |
| Signed out / access revoked | Clear personal cache; `Sign in to check pickups` or household setup as applicable | End personal activity and remove sensitive retained content immediately; authenticate before restoring detail |

Thirty-five minutes old means stale on both surfaces. It does not prove offline: use `Update delayed` unless connectivity failure is actually known. Schedule meaningful timeline entries at stale boundaries and expected pickup changes; request reloads after confirmed changes within system budgets. System-controlled refresh can be late. Use platform date/time rendering for age, and preplanned expiry/stale states rather than claiming every-second network refresh. Validate this degradation under real suspension. [Widgets: updating content](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content)

## Privacy and presentation

| Data | Purpose and exposure policy |
|---|---|
| Household counts and readiness | Explicitly shared aggregate feed; contains only opted-in household items |
| Recipient name and full destination | Authenticated parcel detail only; omit from all specified glance payloads |
| Gate code | Reveal only through an explicit authenticated app action for an authorized parcel; exclude from widget/activity payloads, previews, deep-link URLs, logs and shared caches |
| Event ID, stage, observation time, ETA | Personal activity payload with opaque routing ID; shared widget gets only aggregate data |

Do not repeat the supplied secret in this artifact. No location, contacts or tracking permission is needed merely to display server delivery state. Additional permissions require a demonstrated feature need at the point of use. Store access secrets using established protected storage; account authorization must be checked at the destination, not inferred from possession of a link. On a shared HomeView, private-detail navigation must require the owner's authenticated personal context; otherwise remain in the safe summary. [Privacy: minimization and protecting data](https://developer.apple.com/design/human-interface-guidelines/privacy#Protecting-data)

Use system text styles, real text and status symbols with labels; no color-only ready/stale distinction. Full-color mode uses semantic foregrounds; accented mode keeps count/status primary and supporting glyphs accented. Vibrant mode uses grayscale brightness hierarchy rather than just reduced white opacity. Test light/dark, Home Screen tint/clear, removable HomeView background, and HomeView/StandBy red Night Mode. Dynamic Island backgrounds remain system-controlled; any custom background is confined to Lock Screen. StandBy scales the activity layout without adding private details. If mirrored to CarPlay, show the same status without dependence on controls; Mac activation follows system iPhone Mirroring behavior. [Widgets: rendering](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes), [Live Activities: destinations](https://developer.apple.com/design/human-interface-guidelines/live-activities#Presentation)

Always On/wrist-down keeps the safe status and stale cue in stable positions, dims secondary detail, and uses no continuous animation; wrist raise restores the same delivery context. No address or secret becomes visible merely because the device is active. Protect private fields even if redaction fails by omitting them from glance data. Always On hardware support is device-specific. [Always On](https://developer.apple.com/design/human-interface-guidelines/always-on#Best-practices)

## Watch surface decision

| Concern | Watch-face complication | Delivery Live Activity in Smart Stack |
|---|---|---|
| Task fit | Recurring question at wrist raise: “Any pickups ready?” Uses a face slot the person chooses | Temporary, changing 80-minute delivery; timely appearance without dedicating a permanent face slot |
| Freshness | Budgeted timeline and reloads; never a second-by-second tracker | Event updates with explicit stale/offline fallback; push transport still cannot guarantee freshness |
| Privacy | Safe count only, including Always On; no identity, address or code | Personal delivery scope, but visible to bystanders; safe stage/age only |
| Ending | Slot persists: return to confirmed `No pickups` or stale `Check status`, never an old delivery ETA | End on terminal signal or bounded tracking cutoff; 15-minute safe retained summary where allowed |
| Tap | Watch household pickup list, carrying selected household | Watch delivery detail for that exact event when app exists; otherwise system full-screen activity with paired-iPhone launch button |

Choose Smart Stack Live Activity as the primary delivery glance. Offer the pickup complication only as an optional persistent entrypoint. Do not force face customization for a one-off event or create a second permanent delivery widget duplicating the same tracking state. [Complications](https://developer.apple.com/design/human-interface-guidelines/complications#Best-practices), [Live Activities: watchOS](https://developer.apple.com/design/human-interface-guidelines/live-activities#watchOS)

For the optional complication, ship a modern WidgetKit accessory rectangular design: `Pickups` / `1 ready · Updated 2 min ago`; stale variant `Pickups` / `Check status`. Inline uses `Pickups: 1 ready` or `Pickups: check status` with one destination. Defer circular/corner until useful count plus stale meaning fits without ambiguity; do not substitute a misleading live ETA or progress ring. Use separate static placeholders, no arbitrary legacy template dimensions, and verify tint/Always On. The shared HomeView widget is system small, not this complication. Watch detail should be independently useful: safe current state, last-confirmed time and retry; continue protected address/code access on iPhone. Preserve context through wrist lowering. [Designing for watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices)

## Acceptance checks and evidence

Passed by static design inspection: the contract separates household and personal feeds; removes secrets from glance content; replaces continuous widget polling; defines one inline target; compares Watch surfaces before choosing; covers stale/offline/empty/account states and bounded ending. These are specification checks, not implementation results.

Failed in supplied proposal: shared address/code exposure, every-second refresh promise, and three inline targets. This document corrects the design; no supplied implementation proves those defects are fixed at runtime.

Not executed — acceptance scenarios for implementation:

1. Feed the supplied 35-minute-old record: both surfaces show stale wording, no live ETA/countdown/readiness assertion, and no offline claim without connectivity evidence. Reconnection with an old version leaves it stale; a newer valid observation restores confirmed content.
2. Advance through freshness deadlines without foreground execution; interrupt network, phone pairing and update transport. Verify cached content remains useful and stale cues appear; test future/invalid timestamps conservatively as unknown. Confirm system scheduling limitations do not turn expired data into a live promise.
3. Test active, delivered, cancelled, failed, dismissed, cutoff and sign-out paths; confirm terminal events cannot be reversed by delayed updates. Verify removal versus 15-minute retained summaries separately on iPhone and Watch. Check no duplicate alert.
4. Inspect payloads, logs, snapshots, gallery previews and household feeds for identity/address/secret leakage; revoke sharing and account access. Test household members and guests, not just the owner account.
5. Follow every tap to its exact household/event, through locked/signed-out states, then resume after interruption. Verify inline has one target and no fake buttons. Test Watch app installed/absent, disconnected Watch, unsupported Live Activities, no Dynamic Island, and multiple simultaneous activities.
6. Render all selected families with long localized text and large counts. Preserve status and freshness before secondary detail; no shrinking essential text to fit. Test iPhone Dynamic Type through AX5 and at least 200% text enlargement, Watch at 140%, portrait/landscape app destinations, and supported small/large Watch sizes. Verify system margins and measured activation areas; start from 44 × 44 pt controls in iPhone/Watch app detail.
7. Measure actual contrast in light/dark, tinted/clear, vibrant grayscale, red Night Mode and Always On; verify status without color. Check VoiceOver names and order, Switch Control activation and relevant alternative input. No information may require hearing, color or timed reactions. [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

Missing evidence: project implementation and framework; minimum OS/device targets; shipping HomeView capabilities and destination routing; ActivityKit/WidgetKit SDK availability and compilation; server event/ETA/readiness semantics, sharing authorization model, update cadence and terminal-event reliability; real layout previews and measured contrast; physical Watch readability; native deep links, system scheduling, redaction, accessibility and lifecycle tests. Product owners must validate the proposed 5/15-minute freshness thresholds, 120-minute tracking cutoff and sharing copy. No device, SDK, GUI, energy, security certification or accessibility execution is claimed.

## Local audit route

Read the installed root `apple-hig/SKILL.md`, `interface.md`, and relevant topic-index rows. Then read each selected family and its routed topic procedure before its source guide, using one file per shell command. Package root: `/tmp/hig-eval-7q62nput/.agents/skills/apple-hig`.

- Getting started → Designing for iOS; Designing for watchOS → corresponding local reference guides.
- System experiences → Widgets; Live Activities; Complications → corresponding local reference guides, including surface/family and Watch support sections.
- Foundations → Privacy; Accessibility → corresponding local reference guides.
- Technologies → Always On → corresponding local reference guide.

No newer-release verification was attempted because the task explicitly limits evidence to supplied local files and installed instructions. No screenshot or animation was supplied, so media-specific routing was unnecessary.
