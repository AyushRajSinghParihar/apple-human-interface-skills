The specification establishes **five accessibility defects**. Priorities below reflect their impact on completing checkout, rather than formal compliance severity. No runtime tests have been performed.

**Prioritized corrections**

| Priority | Confirmed issue and impact | Correction |
|---|---|---|
| **P1** | **Pay has no accessible name.** People using VoiceOver cannot reliably identify the payment action. | Prefer a standard text-labeled **Pay** button. Supply the accessible name “Pay,” button role, and enabled/disabled state. [HIG: Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons) |
| **P1** | **Traveller removal requires a three-finger swipe.** This excludes people unable to perform complex gestures and hides an essential action. | Add a visible **Remove traveller** button associated with each traveller; include the traveller’s name in its accessible identification. Remove the gesture requirement. Its direction is unspecified, so a particular system-gesture conflict is unconfirmed. [HIG: Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures) |
| **P1** | **Body text clips at 200%.** People enlarging text lose checkout information. Fixed 12 pt body text also falls below the recommended iPhone default. | Use semantic Dynamic Type body text—17 pt at the default size—and allow wrapping, growing containers, stacking, and scrolling. Preserve essential content and actions at least through 200% enlargement and test larger accessibility sizes. **12 pt is above the stated 11 pt minimum; size alone does not establish a minimum-size violation.** [HIG: Typography](https://developer.apple.com/design/human-interface-guidelines/typography) |
| **P1** | **Availability depends only on red/green.** People who cannot distinguish those colors cannot reliably choose a departure. | Add explicit **Available / Unavailable** text, optionally supported by distinct symbols. Expose availability and relevant control state to assistive technology. [HIG: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) |
| **P1** | **Booking failure is sound-only.** People who cannot hear it receive no failure information or recovery guidance. | Display a persistent, accessible text message explaining the failure and available next step. Make it discoverable to VoiceOver when it appears. Sound and optional haptics may supplement the message. [HIG: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) |

These are standard-app recommendations. The Assistive Access guidance requiring two confirmations for difficult-to-reverse actions does **not** apply here.

**Test plan**

Run on supported iPhones, including the smallest supported screen, using test payments and a reproducible booking failure.

| Test | Pass criteria |
|---|---|
| **Text enlargement** | At default, 200%, and all supported Dynamic Type accessibility sizes, essential text remains readable without clipping or overlap; departure selection, removal, and Pay remain reachable. Repeat with Bold Text. |
| **Availability without color** | With grayscale enabled, every departure’s availability remains clear. VoiceOver conveys the departure time and availability without relying on color names. |
| **Pay semantics and activation** | VoiceOver identifies “Pay” as a button and conveys its state. Activation performs the intended payment action. Voice Control can identify and activate it. |
| **Removal without gestures** | Touch, VoiceOver, Switch Control, and Full Keyboard Access can reach and activate the visible removal action. It identifies and removes the intended traveller; focus remains usable afterward. |
| **Failure without sound** | With audio muted, trigger a booking failure. A readable message explains what happened and the next step, remains available long enough to act, and is discoverable with VoiceOver. |
| **Complete checkout** | Choose a departure, edit travellers, review, activate Pay, encounter failure, and recover using VoiceOver and Switch Control separately. Verify logical focus order, no traps, and access to every required action. |
| **Measurements** | Use Accessibility Inspector and runtime inspection to measure actual contrast, target areas, and spacing in light/dark appearances and with Increase Contrast. Use 44 × 44 pt as the recommended iPhone button target. |

**Evidence status:** All five findings fail the specification review. Contrast, focus order, target geometry, actual assistive-technology behavior, and corrected-layout behavior are **not assessed**, rather than presumed failures. Record device, iOS version, settings, and pass/fail evidence when executing the plan.