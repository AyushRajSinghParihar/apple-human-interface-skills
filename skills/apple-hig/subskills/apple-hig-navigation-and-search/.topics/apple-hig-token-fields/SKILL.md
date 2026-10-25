---
name: apple-hig-token-fields
description: Use when creating, reviewing, or adapting macOS fields that turn entered terms into selectable and movable tokens.
---

# Preserve the term behind the token

Read [the token-field guide](../../references/token-fields.md). This procedure is application advice for a Mac component; search tokens elsewhere are separately scoped.

Inspect the term model, completion source, delimiters, validation, platform, and create/review/adapt mode. Establish what one token represents and whether duplicate/ambiguous terms have distinct identities. Record commit, selection, reorder, transfer, and contextual editing behavior from code/prototype; a pill-shaped label alone proves none of these.

Use tokens for meaningful manipulable units such as recipients. Preserve comma conversion and add useful triggers such as Return deliberately. Suggestions should reduce ambiguity without interrupting entry; tune delay if immediate completions distract. Provide a context menu only when useful details/actions exist, and keep editing/removal/reorder semantics predictable. Distinguish a display title from the underlying identifier so duplicate names cannot silently choose the wrong recipient. Do not claim native token fields on unsupported platforms.

Implement the token model/entry/operations, specify a text-to-token lifecycle, or review concrete wrong-identity and editing defects. For search refinements use the search-field topic before choosing this Mac entry component.

**Worked transformation:** Before: typing `Alex,` commits the first matching contact with no way to inspect which Alex, and dragging copies only the visible name. Decision: display text loses identity. After: resolve ambiguous suggestions before committing and preserve the contact identifier during transfer, with a context action exposing the address.

Deliver the artifact and commit/completion/identity/edit/transfer contract. Verify ambiguous names, unfinished text, delimiter/Return, token deletion, reorder, and cross-field movement. Fail for unintended recipient selection, lost identity, or committed tokens that cannot be corrected. Native text-input/pasteboard behavior must be exercised separately from source inspection.

Load [search-fields](../apple-hig-search-fields/SKILL.md) for query tokens, [text-fields](../../../apple-hig-selection-and-input/.topics/apple-hig-text-fields/SKILL.md) for ordinary entry, or [context-menus](../../../apple-hig-menus-and-actions/.topics/apple-hig-context-menus/SKILL.md) for token actions.
