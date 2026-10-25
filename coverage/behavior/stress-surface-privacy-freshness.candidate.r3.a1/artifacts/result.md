# Pickup summary and delivery activity design

Design specification for iPhone, based on `interface.md` and the installed local HIG snapshot (2026-10-25). No web access or app execution was used. Example future states below are simulated; the brief supplies a parcel, private recipient/address/access-code data, a 35-minute-old server update, and an 80-minute delivery duration. It does not establish pickup readiness, current delivery phase, or an ETA.

## Concrete result

The widget answers “What household pickup needs attention?” The Live Activity answers “What is happening with my current delivery?” They use separate privacy scopes and data projections. The supplied record alone must not be presented as a confirmed ready pickup or an actively moving courier.

### Household-visible pickup widget

Choose system small for iPhone Home Screen and the shared Apple HomeView Modular face. HomeView uses the small family with removable background; it is a household surface, distinct from a personal watch Modular face. This family mapping and shared visibility follow [Widgets: Anatomy and Apple HomeView](https://developer.apple.com/design/human-interface-guidelines/widgets).

Top-to-bottom small layout, using actual system-styled text and a parcel symbol:

```
Household pickups
Status unavailable
Updated 35 min ago
Open to check
```

This is the initial supplied-data state: no pickup count or readiness is known. Once a server-confirmed, explicitly household-shared pickup exists, a simulated fresh example is `Household pickups / 1 ready to collect / By 6 PM / Updated 2 min ago`. Show a deadline only when supplied by the service. With multiple pickups, show the ready count and earliest confirmed deadline; open the filtered household pickup list. Zero confirmed ready items reads `No pickups ready`, only with a fresh successful response.

Configuration is “Household pickups,” restricted to records the owner explicitly shares as safe summaries. Setup explains that everyone near the shared face can see this content. Default sharing is off; unconfigured shared content says `Choose shared pickups / Set up in app`. A signed-out state says `Sign in to see pickups`; revoked sharing or lost authorization clears cached summaries and shows `Pickups unavailable / Open app`. Do not treat sign-out as an empty household.

Never include recipient names, street address, access code, tracking identifier, parcel contents, or courier location in the household projection, preview, accessibility label, or deep-link parameters. The source record’s Sam, address, and gate code remain in authenticated app detail. Household viewers cannot Accept or Cancel from the summary. Activation opens the authorized household pickup list; a viewer without access gets sign-in/access explanation before any detail. A link conveys navigation, never authorization.

Additional variants retain the same question:

| Surface/family | Content and interaction |
|---|---|
| iPhone Lock Screen accessory inline | `Pickup status old · 35m` initially; fresh simulated `1 pickup ready`. Exactly one whole-line target opens household pickups. Remove the proposed independent Accept, Cancel, Details targets. |
| iPhone Lock Screen accessory rectangular | Title `Pickups`; status plus `Updated 35 min ago`. One target to the same list. |
| Watch accessory rectangular in Smart Stack, and compatible watch-face slots | Same compact summary and age; a watch complication is a separate destination from an iPhone Lock Screen widget. Tap opens the watch pickup list, or a safe handoff explanation if no watch app exists. No legacy ClockKit artwork or unsupported slot sizes are promised. |

The watch variant is useful for pickup glances, while the delivery Live Activity provides the active-event glance. Schedule relevance around actual collection windows. Modern WidgetKit family choice, finite reloads, private Always On behavior, and family-specific placeholders follow [Complications: Best practices, Visual design, Rectangular](https://developer.apple.com/design/human-interface-guidelines/complications).

### Private bounded delivery Live Activity

Start on the recipient’s iPhone after a server-confirmed delivery-start event for a followed delivery, with a clear opt-out in delivery detail. If the user opens a delivery with only the supplied stale record, show its stale detail in the app; do not manufacture a live start. An 80-minute delivery is an appropriate bounded event under [Live Activities: Best practices and lifecycle](https://developer.apple.com/design/human-interface-guidelines/live-activities).

“Private” means recipient-scoped authorization plus minimal exposed content, not a promise that Lock Screen content is invisible to bystanders. Never display or send the address, gate code, recipient name, exact location, or parcel contents in activity content. Keep those fields in authenticated app detail. Default exposed identity is `Delivery`; an opaque internal event key resolves to authorized detail without embedding secrets in the URL. More than one unrelated delivery uses separate event keys; related parcels on one delivery share an activity and safe parcel count.

| iPhone presentation | Fresh simulated content | Stale/offline replacement |
|---|---|---|
| Compact leading/trailing | Parcel symbol / `12m`, only from a valid server estimate | Parcel with warning symbol / `Old`; use `Offline` where it fits when connectivity loss is known |
| Minimal, including multiple activities | Parcel plus `12` with accessible label `Delivery, estimated 12 minutes` | Warning parcel; label `Delivery update overdue` or `Delivery offline`. Never a static logo alone. |
| Expanded | Leading `Delivery`, trailing `About 12 min`; below `On the way`, then `Updated 1 min ago`; `View delivery` destination | `Delivery / Update overdue / Last update 35 min ago / Open for latest status`; known offline adds `Offline` and replaces the freshness heading |
| Lock Screen | Same hierarchy as expanded, with phase text and optional server estimate window | Same explicit stale/offline wording; no countdown or advancing progress |

Compact halves open the same delivery detail; minimal taps open it and hold expands according to system behavior. Expanded and Lock Screen use one clear `View delivery` link, not Accept/Cancel buttons. Cancellation and acceptance require authenticated current detail and belong in the app. With privacy redaction enabled, use `Delivery in progress / Open app`; redact the accessibility representation too. When authorization is revoked or the user signs out, clear cached event data and request activity termination.

Keep identity leading and timing/freshness trailing as the activity expands. Use phase text, not a time-derived percentage: elapsed time cannot prove route progress. Fit the limited-width Dynamic Island representation within the guide’s 28-pt circle context; use symbol-only warning plus descriptive accessibility text when needed. Custom background treatment is confined to Lock Screen; Dynamic Island backgrounds remain system controlled. See [Live Activities: Anatomy, Presentation, Choosing colors](https://developer.apple.com/design/human-interface-guidelines/live-activities).

Other system destinations carry the same sanitized payload. StandBy scales the Lock Screen hierarchy, retains large status and age, removes detail before reducing text, and supports red Night Mode. Paired watch Smart Stack combines compact content with explicit status/age; tap opens watch delivery detail if available, otherwise the system paired-iPhone launch flow. CarPlay must communicate status with controls disabled. Paired Mac activation follows iPhone Mirroring. These are design contracts, not verified platform execution. No Live Activity is proposed for tvOS or visionOS. See [Live Activities: StandBy, CarPlay and platform considerations](https://developer.apple.com/design/human-interface-guidelines/live-activities).

## Freshness, updates and lifecycle

The following thresholds and timeout are proposed product policy, not Apple limits. Service owners must validate them before release.

Maintain server event version, server observation time, last successful fetch, estimate expiry, terminal event, and known connectivity separately. Reject older event versions and terminal-to-active regressions. A recent local fetch of an old server observation does not reset freshness.

| State/trigger | Widget behavior | Activity behavior |
|---|---|---|
| Initial load, no authorized cache | Static title plus placeholder blocks; if fetch fails, `Status unavailable / Open app` | No activity until a confirmed start exists |
| Fresh confirmed data | Summary with age; widget observation age under 15 min | Phase and valid estimate; observation age under 5 min and estimate not expired |
| Refresh underway | Keep authorized existing content and its real age | Keep current content until freshness expires; no indefinite spinner |
| Stale threshold or expired estimate | `Status may have changed`, last known summary qualified `Previously …`, age; omit outdated deadline | `Update overdue`, last observation age; remove ETA/countdown and any implied movement |
| Known offline | `Offline`, qualified cached summary and age; no cache means `Offline / Status unavailable` | `Offline / Last update …`; no ETA. Connection recovery alone does not make data fresh |
| Service error without connectivity evidence | `Can't update`, cache qualified by age | `Can't update`, age; do not assert offline |
| Fresh successful recovery | Replace cache only after validating event version and observation age | Resume valid phase/estimate, unless terminal or hard-ended |
| Authorization/share revoked | Clear cached shared content immediately when observed | End and clear private event cache when observed |

The supplied 35-minute-old update exceeds both thresholds. Display stale from the first render; offline status requires additional evidence. If a previously confirmed pickup count is retained, say `Previously 1 ready`, never an unqualified live count.

Widget requests occur at meaningful events and boundaries: collection window, stale deadline, successful app sync, and changed server state. Request a fallback reload after 15 minutes while relevant, subject to system scheduling; do not promise delivery at that time or per-second refresh. Use system date/time presentation for age where possible. Precompute stale timeline entries and suppress expired deadlines even when network refresh fails. Preserve useful cached data during refresh, per [Widgets: Updating widget content and Adding interactivity](https://developer.apple.com/design/human-interface-guidelines/widgets).

Activity states are `confirmed start → active phase → delivered/canceled/failed → ended`. Server phase/estimate changes produce updates, not per-second network traffic. Schedule stale behavior from observation time and estimate validity so an absent push cannot leave a fake live ETA. Critical arrival or failure may alert once; do not issue a duplicate push for the same activity update. No promotional content.

A nominal 80-minute estimate is not proof of completion at minute 80. On confirmed delivery/cancellation/failure, end immediately and remove active Dynamic Island presentation; retain a safe `Delivery complete`, `Delivery canceled`, or `Delivery ended` Lock Screen summary for 15 minutes, then remove. On unknown outcome, a proposed hard stop at start +120 minutes ends tracking with `Tracking ended / Check app for delivery status`, never `Delivered`. Request/schedule this fallback using supported lifecycle mechanisms; reliable remote ending and removal timing require SDK/runtime validation. Late events after hard stop update app history without silently restarting the activity. User dismissal stops this surface, not the real delivery. The 15-minute summary fits the guide’s suggested shorter retention rather than the possible four-hour retention window.

## Visual and accessible contract

Use semantic system text styles and symbols, restrained brand accents, and flexible system family geometry rather than a fixed screenshot canvas. Generally keep widget text at least 11 pt; typical widget margins are 16 pt, with contextual adjustments, while the Live Activity Lock Screen guide gives 14 pt standard margins. These are scoped source guidance, not universal fixed geometry. Drop optional deadline/action hint before losing status and freshness; never shrink all text to fit.

Primary group: count/status. Accent group: parcel symbol and optional deadline. Secondary group: age. Fresh, stale, offline and terminal states always use text/symbol differences as well as color. Verify full-color light/dark, accented tint and clear Home Screen modes, vibrant Lock Screen grayscale, removable-background HomeView, red Night Mode, watch tint, and reduced-luminance Always On where applicable. In vibrant mode, use grayscale brightness for hierarchy rather than relying on white opacity. See [Widgets: Rendering modes, Displaying text, Platform considerations](https://developer.apple.com/design/human-interface-guidelines/widgets).

Proposed spoken order is surface title, state/count, valid timing if present, observation age, then link purpose. Decorative symbols are not separate repeated announcements. All sanitized labels must remain meaningful without recipient/address data. Gallery previews use clearly simulated safe data; loading placeholders reserve the same hierarchy without invented status.

## Acceptance checks and evidence status

Passed means checked against this written specification and supplied text only.

| Status | Check and evidence |
|---|---|
| Passed — specification | Initial 35-minute-old record is explicitly stale on both surfaces; neither pickup readiness nor ETA is invented. |
| Passed — specification | Shared summary excludes the supplied name/address/code; activity uses a distinct authorized sanitized projection. |
| Passed — specification | Small-family HomeView, iPhone accessory widgets and watch complications are distinguished; inline has one target. |
| Passed — specification | Widget refresh is system-controlled; delivery has start, terminal events, stale fallback, hard stop and short retained summary. |
| Passed — specification | Compact, minimal, expanded, Lock Screen and secondary destination behavior are defined. |
| Failed — supplied proposal | Per-second widget refresh, full shared address/code, and three independent inline targets conflict with the routed guidance. This document replaces them; no implementation correction is evidenced. |
| Not executed | Native family fit, timeline refresh, push/update delivery, deadline-driven stale rendering, activity ending/removal, deep links and authorization boundaries. |
| Not executed | VoiceOver order/labels, Dynamic Type through supported accessibility sizes, contrast, physical watch readability, household viewing behavior and privacy redaction. |
| Not executed | SDK compilation/API availability, simulator/device, GUI, Always On, tint/clear, background removal, StandBy red mode, multiple activities and CarPlay control-disabled rendering. |

Before implementation acceptance, exercise these fixtures: fresh/15-minute widget boundary; fresh/5-minute activity boundary; supplied 35-minute age; expired estimate with recent observation; offline with/without cache; service error; out-of-order event; reconnect with old data; signed out; revoked sharing; zero and many pickups; delivered/canceled/failed; missing terminal push at 120 minutes; late terminal event; user dismissal; simultaneous activities. Assert exact qualified copy, no expired ETA, no secret in content/accessibility/deep links, correct destination and no restart after termination.

Preview each selected family with long localized text, right-to-left layout, large counts, narrow devices and accessibility text sizes. Verify status and age survive truncation and monochrome rendering. On capable Apple devices, follow every link, test lock/unlock and account switching, confirm screen-reader order, and observe terminal removal and stale transitions with networking disabled. These remain acceptance work, not claimed results.

## Missing evidence and decisions to validate

The supplied material has no app code, OS deployment target, SDK documentation, backend event schema, actual pickup state, observation timestamp/time zone, ETA expiry, authorization/share implementation, watch app, screenshots, push logs or device results. Confirm that pickup summaries are an actual supported product workflow rather than inferring pickup readiness from delivery data. Confirm household opt-in/revocation behavior and whether members can accept aggregate pickup visibility.

Validate proposed 15-minute/5-minute freshness thresholds and 120-minute hard stop against service latency and delivery exceptions. Obtain evidence for server-authoritative termination, outage fallback, credential-safe payloads/caches, offline detection, supported system privacy controls and lifecycle scheduling APIs. Native font fit, color contrast, accessibility, watch readability and shared-room comprehension require actual execution/research. The local HIG snapshot supplies guidance, not SDK or product-support verification; official links above identify source articles without claiming they were visited.

Audit route read from installed package: root `apple-hig/SKILL.md` → `subskills/apple-hig-system-experiences/SKILL.md` → `.topics/apple-hig-widgets/SKILL.md`, `.topics/apple-hig-live-activities/SKILL.md`, `.topics/apple-hig-complications/SKILL.md` → corresponding `references/widgets.md`, `references/live-activities.md`, `references/complications.md`. Each file was read using a separate `cat` command before using its guidance.
