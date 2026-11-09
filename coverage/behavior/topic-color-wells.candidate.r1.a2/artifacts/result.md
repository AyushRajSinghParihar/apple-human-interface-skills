# Accent-color repair

Patched interface.md in place into a concrete macOS specification. Its original prose reports four defects: clicking randomizes every shape, mixed colors appear black, Cancel commits, and keyboard users cannot reach the control. These are supplied observations, not independently reproduced failures.

## Decisions and changes

- Replace the unlabeled randomizer with a labeled color well; evaluate and prefer the system picker. Activation opens it without mutation.
- Bind edits to selected editable shapes in the active document. Empty or partially locked selections disable editing. A dash and “Multiple colors” distinguish mixed values from actual black.
- Stage previews separately from committed data. Apply commits one reversible operation; Cancel, close, and context changes discard it. Session tokens reject stale callbacks.
- Preserve color transfer with copy semantics and the same Apply/Cancel contract. Reject invalid drops; provide picker selection as a non-drag alternative.
- Specify keyboard entry, activation, exit, focus return, accessible name/value/state, text enlargement, and appearance checks.

System-picker preference and Mac well behavior follow [Color wells](https://developer.apple.com/design/human-interface-guidelines/color-wells). Accessible meaning and navigation follow [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards), and [Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection). Transfer feedback and reversal follow [Drag and drop](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop) and [Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo). These official links come from local guides; no web retrieval occurred. Exact mixed-state and transaction policies are product decisions rather than claims of Apple mandates.

## Worked before/after

Start with selected A=red and B=blue, and unselected C=green.

Before: the supplied behavior shows black for A/B, clicking randomizes all three, Cancel still commits, and the square is unreachable by keyboard.

After: the well reads “Multiple colors”. Tab reaches it and Space opens the picker without changing anything. Choosing purple previews A=B=purple while C stays green. Cancel restores A=red/B=blue without history or dirty-state changes. Reopen, choose purple, and Apply: only A/B commit, with one undo entry. Undo restores the different originals; Redo reapplies purple. If selection changes to C during preview, cancel and invalidate the old session first; a delayed purple callback changes neither the old targets nor C.

## Acceptance checks

| Check | Required outcome | Status |
| --- | --- | --- |
| Artifact coverage | All four reported defects have concrete replacement behavior in interface.md | Passed: static specification review |
| Binding and mixed values | One/many targets only; no-selection and locked states disabled; actual black distinct from mixed | Specified; runtime not executed |
| Open and repeated choices | Opening changes nothing; several choices preview; Apply commits only the final color as one operation | Specified; runtime not executed |
| Cancellation | Cancel, Escape, Command-Period, close restore exact originals and leave persistence/history unchanged | Specified; runtime not executed |
| Retargeting | Selection/document changes and target deletion/locking abort; stale callbacks ignored; reopen binds fresh targets | Specified; runtime not executed |
| Persistence and history | Autosave excludes preview; no-op Apply has no history; Undo restores mixed originals; Redo works; new edits clear redo | Specified; runtime not executed |
| Transfer | Picker-to-well and well-to-well copy and stage; source intact; invalid/multiple/unavailable drops reject; feedback clears on exit/cancel | Specified; runtime not executed |
| Keyboard completion | Reach, open, choose, Apply, reopen, Cancel, exit without pointer; field Return cannot accidentally Apply | Specified; macOS execution not performed |
| Assistive semantics | Inspector/VoiceOver confirm role, name, value, disabled/preview state; Full Keyboard Access reaches all actions | Specified; execution not performed |
| Visual access | Measure activation geometry and actual contrast; verify Light/Dark/Increase Contrast and 200% text without lost actions | Specified; measurements/execution not performed |

## Evidence limits

Explicitly read the installed apple-hig root SKILL.md and searched its topic index. For each selected route, read the owning family, then topic procedure, then source guide: Color wells; Accessibility; Keyboards; Focus and selection; Drag and drop; Undo and redo. Each instruction/source read used a separate single-file command.

Passed checks establish specification coverage only. No runtime checks passed or failed because none were executed. No app code, screenshots, SDK documentation, build, GUI, or device evidence was supplied. Native picker integration and saved colors, SDK availability/compilation, actual control geometry/contrast, display color fidelity, focus order, drag behavior, VoiceOver, and Full Keyboard Access remain unverified. Work was confined to local files on the headless Linux server; no Mac or accessibility execution is claimed.
