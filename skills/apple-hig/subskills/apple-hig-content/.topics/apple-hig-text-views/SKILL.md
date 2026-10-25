---
name: apple-hig-text-views
description: Use when creating, reviewing, or adapting multiline reading or editing surfaces, including selection, copying, text scaling, and input behavior.
---

# Define reading and editing independently

Read [the text-view guide](../../references/text-views.md). This operating procedure is application advice; use the guide for platform qualifications.

Inspect the supplied content, view/code, platform, and create/review/adapt request. Determine whether the text is long or formatted, editable or read-only, and useful to copy elsewhere. Identify scrolling ownership, text scaling, selection, and keyboard behavior from evidence. Do not assume a read-only view should also be unselectable.

Choose a text view for lengthy, specially formatted, or multiline editable content; use a label for short static text and a field for short entry. Preserve leading alignment and system color behavior where appropriate. Decide how long content reflows rather than truncating information the task requires. Support Dynamic Type and Bold Text without hardcoding a dense reading layout. Allow selection/copy for useful identifiers, addresses, errors, and prose people may reuse.

Implement the authorized view or produce an annotated reading/editing specification; in review identify the exact blocked task and replacement behavior. Match the iOS/iPadOS keyboard to expected input. On tvOS use text views for display and fields for editing, minimizing entry; do not copy a phone's long-form editor unchanged. Retain the user's framework and distinguish a desired capability from one verified in that framework.

**Worked transformation:** Before: a support app renders a long diagnostic report as clipped, unselectable labels. Decision: people need to read the full report and copy its reference numbers without editing them. After: a read-only multiline text view reflows and scrolls, permits selection/copy, and preserves contextual formatting; identifiers remain actual text.

Deliver the changed view plus its editability, copy, sizing, and scrolling contract. Verify a long paragraph, an unbroken identifier, enlarged text, and selection across lines; when editable, verify keyboard and saved content. Fail for inaccessible clipped content, accidental edits in read-only material, or useful text that cannot be copied. Mark VoiceOver/native keyboard execution unknown if only static inspection was possible.

Load [text-fields](../../../apple-hig-selection-and-input/.topics/apple-hig-text-fields/SKILL.md) for short entry, [labels](../../../apple-hig-layout-and-organization/.topics/apple-hig-labels/SKILL.md) for static captions, or [typography](../../../apple-hig-foundations/.topics/apple-hig-typography/SKILL.md) when reading hierarchy needs deeper work.
