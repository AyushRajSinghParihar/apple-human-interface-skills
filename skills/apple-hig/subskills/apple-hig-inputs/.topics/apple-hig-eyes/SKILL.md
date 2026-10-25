---
name: apple-hig-eyes
description: Use when designing or reviewing visionOS eye-targeted controls, system hover effects, target separation, comfortable gaze shifts, or gaze privacy assumptions.
---

# Offer a clear target without observing private gaze

Read [Eyes](../../references/eyes.md). Inspect target bounds, normal/hover states, content depth, competing movement, and assistive input routes. Establish design, review, or adaptation mode. This is visionOS guidance; retain the current stack and separate system hover from connected-keyboard/controller focus.

Choose a recognizable stable target and use standard hover responses where appropriate. Group an image and its label into one containing hover region when they form one action. Check separation using the guide's 16 pt margin or 60 pt center-distance guidance; avoid overlapping feedback. Remove noisy patterns and peripheral movement that pull attention away or create ambiguous depth.

Keep important content in comfortable view without repeated broad eye movement or rapid refocusing. Sustained reading normally belongs at least 1 m away; reserve closer content for brief interaction. Do not invent exact field-of-view dimensions or assume head-pose access outside its platform context.

For custom hover, declare normal/hover appearances and keep a primary visual stable. Use immediate subtle affordance, a short delay for expansion that could interfere with quick action, and a longer delay for optional information. The system applies effects outside the app process: it does not disclose pre-tap gaze or run gaze-dependent business logic. Hover may reveal a predefined favorite affordance, but cannot favorite an item itself. Provide alternative input/assistive routes.

**Before → decision → after:** A gallery marks a work as viewed and enlarges its target into a neighbor whenever someone looks toward it. Decision: hover is private system feedback, not an app event, and targets need stable separation. After, a contained stable artwork/label region receives system hover emphasis; explicit activation opens the work, while any viewed state follows a supported deliberate event.

Deliver corrected target/hover specifications or implementation. Fail if looking alone changes stored content, targets collide, or required interactions have no alternative. Only a worn Vision Pro can establish responsiveness, gaze comfort, and distraction; static geometry cannot.

Use [Spatial layout](../../../apple-hig-foundations/.topics/apple-hig-spatial-layout/SKILL.md) for depth/anchors and [Focus and selection](../apple-hig-focus-and-selection/SKILL.md) for actual keyboard/controller focus.
