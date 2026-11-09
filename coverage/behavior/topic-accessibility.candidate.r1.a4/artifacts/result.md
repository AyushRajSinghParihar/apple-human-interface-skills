# iPhone trip checkout accessibility audit

## Decision and scope

Correct all five verified barriers before releasing this checkout. Priority below is an engineering judgment based on ability to complete and recover from booking, not an Apple severity scale. Evidence is only `interface.md`; “verified” means explicitly stated there, not reproduced on a device. This is a framework-agnostic correction specification, not an implementation.

Target: iOS standard app mode. Assistive Access is explicitly outside scope; its special two-confirmation rule does not apply here. “Pay” does not establish Apple Pay integration.

## Ranked verified findings

| Rank | Evidence and effect | Correction and source |
|---|---|---|
| 1 — P0 | Pay is a custom icon with no accessible name. A nonvisual user cannot reliably identify the final action. | Use a visible **Pay** label and accessible name “Pay”, button role, and accurate enabled/busy state. If activation actually opens review rather than pays, name that outcome instead. Keep any duplicate icon decorative. [VoiceOver: Descriptions](https://developer.apple.com/design/human-interface-guidelines/voiceover#Descriptions), [Buttons: Content](https://developer.apple.com/design/human-interface-guidelines/buttons#Content). |
| 2 — P0 | Removing a traveller requires a three-finger swipe, with no onscreen alternative. People unable to perform it cannot correct the booking. | Add a visible **Remove Traveller** button for each traveller, accessible name “Remove traveller, {name}”. Remove the required custom gesture; all activation paths invoke the same operation. [Accessibility: Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility), [Gestures: Custom gestures](https://developer.apple.com/design/human-interface-guidelines/gestures#Custom-gestures). |
| 3 — P0 | Booking failures only play sound. Users who cannot hear or have muted audio miss the failure and cannot understand recovery. | Show persistent, accessible text explaining the known failure and a relevant next action. Sound may supplement it. Preserve entered information. Do not assert “not charged” unless transaction evidence establishes it. [Accessibility: Hearing](https://developer.apple.com/design/human-interface-guidelines/accessibility#Hearing), [Feedback: Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices). |
| 4 — P1 | Body text is fixed at 12 pt and clips at 200% enlargement. Essential checkout content becomes unreadable. | Use semantic body typography with a 17 pt iOS default and preference-driven scaling, including Dynamic Type or equivalent behavior and Bold Text. Wrap text, grow containers, stack rows, and allow scrolling so content/actions survive enlargement. 12 pt is above the supplied guide’s 11 pt minimum: it is not a proven minimum-size violation. The confirmed failure is clipping; the default size is also poorly suited to body reading. [Typography: Ensuring legibility](https://developer.apple.com/design/human-interface-guidelines/typography#Ensuring-legibility), [Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type), [Layout: Adaptability](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability). |
| 5 — P1 | Availability uses only red versus green text. Users who cannot distinguish the hues lose departure status. | Display “{time} — Available” or “{time} — Unavailable” and expose the same status semantically. Keep color supplementary. Represent selection separately from availability. [Color: Inclusive color](https://developer.apple.com/design/human-interface-guidelines/color#Inclusive-color), [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |

Ranks 1–3 are task blockers for different users, not reasons to postpone 4–5. Three-finger swipe direction is unspecified: left/right would also conflict with iOS undo/redo; actual conflict is unverified. Avoid the binding regardless. See [Gestures: iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/gestures#iOS-iPadOS).

## Corrected interaction contract

Control inventory: Pay → Buttons and VoiceOver; Remove Traveller → Buttons and Gestures; departure-time options → Buttons as candidate activation surfaces, with Accessibility/Color state semantics. The specification does not reveal whether departures are selectable rows or merely read-only labels, so a specific picker or segmented-control implementation cannot be inferred. If interactive, inspect its actual selection component before implementation; if read-only, expose time and status as text rather than inventing a button. Body → Typography/Layout; failure message → Feedback/VoiceOver.

Proposed structure follows the task: Checkout title, Departures, Travellers, booking summary, Pay, and nearby booking outcome. These sections/order are design proposals, not observations. Group each time with its status and each traveller with its removal action; expose meaningful headings. Changes must update accessible values and notify assistive technology. [VoiceOver: Navigation](https://developer.apple.com/design/human-interface-guidelines/voiceover#Navigation).

```text
renderBody(content):
  use semantic body role, default 17 pt, user-adjusted size and weight
  wrap essential text; use content-driven height
  stack adjacent content when it no longer fits; scroll to all actions

renderDeparture(time, availability, selected):
  visibleText = time + " — " + availability
  accessibleText = same time and status
  if selectable:
    expose selection role/state independently of availability
    prevent committing an unavailable departure; keep its status discoverable

renderTraveller(traveller):
  show traveller.name and button("Remove Traveller")
  button.name = "Remove traveller, " + traveller.name
  on supported activation: remove that traveller from this booking
  update traveller summary; move focus to next traveller or Travellers heading
  notify removal without leaving focus on a deleted element

renderPay():
  button(label="Pay", accessibleName="Pay", role=button)
  preserve perceivable focus, press feedback, and current availability

onPay:
  guard against duplicate submission
  state = submitting; expose busy state and "Booking…" text
  on confirmed success: show durable booking confirmation
  on confirmed failure:
    state = failed
    retain departure/traveller data
    show persistent failure reason and a valid recovery action
    expose message to assistive technology; avoid repeated announcements
  on unknown transaction outcome:
    state = unresolved
    explain uncertainty and offer status checking before another payment
```

Busy/outcome handling and retaining input are proposed recovery safeguards, not additional verified defects. Use an in-button activity indication if submission is delayed, with accessible status text; duplicate handling and truthful results require transaction integration. [Buttons: iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS), [Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback).

Adopt at least 44 × 44 pt activation regions with adequate separation for Pay and removal buttons; let labels wrap and targets grow. This is a proposed target, not a finding about current geometry. The accessibility guide lists a 44 × 44 pt iOS default and 28 × 28 pt minimum; the buttons guide says general hit regions should be at least 44 × 44 pt. Use the conservative 44 pt target here rather than treating 28 pt as a comfortable default. [Accessibility: Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility), [Buttons: Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices).

## Worked before/after

Illustrative values below are test fixtures, not supplied trip data.

**Before:** At 200%, body copy clips. “09:00” appears red and “10:00” green, with no other distinction. Alex can only be removed with a three-finger swipe. Pay is an unnamed icon. A rejected booking plays only a sound.

**After:** The same trip remains readable in growing, stacked rows. The screen reads “09:00 — Unavailable” and “10:00 — Available”; selecting 10:00 exposes its selected state. Alex’s row has a visible Remove Traveller button, announced as “Remove traveller, Alex”. After activation, Alex disappears, the summary updates, and focus has a defined surviving destination. The visible Pay button is named “Pay”. A confirmed rejection shows a persistent “Booking could not be completed. {known reason}” message with the applicable recovery action. Data remains available to correct. With sound muted and without color discrimination, the user can still understand and finish or recover from this task.

## Prioritized test and acceptance plan

All execution checks below are **not executed**. Apply the same end-to-end scenario: read departures → choose an available departure → inspect/remove a traveller → review → pay → recover from failure → confirm success. Record build, device/OS, dimensions, settings, observations, and failures for each run.

| Order | Check | Acceptance |
|---|---|---|
| 1 | Inspect implemented semantics and activate Pay with VoiceOver on a supported iPhone. | Name matches visible action; button role/state is accurate; action is reachable and submits once. No decorative duplicate stop. |
| 2 | Remove the fixture traveller using touch, VoiceOver, Switch Control, Full Keyboard Access, and AssistiveTouch as applicable. | Visible removal works without custom multi-finger input or speech; correct traveller is removed; summary updates; focus lands predictably on surviving content. System gestures remain available. |
| 3 | Inject a confirmed booking rejection with sound muted; repeat nonvisually. Also test delayed, successful, and unknown outcomes. | Persistent readable reason/recovery survives long enough to navigate; assistive users discover the update; input survives; no false success or unsupported charging claim; no duplicate payment. |
| 4 | Check default, 200% of corrected baseline (17 → 34 pt for an equivalent scaling test), every supported text category including largest accessibility size, and Bold Text. Include smallest supported viewport and portrait/landscape where supported. | Full essential content and labels remain available; no clipping/overlap; departure status, removal, Pay and recovery remain reachable. Passing 200% alone does not establish largest-category support. |
| 5 | Inspect departures without hue cues and with VoiceOver. | Available/unavailable and selected states are independently understandable; unavailable options cannot be committed; status stays discoverable. |
| 6 | Measure rendered foreground/background pairs and actual activation bounds; run light/dark and Increase Contrast variants. | Save calculator inputs, font size/weight, appearance and results. Local guide’s Inspector table: text up to 17 pt all weights 4.5:1; 18 pt all weights 3:1; bold text any size 3:1. Preserve this table’s stated scope; it is not proof of full WCAG conformance. If default contrast falls short, Increase Contrast supplies a higher-contrast scheme. Buttons meet the adopted 44 × 44 pt target with no overlapping regions. |
| 7 | Complete the entire corrected task nonvisually, including headings/navigation and dynamic changes; inspect with Accessibility Inspector in an available Apple environment. | Logical locale reading order, meaningful grouping/current states, no unreachable required action, no focus loss or trap. Log actual spoken output and focus transitions. |

Contrast guidance: [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). Prefer adaptive semantic color roles or equivalent tested light/dark/increased-contrast tokens; no palette can be selected or measured from the supplied evidence.

## Evidence status and limits

- **Passed — static audit only:** inspected `interface.md`; each ranked finding has explicit specification evidence; produced a correction contract and acceptance plan. Installed root skill, relevant family routes, topic procedures and supporting local guide passages were read. Topic index was searched before finalizing the route.
- **Failed — supplied design specification:** unnamed Pay; gesture-only removal; sound-only failure; clipping at 200%; color-only availability. These are not device reproductions.
- **Not executed / unknown:** corrected rendering, actual focus/rotor order, announcements, activation geometry, contrast ratios, gesture recognition/conflicts, payment behavior, physical comfort, accessibility preference behavior, SDK compilation, GUI/device and assistive-technology tests. No screenshots, implementation, palette, runtime or test harness were supplied.

Guidance route: Foundations → Accessibility, Typography, Color and Layout; Menus and actions → Buttons; Inputs → Gestures; Patterns → Feedback; Technologies → VoiceOver. Official links identify the source of material advice; only installed local snapshots were consulted, with no web access. The package is derived guidance, not an SDK reference or an independently verified current conformance certification. No Apple SDK is assumed, and no accessibility execution or certification is claimed.
