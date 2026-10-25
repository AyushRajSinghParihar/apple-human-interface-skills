---
name: apple-hig-digital-crown
description: Use when designing or reviewing Watch Crown navigation or adjustment, touch equivalents, detents, or the system-owned Vision Pro Crown behavior.
---

# Assign Crown rotation without conflicting with navigation

Read [Digital Crown](../../references/digital-crown.md). Identify Watch versus Vision Pro, the current scroll/navigation context, any adjustable value, and requested design/review/adaptation. Preserve the stack and inspect actual state transitions rather than assuming every hardware rotation can become an app command.

On Vision Pro, retain the system's volume, immersion, recentering, accessibility, and Home behavior; do not map these controls to arbitrary application actions. On Watch, reserve Crown presses for the system. Since watchOS 10, rotation is the main navigation mechanism, so use it for adjustment only where it is not already needed to navigate.

Define which visible content responds and how touch performs an equivalent operation. Keep the response visibly connected to rotation. Tune change rate to speed while retaining precise selection; a fast turn may cover a range quickly, but a slow turn must settle on a value. Choose appropriate default haptic detents, avoiding conflicting taps/animation. For variable-height rows, consistent linear detents can be more predictable than treating every row as equal physical distance.

**Worked transformation:** Before, a Watch altitude history simultaneously scrolls the page and changes a selected day on Crown rotation, with no touch alternative. Decision: the same rotation cannot ambiguously navigate and adjust. After, the main page uses rotation for scrolling; entering an explicit day-inspection view adjusts the highlighted day with visible values and an equivalent touch selector, then returns to the prior scroll position.

Deliver a context-to-rotation mapping, response/rate rules, touch equivalent, and corrected artifact. Fail if one rotation affects unrelated states, a value changes invisibly, precision is lost at slow speed, or a system press/control is repurposed. Real haptic feel, rotation responsiveness, and system navigation require supported Watch/Vision Pro checks; code inspection establishes mappings only.

Use [Designing for watchOS](../../../apple-hig-getting-started/.topics/apple-hig-designing-for-watchos/SKILL.md) for task scope and [Immersive experiences](../../../apple-hig-foundations/.topics/apple-hig-immersive-experiences/SKILL.md) when the Crown governs immersion.
