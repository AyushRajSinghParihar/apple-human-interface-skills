# Pickup summary and delivery activity

Design specification based on `interface.md` and the installed apple-hig snapshot dated 2026-10-25. No web sources were fetched. Official links below identify the articles represented by the local guides; current SDK support is unverified.

## Decisions and scope

The household glance answers **“Is there a pickup to check, and how current is that information?”** The personal delivery glance answers **“What is the last confirmed stage of my active delivery?”** Keep these as separate data projections and lifecycles.

Replace the proposed every-second widget refresh with meaningful timeline entries and system-controlled reload requests. Use a Live Activity for the bounded 80-minute delivery. Replace the inline accessory’s Accept, Cancel and Details targets with one tap opening the relevant app context. Inline accessories have a single target. [Widgets: updating and interactivity](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content)

The brief supplies a parcel for Sam, a full street address, a gate secret, and a server update 35 minutes old. It does **not** establish pickup readiness, an ETA, current delivery stage, start time, connectivity failure, or household sharing consent. Do not infer any of these. The example below therefore starts with “Pickup status outdated.” Fresh-state samples are simulated.

## Concrete surface contract

| Surface | Family and hierarchy | Activation |
|---|---|---|
| iPhone Home Screen | System small: “Pickups” label, prominent status/count, freshness line. No independent controls. | Household pickup summary, preserving the selected household. |
| Shared Apple HomeView Modular face | System small, deliberately shared configuration. Same summary, larger status, no personal details. Removable background; preserve meaning without it. | Safe household summary where supported; private detail requires personal-device authentication. Never reveal secrets through a shared destination. |
| iPhone Lock Screen | Accessory rectangular: “Pickups” / “Status outdated” / last-check time where space permits. Inline alternative: “Pickups · Outdated”, one target. | Pickup summary after system access rules; authentication before private details. |
| Watch glance | Modern WidgetKit accessory rectangular complication and Smart Stack variant: “Pickups” / “Outdated” / last-check time. No inline multi-action layout. | Watch pickup summary; same object/context. If no Watch app exists, do not promise this complication until one is delivered. |

Small-family HomeView support and accessory family placement come from the local [Widgets platform tables](https://developer.apple.com/design/human-interface-guidelines/widgets#Apple-HomeView). HomeView Modular is a shared household surface, distinct from an Apple Watch Modular face. Watch uses complication-specific placement and system sizing; do not reuse legacy ClockKit image dimensions. [Complications](https://developer.apple.com/design/human-interface-guidelines/complications)

Proposed small widget, with supplied stale data:

```text
[parcel symbol] Pickups
Status outdated
Last checked 35 min ago
```

Simulated fresh-ready sample: `Pickups / 1 ready / Checked 2 min ago`. Empty verified result: `Pickups / None ready / Checked 2 min ago`. Never replace missing data with zero.

Configure one household in the authenticated app. Before sharing, explain: “People in your household can see pickup counts and status. Names, addresses and access codes stay private.” Sharing is off until the account owner chooses it. Unconfigured shared widget reads `Pickups / Set up sharing`; signed-out or revoked access reads `Pickups / Open app to connect`, without cached counts. Offer account setup in the app, not a miniature form in the widget. Gallery description: “Check household pickups.” Use clearly simulated safe previews; initial loading uses neutral placeholder blocks, never real parcel details. [Widgets: previews](https://developer.apple.com/design/human-interface-guidelines/widgets#Previews-and-placeholders)

## Privacy boundary

| Data | Permitted purpose and destination |
|---|---|
| Household count, coarse readiness, last server timestamp | Explicitly shared pickup summary only; derive an allowlisted public payload. |
| Recipient and street address | Authenticated parcel detail for an authorized person. Excluded from widget and activity payloads, URLs, previews and accessibility labels. |
| Gate code | Explicit reveal in authenticated personal app detail; established secure storage. Never in shared caches, Live Activity content, logs or deep-link parameters. |
| Opaque delivery identifier, stage, freshness, verified ETA window | Personal Live Activity projection; no household publication. Identifier carries no address or secret. Reauthorize destination on opening. |

“Private Live Activity” means attached to the personal account with minimized content; a Lock Screen is still visible to bystanders. Default to coarse status without a name, address, gate code, route map or courier location. If the person hides delivery status, render `Delivery active / Open app for details`; apply the same rule to spoken labels and mirrored destinations. Never depend only on system redaction. On logout/revocation, purge projections and end the activity. No new location, contacts, HomeKit or tracking access is necessary for this design. Ask for additional access only if a later feature requires it at the moment of use. These are product safeguards guided by [Privacy: data protection](https://developer.apple.com/design/human-interface-guidelines/privacy#Protecting-data), not a security certification.

## Freshness and offline state model

The following thresholds are proposed product policy, not Apple limits. Backend cadence must validate them before release. Keep `serverUpdatedAt`, `receivedAt`, source revision, stage, optional ETA window, and connection observation separate. Age is based on server confirmation, not the last attempted refresh. Implausible future timestamps become unknown freshness.

| State / trigger | Widget | Live Activity |
|---|---|---|
| No confirmed snapshot | “Status unavailable” | Do not begin from invented progress; app offers tracking when confirmed data arrives. |
| Confirmed snapshot age ≤5 min | Count/readiness with age | Confirmed stage and optional server ETA window labeled “Estimated”. |
| Age >5 min | “Status outdated”; old count only as “Last known: …” when space allows | “Updates delayed”; last confirmed stage explicitly labeled; suppress ETA and moving progress. |
| Known fetch/network failure | “Offline · Last checked …” plus safe last-known data if it fits | “Offline · Last update …”; retain last-confirmed stage, suppress ETA. |
| Refresh underway | Retain existing data and its age | Retain existing data and freshness warning. No reset to “live”. |
| Successful authoritative response | Replace atomically, recompute age | Accept only newer revision; clear offline only after successful response. A still-old response remains stale. |

At 35 minutes the supplied snapshot is stale, even if connectivity is available. Use “Updates delayed” rather than “Offline” unless a failure is actually known. When background execution cannot detect current connectivity, show last-confirmed time; do not imply a continuously monitored network. Prefer a stable localized absolute “Last checked [time]” if relative age cannot render reliably; a displayed “35 min ago” must not freeze indefinitely.

Request widget reloads on relevant server changes, authentication changes, and foreground reconciliation; schedule freshness-boundary entries. The system controls actual execution, so render age/stale status from timestamp at presentation where supported and validate this in WidgetKit. No per-second network or reload promise. For activity staleness, supply an expiration boundary using verified SDK mechanisms; do not rely on another push arriving to mark old content stale. [Widgets: updates](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content)

## Bounded delivery Live Activity

Start only for a confirmed active delivery the person follows, at dispatch or when they choose tracking in its app detail. Include an easy “Stop showing delivery” option there. Denial or disabled Live Activities leaves the app tracking screen usable. The expected 80 minutes is a service estimate, not proof of arrival or percentage completion.

Lifecycle: `not started → confirmed in transit → arriving → delivered`, with server-confirmed cancellation/failure terminal branches. Freshness/offline is an orthogonal presentation state. Do not derive “arriving” from elapsed time. An authenticated terminal event ends the activity immediately; remove Dynamic Island presence and retain a safe `Delivered` or `Delivery canceled` Lock Screen summary for 15 minutes where allowed. Retention is a product choice within the guide’s shorter-summary advice. User dismissal/stop ends presentation without canceling the delivery.

At expected start +80 minutes without completion, show `Delivery taking longer` only if a fresh server state confirms it remains active; otherwise show `Updates delayed`. Product tracking cutoff is start +120 minutes: end the tracking session with `Tracking ended · Check app`, never `Delivered`. A delayed delivery can be followed again from fresh app confirmation. Backend termination plus local/system expiration must cover missed end pushes; exact API and lifecycle enforcement remain an SDK validation item. This keeps tracking bounded while preserving truthful parcel status. [Live Activities: lifecycle](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity)

| Presentation | Fresh simulated content | Stale/offline adaptation |
|---|---|---|
| Compact | Leading parcel/stage glyph, trailing verified ETA such as “20m” | Warning glyph plus “Stale”; no old countdown. Both halves open the same delivery. |
| Minimal / multiple activities | Parcel plus changing stage badge; meaningful stage rather than logo alone | Warning badge; accessible label explains delayed updates. Distinct opaque delivery identity routes correctly. |
| Expanded | Leading parcel glyph and “Delivery”; stage beneath; trailing estimated window; last-update line | Keep relative positions; replace ETA with “Updates delayed” or “Offline”, and last-confirmed stage/time. |
| Lock Screen | Same hierarchy in a compact task banner; whole-banner tap opens delivery | Example: `Delivery / Updates delayed / Last confirmed status unavailable / Updated 35 min ago`. No invented stage from the brief. |

Use app identity consistently without a full app icon. All activations deep-link to the authorized delivery tracking screen, with sign-in/unlock and object authorization before displaying detail. Accept and Cancel remain app actions after current-state validation; their meaning is unspecified in the brief, so no delivery mutation is assigned to a glance. There is no need for an independent Details button when the surface already opens detail. [Live Activities: presentation and interaction](https://developer.apple.com/design/human-interface-guidelines/live-activities#Offering-interactivity)

Send only changed content, reject out-of-order revisions, and never let an old in-transit message revive a terminal activity. Alert only for crucial confirmed changes such as arrival; deduplicate the same event across activity alerts and ordinary pushes. No freshness alerts or promotional content. Update delivery is not guaranteed.

Adapt propagated presentations: StandBy scales essential status with safe margins and red Night Mode support; Watch Smart Stack shows stage plus freshness and opens the Watch tracking view if available, otherwise the system continuation; wrist-down retains only safe status. CarPlay must remain useful with all controls disabled. Paired Mac activation follows system iPhone Mirroring behavior. Do not publish this private activity on HomeView or claim support in tvOS/visionOS. [Live Activities: platform considerations](https://developer.apple.com/design/human-interface-guidelines/live-activities#Platform-considerations)

## Visual and access contract

Use semantic system text: headline/semibold for primary status, body for stage/count, caption for freshness. Use real text and matching system symbols. Flexible containers and contextual system margins replace a fixed screenshot canvas. On enlargement, stack freshness below status and remove decorative glyphs before reducing essential status. For constrained accessories use “Outdated” as the visible core and expose full status/time through the accessible value and app destination. Check iPhone supported sizes through AX5 and at least 200% text enlargement; Watch at least 140%, with native family fit verified. [Typography](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type)

Primary status uses the primary rendering group; label/freshness form the secondary hierarchy, with an accent glyph where appropriate. Test full-color light/dark, Home Screen accented/tinted/clear, vibrant Lock Screen grayscale, background-removed HomeView, HomeView/StandBy red Night Mode, Watch tint, and reduced-luminance Always On. State always includes words or a meaningful symbol, never color alone. Keep Dynamic Island backgrounds system-controlled; use default Lock Screen background unless measured contrast justifies customization. No custom backgrounds in compact/minimal/expanded activity states. [Widgets: rendering modes](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes), [Live Activities: colors](https://developer.apple.com/design/human-interface-guidelines/live-activities#Choosing-colors)

Specify one accessible activation per summary, reading purpose → status → freshness, for example “Household pickups. Status outdated. Last checked 35 minutes ago. Open pickup summary.” Hide redundant decorative symbols. Privacy-hidden content must also be hidden from accessibility output. Do not announce every age tick. Avoid continuous animation; Reduce Motion uses an immediate change or gentle fade. App controls use the iOS 44 × 44 pt default target as a starting point with adequate separation; system surface targets remain native. Measure actual contrast and layout; this document establishes no measured pass. [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

## Acceptance audit

**Passed — static specification only:** supplied brief inspected; root → family → topic → local article routing read; public/private projections defined; 35-minute snapshot labeled stale; one inline target specified; periodic widget versus bounded activity separated; start, terminal events, cutoff, retention, stale/offline and deep links specified. These passes establish design coverage only.

**Failed — supplied proposal:** every-second widget reload expectation; full address/gate secret on household face; three independent inline accessory targets. The replacement above removes those design failures. No running implementation was supplied to judge.

**Not executed — implementation acceptance:**

| Check | Required evidence / pass condition |
|---|---|
| Privacy fixtures | Address, recipient and gate secret absent from all surface payloads, caches, URLs, previews, logs and spoken labels; authenticated app reveal works; revoked sharing clears cached summaries. |
| Freshness boundaries | Test 4:59, 5:00, 5:01 and 35 minutes, process suspension, future timestamps, failed fetch and stale successful response. Old data never looks current; offline requires observed failure. |
| Widget timeline | Device execution under system budget shows useful old data during refresh and stale fallback despite missed reloads; no every-second requests. |
| Lifecycle | Confirmed dispatch starts once; delivery/cancel/failure ends immediately; missed terminal push, +80-minute delay, +120-minute cutoff and 15-minute retention behave truthfully. Dismissal does not cancel delivery. |
| Event ordering | Duplicate and older updates cannot regress status or restart a terminal activity; crucial alerts occur once. |
| Destinations | Each variant opens its intended household/delivery; locked, signed-out, deleted-object and unauthorized-account cases protect details. Multiple minimal activities preserve identity. |
| Rendering | Native previews and devices cover each listed mode, Dynamic Island/no Island, long localized status, zero/one/many counts, no data, auth loss, and enlarged text. No essential clipping or color-only status. |
| Accessibility | Accessibility Inspector contrast measurements, VoiceOver activation/order, Voice Control and Switch Control; Dynamic Type/Bold Text/Reduce Motion; iPhone/Watch enlargement and actual target geometry. |
| Other destinations | HomeView across-room and household privacy checks; Watch wrist-up/down and independence; StandBy red; CarPlay control-disabled layout; Mac continuation where supported. |

## Evidence still missing

No implementation, images, deployment target, SDK documentation, WidgetKit/ActivityKit entitlement or availability evidence, backend cadence/SLA, authoritative dispatch/completion schema, push traces, household authorization model, secure-storage audit, or native device tests were supplied. The brief does not establish pickup readiness or ETA. The 5-minute freshness threshold and 120-minute tracking cutoff require product/backend confirmation. Exact HomeView deployment support and every propagated destination need SDK/device verification; local snapshot tables alone do not prove shipping support.

All runtime, GUI, SDK compilation, assistive-technology and device checks above remain unexecuted. Work here was local file inspection and design authoring on Linux. No security, accessibility conformance or delivery reliability certification is implied.
