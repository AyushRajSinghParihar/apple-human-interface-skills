---
name: apple-hig-labels
description: Use when creating, reviewing, or adapting short uneditable text and its relationship to nearby controls.
---

# Make short text carry the right context

Read [the labels guide](../../references/labels.md). Apply its documented semantics; the procedure is application advice.

Inspect text, surrounding controls, platform, and create/review/adapt intent. Determine whether each string is a static caption, editable value, long-form content, or useful portable information. Record its association, hierarchy, truncation, scaling, and copy behavior where evidenced.

Choose a field for short editing and a text view for longer/formatted content. Keep labels actual text with system typography and semantic colors appropriate to primary/supporting/unavailable meaning. Do not assign a faint semantic role solely to make essential content visually quiet. Preserve Dynamic Type where supported and inspect custom-font readability. Allow copying when an error, location, or address needs reuse. On watchOS, use system date/time or timer text for temporal values rather than repeatedly rebuilding a static label; do not imply every framework provides Apple's automatic updating behavior.

Implement the label and association, provide concrete replacement text/style rules, or review identifiable ambiguity/legibility issues. Apply component-specific wording conventions when the label belongs to a button or another constrained control.

**Worked transformation:** Before: a shipping screen shows `ID` in faint gray above an uncopyable tracking number rendered as an image. Decision: the identifier is primary portable information, not unavailable content. After: label it `Tracking Number`, render the value as scalable selectable text, and reserve secondary hierarchy for supporting delivery notes.

Deliver the edited text and semantic/association contract. Verify long localization, enlarged/bold text, appearance changes, copy where relevant, and accessible association with the correct control. Fail for a label attached to the wrong input, rasterized essential text, or loss of meaning through clipping. Report native text/assistive rendering separately from code inspection.

Load [text-views](../../../apple-hig-content/.topics/apple-hig-text-views/SKILL.md) for longer selectable material or [text-fields](../../../apple-hig-selection-and-input/.topics/apple-hig-text-fields/SKILL.md) when the value is editable.
