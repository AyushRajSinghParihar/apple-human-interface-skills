# Decisions and patch

Replaced the one-line `interface.md` in place with a concrete timeline interaction specification. The patch removes hover prerequisites, immediate secondary-click deletion and arbitrary blank-region pointer shapes. It adds visible touch alternatives, selection scope, platform-specific pointer effects, manipulation preview/commit/cancel states, contextual menus, reversible deletion, documented modifiers, keyboard groups and assistive task routes.

The original explicitly states the three problematic behaviors and undocumented modifiers; it supplies no application implementation. Frame snapping, non-overlap rules, exact commands, single-clip duplication and session-history boundaries are proposed product decisions, not Apple mandates. Preserve the existing framework.

Material source links appear in `interface.md`. The local guidance supports coherent input switching, semantic cursor effects, supplemental context menus, standard modifiers and recoverable editing. iPad circle/highlight/lift/magnetism are scoped separately from Mac cursors and menu access. Approximate pointer padding remains tuning advice. The contract adopts 44 × 44 pt iPad action targets: the accessibility guide lists 44 pt defaults and 28 pt minima, while Buttons gives general 44 pt guidance. The conservative button specification uses 44 pt rather than adopting the smaller minimum for density.

# Worked before/after

Scenario: unlocked clip A occupies frames 100–200, with space afterward.

Before: all actions require hover, preventing the specified touch editing path. Secondary click deletes A immediately. Blank-region shapes have no stable meaning. Recovery behavior is unspecified.

After: click or tap A; its selection survives pointer exit. Open visible Edit Clip and shorten Source Out by 20 frames, then Apply. A now ends at frame 180 and one trim history unit exists. Secondary click opens A's menu without modifying data; dismissal leaves it unchanged. Explicit Delete removes only its timeline reference. Undo Delete Clip restores A with its identity, selection and trimmed timing. Undo Trim Clip restores end frame 200; Redo reapplies the trim. Touch performs the same sequence with Edit Clip, Delete and Undo buttons. Keyboard users focus A, select with Space, open with Enter, edit fields, activate Apply through keyboard access and recover with Command-Z.

# Acceptance checks and status

Passed — static specification review:

- Every essential editing action has a visible route independent of hover and modifiers.
- Secondary click opens a scoped menu; deletion requires explicit activation and has a defined inverse.
- Blank-region pointers are stable; clip, trim, text, copy and invalid states have semantic platform-specific feedback.
- Hover, focus and selection are distinct. Switching inputs, cancellation and interruptions have defined outcomes.
- Modifier meanings, text-field precedence, keyboard groups and history units are documented.

Failed: no static contract failures identified. This does not establish an application pass.

Not executed — implementation acceptance scenarios:

1. With no accessories, select, trim via Edit Clip, duplicate, delete and undo. Repeat at narrow iPad window widths; essential controls remain available.
2. Sweep blank regions, clips, text and handles. Verify stable roles, contiguous action-bar regions, no overlapping targets or neighbor occlusion, and escapable magnetism. Measure actual target geometry.
3. Exercise configured secondary click for one/multiple selected clips, unselected clips, locked clips and blank space. Verify target scope, hidden unavailable actions, preview clipping, above/below menu placement and zero edits on dismissal.
4. Move, trim and Option-drag into valid/invalid destinations. Cancel, disconnect input and switch apps during drags. Verify frame snapping, exact rollback, collision rejection and one history unit per commit.
5. Rectangle-select a group, switch to touch, resize and move it. Verify persistent selection and relative track/time offsets.
6. Run trim → delete → Undo → Undo → Redo; restore offscreen content; save during the session; commit a new edit after Undo. Verify exact restoration, visible reveal and Redo invalidation.
7. Complete select → edit → Apply → Undo using keyboard and Full Keyboard Access. Verify group entry/exit, arrows, deletion focus, field Delete precedence, localized shortcuts and preservation of system gestures.
8. Exercise assistive activation with VoiceOver, Switch Control and AssistiveTouch on supported Apple hardware. Verify names, values, states and complete editing without drag precision; inspect rendered readability and state distinctions.
9. On Mac verify native cursors, configured clicks, main-menu parity, resizing and app reactivation with preserved work.

# Evidence limits and instruction audit

Only supplied local files and installed instructions were used. No web browsing occurred. Official links attribute the installed snapshot dated 2026-10-25; they do not establish live verification or independent source review.

All paths were resolved from `.agents/skills/apple-hig/`. Explicit reads covered root `SKILL.md`; Inputs family and relevant topic-index rows; Getting started family and iPadOS/macOS procedures; Pointing devices, Keyboards, Gestures and Focus and selection procedures; Menus and actions family and Context menus/Buttons procedures; Patterns family and Undo and redo procedure; Foundations family and Accessibility procedure. Each topic procedure preceded its corresponding source guide in the family's `references/` directory. Each file was read by a separate cat or rg command. A truncated combined output was followed by separate reads of the affected input and platform references.

No device, SDK compilation, GUI, native pointer rendering, physical comfort, gesture recognition, accessibility execution or API availability was tested. Static review establishes specification coverage only. Runtime scenarios remain unexecuted.
