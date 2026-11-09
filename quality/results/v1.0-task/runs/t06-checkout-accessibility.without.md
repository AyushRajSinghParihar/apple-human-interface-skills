The specification identifies five accessibility issues. The priorities below reflect their impact on completing checkout; they are not formal conformance ratings.

| Priority | Issue | Correction |
|---|---|---|
| **P0** | **Pay has no accessible name.** People using VoiceOver cannot reliably identify the purchase action. | Give the control a clear label such as “Pay,” expose its button role, and ensure it supports standard activation. Prefer a visible text label alongside the icon. |
| **P0** | **Booking failure is communicated only by sound.** People who cannot hear the sound may not know the booking failed. | Show a persistent, accessible text message that explains the failure and offers an appropriate recovery action. Announce it to VoiceOver without requiring the person to find it. Keep sound supplementary. |
| **P1** | **Traveller removal requires a three-finger swipe.** The action has no visible alternative, and the gesture can conflict with accessibility gestures. | Add a clearly labelled on-screen control, such as “Remove Alex.” Support ordinary activation and optionally expose a VoiceOver custom action. |
| **P1** | **Fixed 12 pt body text clips at 200%.** Enlarging text makes checkout content unreadable. | Use Dynamic Type text styles and flexible layouts. Allow wrapping and vertical growth; remove fixed heights that clip text. Validate all supported accessibility text sizes, including the reported 200% case. |
| **P1** | **Departure availability relies on red and green alone.** People who cannot distinguish the colours cannot reliably choose a departure. | Add explicit “Available” and “Unavailable” text or equivalent clear indicators, and expose availability programmatically. Retain colour as a supplementary cue. |

Test the corrected checkout on a real iPhone:

| Test | Pass criteria |
|---|---|
| **VoiceOver purchase action** | Pay is announced with a clear name and button role, is reachable, and activates using the standard VoiceOver gesture. |
| **Booking failure** | Trigger a failure with sound muted and with VoiceOver enabled. A visible text message explains what happened and how to proceed; VoiceOver announces it. |
| **Traveller removal** | Remove a traveller using the visible control with touch, VoiceOver, Switch Control and Voice Control. No three-finger gesture is required, and the intended traveller is unambiguous. |
| **Text resizing** | Check 200% enlargement and every supported Dynamic Type size, including accessibility sizes. Text, prices, departure details and controls remain readable and usable without clipping or overlap. |
| **Availability without colour** | Use grayscale and VoiceOver. Every departure’s availability remains clear, and unavailable choices cannot be mistaken for selectable ones. |
| **End-to-end checkout** | Choose an available departure, manage travellers, pay, trigger a failure and recover using the corrected controls and messages. |

Contrast, focus order and visual layout **cannot be assessed from this specification**. Measure contrast and inspect actual focus traversal and rendered layouts when a build becomes available; do not treat those areas as passing. Test the standard app with accessibility features enabled—Assistive Access is outside this audit’s scope.