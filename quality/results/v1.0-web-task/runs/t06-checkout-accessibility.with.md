The specification establishes **five accessibility defects**. All are high priority because they affect checkout access or understanding. The order below is a proposed fix sequence, not an Apple severity rating.

| Priority | Confirmed barrier | Correction |
|---|---|---|
| 1 | **Pay has no accessible name.** People using VoiceOver cannot reliably identify the payment action. | Give it an accessible name such as “Pay” and button semantics. Prefer a standard, visibly labeled button; verify custom control activation and states. [HIG: Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons) |
| 2 | **Traveller removal requires a three-finger swipe.** This excludes people who cannot perform the gesture and risks conflict with assistive gestures. | Add a visible “Remove traveller” button for each traveller. Its accessible name or context must identify which traveller it removes. Make it operable with a single tap and assistive input. [HIG: Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility) |
| 3 | **Body text is fixed and clips at 200%.** Enlarging text loses content. | Use Dynamic Type with semantic text styles. Prefer the iOS Body style, which defaults to 17 pt; allow wrapping, growing containers and scrolling. Preserve content and actions at least through 200% enlargement and test the largest accessibility sizes. **12 pt is above the stated 11 pt minimum**; the confirmed defects are fixed sizing and clipping. [HIG: Typography](https://developer.apple.com/design/human-interface-guidelines/typography) |
| 4 | **Departure availability depends entirely on red versus green.** People who cannot distinguish those colors lose the status. | Add explicit “Available” and “Unavailable” text, optionally with distinct symbols. Expose availability through accessibility semantics as well. [HIG: Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision) |
| 5 | **Booking failure is sound-only.** People who cannot hear the sound receive no failure information. | Show a persistent, accessible text message explaining the known failure and an appropriate next step. Make the update discoverable to VoiceOver. Sound and optional haptics can supplement the message. [HIG: Accessibility — Hearing](https://developer.apple.com/design/human-interface-guidelines/accessibility#Hearing) |

**Test plan — proposed; no runtime tests executed**

| Test | Acceptance criteria |
|---|---|
| Text enlargement | On the smallest supported iPhone, exercise every supported Dynamic Type size, including at least 200% and the largest accessibility size; repeat with Bold Text. Essential text is readable without clipping or overlap, and all checkout actions remain reachable. |
| Availability without color | Inspect with Differentiate Without Color enabled and in grayscale. Every departure’s status remains explicit. VoiceOver identifies the departure and its availability. |
| Payment semantics | Use Accessibility Inspector and VoiceOver. Pay has the correct name, button role and applicable state; activation performs the intended action. |
| Traveller removal | Remove a specified traveller using the visible button, then repeat with VoiceOver, Switch Control, Voice Control and Full Keyboard Access. No multi-finger gesture is required; the correct traveller is removed. |
| Failure feedback | Trigger booking failure with audio muted, then with VoiceOver enabled. The failure and recovery action are understandable without sound; the message remains available long enough to read and navigate. |
| Complete checkout | Traverse departure selection, traveller editing, payment and failure recovery using VoiceOver and alternative input. Verify logical focus order, reachable controls and sensible focus after removal or error presentation. |
| Contrast and targets | Measure actual foreground/background contrast in light and dark appearances and with Increase Contrast. Inspect activation areas and spacing, using 44 × 44 pt as the recommended iPhone target baseline. Record measurements. |

**Evidence limits:** Contrast, focus order, target geometry and visual layout are unknown, so none can be reported as passing or failing. No runtime passes are established.

This is the standard app: Assistive Access guidance about one interaction per screen and two confirmations for difficult-to-reverse actions does **not** apply automatically.