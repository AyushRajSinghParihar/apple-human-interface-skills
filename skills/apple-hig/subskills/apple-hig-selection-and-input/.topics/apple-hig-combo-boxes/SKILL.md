---
name: apple-hig-combo-boxes
description: Use when creating, reviewing, or adapting macOS entry that combines likely suggestions with free custom text.
---

# Keep suggestions distinct from permitted values

Read [the combo-box guide](../../references/combo-boxes.md). This workflow is application advice for a Mac-only component.

Inspect expected value type, suggested list, custom-entry rules, validation, platform, and create/review/adapt mode. Establish whether values outside the list are genuinely allowed. If only listed choices are valid, choose a selection control instead. Record the stored value separately from displayed suggestion text.

Use a meaningful initial listed value where appropriate, label the category with a title-case label and colon, and keep relevant suggestions short enough to fit. Preserve free entry: a custom value does not automatically become a new list item. Define normalization and commit timing so selecting a suggestion and typing the same value produce equivalent results where intended. Do not present a Mac combo box as natively supported on other platforms; adapt to appropriate entry/suggestion UI.

Implement the field/list/value contract, supply concrete suggestion and validation behavior, or review exact restriction/commit defects. Avoid inventing “invalid” status solely because the value is absent from the suggestions.

**Worked transformation:** Before: a Mac print preset editor offers common paper widths in a combo box but rejects any unlisted width and silently adds typed values to everyone's suggestions. Decision: a combo box promises custom entry without list mutation. After: accept valid custom widths, preserve the curated list, and use a separate explicit save-preset action if desired.

Deliver the artifact, label, initial value, suggestions, and free-entry/commit policy. Verify list choice, custom value, invalid format, focus departure, and long localized values. Fail for silently changing the suggestion list, rejecting permitted custom entry, or storing a value unlike the displayed one. Mark native keyboard/assistive behavior separately from inspected logic.

Use [pop-up-buttons](../../../apple-hig-menus-and-actions/.topics/apple-hig-pop-up-buttons/SKILL.md) for closed choice or [text-fields](../apple-hig-text-fields/SKILL.md) for ordinary custom entry.
