---
name: apple-hig-motion
description: Use when designing, reviewing, or adapting interface motion, interruptibility, reduced-motion behavior, game movement, or spatial animation comfort.
---

# Animate a meaningful relationship

Read [Motion](../../references/motion.md). Inspect the actual transition/animation, trigger, frequency, input, and platform. Establish design, review, or adaptation mode and identify what the movement communicates: feedback, continuity, progress, or something else. If removing it loses no information or useful character, consider removing it instead of tuning a pointless effect.

Prefer system component motion when it already supplies the right response. For custom movement, connect start/end states so entering and leaving form a coherent relationship. Tie gesture-driven feedback to the gesture and permit interruption or reversal; repeated operations should not wait for decorative playback. Preserve important information through text, shape, tactile, or audio feedback as appropriate rather than motion alone.

Define a reduced or optional version for automatic/repeated motion. Choose a less spatial transition when travel does not explain anything, and ensure reduced behavior preserves state and completion. For games, select device-appropriate performance defaults and expose meaningful performance/battery tradeoffs rather than assuming one setting works everywhere.

For visionOS, inspect the entire moving visual field. Avoid peripheral motion, large high-contrast moving objects that imply moving surroundings, and world rotation. Maintain a stationary reference; use restrained translucency/contrast where motion is needed. Replace unhelpful object travel or world reorientation with an appropriate fade. The guide's watchOS framework/easing limitations qualify implementation choices; do not promise unsupported custom easing.

**Worked transformation:** Before, changing a spatial dashboard filter rotates the entire room while each card flies to a new position. Decision: filter changes need updated results, not simulated movement of the world. After, the environment stays stable, results update with a restrained transition, and a reduced-motion setting removes spatial travel while keeping the selected filter and result count clear.

Deliver the revised motion/state specification or implementation, including interruption and accommodation behavior. Fail if rapid input queues stale transitions, movement blocks the next task, or reduced motion hides a state change. Record actual timing/performance observations only when measured; Linux/static review cannot establish worn-device comfort or native animation response.

Use [Accessibility](../apple-hig-accessibility/SKILL.md) for accommodation requirements, [SF Symbols](../apple-hig-sf-symbols/SKILL.md) when a symbol effect supplies feedback, or [Spatial layout](../apple-hig-spatial-layout/SKILL.md) for stable spatial references.
