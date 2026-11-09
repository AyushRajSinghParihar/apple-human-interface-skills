The specification identifies five accessibility failures. Fix the checkout blockers first; then address departure selection and text resizing. This is a standard iPhone app, so corrections should use standard accessibility behavior without assuming Assistive Access.

| Priority | Finding | Correction |
|---|---|---|
| **P0** | **Pay has no accessible name.** People using VoiceOver cannot reliably identify the payment action. | Give the control a clear accessible name, such as “Pay,” and expose it as a button. Ensure its enabled or disabled state is conveyed. |
| **P0** | **Booking failure is sound-only.** People who cannot hear the sound receive no failure information. | Display a persistent, readable error explaining the failure and any available recovery action. Make the message available to VoiceOver and announce it when it appears. Keep sound supplementary. |
| **P1** | **Removing a traveller requires a three-finger swipe.** There is no alternative for people who cannot perform that gesture or whose assistive technology uses it. | Add a visible, accessible “Remove traveller” button associated with the correct traveller. The swipe may remain as an optional shortcut. |
| **P1** | **Departure availability relies only on red and green.** People who cannot distinguish those colors cannot reliably select a departure. | Add explicit “Available” and “Unavailable” labels or another clear non-color indicator. Include availability in the accessible information for each departure. |
| **P1** | **Fixed 12 pt body text clips at 200%.** Enlarging text causes information loss. | Support Dynamic Type and flexible layouts. Allow text to wrap and containers to expand so content and controls remain readable and usable at 200% and supported accessibility text sizes. |

All five need correction before calling the checkout accessible. The priorities reflect direct payment and failure-recovery barriers first, not a claim that the remaining issues are minor.

Test the corrected checkout on an iPhone:

| Test | Pass criteria |
|---|---|
| **Pay with VoiceOver** | Pay is announced with a meaningful name, button role, and correct state; activating it performs the payment action. |
| **Trigger a booking failure with sound muted** | A visible text message communicates failure and the available next step. It remains long enough to read and act on. |
| **Trigger a failure with VoiceOver active** | The failure message is announced and can be found again; recovery controls are reachable and clearly named. |
| **Remove a traveller without swiping** | A visible button removes the intended traveller using a tap. Repeat using VoiceOver and Switch Control; neither requires a three-finger gesture. |
| **Inspect departures without color cues** | Availability remains understandable in grayscale and through VoiceOver. Unavailable departures cannot accidentally be booked. |
| **Enlarge text** | At 200% and supported accessibility text sizes, text does not clip or overlap, and all checkout content and actions remain reachable. |
| **Complete the full flow** | With enlarged text, VoiceOver, and Switch Control in separate runs, select a departure, manage travellers, pay, encounter a failure, and recover without getting stuck. |

**Not assessable from this specification:** color contrast, actual focus order, touch-target dimensions, or visual layout beyond the stated clipping. Measure contrast and verify focus order and targets in the implemented app; no pass or failure can be assigned to those areas from the supplied information.