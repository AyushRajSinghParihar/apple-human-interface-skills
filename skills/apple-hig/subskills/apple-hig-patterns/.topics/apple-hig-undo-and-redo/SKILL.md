---
name: apple-hig-undo-and-redo
description: Use when creating, reviewing, or adapting reversible edits, history grouping, command labels, shortcuts, and visible restoration.
---

# Make the action being reversed predictable

Read [the undo/redo guide](../../references/undo-and-redo.md). This workflow is application advice; the source marks this pattern unsupported on tvOS/watchOS.

Inspect meaningful edit sequence, object identity, save/open boundaries, incremental controls, command access, platform, and create/review/adapt mode. Establish what each undo reverses and how redo changes after new work. Record actual history behavior rather than assuming a disabled icon represents it.

Group related increments when they form one meaningful adjustment; avoid arbitrary shallow history that prevents recovering the meaningful sequence since opening/saving. Name targets precisely in menu/shake text. Reveal offscreen changes enough to show the result, preventing repeated undo because nothing appeared to happen. Prefer standard menus/keys/gestures, adding toolbar buttons only when needed. On Mac retain top-of-Edit Undo/Redo shortcuts. On iOS/iPadOS preserve standard gestures/shake and add only the operation wording after system-provided title text.

Implement the reversible command/history/reveal model, provide a concrete action/inverse/grouping specification, or review exact wrong-target and lost-history defects. Treat network/external irreversible effects honestly: do not label a cosmetic rollback as undoing a completed external action.

**Worked transformation:** Before: a drawing editor records every slider pixel separately, calls all history “Undo,” and restores deleted offscreen text without revealing it. Decision: recovery units and feedback are unpredictable. After: group one continuous adjustment, label its target, and reveal restored text while preserving context.

Deliver the artifact, history unit/boundary, inverse, labels, and reveal contract. Verify a sequence, grouped drag, undo/redo, new edit after undo, offscreen restoration, and save/open policy. Fail for reversing the wrong object, false reversal of irreversible work, or no visible evidence of restoration. Native gesture/shortcut execution remains distinct from logic checks.

Load [edit-menus](../../../apple-hig-menus-and-actions/.topics/apple-hig-edit-menus/SKILL.md), [feedback](../apple-hig-feedback/SKILL.md), or [drag-and-drop](../apple-hig-drag-and-drop/SKILL.md) for the affected operation.
