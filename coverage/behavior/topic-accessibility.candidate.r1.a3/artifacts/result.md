# iPhone trip checkout accessibility audit

This is a specification audit of `interface.md`, for iOS standard app mode. Five barriers are verified by the supplied description. The corrections below are proposed behavior, not implemented or device-tested behavior. Priority reflects task impact and is an audit decision, not an Apple severity classification. All five should be corrected before checkout release.

## Prioritized findings and decisions

| Rank | Verified evidence and task effect | Corrected behavior | Source support |
|---|---|---|---|
| 1 — P0 | Pay is a custom icon with no accessible name. People relying on spoken control identification cannot reliably identify the payment action. | Show a visible **Pay** label and expose accessible name “Pay”, button role, enabled/busy state, and activation action. Retain an icon only as supplementary decoration. Activation must have perceivable press feedback. | [Buttons: Content and Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Content); [Accessibility: Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility). |
| 2 — P0 | Removing a traveller requires a three-finger swipe with no onscreen alternative. This blocks correction for people unable to perform the gesture. | Add a visible **Remove traveller** button in each traveller section; accessible name includes the traveller’s displayed identifier. Remove the required custom three-finger gesture. | [Accessibility: Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility); [Gestures: Custom gestures and iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/gestures#Custom-gestures). |
| 3 — P1 | Body text is fixed at 12 pt and clips at 200% enlargement. Enlarged checkout information becomes unreadable. | Use a scalable semantic body role, with 17 pt at the default iOS size as the design baseline. Support at least 200% enlargement and all supported accessibility text sizes. Wrap text, grow rows, stack status/actions, and allow vertical scrolling so essential content and Pay remain reachable. Support equivalent Bold Text behavior. | [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision); [Typography: Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type). |
| 4 — P1 | Available departures are green only; unavailable departures are red only. Availability cannot be reliably distinguished without color perception. | Display “Available” or “Unavailable” beside every time, and expose that status semantically. Keep color supplementary. Expose selected state separately from availability. | [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |
| 5 — P1 | Booking failures play only a sound. A person who cannot hear it receives no failure explanation. | Show persistent text “Booking failed” with the actual known reason and an appropriate recovery action. Expose the message to assistive technology when it appears. Retain sound only as supplementary feedback; haptics may supplement it. | [Accessibility: Hearing and Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Hearing). |

The 12 pt size is above the local guide’s 11 pt iOS minimum; it is not a verified minimum-size violation. The confirmed failure is clipping at 200%, with fixed small body text also departing from the 17 pt default baseline. A three-finger horizontal swipe has a documented undo/redo meaning; direction is unspecified here, so an actual system gesture collision is a risk to inspect, not an additional verified defect.

## Control mapping and implementation decisions

- **Pay and traveller removal → Buttons procedure:** immediate commands. Name the outcome and affected traveller. Pay is the prominent action; removal is secondary. Removal concerns checkout membership; permanent deletion, reversibility, and backend consequences are unspecified. Do not invent a destructive confirmation requirement.
- **Departure choices → candidate Pickers procedure:** an ordered, single-choice set. Control type and option count are unknown, so there is no verified picker-style defect and no mandate to install a native date picker. Preserve supplied departures and their identifiers rather than allowing arbitrary time entry. Specify name/time, availability, selected state, and choice activation independently of rendering.
- **Required swipe → Gestures procedure:** replace the essential gesture dependency with the visible removal command. Preserve system gesture meanings.
- **Body/status/error text → Accessibility and Typography procedures:** preserve content, readable hierarchy, semantic status, and usable actions at enlarged sizes. The failure message needs no assumed modal alert; use persistent inline feedback in the checkout context.

For Pay and removal, choose activation regions of at least 44 × 44 pt with clear separation. No existing dimensions are known. The local accessibility guide lists 44 × 44 pt as the iOS default and 28 × 28 pt as its minimum, while the Buttons guide says general hit regions should be at least 44 × 44 pt. Use the conservative 44 pt target here; neither number proves the supplied control fails. See [Buttons: Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices).

## Worked before/after contract

Illustrative times and traveller name below are test fixtures, not supplied product data.

**Before:** At 200% body text clips; “09:00” is green and “10:00” red with no other distinction. Alex can be removed only by a three-finger swipe. Pay is an unnamed icon. A failed booking produces a sound and no message.

**After:** At default size, scalable body text starts at 17 pt. At 200% it is 34 pt for an equivalent linear custom scale; rows expand and actions stack. Actual Dynamic Type categories must also be tested rather than treated as a linear multiplier. A departure reads “09:00 — Available”; another reads “10:00 — Unavailable”. Alex’s section contains a visible “Remove traveller” button named “Remove traveller Alex”. The primary button reads and is named “Pay”. After a simulated failure, visible persistent text reads “Booking failed. [Known reason]”, with an appropriate recovery action.

Framework-agnostic contract (product choices beyond the verified fixes are explicit):

```text
renderCheckout(textPreference, boldPreference):
  body = scalableRole("body", defaultIOSPoints=17)
  honor(textPreference, boldPreference)
  layout = wrapping, contentSizedRows, verticalScroll
  when space is insufficient: stack status and actions
  never clip essential text or hide an essential action

for departure in suppliedDepartures:
  show(localizedTime(departure), textAvailability(departure))
  expose(name=localizedTime(departure), value=availability,
         selected=(departure.id == selection))
  activation selects only an available departure
  unavailable choices remain understandable and nonselectable
  # Proposed validation policy; current selection behavior is unknown.

for traveller in travellers:
  button(visible="Remove traveller",
         accessibleName="Remove traveller " + displayedIdentifier(traveller),
         role=button, targetAtLeast=44x44pt):
    removeFromCheckout(traveller.id)
    preserve(otherTravellers, departureSelection)
    refreshSummaryFromActualData()
    moveFocusTo(nextTravellerOrTravellersHeading)
    exposeStatus("Traveller removed")

button(visible="Pay", accessibleName="Pay", role=button):
  if requestInFlight: ignoreDuplicateActivation()
  else:
    preserveCheckoutInputs()
    state = pending
    showInButtonActivityAndText("Booking…")
    exposeBusyState()
    submitOnce()

onBookingResult(result):
  if confirmedSuccess:
    showAndExposeConfirmedBooking()
  else:
    state = failed
    showPersistentText("Booking failed", actualKnownReason)
    announceMessageOnceWithoutRepeatedFocusInterruption()
    preserveCheckoutInputs()
    offerRecoveryAppropriateToKnownTransactionState()
    # Retry only when safe; reconcile uncertain payment/booking outcomes first.
```

Submission deduplication, input preservation, focus recovery, and transaction reconciliation are proposed robustness decisions, not additional defects established by `interface.md`. Do not assert “not charged” or offer an unsafe repeat payment when the outcome is unknown. No Apple Pay integration is assumed. Standard app mode does not inherit the Assistive Access-specific two-confirmation rule.

## Prioritized correction and acceptance plan

Implement ranks 1–2 first to restore identifiable payment and a reachable correction path, then ranks 3–5. Validate all together on the same journey: inspect availability → select departure → remove a traveller → Pay → receive failure → recover → receive confirmed success.

| Check | Acceptance condition | Current evidence/status |
|---|---|---|
| A1 — Pay naming | Accessibility tree exposes name “Pay”, button role, current state and activation. On a supported iPhone, VoiceOver identifies and activates it; visible label agrees. | Specification **fails** name requirement; corrected implementation not executed. |
| A2 — Removal alternative | Remove Alex through the visible control without any multi-finger gesture. Only Alex leaves checkout; summary updates; focus remains on a meaningful surviving element. | Specification **fails** onscreen-alternative requirement; corrected path not executed. |
| A3 — Enlargement | At 100%, 200%, and every supported larger accessibility category, all essential text is readable and Pay/removal remain reachable without overlap or clipping. Repeat with Bold Text and narrow supported iPhone width. | Specification **fails** at 200%; other sizes, corrected layout and rendering not executed. |
| A4 — Color independence | With color removed from a test rendering, each departure’s availability and selection remain distinguishable in text/semantics. Unavailable choices cannot be committed under the proposed policy. | Specification **fails** redundant availability cue; selection behavior not supplied or executed. |
| A5 — Failure feedback | With sound muted, inject a known booking failure. Persistent text states failure and known reason; assistive technology receives the update; recovery preserves inputs and does not duplicate submission. | Specification **fails** visual/text feedback; announcements and recovery not executed. |
| A6 — Complete alternative-input path | On supported Apple hardware, complete the journey using VoiceOver, Switch Control, Full Keyboard Access and AssistiveTouch as applicable; verify every essential control is reachable, identified and activatable. No required custom gesture or speech. | **Not executed**; actual focus order is unknown. |
| A7 — Geometry and states | Measure actual activation regions in pt: proposed Pay/removal targets ≥44 × 44 pt, separated and nonoverlapping even with enlarged labels. Verify custom press feedback, busy and unavailable states. | **Not executed**; no geometry or implementation supplied. |
| A8 — Contrast | Obtain actual foreground/background colors and weights; calculate contrast for text, status and controls in light/dark appearances and Increase Contrast. Record pairs, ratios and calculator. | **Not executed**; no colors or screenshots supplied. |

For A8, the installed Accessibility guide’s Inspector table states 4.5:1 for text up to 17 pt at all weights, 3:1 at 18 pt at all weights, and 3:1 for bold text at any size. Preserve that table’s scope; it does not by itself establish WCAG conformance. If default colors fall short, specify an Increase Contrast treatment. Do not diagnose poor contrast from “red” and “green” alone. See [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

## Evidence limits and completion record

**Passed — static audit checks:** read the supplied interface specification; explicitly read the installed root skill; followed family → topic procedure → supporting guide order for Accessibility, Typography, Buttons, Gestures and candidate Pickers. Each file read used its own shell command. Mapped supplied controls to candidate component procedures and produced a corrected behavior contract with acceptance conditions.

**Failed — specification checks:** A1–A5 each have the verified barrier recorded above. These are description-level findings, not observed device failures.

**Not executed:** all runtime acceptance checks, accessibility-tree inspection, actual focus traversal, announcements, input activation, geometry measurements, contrast calculation, device readability/comfort, native rendering, SDK compilation and backend transaction tests. No implementation, screenshots, colors, focus order, SDK or device evidence was provided. There is no basis to claim overall accessibility conformance or App Store accessibility-label eligibility.

Only local `interface.md` and installed instructions/guides were used. Official links identify the source articles and sections recorded in the local snapshot; they were not opened or verified online. No GUI, device, SDK, browser or assistive-technology execution was performed. The result is a framework-agnostic audit and specification, ready for implementation and subsequent testing on a supported Apple environment.
