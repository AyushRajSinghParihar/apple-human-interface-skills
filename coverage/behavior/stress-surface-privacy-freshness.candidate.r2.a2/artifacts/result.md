# Pickup summary and delivery Live Activity

Design specification based on `interface.md` and the installed local HIG snapshot (2026-10-25). No web access, SDK verification, implementation, simulator, GUI, device, or assistive-technology execution was performed. Official links below identify the local guidance's sources; they were not opened.

## Decisions and supplied evidence

The task is a brief household pickup check plus private tracking of one bounded, 80-minute delivery. The brief supplies one parcel, a recipient, a full address and gate credential, and a server update aged 35 minutes. It supplies no confirmed pickup readiness, delivery stage, ETA, timestamp, backend contract, or minimum OS version. Do not invent these values. Examples below that describe readiness or transit are conditional fixtures.

Replace the proposed one-second widget reload loop with meaningful timeline entries and system-controlled refresh opportunities. Use a Live Activity for frequent changes during the delivery. Replace the inline Accept/Cancel/Details targets with one parcel-details destination. Exclude recipient, address and gate code from household content. These correct the supplied proposal against [Widgets: Updating widget content, Adding interactivity, Apple HomeView](https://developer.apple.com/design/human-interface-guidelines/widgets).

## Household pickup widget

Glance question: “Is there a household pickup to check, and how trustworthy is this summary?”

Use a separate **Household pickups** configuration with a strict safe-data projection. An authorized person selects a household and explicitly enables sharing: “Show pickup counts and status to everyone in this household. Names, addresses, and access codes stay private.” Default before setup: `Choose household in app`. Only parcels explicitly shared with that household contribute. Do not automatically publish Sam's parcel merely because it exists on a connected phone. The shared Modular face is household-visible, distinct from personalized Home Screens; use system-small there, not a watch complication. [Widgets: Apple HomeView](https://developer.apple.com/design/human-interface-guidelines/widgets#Apple-HomeView).

| Surface/family | Content, highest priority first | Activation |
|---|---|---|
| iPhone Home Screen, system small | `Household pickups`; safe count/status; freshness | Entire widget opens that household's pickup list |
| Shared HomeView Modular, system small | Same safe summary, enlarged status, removable background | Opens safe household pickup context where supported; private details require personal authenticated continuation |
| iPhone Lock Screen, accessory rectangular | `Pickup status`; safe status/count; freshness | One household pickup-list destination |
| iPhone Lock Screen, accessory inline | `Pickups: update needed` for supplied stale fixture; fresh conditional fixture `Pickups: 1 ready` | One target only; no button-like Accept/Cancel/Details regions |
| Optional Watch face, accessory rectangular | Same safe status plus age; native face typography | Opens Watch household pickup view |

Do not offer medium/large widgets until additional useful household summary information exists. Do not claim accessory families work on the shared Modular surface. Watch support assumes a native companion view; otherwise defer the optional complication. A complication is watchOS-specific, while iPhone Lock Screen accessories are widgets. [Complications: Best practices and Platform considerations](https://developer.apple.com/design/human-interface-guidelines/complications).

Concrete supplied-data layout, only after sharing is authorized:

```text
Household pickups
1 parcel to check
Update needed
Last updated 35 min ago
```

Count describes the cached shared record; it does not imply readiness. If not shared, show `No shared pickups` only after a successful authorized query confirms that result. A fresh confirmed ready fixture may read `1 pickup ready · Updated 2 min ago`. Do not display “ready” from an unknown stage.

Gallery description: `Check household pickups.` Use simulated, labeled example content without personal data. Initial placeholder preserves title and redacted status blocks, never fabricated counts. Signed out: `Sign in to view pickups`; revoked membership: `Household unavailable`; confirmed empty result: `No pickups`; failed first load: `Pickup status unavailable`. Each opens the relevant setup, sign-in, or household context. Never equate missing data with zero pickups.

## Freshness and offline contract

These thresholds are product decisions for validation with operations, not Apple requirements. Keep event time, last successful server confirmation, and local fetch time separate. Re-rendering cached data never renews server freshness.

| State | Entry condition | Widget / expanded activity behavior |
|---|---|---|
| Fresh | Valid server confirmation age ≤5 min | Confirmed state; `Updated … ago`; ETA only if separately valid |
| Stale | Age >5 min or ETA validity expires | `Update needed`; keep explicitly last-known state and timestamp; suppress current ETA/countdown |
| Offline with cache | Observed connectivity/fetch evidence, not just old data | `Offline · Last updated … ago`; cached status labeled last known |
| Failed/unknown connection | Fetch failure without proof of offline status | `Couldn't update`; timestamp; no invented offline assertion |
| Refreshing | Fetch in progress | Keep existing safe content and freshness; no full skeleton replacement |
| No cache | No valid snapshot | `Status unavailable`; open app to retry |

The supplied 35-minute age is stale. Connectivity is unknown. It must not show “live,” a current ETA, or “offline” solely from that age. Compact forms prioritize `Update needed` over a count if both will not fit; full timestamp remains in the destination. At very large text, use `Update needed` plus a compact age rather than dropping the freshness warning.

Request widget timelines at meaningful status/window changes and the five-minute freshness boundary; request reload after relevant server changes when supported. System scheduling can delay rendering: keep last-updated text visible even in the fresh template so an old entry cannot silently look current. Use system relative date presentation where supported, never per-second network polling. The authenticated app retries on opening and offers explicit retry; reconnect alone does not mark data fresh. Only a newer valid response clears stale/offline. Reject older/out-of-order event revisions. [Widgets: Updating widget content](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content).

## Private delivery Live Activity

“Private” means a personal delivery context with minimized public-facing content, not a guarantee that a Lock Screen or paired display is visible only to its owner. Never put Sam's name, the full address, gate code, a route map, or credential-bearing links in activity content, previews, spoken labels, or payloads. All surface layouts use generic `Delivery`; sensitive detail is available only after app authentication and parcel authorization. Even the unlocked activity omits the gate code. This is a deliberate stricter product policy based on [Live Activities: Best practices](https://developer.apple.com/design/human-interface-guidelines/live-activities#Best-practices) and [Privacy: Protecting data](https://developer.apple.com/design/human-interface-guidelines/privacy#Protecting-data).

Start once after server-confirmed dispatch for this delivery, when expected by the person, subject to system authorization. Offer `Track delivery` in the parcel view and an easy per-delivery opt-out. If unavailable or declined, the app's delivery view remains usable. Do not start a live event from the 35-minute-old record alone. Track one activity per delivery; update the existing activity across its stages.

| Presentation | Fresh confirmed transit fixture | Stale/offline adaptation |
|---|---|---|
| Compact leading / trailing | Parcel-transit symbol / valid estimated minutes such as `20m`, otherwise short stage | Parcel-warning symbol / `Stale`; use offline symbol only with evidence |
| Minimal, including competing activities | Parcel symbol with small transit state mark; completion check only when confirmed | Parcel plus warning mark; meaningful status, not static logo |
| Expanded | `Delivery`; `On the way`; `Estimated 14:20–14:30` only if provided and valid; `Updated 2 min ago` | `Delivery · Update needed`; `Last known: On the way`; `Last updated 35 min ago`; omit ETA |
| Lock Screen | Same hierarchy in a distinct delivery layout | Same last-known labeling and age; no sensitive identity |
| StandBy | Scaled Lock Screen layout with less secondary detail | Large freshness warning retained; red Night Mode legible |
| Watch Smart Stack | Stage and freshness, combining compact content or custom small layout | Warning replaces ETA; tap opens native delivery context if available, otherwise system paired-phone continuation |

Both compact halves and the activity body open the same opaque delivery-ID route. Authentication resumes that exact delivery; wrong-account access shows an unavailable state. No sensitive values in the URL. Retain parcel identity and stage positions as the activity expands. Use system-controlled Dynamic Island backgrounds; custom background only on Lock Screen. Fit limited-width content within the guide's 28-pt circle guidance, with no fixed universal canvas. [Live Activities: Presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Presentation).

Use a single details destination; there is no necessary direct mutation for this glance. Accept and Cancel remain authenticated in-app workflows. An offline request must not display success without server confirmation. No fake independent inline targets and no claim that tapping bypasses locking. A future essential direct action would need its own authorization, pending/failure, and retry contract.

### Lifecycle and updates

`Not started → dispatched → on the way → arriving → delivered/cancelled/failed` uses authoritative server events. Freshness/connection state overlays any nonterminal stage. Do not infer completion from the planned duration, elapsed-time percentage, or ETA reaching zero.

The expected event lasts 80 minutes, within the local HIG's preference for bounded events ideally no more than eight hours. At start, assign a product tracking cutoff of dispatch +120 minutes (80 minutes plus a proposed 40-minute grace period). If no terminal confirmation arrives, end tracking with `Tracking ended · Check delivery status`; the delivery itself remains unresolved in the app. Do not auto-restart indefinitely. An authenticated fresh confirmation can offer a new explicitly bounded tracking session if needed. This cutoff is a product proposal requiring operational approval, not a platform limit.

On delivered/cancelled/failed confirmation, end immediately; remove from Dynamic Island and other nonretaining destinations. Retain a safe Lock Screen summary for 15 minutes where supported, then dismiss. Use `Delivered`, `Delivery cancelled`, or `Delivery needs attention` accurately. Persist the result in the app for later reading. Stopping tracking or system dismissal does not cancel delivery. At cutoff without connectivity, end using the planned deadline where supported; actual background enforcement is an implementation acceptance gate.

Send updates only when content changes, with freshness expiry scheduled independently of network updates. Alert only for confirmed arrival requiring attention or a blocking exception; do not send a duplicate push for the same update. Routine progress and stale state remain quiet. Foreground and remote updates share revision ordering; terminal events close the activity and reject later nonterminal updates. Verify ActivityKit lifecycle, expiry and termination scheduling against the eventual SDK; no API availability is established by this design. [Live Activities: Starting, updating, and ending](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity).

Where the system propagates the activity, CarPlay must remain useful with controls disabled; paired Mac activation uses iPhone Mirroring. Do not promise Live Activities on tvOS or visionOS. No custom driving workflow is required. HomeView receives only the separate safe pickup widget, not private delivery content.

## Data, appearance and access

| Data | Purpose and exposure |
|---|---|
| Household ID, shared safe count/status, confirmation timestamp | Authorized household summary projection; revoke access and clear cached projection on membership/account changes |
| Opaque delivery ID, stage, revision, timestamps, valid ETA window, tracking deadline | Personal activity projection; no personal destination or access credential |
| Recipient/address | Authenticated parcel detail only, authorized per account |
| Gate credential | Explicit reveal in authenticated parcel detail only; established protected storage, no widget/activity cache or logs |

No new location, contacts, HomeKit, or tracking permission is needed merely to display server-provided logistics status. Sharing setup is an ordinary product choice, not a simulated system permission prompt. Revalidate disclosure requirements against actual storage/transfer behavior. Revocation must clear projections locally and propagate removal where possible; offline remote displays may retain old safe summaries until refreshed, so privacy relies on payload minimization rather than immediate remote erasure. [Privacy: Best practices and Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy).

Use semantic system type: headline for status, body for stage, caption for freshness, medium or stronger for activity status. Actual text and scalable symbols, no rasterized labels. Stack age beneath stage at enlarged sizes; drop decorative identity before status/freshness. Preserve the glance question through widget Large–AX5, iOS text enlargement of at least 200%, and watchOS at least 140%; fixed accessories use concise safe text with full detail in the accessible destination. These are design targets pending fit checks. [Typography: Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type), [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility).

Full color uses semantic light/dark foregrounds. Accented mode keeps status primary and supporting symbol accent. Vibrant mode uses grayscale luminance hierarchy, not white-opacity tricks. Text plus warning/check symbols preserves meaning in tint, clear, grayscale and red Night Mode. HomeView/StandBy backgrounds are removable. Always On keeps the same safe fields and positions, dims secondary information, retains freshness, and uses no continuous animation; waking restores the same delivery context. Device support must be verified; the local Always On guide names particular iPhone Pro models rather than all iPhones. [Widgets: Rendering modes](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes), [Always On](https://developer.apple.com/design/human-interface-guidelines/always-on).

Accessibility contract: expose status, freshness and destination as meaningful text; decorative parcel art adds no redundant announcement. A combined widget label could read `Household pickups. One parcel to check. Update needed. Last updated 35 minutes ago.` Never include private data in accessibility labels. Use native link behavior for the single destination. In-app controls use comfortable 44×44-pt default activation areas on iOS/watchOS. No essential information depends on color, sound or animation. Runtime spoken order and activation remain unverified.

## Acceptance checks and evidence still missing

**Passed — static specification inspection only:** supplied 35-minute fixture is stale without an invented offline claim; household projection omits personal identity and credentials; inline accessory has one destination; widget scheduling makes no continuous refresh promise; delivery has explicit start, terminal signals, fallback cutoff and retention; no ETA or pickup readiness is invented from the brief. Installed root, selected families, topic procedures and supporting local guides were read through separate file-reading commands.

**Failed — supplied proposal:** per-second widget refresh promise; full address/code on the shared face; three independent inline targets. This specification replaces each. No implemented product was inspected, so these are proposal findings, not measured runtime defects.

**Not executed — implementation acceptance gates:**

| Scenario | Required result / missing evidence |
|---|---|
| Inject age 4:59 → 5:01 → 35 min; delay reload; fail fetch; reconnect | Freshness warning/age remains truthful; no stale ETA; offline only with evidence; newer server confirmation alone restores freshness. Needs timeline and network execution. |
| Dispatch, arrival, terminal event, cutoff with no network, late reordered update | One activity, no inferred delivery, prompt ending, 15-minute summary expiry, no resurrection or duplicate alert. Needs backend event contract and ActivityKit execution. |
| Shared/nonshared parcel; revoke membership; sign out; wrong account; locked tap | Only approved summary visible; private route authenticates and preserves destination; no secret in payload, cache, link, log, preview or spoken output. Needs data-flow/security inspection and locked-device tests. |
| Tap every surface; inline boundaries; two or more simultaneous activities | Correct household/delivery route, single inline target, informative minimal state. Needs native navigation/system integration tests. |
| Smallest/largest supported iPhone and Watch; long localized strings; text sizes through AX5/Bold Text | Status and freshness remain legible without overlap; companion app exposes full detail. Needs previews, actual rendered geometry and device-distance checks. |
| Light/dark, tinted/clear, vibrant grayscale, removed background, red Night Mode, Always On/wrist lower | Meaning survives loss of color/background; no sensitive reveal or layout jump; contrast measured with actual foreground/background. Needs rendered variants, measurements and supported devices. |
| VoiceOver, Voice Control, Switch Control, relevant keyboard/assistive paths | Meaningful labels, no hidden secrets or fake controls, destination reachable and activatable. Needs Accessibility Inspector and assistive-technology execution. |
| Watch/StandBy/CarPlay/paired Mac propagation | Readable glance, disabled driving controls harmless, correct paired continuation. Needs supported hardware/OS and simulator evidence. |

Still missing: minimum OS and hardware list; SDK/API feasibility for household/remote surfaces, expiry and background cutoff; genuine pickup stage and time data; service freshness/ETA guarantees; validated sharing and authorization model; user confirmation of the proposed five-minute stale and 120-minute tracking thresholds; household comprehension and privacy research. The local snapshot contains unrelated Mac accented-mode and legacy complication sizing inconsistencies; this design makes no support or fixed-art sizing promises from those passages. No native rendering, energy, push reliability, accessibility conformance, or platform support certification is claimed.
