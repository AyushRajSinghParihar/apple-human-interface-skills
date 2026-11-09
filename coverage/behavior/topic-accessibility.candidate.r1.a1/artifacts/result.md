# iPhone trip checkout accessibility audit

This is a specification audit of `interface.md`, for standard iOS app mode. Five barriers are verified by the supplied description; no implementation or device behavior was tested. Priority reflects task impact, not a formal conformance score. All five should be corrected before release.

## Prioritized findings and decisions

| Rank | Verified evidence and effect | Correction and corrected behavior | Source |
|---|---|---|---|
| 1 — P0 | “Pay is a custom icon with no accessible name.” People using spoken control identification cannot reliably identify the purchase action. Its role and activation support are unknown. | Show a text-labeled **Pay** button; expose accessible name “Pay”, button role, and enabled/busy state. Retain any icon as decoration. Ensure the same payment action is available through touch and assistive activation. | [Accessibility: Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility) |
| 2 — P0 | Booking failures “play a sound with no visual or text message.” People unable to hear the sound lose the failure outcome and recovery information. | Present persistent visible text, “Booking failed,” with an accurate reason and recovery action when known. Expose the message to assistive technology and announce the result once. Preserve entered checkout data. Do not imply success or payment status without a confirmed result. | [Accessibility: Hearing](https://developer.apple.com/design/human-interface-guidelines/accessibility#Hearing), [Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive) |
| 3 — P1 | Available times are green only; unavailable times red only. Availability cannot be determined reliably without color perception. | Each time displays “Available” or “Unavailable” in text; color may reinforce it. Expose the time, status, and selection state semantically. Unavailable times must not book; explain their status rather than silently ignoring activation. | [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision) |
| 4 — P1 | Removing a traveller requires a three-finger swipe with no onscreen alternative. People unable to perform the gesture cannot complete that edit; it can also conflict with assistive gestures. | Provide a visible **Remove traveller** button per traveller with a distinguishing accessible name, such as “Remove traveller, Alex”. The button performs the same removal without a gesture. Avoid requiring the three-finger action or intercepting system accessibility shortcuts. | [Accessibility: Mobility and Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility) |
| 5 — P1 | Body text is fixed at 12 pt and clips at 200% enlargement. Essential checkout information can disappear. | Use an adaptive body style starting from the iOS 17 pt default and support at least 200% enlargement. Reflow rows, wrap text, allow vertical scrolling, and grow controls to preserve labels and actions. The supplied 12 pt is above the guide’s 11 pt iOS minimum; it is not itself a minimum-size violation. Fixed sizing and confirmed clipping are the defects. | [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision) |

P0 means a direct barrier to identifying completion or understanding its outcome; P1 means a serious barrier to selecting, editing, or reviewing the trip. The exact ranking is an audit judgment, not an Apple severity classification.

## Framework-agnostic correction contract

Use equivalent capabilities in the project's existing stack; no Apple SDK is assumed.

```text
Checkout:
  textStyle.body = adaptive(base = 17 iOS points, enlargement >= 200%)
  layout = wrapping rows + growing controls + vertical scrolling
  essential labels never truncate or overlap

Departure(time, available, selected):
  visible = time + (available ? "Available" : "Unavailable")
  semantics = {name: time, status: availability, selected: selected}
  if selectable: expose selection role and activation
  else: expose unavailable state; never submit this departure

Traveller(person):
  visible action = "Remove traveller"
  semantics = {name: "Remove traveller, " + person.displayName, role: button}
  activate -> remove that traveller; preserve all other checkout data
  after removal -> focus next traveller action, else traveller section heading
  expose removal result without requiring sound

Pay:
  visible label = "Pay"
  semantics = {name: "Pay", role: button, state: enabled or busy}
  activate -> submit once; expose busy state and visible "Booking…"
  confirmed failure -> preserve inputs; show persistent failure text
    expose error as readable content and announce once without moving focus
    offer recovery action appropriate to the actual failure
  confirmed success -> show and expose confirmed booking outcome
```

Busy-state handling, data preservation, removal focus fallback, and the precise announcement strategy are proposed engineering decisions supporting the task. They are not additional verified defects or universal HIG requirements. Recovery must use the actual booking/payment result; this specification supplies no payment protocol or error taxonomy.

Use the iOS default 44 × 44 pt activation area as the starting target for Pay, Remove, and selection controls, with sufficient separation. The local guide lists a 28 × 28 pt minimum; that is not a recommendation to shrink controls. Measure the interactive area, not merely the icon. Geometry is presently unknown. [Accessibility: Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility)

## Worked before/after

Illustrative data below is invented to demonstrate the contract, not observed screen content.

**Before:** A person who cannot distinguish red from green sees “09:00” and “10:00” with no other availability cue. After reviewing clipped enlarged text, they encounter an unnamed payment icon. A failed booking produces only a sound. Removing Alex requires a three-finger swipe.

**After:** Departure rows read “09:00 — Unavailable” and “10:00 — Available.” The person selects 10:00, reads the complete reflowed checkout at 200%, and activates “Remove traveller, Alex” through the visible button or assistive input. Remaining trip data persists and focus has a defined destination. They activate the named “Pay” button. If submission fails, a persistent “Booking failed” message appears and is exposed for speech output; a reason and recovery action appear only when supported by the result. They can understand and recover without hearing a sound or performing a multi-finger gesture.

## Acceptance and test plan

Implement ranks 1–2 first, then 3–5; verify them together along the same checkout path. The checks below are **not executed** and describe release acceptance, not existing passes.

| Check | Procedure and pass condition |
|---|---|
| Payment semantics and activation | Inspect exposed accessibility information, then identify and activate Pay using VoiceOver and Voice Control on a supported iPhone environment. It has the correct name, button role, and state; one activation submits once. Repeat through Switch Control and Full Keyboard Access; no essential action is unreachable. |
| Failure without sound | Trigger a controlled booking failure with sound muted. Visible readable failure text persists until resolved or explicitly dismissed; input data remains. With VoiceOver, the failure is announced once and can be revisited. Recovery reflects the actual result and returns to a usable checkout path. |
| Availability without color | Review with color removed or ignored. Every time's availability is explicit in text and semantic output. Select an available time; an unavailable time cannot be submitted and its status remains discoverable. Check selected state separately from availability. |
| Removal without gesture | Remove a traveller using the onscreen button, VoiceOver, Switch Control, Full Keyboard Access, and AssistiveTouch as applicable. The intended traveller is removed, other data remains, and focus reaches the specified surviving element. System gestures/shortcuts still work. |
| Enlarged reading and operation | At default and at least 200% text enlargement, review departure status, traveller details, totals, Pay, and failure/recovery text on supported iPhone layouts. No essential text clips, overlaps, or disappears; all actions remain reachable through scrolling and usable with assistive navigation. Test supported larger text settings too. |
| Geometry and contrast | Measure actual activation bounds and spacing. Use 44 × 44 pt as the iOS design target. Obtain foreground/background colors for normal, selected, unavailable, busy, and error states; calculate contrast in light/dark appearances and with Increase Contrast. Apply the local source's stated text table scope, not a blanket conformance claim. |
| Full task regression | Select a departure, edit travellers, review the full total, submit, recover from failure, and complete a confirmed booking with each supported input path. Check actual reading/focus order, meaningful grouping, state announcements, and absence of traps. |

The local contrast table gives 4.5:1 for text up to 17 pt at all weights, 3:1 for 18 pt at all weights, and 3:1 for bold at any size. Preserve that table’s scope; it does not alone establish WCAG conformance. If default colors fall short, specify a higher-contrast Increase Contrast treatment. No colors are supplied to calculate a result. [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision)

## Evidence and execution limits

- **Passed — static audit work:** Read the supplied specification and installed root → Foundations family → Accessibility topic procedure → Accessibility reference, in that order before using source guidance. Produced corrections, interaction contract, worked transformation, and acceptance criteria.
- **Failed — specification checks:** Text preservation at 200%; non-color availability information; meaningful Pay name; onscreen alternative to required complex gesture; non-auditory booking failure information. These failures are explicit in `interface.md`, not independently reproduced.
- **Not executed:** Device/GUI rendering, SDK compilation, contrast measurement, target geometry, VoiceOver reading or focus order, announcements, Voice Control, Switch Control, Full Keyboard Access, AssistiveTouch, physical comfort, and booking/payment execution. No runtime accessibility pass or compliance certification is claimed.

Only local files were consulted; official links above identify the guidance and were not browsed. Source used: `.agents/skills/apple-hig/subskills/apple-hig-foundations/references/accessibility.md`, a local derived HIG snapshot marked retrieved 2026-10-25. Its existence does not establish independent review.

The installed Foundations route links a Typography topic and the Technologies route links a VoiceOver topic, but both topic `SKILL.md` files are absent at their installed paths; file reads and a hidden-file search confirmed this. The Technologies family was read while resolving that route. No supporting Typography or VoiceOver article was substituted ahead of a missing procedure. This audit therefore uses the successfully read Accessibility procedure and article for resizing and basic semantics; detailed rotor or framework-specific guidance is outside its evidence.

Standard iOS mode is explicit. Assistive Access's special two-confirmation guidance is not imposed on this checkout. Motion, timing, contrast defects, target-size defects, and focus-order defects are not inferred from absent evidence.
