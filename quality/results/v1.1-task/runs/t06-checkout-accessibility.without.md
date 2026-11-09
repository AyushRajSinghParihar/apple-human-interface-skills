The specification identifies five accessibility problems. Prioritize the blockers to completing checkout, then readability and status clarity. This audit applies to the standard iPhone app.

| Priority | Problem | Correction |
|---|---|---|
| **P0** | **Pay has no accessible name.** A VoiceOver user cannot reliably identify the payment action. | Prefer a native button. Give it a clear accessible label such as “Pay,” the button trait, and an appropriate enabled state. |
| **P0** | **Removing a traveller requires a three-finger swipe.** The gesture is hard to discover and may conflict with assistive technology. | Add a visible “Remove traveller” button for each traveller, accessible through VoiceOver and alternative input. A gesture may remain as an additional shortcut. |
| **P0** | **Booking failure is communicated only by sound.** People who cannot hear it may not know checkout failed. | Show a persistent, accessible text error explaining the failure and available next steps. Announce the error to VoiceOver when it appears; sound can supplement it. |
| **P1** | **Fixed 12 pt body text clips at 200%.** Enlarging text hides information. | Use Dynamic Type text styles and adaptive layouts. Allow text to wrap and containers to grow or scroll so content and controls remain readable and usable at accessibility text sizes. |
| **P1** | **Departure availability relies entirely on red and green.** People who cannot distinguish the colors cannot determine availability. | Add explicit “Available” and “Unavailable” text or equivalent non-color cues with accessible status information. Expose unavailable options as disabled where appropriate. |

**Test plan**

1. **Payment:** With VoiceOver, navigate to Pay and verify its label, button role, enabled state, and activation. Verify it is reachable and operable with Switch Control and identifiable through Voice Control.
2. **Traveller removal:** Remove a specific traveller using the visible button, VoiceOver, and Switch Control without performing the swipe. Confirm each control identifies its traveller and that focus remains in a sensible place after removal.
3. **Failure feedback:** Trigger a booking failure with audio muted. Verify a visible text message explains what happened and what to do next. With VoiceOver running, confirm the error is announced and remains available to review.
4. **Text enlargement:** Test at the default size, 200%, and the largest supported accessibility Dynamic Type sizes. Check the whole checkout for clipping, truncation, overlap, hidden actions, and unreachable content.
5. **Departure status:** Verify availability remains understandable in grayscale and with color filters enabled. With VoiceOver, confirm each time’s availability and disabled state are conveyed accurately.

Contrast and focus order remain **unassessed**, because the specification provides neither measurements nor interaction evidence. During implementation testing, measure text and control contrast and inspect VoiceOver navigation order across checkout. No screenshots or rendered interface were supplied, so this is not a complete visual or accessibility conformance audit.