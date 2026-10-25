---
name: apple-hig-steppers
description: Use when creating, reviewing, or adapting small increment and decrement controls with a nearby value display.
---

# Make both the amount and affected value obvious

Read [the stepper guide](../../references/steppers.md). This procedure is application advice; acceleration is a Mac option rather than a universal behavior.

Inspect quantity, units, allowed range, increment, nearby controls, platform, and create/review/adapt intent. Identify the value each segment changes and whether people need large jumps. Obtain actual boundary/wrapping behavior from implementation; plus/minus glyphs do not establish it.

Use a stepper for small adjustments with an unmistakable adjacent value. Add editable numeric entry if crossing a wide range by repeated activation would be burdensome. Keep display and stored value synchronized, define bounds and overflow deliberately, and disable or otherwise explain impossible changes without silently wrapping to the opposite extreme unless the quantity requires it. On Mac accelerated Shift-click can help with large changes. Do not prescribe steppers on tvOS/watchOS, where this component is unsupported.

Implement the value binding, provide quantity/range/step/precision specifications, or review concrete target and effort failures. Preserve locale-aware numeric handling when adding an editable field; these data rules are application decisions to verify.

**Worked transformation:** Before: a print dialog has two unlabeled steppers beside Pages and Copies and requires hundreds of clicks to request 500 copies. Decision: affected values are ambiguous and the range exceeds small adjustments. After: align each stepper with its value/label, provide a Copies field for direct entry, and keep all routes within the same bounds.

Deliver the artifact and target/value/increment/boundary contract. Verify first/last allowed values, repeated changes, direct entry, and any acceleration. Fail for the wrong quantity changing, value/display mismatch, or impractical access to a valid value. State native keyboard/assistive interaction checks separately from logic tests.

Load [text-fields](../apple-hig-text-fields/SKILL.md) for direct entry or [pickers](../apple-hig-pickers/SKILL.md) when selection from ordered values is clearer.
