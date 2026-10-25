# Pickup summary and delivery activity — design contract

Design specification based on `interface.md` and the installed local HIG snapshot dated 2026-10-25. No web lookup, implementation, SDK validation, simulator, GUI, device or accessibility execution was performed. Examples below are proposed copy, not observed delivery events.

## Decisions and boundaries

The widget answers **“What pickup information can the household safely see?”** The Live Activity answers **“What is happening to the delivery I am following?”** Keep periodic pickup data separate from an 80-minute bounded delivery. Do not infer that a parcel is ready for pickup from the supplied address or delivery duration; the brief supplies no readiness event or current delivery stage.

Replace second-by-second widget refreshes with meaningful timeline entries and system-controlled refresh opportunities. Use the Live Activity for changed delivery events, without promising second-by-second network delivery. Replace the inline accessory’s Accept, Cancel and Details targets with one details destination. These choices follow [Widgets: updating and interactivity](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content).

A shared Apple HomeView Modular face is household-visible even when its data originates on one member’s iPhone. It uses a small-family widget, not a watch-face accessory. Keep personal recipient, street address and gate code out of every widget and Live Activity payload, preview, accessible label and deep-link URL. “Private Live Activity” means personal event selection and minimized content, not a guarantee that the Lock Screen is private. Details require authenticated app access. See [Widgets: Apple HomeView](https://developer.apple.com/design/human-interface-guidelines/widgets#Apple-HomeView), [Live Activities: best practices](https://developer.apple.com/design/human-interface-guidelines/live-activities#Best-practices), and [Privacy: protecting data](https://developer.apple.com/design/human-interface-guidelines/privacy#Protecting-data).

## Widget: Household pickups

Configuration: choose a household and explicitly enable “Share pickup summary,” with explanation “Everyone viewing the shared face can see pickup counts and status.” Default shared publication is off. Select only parcels authorized for this household; private parcels do not contribute to counts. No shared configuration may enable recipient names, address, codes or item descriptions. A member’s personalized HomeView Home Screen remains distinct from the single shared Modular face; this product deliberately uses the same safe summary on both.

| Surface / family | Content in priority order | Activation |
|---|---|---|
| iPhone Home Screen / system small | “Household pickups”; large “1 ready” only after verified readiness; freshness line | Open selected household pickup list |
| HomeView Modular / system small | Same summary; larger count/status, removable background, no secondary controls | Open safe household pickup summary in the supported app context; private detail requires personal authenticated continuation |
| iPhone Lock Screen / accessory rectangular | “Pickups · 1 ready”; “Updated 2 min ago” | Open household pickup list after system access requirements |
| iPhone Lock Screen / accessory inline | “Pickups: 1 ready” when fresh; “Pickups: update needed” when stale | One target to the same pickup list; no simulated buttons |
| Optional watch glance / accessory rectangular in Smart Stack | “Pickups”; count/status; short freshness line | Corresponding pickup list in a watch app if supplied; defer this widget variant until that destination exists |

No watch-face complication is proposed; a future face placement requires its own Complications route. The delivery Live Activity can already provide a paired-watch Smart Stack glance as specified below. Supported family/context decisions come from [Widgets: anatomy and platform considerations](https://developer.apple.com/design/human-interface-guidelines/widgets#Anatomy); watch responsibility follows [Designing for watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices).

**Concrete supplied-data rendering:** no pickup readiness is known. Show:

> Household pickups  
> Status unavailable  
> Last update 35 min ago

If an actual prior snapshot contains a ready count, stale rendering instead reads “Last known: 1 ready” and “Updated 35 min ago · Check in app.” Never manufacture that count from the supplied parcel. At the largest text size, retain “Update needed” and the single app destination before optional headings or decoration.

Fresh ready example: “Household pickups / 1 ready / Updated 2 min ago.” Verified empty example: “No pickups ready / Updated 2 min ago”; unavailable data must never become a zero count. Gallery description: “Check household pickups.” Gallery previews use labeled simulated safe data, including the stale variant. Initial placeholder retains the title with placeholder blocks; prolonged absence becomes “Pickup status unavailable.”

## Freshness and connectivity contract

The following thresholds are **product decisions**, not Apple requirements: pickup data becomes stale after 15 minutes; active-delivery data after 5 minutes, or earlier when the server’s validity ends. Store source timestamp separately from fetch timestamp. A cache read or failed refresh never resets source age. Reject older event revisions; reject implausible future timestamps as unavailable until reconciled.

| Condition | Widget | Live Activity | Recovery |
|---|---|---|---|
| Fresh valid data | Verified count/status and source age | Verified stage and valid arrival window | Apply newer authoritative revisions only |
| Refresh in progress | Keep last known content and original age | Keep current content while validity holds | No blanking or fake progress |
| Stale, connection unknown | “Last known…” plus age; inline “Update needed” | “Update delayed”; last confirmed stage and age; hide ETA | Request update when allowed; open exact app context |
| Connection failure actually observed | “Offline · Last update 35 min ago” with last known state if any | “Offline · Update delayed”; source age; no ETA | App offers Retry; restore freshness only after successful authoritative update |
| No usable cached data | “Pickup status unavailable” | “Delivery status unavailable” | Open app; explain failure and retry there |
| Signed out / revoked membership | “Open app to set up pickups”; clear household cache | End associated activity and remove private local event association | Authenticate and recheck authorization; never reveal cached household data |
| Sharing disabled / no household selected | “Choose a household in the app”; no counts | No effect on separately authorized personal delivery | Explicit setup in app |

Age alone does not prove offline. With the supplied 35-minute update and no connectivity evidence, use **stale**, not “Offline.” Retain the last successful snapshot during errors. Schedule a stale-state timeline entry at expiry and request reloads on meaningful server changes; actual widget execution is system-controlled. Always show source age or “Last known” where delayed reload could otherwise imply freshness. System date presentation may update the age without network polling. On app entry, revalidate and expose Retry if needed. See [Widgets: updating content](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content).

## Private bounded delivery Live Activity

Start from the authenticated delivery detail when the person chooses “Follow delivery,” once an active event is confirmed; explain that safe delivery status can appear on the Lock Screen and paired displays. Respect unavailable/disabled system capability with the same status in the app. Provide “Stop following” in delivery detail; this ends tracking without cancelling the delivery. Do not start from the 35-minute-old snapshot alone.

Event data: opaque delivery ID, monotonic revision, confirmed stage, source timestamp, validity deadline, optional arrival window, event start, and planned monitoring end. Shared pickup publication uses a separate authorization and sanitized model. Do not collect location, contacts, camera, microphone or HomeKit access for these glances; logistics status comes from existing authorized service data.

**Lifecycle:** not followed → confirmed active → followed → delivered / cancelled / failed / monitoring expired → ended. Freshness is an independent state while followed. Example confirmed stages are “Preparing,” “On the way,” and “Arriving”; they change only on server evidence. Do not draw an elapsed-time percentage as physical delivery progress. The supplied 80 minutes is the planned event duration, not an arrival guarantee. At start + 80 minutes without terminal confirmation, end with “Tracking window ended · Open app for latest status,” never “Delivered.” A new bounded follow session requires a new confirmed event window and explicit user action.

On confirmed delivery, cancellation or failure, end immediately. Keep a safe terminal Lock Screen summary for 15 minutes, then remove it; Dynamic Island and CarPlay remove the ended activity immediately. Stop following, sign-out and access revocation request immediate removal without retained summary. Request termination through server and local paths as available; expiry/ending while offline must be verified against actual SDK/runtime support and must not rely on app foreground execution. The UI must still mark updates stale if an end signal is delayed. Apple recommends clearly bounded activities, ideally no more than 8 hours, with immediate ending and a shorter useful retained summary; 80 minutes fits that design guidance. See [Live Activities: lifecycle](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity).

| Presentation | Fresh example (simulated) | Stale/offline replacement |
|---|---|---|
| Compact Dynamic Island | Leading parcel + stage symbol; trailing “12–20m” only with valid server ETA | Leading parcel + warning symbol; trailing “Stale” or “Offline”; omit stage if needed for fit |
| Minimal, including multiple activities | Parcel + stage/check/warning glyph conveying current state, rather than logo alone | Parcel + warning; accessible description includes update delay |
| Expanded | Top leading parcel + “Delivery”; top trailing valid arrival window; below confirmed stage and source age | Same identity positions; “Update delayed” or “Offline”; “Last confirmed: On the way”; “Updated 35 min ago”; omit arrival window |
| Lock Screen | “Delivery”; prominent confirmed stage; valid arrival window; source age; one “Details” link | “Delivery / Update delayed / Updated 35 min ago / Details”; add last known stage only when known |

All taps, including both compact halves, resolve the opaque delivery ID to the same authenticated delivery detail, preserving context through interruption and sign-in. “Details” is the only action; Accept and Cancel remain inside authenticated detail after current-state validation. No cancellation or acceptance is queued silently while offline. Multiple deliveries retain independent opaque IDs; minimal presentations remain distinguishable by accessible event labels without exposing recipient/address.

Updates occur only for changed content, validity or lifecycle; no one-second polling, fake live spinner, or speculative countdown to delivery. Alert once for a confirmed crucial arrival/action-needed event, subject to user/system settings; do not issue a duplicate push. Staleness alone is a quiet status change. [Live Activities: presentation and interactivity](https://developer.apple.com/design/human-interface-guidelines/live-activities#Presentation).

## Appearance, privacy and continuation

Use semantic system text styles: headline for status, body for detail, caption for freshness, medium/semibold for essential Live Activity text. Use actual text and scalable symbols. Stack source age beneath status, remove optional heading/detail before essential state, and grow expanded/Lock Screen content within system constraints. Keep fixed-family widget layouts flexible instead of assuming one production canvas. Preserve core stale/unknown wording through long text, Bold Text and large text. [Typography: Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type).

Full color: semantic foreground/background. Accented: primary group holds state and freshness; accent group holds only supporting parcel identity. Vibrant: opaque grayscale values preserve hierarchy. Test light/dark, tinted/clear and removed backgrounds. HomeView Modular and StandBy use background removal and readable large summaries; red monochrome Night Mode retains written stale state. Do not use color alone for ready/offline/stale. Only Lock Screen Live Activity gets a restrained custom background; Dynamic Island backgrounds remain system-owned. See [Widgets: rendering modes](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes) and [Live Activities: colors](https://developer.apple.com/design/human-interface-guidelines/live-activities#Choosing-colors).

Always On pairs: active shows status, freshness and Details; dimmed preserves positions and safe status, reduces secondary emphasis, and does not animate. No names, address or code appear in either. Resume preserves selected event. Respect system privacy redaction, using “Delivery update / Open app for details” if needed. Always On support depends on hardware/OS; the local guide’s specific device examples are not a complete current support list. [Always On](https://developer.apple.com/design/human-interface-guidelines/always-on#Best-practices).

Paired watch Live Activity: use default Smart Stack composition with stage/valid arrival window or “Update delayed”; tap opens watch detail if available, otherwise system full-screen continuation with paired-iPhone launch. No independent watch app is assumed. StandBy uses the safe Lock Screen layout scaled for distance and red-mode legibility. CarPlay shows readable status without depending on buttons/toggles, which are disabled there. Paired Mac activation follows system iPhone Mirroring. Do not promise Live Activity support on HomeView, tvOS or visionOS from this guide; HomeView receives the summary widget. [Live Activities: destination qualifications](https://developer.apple.com/design/human-interface-guidelines/live-activities#Platform-considerations).

Privacy data-purpose matrix:

| Data | Purpose / location | Access policy |
|---|---|---|
| Household authorized pickup count and timestamp | Shared glance, sanitized widget cache | Explicit sharing selection; exclude private parcels; purge on revocation |
| Delivery stage, timestamp, valid arrival window | Personal bounded activity | Followed event only; safe even when externally visible |
| Recipient and street address | Identify destination in app | Authenticated authorized detail only |
| Gate code | Entry instruction in app | Authenticated explicit reveal; encrypted secret storage where cached; never surface payload or URL |

This minimizes exposure; it does not certify security. Shared caches and already-rendered snapshots may persist until system refresh/removal. Revocation propagation and secure cache deletion require implementation evidence. [Privacy: best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices).

## Acceptance checks and evidence status

**Passed — specification inspection only:** supplied 35-minute snapshot is explicitly stale; unknown readiness stays unknown; no unsupported one-second widget promise; shared/public surface content excludes recipient/address/code; inline has one destination; delivery has a bounded lifecycle and terminal behavior; compact/minimal/expanded/Lock Screen and paired-watch contracts exist. The commands read the installed root, selected families, topic procedures and local references; no external sources were fetched.

**Failed — supplied proposal:** full address/code on shared face exposes private information; one-second widget refresh promises continuous behavior the widget contract cannot guarantee; independent Accept/Cancel/Details inline targets conflict with its single target. These are brief-level findings, not observed runtime failures. The replacement specification resolves them on paper.

**Not executed — implementation acceptance gates:**

| Check | Expected observable result / missing evidence |
|---|---|
| 35-minute snapshot, refresh failure and recovery | Stale visible; age unchanged after cache read/failure; Offline only after observed failure; newer authoritative revision restores fresh state. Need state reducer fixtures and runtime evidence. |
| Expiry while backgrounded/offline | Widget retains honest source age; activity invalidates ETA and ends bounded monitoring; delayed push cannot resurrect terminal event. Need SDK-supported lifecycle design and timed disconnected-device run. |
| Completion and opt-out | End immediately; 15-minute summary only for terminal outcomes; Stop following never cancels delivery. Need server events and actual activity dismissal observations. |
| Routing/auth | Each target opens correct household/event; sign-in preserves destination; revoked user cannot view old detail; no secret in URLs. Need implemented routes and authorization tests. |
| Privacy | Shared face, gallery, dimmed screen, accessible labels and paired surfaces contain no private fields; sharing/revocation reflected. Need payload/cache inspection and multi-account household-device tests. |
| Rendering | Status/freshness readable in light/dark, accent, clear, vibrant, background removal, Night Mode and Always On; Dynamic Island limited-width layout fits without lost warning. Need native previews/screenshots and physical viewing checks. |
| Text and access | Check supported Dynamic Type sizes through AX5 on iPhone widgets, at least 200% text on iPhone and 140% on watch per local guidance; long/localized labels preserve essential status. VoiceOver announces status then freshness then destination; no secret labels. Need actual native text layouts, VoiceOver and assistive input execution. |
| Contrast and activation | Measure actual foreground/background pairs; use iOS/watchOS 44 × 44 pt default control areas where app controls are provided; system accessory targets use native family behavior. Need measured contrast/geometry, Increase Contrast checks and device usability. |
| Alerts / competing activities | One crucial event produces one alert; no duplicate push; minimal state communicates current status with other activities present. Need push logs and multi-activity device run. |

Accessibility values are scoped guidance from [Accessibility: vision and mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision), not evidence of conformance. No runtime checks are claimed passed.

Still missing: actual pickup readiness and confirmed delivery stage; backend freshness/ETA guarantees and event timestamps; meaning of Accept and cancellation rules; household membership and sharing authorization model; supported OS/hardware/SDK versions; whether watch app and HomeView app continuation exist; secure storage and revocation behavior; all native renderings, measurements and execution above. The 15/5-minute freshness thresholds and 80-minute monitoring cutoff require product/backend approval before implementation. Local snapshot source links document rationale; current API availability remains unverified under the local-only constraint.

## Local routing audit

Resolved under `.agents/skills/apple-hig/`: root `SKILL.md` → topic-index search → `subskills/apple-hig-getting-started/SKILL.md` with Designing for iOS and Designing for watchOS topic procedures before their references; `apple-hig-system-experiences/SKILL.md` with Widgets and Live Activities procedures before their references; `apple-hig-foundations/SKILL.md` with Privacy, Accessibility and Typography procedures before their references; `apple-hig-technologies/SKILL.md` with Always On procedure before its reference. Each file read used a separate `cat`, `sed`, or `rg` command. Typography reference use is limited to relevant prose rather than freezing its size tables into a layout.
