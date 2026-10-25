# Pickup summary and delivery activity design

Design specification based on `interface.md` and the installed apple-hig package, read locally on 2026-10-25. No web access, implementation, SDK validation, simulator, GUI, device, or assistive-technology execution was performed. Official links below identify the sources represented by the local snapshot; they were not fetched.

## Concrete result

Use a periodic, household-safe **Pickup summary** widget and a separate, personal **Delivery** Live Activity for the bounded 80-minute delivery. Choose the delivery Live Activity in the paired Watch Smart Stack for the temporary wrist glance. Offer an optional watch-face complication only for recurring pickup needs.

The supplied parcel belongs to Sam at 14 Willow Road with gate code 9182. Treat the recipient, address, and especially gate code as private. None appears on the household widget, face configuration, gallery preview, Live Activity payload, or complication. Authenticated parcel detail is the destination for those values. “Private” means a personal activity with minimized data; a Lock Screen or wrist display is still observable by others.

The brief does not establish that this parcel is ready for pickup, its current delivery stage, or its ETA. Do not invent those facts. The supplied 35-minute-old server update is stale under the proposed policy below. Counts, stages, and times in examples other than that age are simulated test fixtures.

## Household pickup widget

Glance question: **“Is there a household pickup that needs attention?”**

| Surface/family | Content and hierarchy | Activation |
|---|---|---|
| iPhone Home Screen, system small | `Household pickups`; large confirmed ready count when fresh; `Ready for pickup`; freshness line | Entire widget opens the selected household pickup list |
| Apple HomeView shared Modular face, system small | Same summary, enlarged count/status, shorter secondary text, removable background | Opens household summary through the host’s supported destination mechanism; verify handoff, never promise a native iPhone app launch on HomeView |
| iPhone Lock Screen, accessory rectangular | `Pickups`; count plus `ready` when fresh; freshness/status beneath | Opens household pickup list after system unlock if needed |
| iPhone Lock Screen, accessory inline | One line, e.g. `Pickups: update needed` | **One target**, opening household pickup list |

For the supplied stale fixture, the small layout reads:

> Household pickups  
> Update needed  
> Last checked 35 min ago

If a cached ready count exists, show it only as secondary `Last known: 1 ready`, never as the large current headline. Rectangular: `Pickups · Update needed / Checked 35 min ago`. Inline: `Pickups: update needed`. Do not show Accept, Cancel, and Details as independent inline controls. All actions requiring personal authorization happen in app detail. This informational version has no in-place buttons.

Configuration: select a household and explicitly enable “Share pickup summary with household.” Explain: “People in this household can see pickup counts and status. Names, addresses, and codes stay private.” Default to unconfigured until the scope is selected; personal-only parcels never contribute. Membership and sharing eligibility must be enforced in the data projection, not just visually hidden. Revocation purges cached shared records and requests a reload; system scheduling means removal latency needs testing. Warn in configuration that already displayed summaries can persist until refreshed. A personalized HomeView Home Screen and the shared Modular face are different privacy contexts; do not infer personal visibility on the shared face.

This follows the local [Widgets guidance on updating, interaction, and Apple HomeView](https://developer.apple.com/design/human-interface-guidelines/widgets#Platform-considerations): small widgets are supported on HomeView; the shared Modular face can expose one person’s data to the household. HomeView Modular is not an Apple Watch face. Sharing a configured Watch face does not make it a shared household data display ([Watch faces](https://developer.apple.com/design/human-interface-guidelines/watch-faces)).

## Freshness and unavailable-data contract

The following thresholds are **product decisions**, not Apple refresh guarantees. Store source observation time separately from local receipt time, known connectivity, and rendering time. A successful cache read does not reset source freshness. Reject older event revisions; invalid or future source times yield `Update needed`.

| Condition | Pickup summary | Delivery activity |
|---|---|---|
| Fresh | Source age ≤15 min: confirmed count/status and last checked time | Source age ≤5 min: confirmed stage and an ETA window only if supplied by source |
| Stale | Age >15 min: `Update needed`; last checked time; cached count explicitly last known | Age >5 min: `Delivery · Update needed`; `Last update 35 min ago` for supplied fixture; stage prefixed `Last known`; remove ETA/countdown |
| Known offline | `Offline · Last checked 35 min ago`, with optional last-known count | `Offline · Last update 35 min ago`; last-known stage only; no moving courier, inferred progress, or ETA countdown |
| No cache / first load | `Checking pickups…`, then `Pickup information unavailable` if retrieval fails | Do not start an empty activity; show unavailable state in app. An existing activity with unusable data says `Delivery status unavailable` |
| Refresh in progress | Retain cached information and its age | Retain last known state and age; no optimistic stage advance |
| Signed out / scope removed | `Open app to set up pickups`; no prior account content | End personal activity and clear private caches; app destination requests sign-in |
| Confirmed empty | `No pickups ready`, with freshness line | No active event: no Live Activity |

Offline is shown only when connectivity failure is known; silence from a server is stale, not proof of offline. On reconnection request authoritative state, retain stale wording until a valid newer response arrives, then replace it atomically. Account switches must not reuse prior-account caches.

Request widget timeline entries for known pickup-window boundaries and freshness transitions; request reloads for meaningful source changes and household/configuration changes. Use system date/time text where appropriate to display elapsed time without per-second reloads. The system controls refresh opportunity. A scheduled threshold is not proof the screen updates at that instant; prefer conservative last-checked wording and verify transition delays. No one-second polling promise. See [Widgets: Updating widget content](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content).

## Private bounded delivery Live Activity

Start when the user follows an active delivery from its detail view, or at an expected delivery-start event after that choice. Provide “Stop tracking on Lock Screen” in the corresponding app view. Declining/unsupported activities leaves the same information in app. No additional location, contacts, or HomeKit permission is needed merely to display server-provided delivery status. Explain sharing when invoked; do not add launch-time permission gates. See [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy).

Data projection: opaque delivery identifier, monotonic revision, server observation time, confirmed stage, optional ETA interval and its validity, start time, terminal status, hard tracking deadline. No name, address, gate code, parcel contents, map, or exact courier location. Use established authentication and protected secret storage for app detail; exclude secrets from deep-link query strings and diagnostic logs.

| Presentation | Fresh content | Stale/offline replacement |
|---|---|---|
| Dynamic Island compact | Leading parcel/stage symbol; trailing short ETA window if it fits, otherwise stage abbreviation | Leading parcel plus warning mark; trailing `Old` or `Offline`; accessible label includes update age |
| Dynamic Island minimal, including multiple activities | Stage symbol with changing status badge; meaningful current state rather than logo alone | Warning badge; accessible `Delivery update needed` |
| Expanded | `Delivery` at leading edge; confirmed stage and ETA window; last update beneath | `Update needed` or `Offline`; last-known stage and age; no ETA |
| Lock Screen | Same hierarchy in a distinct task banner with restrained background; whole banner opens delivery detail | Same stale wording, with age always visible |
| Watch Smart Stack custom layout | `Delivery`; confirmed stage/ETA window; brief update age | `Delivery · Update needed` or `Offline`; `Updated 35 min ago` |

Keep identity and relative positions consistent between compact and expanded. Both compact halves and the banner open the exact delivery detail, preserving item identity across interruptions. No Accept/Cancel action is justified by the brief, so this activity has no direct transactional control. App detail handles any eventual actions with current server validation. Multiple concurrent deliveries must remain distinguishable through a safe nonpersonal label in larger layouts; minimal activation still resolves the exact event.

Activity state machine:

`followed + active → tracking ↔ stale/offline → terminal → ended`

A valid newer update restores tracking; elapsed time alone never proves delivery. An 80-minute expected duration fits a bounded Live Activity, but is not an ETA countdown or a success signal. End immediately on authoritative delivered/cancelled/failed status or user stop. Delivered shows `Delivered`, cancelled shows `Delivery cancelled`, failure shows `Delivery ended — open for details`; retain a safe terminal summary for 15 minutes on surfaces that permit it. Dynamic Island removes it on ending. User stop, sign-out, or revoked access uses immediate dismissal where supported.

To prevent a lost terminal signal from creating indefinite tracking, propose a hard deadline at start +120 minutes (80-minute plan plus 40-minute contingency). At that deadline, end with `Tracking ended · Status unconfirmed`, retaining it for 15 minutes where allowed. This is a product timeout, not a claim that the delivery ended or a platform-enforced timer. Configure an authoritative server termination path; verify deadline/end delivery under network loss and platform limits. If no fresh server state is available, app detail continues to show unconfirmed status. Never silently restart tracking after timeout.

Update only changed content and freshness state; transport/push cadence is not guaranteed rendering cadence. Alert only on a confirmed crucial event, such as arrival requiring attention; do not send a duplicate notification for the same event. No stale-data alert loop, promotion, or decorative progress animation. These choices follow [Live Activities: lifecycle and presentations](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity), which recommends bounded events, immediate ending, and a shorter retained summary rather than the maximum retention.

## Watch surface comparison and selection

| Decision | Watch-face complication | Delivery Live Activity in Smart Stack |
|---|---|---|
| Task fit | Recurring “Any pickups ready?” on wrist raise; requires a user-selected compatible face slot | Temporary 80-minute delivery; timely stage changes without permanently occupying a face slot |
| Freshness | Budgeted timeline/reloads; source age and stale state required; unsuitable for continuous delivery tracking | Frequent meaningful event updates; can still become stale/offline; same source-age policy as phone |
| Privacy | Visible on the face and potentially Always On; only safe household summary | Personal paired-watch activity, still observable; generic delivery context, no address/code/name |
| Ending | Persistent configured slot; after pickup clears, show `0 ready` or `No pickups`, not a departed courier | End with phone event; remove active tracking immediately; short terminal summary only where supported |
| Tap destination | Native Watch household pickup list, with matching scope and cached age | Exact delivery in Watch app if installed; otherwise system full-screen activity with paired-iPhone launch button |

**Choose Smart Stack Live Activity for delivery.** Do not require a new face or duplicate it with a delivery complication. Optionally offer an accessory rectangular **Pickup summary** complication for people with recurring pickup needs: `Pickups / 1 ready` when fresh, `Pickups / Update needed` when stale, and `Pickups / Set up in app` without scope. Its placeholder uses neutral label blocks and a parcel symbol, without realistic private content. Slot compatibility follows the selected system face; do not advertise universal face support or a proprietary custom face. If unsupported, use the Watch app pickup list rather than an error-only path. Legacy complication templates and their conflicting inline dimensions are outside this selected modern rectangular design.

The Smart Stack activity is a Live Activity, not the optional periodic rectangular widget/complication. Per the local [Live Activities watchOS section](https://developer.apple.com/design/human-interface-guidelines/live-activities#watchOS), it combines compact halves by default, can use a custom layout, and has the app-present/app-absent tap behavior above. Support/OS availability still requires SDK verification. The custom layout must also remain useful in CarPlay, where controls are disabled; this status-only layout does. No obligation to install a Watch app just to read the activity. If built, the Watch app should independently show cached delivery state, age, and terminal history rather than only redirecting to iPhone. See [Complications](https://developer.apple.com/design/human-interface-guidelines/complications) and [Designing for watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos).

## Appearance and accessible content

Use real text, system text styles, medium-or-stronger status weight, and parcel/status symbols paired with words. Count/status is primary, freshness secondary but never omitted when stale. Use adaptable containers and system margins, not one fixed canvas. At enlarged text, remove optional decoration and last-known stage before compromising the status or age. Inline remains a single short statement and one activation target. Define semantic reading order as scope/title → state/count → freshness → destination; exclude decorative glyphs from redundant speech.

Check Home Screen light/dark, accented tint and clear appearances; Lock Screen vibrant grayscale; HomeView background removal, accent and red Night Mode. Preserve status without green/red alone. In vibrant mode use suitable grayscale brightness, not opacity alone. For Watch tint and wrist-down, retain status/age, dim secondary treatment, settle motion, preserve layout and restore the same context at wrist raise. Private details remain excluded even in active presentations. On devices supporting Always On, verify actual reduced-luminance behavior; the local guide is device-qualified, not universal support. StandBy should retain the safe summary at scaled size and in red Night Mode; other auto-presented Live Activity destinations must not reveal extra fields. See [Widgets rendering modes](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes) and [Always On](https://developer.apple.com/design/human-interface-guidelines/always-on).

Use [Accessibility guidance](https://developer.apple.com/design/human-interface-guidelines/accessibility) for text enlargement (at least 200% on iPhone, 140% on watchOS in this snapshot), measured contrast, and assistive activation. In app detail, start from platform default 44×44 pt control areas on iPhone/Watch. Do not infer custom tiny targets are acceptable in a constrained system accessory; use the native whole-surface target. Gallery previews are explicitly simulated, show plausible fresh and stale states, and contain no supplied private details. Initial loading placeholders differ from signed-out and unavailable states.

## Acceptance checks and evidence

**Passed — static design inspection only:** This document specifies separate shared/personal projections, supported selected widget families from the local matrix, one inline target, explicit 35-minute stale copy, no continuous-widget-refresh promise, Watch surface comparison and destinations, and bounded start/end/timeout behavior. Installed root → family → topic → source routing was read with separate single-file commands, with topic-index search before finalizing routes.

**Failed — supplied proposal:** one-second widget refresh promise; full address/gate code on shared HomeView; three independent inline targets. The replacement specification corrects these at design level. No implemented fix is evidenced.

**Not executed — implementation acceptance:**

| Scenario to execute | Required result |
|---|---|
| Load supplied fixture | All surfaces mark 35-minute data stale; no fabricated ETA, pickup-ready assertion, or live progress |
| Cross freshness boundary; deny network; reconnect with an older revision | Conservative freshness wording persists; offline only when known; old response cannot restore fresh state |
| Share/revoke scope, sign out, switch account | Only eligible summary crosses household boundary; private fields absent from payload/cache/previews/logs; no prior-account disclosure |
| Activate inline, compact halves, banner, optional complication | Exactly the specified object/scope opens; authentication resumes that destination; inline has one target |
| Watch app installed/absent; phone unreachable | Native delivery detail or documented system fallback; cached age visible; no false connected state |
| Terminal event, timeout, user dismissal, late update | End immediately on confirmed terminal; retention bounded; timeout says unconfirmed; stale/later packets cannot resurrect ended activity |
| Multiple activities; no Dynamic Island; small Watch; supported/unsupported face | Meaningful minimal state, Lock Screen fallback, legible safe Watch glance, compatible pickup-list fallback |
| Tint/clear/dark/grayscale/background removal/red Night Mode/Always On | Status and freshness remain legible, stable and private; no color-only meaning or control-dependent CarPlay layout |
| Long localization, iPhone 200% and supported Dynamic Type sizes through AX5, Watch 140%, VoiceOver and assistive activation | No essential state/age clipped; coherent reading order and exact destination; no redundant secret announcements |

Missing evidence: deployment OS/device matrix; ActivityKit/WidgetKit availability and actual host deep-link behavior; server freshness SLA, stage/ETA schema, monotonic revisions and terminal/timeout delivery mechanism; actual household membership/consent and parcel eligibility rules; real pickup records and windows; Watch app existence; cache protection/redaction behavior; native previews and measured geometry/contrast; SDK build, timeline/push/offline/termination logs; device rendering, Always On, battery, physical wrist readability, and accessibility execution. Product thresholds and the 120-minute deadline require validation against that backend evidence. No runtime, security certification, or accessibility conformance is claimed.
