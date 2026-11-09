The specification establishes **five accessibility defects**. All are high priority because they affect choosing, editing, paying for, or recovering a booking. The order below reflects task impact, not a formal compliance rating.

| Priority | Confirmed barrier and effect | Correction |
|---|---|---|
| **1 — Pay has no accessible name** | A person using VoiceOver cannot reliably identify the payment action. | Prefer a standard, visibly labeled **Pay** button. Give it an accessible name matching the action, button semantics, and an exposed enabled/disabled state. A custom icon still needs these semantics. |
| **2 — Traveller removal requires a three-finger swipe** | The essential action excludes people who cannot perform the gesture and can conflict with system accessibility gestures. | Add a visible **Remove traveller** button for each traveller. Its accessible name should identify the traveller, such as “Remove Alex.” Make it operable with a simple tap and assistive input. |
| **3 — Body text is fixed and clips at 200%** | Enlarging text loses checkout information. Fixed 12 pt is also poorly suited to primary body content. | Use Dynamic Type with the semantic Body style—normally **17 pt at the default iOS size**. Allow wrapping, growing containers, stacked layouts, and scrolling so content and actions remain usable at least at 200% enlargement and larger accessibility sizes. **12 pt is above the cited iOS 11 pt minimum; the confirmed failure is fixed sizing and clipping**, not being below that minimum. |
| **4 — Departure availability uses color alone** | People who cannot distinguish red and green cannot reliably determine availability. | Add explicit **Available / Unavailable** text, optionally reinforced with distinct symbols. Expose availability and selection state to assistive technology. Color can remain supplementary. |
| **5 — Booking failure is sound-only** | People who cannot hear the sound, or have audio muted, may miss the failure and have no recovery guidance. | Show a persistent, accessible text message explaining the failure and the appropriate next action. Ensure VoiceOver users are notified and can reach recovery controls. Sound and haptics may supplement the message. State payment/booking status only when known. |

These corrections follow Apple’s [Accessibility guidance on vision, hearing, and mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [Typography guidance](https://developer.apple.com/design/human-interface-guidelines/typography), and [Buttons guidance](https://developer.apple.com/design/human-interface-guidelines/buttons). Assistive Access’s special interaction and confirmation guidance does **not** apply to this standard app.

**Test plan — proposed, not executed**

| Test | Pass criteria |
|---|---|
| **Text enlargement** | On the smallest supported iPhone, test default size, at least 200% enlargement, and all accessibility Dynamic Type sizes, including Bold Text. Departure details, traveller information, Pay, and errors remain readable and reachable without clipping or overlap. |
| **Availability without color** | In grayscale and with relevant color filters, every departure’s availability remains explicit. VoiceOver announces the time, availability, and selection state accurately. Unavailable choices cannot be booked. |
| **VoiceOver checkout** | Navigate from departure selection through traveller editing, Pay, and failure recovery. Names, roles, and states are meaningful; focus follows a logical task order without traps. Pay is identifiable and activates the intended action. |
| **Alternative input** | Remove a traveller and complete checkout using Switch Control, Voice Control, and Full Keyboard Access. No essential action requires the three-finger gesture. Verify focus remains useful after removal. |
| **Failure without sound** | Trigger booking failure with audio muted. The message explains the outcome and recovery, remains available long enough to act, and is announced or brought to attention accessibly without stranding focus. |
| **Measurements and appearances** | Use Accessibility Inspector and runtime measurements to check contrast in light/dark appearances and with Increase Contrast. Measure actual hit regions and spacing; use **44 × 44 pt as the default iPhone control target**. |

**Evidence status:** Five failures are established by the specification; no runtime checks passed or were executed. Contrast, focus order, target geometry, and overall visual layout remain **unverified**, not confirmed failures.