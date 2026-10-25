---
name: apple-hig-text-fields
description: Use when creating, reviewing, or adapting short input fields, labels, validation, secure entry, formatting, and focus order.
---

# Preserve meaning while people enter a value

Read [the text-field guide](../../references/text-fields.md). This workflow is application advice; keep platform input capabilities and validation timing qualified.

Inspect value type, required format, sensitivity, labels, validation, target platform/input, and create/review/adapt request. Determine whether short entry is appropriate or a text view/choice control would reduce effort. Record actual format and commit rules rather than guessing from placeholder examples.

Keep purpose understandable after the placeholder disappears by adding persistent labels when necessary. Use secure entry for sensitive content and size/align fields to explain expected values and associations. Preserve logical Tab order. Validate at a useful moment: email often on leaving, creation feedback for username/password before leaving. Use understandable corrective feedback and locale-aware numeric formatters rather than punctuation-stripping shortcuts. Choose deliberate clipping/wrapping and an appropriate keyboard/content type. Offer trailing Clear on iOS/iPadOS; evaluate Mac combo boxes for suggestions plus custom values. Minimize typing on TV/watch and prefer existing choices where useful.

Implement fields/format/validation/focus or supply an input contract; reviews must identify the exact entered value and resulting failure. Do not broaden into account-security changes merely because a password field is present.

**Worked transformation:** Before: a price field labelled only by `$0.00` rejects a comma decimal after every keystroke and loses its label once entered. Decision: purpose and locale semantics must persist while partial input is allowed. After: use a persistent Price label, locale-aware currency representation, and validation that distinguishes intermediate entry from an invalid committed value.

Deliver the artifact and label, type, validation moment, feedback, formatting, and focus contract. Verify empty/partial/invalid/valid input, locale changes, secure content, Tab traversal, and long values. Fail for hidden purpose, exposed secrets, lost valid input, or format coercion changing meaning. Separate inspected logic from native keyboard/assistive execution.

Use [entering-data](../../../apple-hig-patterns/.topics/apple-hig-entering-data/SKILL.md) for form strategy, [virtual-keyboards](../apple-hig-virtual-keyboards/SKILL.md) for entry layout, or [text-views](../../../apple-hig-content/.topics/apple-hig-text-views/SKILL.md) for extended content.
