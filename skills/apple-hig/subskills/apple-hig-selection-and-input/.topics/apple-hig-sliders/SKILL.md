---
name: apple-hig-sliders
description: Use when creating, reviewing, or adapting bounded continuous adjustment, slider scales, precision entry, and live feedback.
---

# Make movement correspond to a meaningful value

Read [the slider guide](../../references/sliders.md). The workflow is application advice; apply only documented platform capabilities.

Inspect value meaning/units, minimum/maximum, step or continuous scale, precision needs, platform/input, and create/review/adapt mode. Determine whether the interval is bounded or wraps/repeats. Record the actual mapping and result feedback; track position alone does not prove a linear scale.

Use a slider for understandable bounded adjustment, with leading-to-trailing increase horizontally and bottom-to-top vertically. Pair wide ranges with exact numeric entry and useful increments when needed. On Mac choose linear for fixed intervals and circular for repeating/continuing values, explaining nonlinear mappings with intermediate labels. Provide live results where feasible and exact value exposure. Use the appropriate volume view for iOS/iPadOS audio output rather than rebuilding it as an arbitrary slider. Prefer horizontal adjustment on visionOS; define increments for the onscreen buttons beside the watch slider. Sliders are unsupported on tvOS in this guide.

Implement the mapping/feedback or supply range, scale, value, endpoint, and precision specifications; reviews must identify a concrete mapping or reachability defect. Avoid customization that hides the quantity or standard interaction.

**Worked transformation:** Before: a Mac opacity control uses a circular dial, has no value display, and makes 1% changes nearly impossible across a wide range. Decision: opacity is a fixed bounded interval and exact adjustment matters. After: use a linear 0–100% slider with live preview and a synchronized numeric field.

Deliver the artifact and mapping/precision contract. Verify endpoints, intermediate values, keyboard/assistive increments, numeric-field synchronization, and cancellation/undo if part of the product. Fail for inverted unexplained mapping, inaccessible required precision, or displayed/applied value disagreement. Report physical input/native value announcements separately.

Use [steppers](../apple-hig-steppers/SKILL.md) for small increments, [text-fields](../apple-hig-text-fields/SKILL.md) for precision, or [playing-audio](../../../apple-hig-patterns/.topics/apple-hig-playing-audio/SKILL.md) for output-volume context.
