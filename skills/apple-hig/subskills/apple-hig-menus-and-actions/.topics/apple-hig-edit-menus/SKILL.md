---
name: apple-hig-edit-menus
description: Use when creating, reviewing, or adapting selected-content editing commands and system edit-menu behavior.
---

# Make commands follow the selection

Read [the edit-menu guide](../../references/edit-menus.md). This procedure applies the source and distinguishes system behavior from product choices.

Inspect selected content types, editability, pasteboard state if available, platform/input, and create/review/adapt mode. Map Cut, Copy, Paste, Delete, custom actions, and undo to their actual scope. A screenshot cannot establish pasteboard or undo semantics.

Use the system edit menu and expected gestures. Remove/dim irrelevant commands; make Paste eligibility follow actual usable content. Distinguish Cut's transfer to the pasteboard from Delete's removal without copying. Group a few custom verbs with related standard actions, and preserve useful static-content copying while leaving ordinary control labels unselectable. Favor undo/redo over confirmation for ordinary edit actions.

Implement/specify command selection/paste/undo behavior, or review concrete semantic mismatches. Test both horizontal touch and vertical keyboard/pointer menus on iPad where relevant, preserving system pointer/menu shape while avoiding essential content obstruction. Mac uses standard Edit ordering. tvOS/watchOS lack this component; do not promise it as an entry solution there.

**Worked transformation:** Before: a transcript offers `Cut` on read-only text, `Paste` with no compatible content, and confirms every highlight removal. Decision: commands do not follow editability or clipboard state, while reversible work is interrupted. After: retain Copy and contextual lookup, expose editing only in an editable context, and make reversible highlight removal undoable.

Deliver the command/eligibility/undo contract and changed artifact. Verify empty selection, incompatible paste content, read-only content, Cut versus Delete pasteboard effects, and undo restoration. Fail for unintended loss, a command acting outside selection, or a falsely enabled action. State actual native pasteboard/gesture checks separately.

Use [undo-and-redo](../../../apple-hig-patterns/.topics/apple-hig-undo-and-redo/SKILL.md), [context-menus](../apple-hig-context-menus/SKILL.md), or [the-menu-bar](../apple-hig-the-menu-bar/SKILL.md) when those determine the command model.
