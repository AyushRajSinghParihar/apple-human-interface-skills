# iPhone trip checkout accessibility audit

This is a specification audit of `interface.md`, for iOS in standard app mode. Five findings are verified by explicit statements in that file; their runtime manifestations have not been tested. All five should be corrected before checkout release. Ranking below is an audit decision based on task impact, not an Apple severity classification.

## Prioritized findings and decisions

| Rank | Verified evidence and impact | Correction and source |
|---|---|---|
| 1 — P1 | Pay is a custom icon with no accessible name. A screen-reader user cannot reliably identify the action that commits payment; voice targeting is also impaired. | Use a visible **Pay** label and expose a button named “Pay”, with enabled/busy state. Treat any accompanying decorative icon as part of that single control, not a second focus stop. Meaningful descriptions and control labels: [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision), [Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility). |
| 2 — P1 | Removing a traveller requires a three-finger swipe, with no onscreen alternative. Users unable to perform the gesture cannot correct the traveller list. | Add a visible Remove button for each traveller, with a distinct accessible name such as “Remove Alex Morgan”. Use one ordinary activation path across touch and assistive input. Remove the mandatory complex gesture; any retained shortcut is optional and must not conflict with system gestures. [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility). |
| 3 — P1 | Body text is fixed at 12 pt and clips at 200% enlargement. Enlarged checkout information becomes unreadable. | Use a semantic body style or equivalent preference-driven scaling, with 17 pt at the iOS default setting as the design baseline. Allow wrapping, growing rows and vertical scrolling; stack crowded content. Preserve complete information at 200% and all supported larger accessibility sizes. The verified failure is clipping/scaling, not a claim that 12 pt violates the 11 pt iOS minimum. [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision), [Typography — Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type). |
| 4 — P1 | Available departures use only green text; unavailable departures use only red. People who cannot distinguish those colors lose the availability information needed to choose a trip. | Add visible “Available” / “Unavailable” text beside each time and include the status in its accessible representation. Color may remain supplementary. Expose selection and enabled state separately; an unavailable time remains readable but cannot be selected for purchase. This selection behavior is a proposed product decision. [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |
| 5 — P1 | Booking failures produce sound without a visual or text message. Users who cannot hear the sound receive no stated failure feedback. | Show a persistent, accessible text message identifying failure and the supported next step. Announce it through the accessibility status mechanism; retain it until resolved or explicitly dismissed. Sound and optional haptics supplement the message. Never infer payment or booking status that the backend has not confirmed. [Accessibility — Hearing](https://developer.apple.com/design/human-interface-guidelines/accessibility#Hearing), [Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive). |

## Worked before/after

The names and times below are illustrative fixtures, not additional observations.

**Before, as specified:** 12 pt body text clips at 200%; 09:30 is green and 10:00 red without status text; the payment icon has no name; Alex can be removed only by a three-finger swipe; a failed booking sounds a tone without a message.

**After, proposed:** the body follows the text-size preference and wraps in growing containers. Departure rows read “09:30 — Available” and “10:00 — Unavailable”. Alex’s row includes a visible Remove button, exposed as “Remove Alex Morgan, button”. Checkout has one visible and accessible “Pay” button. A confirmed unsuccessful booking shows “Booking failed. Review your details and try again” only when retry is known to be safe. A status-unknown response instead shows “We couldn’t confirm your booking. Check booking status before paying again”, with a supported status-check action.

Framework-independent behavior contract:

```text
bodyStyle = semanticBody(userTextPreference, userBoldPreference)
layout = verticallyScrollable, intrinsicRowHeights, wrappingText
when horizontal content no longer fits: stack content in reading order
never shrink body text or clip essential information to retain row height

for each departure:
    show(time, availabilityText)
    expose(time + availabilityText, selectedState, enabledState)
    permit selection only when available

for each traveller:
    show button("Remove", accessibleName="Remove " + uniqueTravellerLabel)
    on ordinary activation:
        remove that traveller; update checkout summary
        announce removal; move focus to next traveller control,
        otherwise previous traveller control, otherwise traveller section heading

show button("Pay", accessibleName="Pay", enabled=checkoutValid && !submitting)
on Pay activation:
    submit once; expose busy state and visible "Processing payment" status
on confirmed booking failure:
    clear busy state; preserve entered details
    show persistent failure text and backend-supported recovery action
    announce the new failure once without requiring sound
on unknown booking/payment status:
    show persistent uncertainty text and supported status-check action
    do not invite another payment until duplicate-payment risk is resolved
```

Focus destinations, single-submission handling, recovery copy and retained details are proposed interaction decisions, not verified defects or prescribed Apple APIs. Actual payment semantics and backend recovery capabilities must determine final copy and actions.

Use comfortable separated controls. Adopt 44 × 44 pt interaction areas as this design's iOS target, growing with content; the supplied HIG snapshot distinguishes this default from a 28 × 28 pt minimum. No supplied dimensions establish an existing target-size failure. Standard app mode does not trigger the snapshot’s Assistive Access-specific two-confirmation rule. This audit does not mandate two confirmations for traveller removal.

## Correction and acceptance plan

Implement ranks 1–2 first to restore identifiable and operable checkout actions, then rank 3 layout changes, then ranks 4–5 status presentation. Check the combined flow after layout changes. All checks below are pending execution.

| Check | Procedure | Acceptance condition |
|---|---|---|
| Pay identity and activation | Inspect the semantic control tree; later use VoiceOver and Voice Control on a supported iPhone. Activate Pay using assistive input. | One button has the visible label and accessible name “Pay”; state changes are exposed; no duplicate icon stop; one activation produces one submission. |
| Traveller correction | Remove first, middle and last travellers with ordinary touch, VoiceOver, Switch Control and Full Keyboard Access. Include duplicate-name fixtures with distinguishable labels. | Each Remove control identifies the intended traveller, removes only that traveller, updates the summary, announces the change and leaves focus on an existing logical element. No multiple-finger gesture is required. |
| Enlargement | At the narrowest supported iPhone width, exercise every supported text size, including Larger Accessibility Text, plus a 200% enlargement fixture. Repeat with Bold Text and long content. Scroll through the full checkout. | All meaningful text remains complete, readable and operable; no clipping, overlap or obscured controls. Containers expand and crowded rows stack. At 200%, the text actually enlarges rather than merely enlarging its container. |
| Availability | Review without color; inspect and read both departure states using VoiceOver. Attempt unavailable selection. | Status text conveys availability without hue; accessible output includes time and status; selected state is distinct from availability; unavailable departure cannot enter the payable selection. |
| Failure feedback | Inject confirmed failure and unknown-status responses with audio muted; test with VoiceOver both on and off and at the largest supported text size. | A readable persistent message and valid next step appear; assistive users receive the new status once; details remain; unknown status never falsely asserts no charge or encourages unsafe repayment. |
| Complete navigation | Traverse checkout with VoiceOver, keyboard and Switch Control; exercise removal, submit, failure and recovery. Also check AssistiveTouch and Pointer Control. | Every required action is reachable and operable, traversal follows the meaningful reading sequence, focus remains visible where applicable, and dynamic updates do not strand focus. Existing order is unknown, so this is validation, not a verified violation. |
| Contrast and geometry | Obtain actual foreground/background colors, font weights, all relevant states, target bounds and spacing; measure light/dark and Increase Contrast variants. | Document measurements and fix failures against the selected criteria. Use the local snapshot’s Inspector guidance with its stated scope: text up to 17 pt, all weights, 4.5:1; 18 pt, all weights, 3:1; bold text at any size, 3:1. Record any separate conformance standard explicitly. Verify the chosen 44 × 44 pt control target and separation. No current contrast or size pass/fail can be assigned. |

These checks require a later runnable implementation and appropriate test equipment. On this Linux server, specification/semantic-fixture checks can be automated once implementation exists. Actual iPhone assistive-technology checks require a tester and device; Apple inspection tooling requires a suitable Mac environment. No Apple SDK is assumed here.

## Evidence and limits

Only `interface.md` and installed local guidance were used. No web browsing occurred. Official article links above identify the guidance represented by the local snapshot; they were not fetched or independently verified as current.

Instruction route consumed: installed `apple-hig/SKILL.md` → `subskills/apple-hig-foundations/SKILL.md` → that family's `references/accessibility.md` and `references/typography.md`. The root topic index was searched for Accessibility and Typography and points to those references. The selected foundations family routes directly to article references; it specifies no intervening topic procedure. All paths resolve within `/tmp/hig-eval-_ceysv1c/.agents/skills/apple-hig/`. Each file was read in a separate command.

No screenshots, implementation, color values, actual focus order, control dimensions, backend behavior or runtime were supplied. No device, GUI, SDK, Accessibility Inspector, VoiceOver or other accessibility execution occurred. Accessibility names beyond Pay, availability semantics, error announcements, and target geometry are unverified. The plan specifies corrected behavior, not an implemented or tested fix, a WCAG conformance verdict, or a complete accessibility certification. Snapshot presence does not establish independent review of its sources.
