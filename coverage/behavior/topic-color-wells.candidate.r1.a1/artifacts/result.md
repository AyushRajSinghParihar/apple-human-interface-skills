# Accent-color repair decisions

Patched interface.md in place, replacing the original defect description with an implementable macOS specification. The repair targets selected editable shapes, labels and enlarges the color well, represents mixed values honestly, separates preview from persistence, makes Cancel discard edits, and defines a complete keyboard route.

## Decisions and rationale

- Prefer the system color picker and retain saved colors, activation highlighting and color dragging, following [Color wells](https://developer.apple.com/design/human-interface-guidelines/color-wells#macOS). The specification preserves the existing framework; it does not prescribe unverified SDK calls.
- “Multiple colors” plus a dash replaces false black. A visible label, textual value, focus indication, accessible semantics and a 28 × 28 pt Mac activation area address the supplied discoverability and reachability problems. These apply [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility) guidance; 28 pt is the local guide's starting default, not a universal minimum. No supplied dimensions establish the original control's exact size.
- An app-owned Apply/Cancel transaction keeps per-object originals and renders transient preview. Closing or changing context cancels; stale callbacks are ignored. This is a product decision applying the color-well procedure's target/preview/cancel checks, not an assertion that the native color panel has transaction semantics built in.
- Full Keyboard Access, standard activation and cancellation enable the whole task, following [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices). No custom shortcut is needed.
- Color drops copy the property, validate the destination at drop time and offer picker selection as an alternative, applying [Drag and drop](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop#Best-practices). One commit creates one reversible change, following [Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#macOS).

## Worked before/after

Fixture: editable shapes A = red, B = blue, C = green; only A and B selected.

Before, according to the supplied brief: the mixed selection appears black. Clicking the unlabeled square randomizes every shape, including C. Cancel in the panel still commits changes. Keyboard users cannot reach the square. Exact random colors and internal persistence behavior were not supplied.

After, as specified: the well reads “Accent color”, “2 selected shapes”, and “Multiple colors”. Opening changes nothing. Choosing purple previews A and B as purple; C remains green. Cancel leaves A red and B blue, with no new undo entry or dirty-state change. Reopen, choose purple and Apply: A and B become purple in one commit; C stays green. Undo restores A red and B blue and the mixed indicator; redo restores purple. Choosing another selection while previewing cancels that preview before rebinding the well, so delayed callbacks cannot recolor the new selection.

## Acceptance checks and status

Static specification review — **passed**: interface.md now defines all four supplied defect corrections, selection scope, uniform/mixed/disabled states, transaction exits, stale callback handling, color drops, keyboard semantics and history behavior. The worked example is consistent with those rules.

Original brief — **failed as described**, not independently reproduced: activation scope, mixed-color representation, cancellation and keyboard reachability.

Implementation acceptance — **not executed**. On a Mac build, verify:

1. Select A/B from the fixture; see “Multiple colors”. Select a truly black shape; see uniform black and its value. Empty, locked and unsupported selections show the specified disabled reasons.
2. Open without choosing; confirm no mutation. Preview several colors, then test Cancel, Escape, Command-Period and picker close separately. Compare all stored values, preexisting dirty state and history before/after each cancellation, including autosave during preview.
3. Apply purple to A/B; verify only their color property changes and exactly one undo unit is created. Undo restores distinct originals, redo reapplies purple. Reapply an identical value and confirm no history entry. Confirm a new commit after undo invalidates redo; verify save/open and offscreen restoration behavior.
4. Preview, then change selection, delete/lock a target, switch/close the document, or invoke undo. Confirm rollback before the new action; deliver a delayed callback and confirm no mutation. Reopen and repeat picking against fresh targets.
5. Drag colors between wells and from the picker. Check source preservation, eligible highlighting and removal on exit. Verify immediate idle drop versus session preview, undo, rejected payloads, multi-color rejection, failed/canceled drags, and Option release before drop. Confirm mixed placeholders cannot be exported as black.
6. Using only the keyboard, select content, reach the well, open the picker, choose a color, reach Apply/Cancel and complete both paths. Verify reverse navigation, visible focus, focus restoration, field typing, no trap and preserved system shortcuts under Full Keyboard Access.
7. Inspect accessible role/name/value/state/count and operate the task with VoiceOver and Switch Control. Check label-based targeting with Voice Control. Measure activation area and separation; inspect text at 200%, light/dark and Increase Contrast, and calculate actual interface contrast for black/white/transparent swatches.
8. Verify native picker/saved-color behavior and color-space fidelity on supported macOS versions. Confirm the app-owned session actions remain visible, associated with the picker and keyboard reachable.

## Evidence and limits

Read the installed root `.agents/skills/apple-hig/SKILL.md` explicitly. Then read Selection and input → Color wells, Foundations → Accessibility, Inputs → Keyboards, and Patterns → Drag and drop / Undo and redo, each family and topic procedure before its supporting source guide. Every instruction/source read used a separate single-file `cat` command. The official links above are attribution from local snapshots, not evidence of web verification.

Only interface.md's original one-paragraph description and installed local instructions/guides informed the repair. No implementation, framework, deployment target, screenshot, exact color model or app runtime was supplied. The property meaning and editable-selection policy are explicit product assumptions in the revised specification. No web browsing, SDK compilation, device/GUI execution, native picker inspection, contrast measurement or assistive-technology execution occurred. These are specification changes, not claims of a repaired executable. Native picker transaction integration and platform API availability remain to be validated during implementation.
