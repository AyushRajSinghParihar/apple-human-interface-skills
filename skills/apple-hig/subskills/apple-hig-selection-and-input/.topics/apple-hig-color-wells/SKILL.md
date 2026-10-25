---
name: apple-hig-color-wells
description: Use when creating, reviewing, or adapting a color-selection well, its picker, swatch, and target-content behavior.
---

# Connect the swatch to the affected content

Read [the color-well guide](../../references/color-wells.md). This workflow is application advice; evaluate the system picker before creating a custom replacement.

Inspect selected content, color property, current swatch, picker behavior, platform, and create/review/adapt request. Identify whether a single object, selection, or document setting is affected and how mixed colors are represented. Do not infer persistence or color accuracy from a screenshot.

Prefer the familiar system picker and saved-color behavior when it fits. Keep the well's displayed color synchronized with actual selected content; distinguish preview from committed change if the product has that concept. On Mac preserve activation highlighting and color drag/drop between wells and from the picker. Specify what happens when selection changes while the picker is open so the next color cannot modify a stale object. Do not prescribe color wells on tvOS/watchOS. The source adds no separate visionOS rules; do not invent spatial picker details.

Implement the well/selection binding, provide a target/picker/commit specification, or review concrete wrong-object and stale-swatch defects. Keep custom-picker requirements tied to a demonstrated need rather than branding alone.

**Worked transformation:** Before: a diagram color well keeps the first shape's swatch after selecting another and drops a color into the wrong object. Decision: selection identity and visual value must be bound together. After: refresh the swatch with selection and route picker/drop changes to the explicitly current target, preserving undo if supported.

Deliver the artifact and target/preview/commit/drop contract. Verify selection change, mixed selection, drag/drop, repeated picking, and cancellation when provided. Fail for the swatch misrepresenting applied color or edits reaching the wrong object. Color fidelity, native picker, and physical display checks require suitable runtime/hardware evidence.

Load [color](../../../apple-hig-foundations/.topics/apple-hig-color/SKILL.md) for color meaning or [drag-and-drop](../../../apple-hig-patterns/.topics/apple-hig-drag-and-drop/SKILL.md) for transfer behavior.
