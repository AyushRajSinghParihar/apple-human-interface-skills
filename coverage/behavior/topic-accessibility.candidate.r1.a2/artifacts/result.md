# iPhone trip checkout accessibility audit

This is a specification audit of `interface.md`, not a running application. All five findings below are verified statements in that file; their runtime severity and the proposed fixes still require validation. Priority reflects task impact and implementation sequencing, not an Apple severity classification.

## Prioritized corrections and decisions

| Rank | Verified evidence and consequence | Correction and corrected behavior | Guidance |
|---|---|---|---|
| P0 · 1 | “Pay is a custom icon with no accessible name.” A person using spoken control identification cannot reliably identify the payment action. This can block checkout. | Show a text label **Pay** (optionally retain the icon). Expose the button role, accessible name “Pay”, and enabled/busy state. Keep the icon decorative when redundant. Payment activation must work through accessible activation as well as touch. | Accessibility: Vision, Mobility |
| P0 · 2 | “Booking failures play a sound with no visual or text message.” A person who cannot hear the sound receives no failure explanation or recovery direction. | Present persistent text “Booking failed” with an accurate explanation when known and a labeled recovery action. Expose the message to assistive technology and announce the failure once. Retain entered checkout data. Sound may supplement the message. Do not offer another charge attempt until the payment outcome is known. | Accessibility: Hearing, Cognitive; recovery/state handling is an audit design decision |
| P1 · 3 | “Body text is hard-coded to 12 pt and clips when enlarged to 200%.” Essential information may become unreadable at the size a person needs. | Use a scalable body style, starting from the iOS 17 pt default, and support at least 200% enlargement. Reflow into vertical rows, allow wrapping and scrolling, and grow containers. Keep prices, status and actions available. **12 pt is above the cited 11 pt iOS minimum; it is not independently a minimum-size violation.** The confirmed failure is clipping, with a small body default also needing correction. | Accessibility: Vision |
| P1 · 4 | “Unavailable departure times are indicated only with red text, available ones only green.” People unable to distinguish the colors cannot determine which departure they can book. | Add visible and accessible “Available” / “Unavailable” text to each time. Expose selection and availability as distinct states. Prevent selecting unavailable times; retain their status for discovery. Color can remain a secondary cue. | Accessibility: Vision |
| P1 · 5 | “Removing a traveller requires a three-finger swipe with no onscreen alternative.” People unable to perform that gesture cannot edit their booking. | Add a visible “Remove traveller” button per traveller, with an accessible name that includes the traveller’s displayed name. Support ordinary activation. Remove the required three-finger interaction; any optional gesture must have the same result as the button and preserve system accessibility gestures. | Accessibility: Mobility, Speech |

Official source links for these recommendations: [Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision), [Hearing](https://developer.apple.com/design/human-interface-guidelines/accessibility#Hearing), [Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility), [Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Speech), and [Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive). Links identify the source of the installed guidance; no web content was fetched.

Use 44 × 44 pt activation areas as the iOS default starting point for Pay, removal and recovery controls, with sufficient separation. The local guidance also lists a 28 × 28 pt minimum; this is not a recommendation to shrink checkout controls. Geometry was not supplied, so undersized targets are **not** a verified finding.

Standard iOS mode is explicit. Do not import Assistive Access’s one-interaction-per-screen or two-confirmation rules into this checkout. A removal confirmation is not established as necessary by the supplied evidence. Offer Undo as a product choice if removal would otherwise be costly to reverse.

## Worked before/after contract

The times and traveller name below are illustrative fixtures, not facts about the supplied interface.

**Before:** A red “09:00” and green “10:00”; fixed 12 pt body text; an unnamed payment icon; a traveller removable only with three fingers. A failed booking emits a sound. At 200% text enlargement, text clips.

**After:** Rows read “09:00 — Unavailable” and “10:00 — Available”. The selected available row also communicates “Selected”. Traveller “Alex” has a visible “Remove traveller” button whose accessible name is “Remove traveller Alex”. Body text scales and wraps. A labeled Pay button initiates payment. On a known booking failure, persistent “Booking failed” text and the appropriate recovery action appear; the failure is also available to a screen reader.

Framework-agnostic specification:

```text
layout:
  body base size = 17 pt; follows preferred text scale through at least 200%
  content grows vertically; scroll when needed; no essential text truncation
  controls use 44 × 44 pt default activation areas with adequate separation

for each departure:
  visible text = time + availability word + selected marker when selected
  accessible content = same time, availability, selection
  role = selection option; unavailable cannot be selected

for each traveller:
  visible action = "Remove traveller"
  accessible name = "Remove traveller " + displayed traveller name
  role = button
  activate by touch or assistive action -> remove this traveller
  update review and total; place focus on next traveller or traveller-section heading

pay:
  visible label = accessible name = "Pay"
  role = button; state reflects whether checkout is ready or submitting
  activate when ready -> submitting; reject repeated submission while pending

on known booking failure:
  state = failed
  preserve form values and chosen available departure
  show persistent heading "Booking failed" and accurate recovery text
  expose message and recovery action in reading order
  announce failure once; do not repeatedly interrupt navigation
  allow user to read and dismiss explicitly

on uncertain payment outcome:
  show persistent "Checking booking status" information
  reconcile outcome before enabling another charge attempt
```

The focus destination after removal, single announcement, retained data and duplicate-submission handling are proposed engineering decisions, not claims that Apple prescribes this exact state machine. For ordinary failure updates, keep focus stable and announce the status; do not automatically move focus without a task reason. The actual reading order is unknown and must be checked.

## Acceptance checks and practical test plan

Implement P0 corrections first, then complete all P1 corrections before accessibility sign-off. Validate each correction individually, then run the complete path: review departures → choose an available departure → remove a traveller → review updated checkout → Pay → injected failure → recovery → confirmed result.

| Check | Acceptance criterion | Current status |
|---|---|---|
| Specification inspection | Verify the five reported behaviors against `interface.md`. | **Passed:** each is explicitly supplied. |
| Accessible payment identity | Pay has a meaningful name, button role and accurate state. | **Failed in supplied specification:** name absent; role/state not supplied. |
| Failure perception | With sound muted, failure and recovery remain understandable; assistive navigation can find the message. | **Failed in supplied specification:** sound only. Runtime check not executed. |
| Enlargement | At default, intermediate and at least 200% enlargement, essential text and controls remain readable and reachable without clipping, overlap or obscuring the payment/recovery actions. Exercise scrolling and keyboard appearance where applicable. | **Failed in supplied specification at 200%.** Corrected layout not executed. |
| Noncolor availability | Without using color, users can distinguish available, unavailable and selected departures; unavailable options cannot be booked. | **Failed in supplied specification for availability distinction.** Selection enforcement not supplied. |
| Alternative removal | Each traveller can be removed through a labeled onscreen action, with no complex gesture or speech required. | **Failed in supplied specification.** Corrected action not executed. |
| VoiceOver | On an iPhone build, traverse all content in coherent task order; hear time/status/selection and named actions; activate Pay/removal; perceive failure once; resume recovery without lost context. | **Not executed.** Actual focus order is unknown. |
| Other input paths | With Switch Control, Full Keyboard Access and AssistiveTouch, reach and activate every required action; test Voice Control labels and supported pointer interaction. Preserve accessibility shortcuts. | **Not executed.** Requires supported Apple environment and implementation. |
| Contrast and geometry | Measure actual text/background pairs in light/dark appearances and Increase Contrast. Measure activation areas and separation, then verify comfortable operation on device. | **Not executed:** colors, screenshots and geometry absent. |
| State and recovery | Inject definite failure and uncertain outcome; verify retained data, persistent feedback, updated traveller/price state and no duplicate charge attempts. Complete the flow after recovery. | **Not executed:** no implementation or backend supplied. |

For contrast measurements, preserve the installed guide’s stated Accessibility Inspector table scope: text up to 17 pt at all weights, 4.5:1; 18 pt at all weights, 3:1; bold text at any size, 3:1. These are reported source values, not a replacement for a separate WCAG conformance evaluation. If default colors fall short, specify a higher-contrast Increase Contrast treatment. No ratio can be calculated from “red” and “green” alone.

Use Accessibility Inspector and supported iPhone assistive technologies when an implementation becomes available. Record device, OS, text settings, input method, build and observed result. Run those interactive checks in the user's Apple environment; this headless Linux specification audit does not establish them.

## Evidence and limits

Read the installed root `apple-hig/SKILL.md`, then `subskills/apple-hig-foundations/SKILL.md`, then `.topics/apple-hig-accessibility/SKILL.md`, then its supporting `references/accessibility.md`, resolving paths within `/tmp/hig-eval-nqa_p915/.agents/skills/apple-hig`. `interface.md` is the sole interface evidence.

The Foundations family and Accessibility procedure route text reflow to `.topics/apple-hig-typography/SKILL.md`. Reading that installed path failed; a subsequent hidden-file search found its reference article but no Typography procedure. That article was not read out of procedure order. This audit therefore uses the Accessibility procedure and its source guide’s explicit iOS text-size and enlargement guidance. No detailed VoiceOver procedure was loaded: the semantic contract here uses Accessibility’s name/role/state/task-order guidance; actual spoken grouping and rotor behavior remain unverified.

No source code, screenshots, actual colors, focus order, payment states or device evidence was supplied. No browser, network, SDK, GUI, Accessibility Inspector, device test or assistive-technology execution occurred. Findings are verified **against the specification**, not reproduced defects. Proposed corrections and acceptance checks are not passing runtime results. Animation, localization, haptics, target geometry and other unspecified behavior cannot be classified as defects from this evidence. The local HIG snapshot is dated guidance, not independent proof of current API availability or comprehensive accessibility conformance.
