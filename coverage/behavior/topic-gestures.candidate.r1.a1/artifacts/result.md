# Result

Patched `interface.md` in place, replacing its original single-paragraph specification with an actionable iPhone interaction contract. The patch removes the three-finger Split circle, speed-dependent swipe deletion, hidden recovery, and interception of standard edge navigation. It adds visible Split/Delete/Undo/Redo, single-tap clip and position controls, a reachable Back equivalent, disabled/error states, nondestructive edit inverses, and explicit history boundaries.

## Decisions and rationale

| Supplied barrier | Revised decision | Local guidance basis |
|---|---|---|
| Split requires a three-finger circle | Labeled Split button; remove custom recognizer | [Gestures — Custom gestures](https://developer.apple.com/design/human-interface-guidelines/gestures#Custom-gestures), [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility) support simple visible alternatives. |
| Left swipe scrubs or deletes depending on speed | Waveform drag always scrubs; explicit Delete removes selected clip | [Gestures — Best practices](https://developer.apple.com/design/human-interface-guidelines/gestures#Best-practices) supports predictable meanings and feedback; [Buttons — Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role) informs destructive semantics. |
| No visible Undo | Persistent Undo/Redo, atomic edit history and visible restoration | [Undo and redo — Best practices](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#Best-practices) prefers standard routes and adds buttons when needed. The one-handed requirement justifies dedicated controls here. |
| Edge navigation intercepted | Restore standard top/edge Back; add bottom equivalent | [Gestures — Custom gestures](https://developer.apple.com/design/human-interface-guidelines/gestures#Custom-gestures), [Toolbars — Navigation](https://developer.apple.com/design/human-interface-guidelines/toolbars#Navigation). |
| All work must be possible one-handed | Bottom controls, sequential taps, 44 × 44 pt targets, text reflow | [Accessibility — Mobility and Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility), [Buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices). Physical comfort is unverified. |
| Accidental deletion needs recovery | Delete only arrangement clip, preserve source, restore exactly with Undo; no routine confirmation | [Alerts — Best practices](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices) generally permits undoable deletion without confirmation. This depends on the specified recovery contract. |

The bottom layout, 8 pt target gaps, 0.1-second steps, non-ripple deletion, retry behavior and history lifetime are explicit product choices. HIG does not prescribe those details. The specification uses the conservative 44 pt iOS default and button guidance rather than treating the accessibility reference's smaller 28 pt minimum as a recommended dense layout.

## Worked before/after

Fixture: clip A spans 0–10 seconds, playhead at 4 seconds, A selected.

Before: splitting requires the three-finger circle. A subsequent fast left swipe may delete instead of scrubbing, with no visible recovery. Returning to the project list conflicts with intercepted edge navigation. These are supplied specification facts, not observed device behavior.

After, using only sequential taps:

1. Tap Split. A becomes contiguous A-left (0–4) and A-right (4–10); A-right is selected.
2. Tap Delete. A-right is removed; 4–10 is a gap and the source remains intact.
3. Tap Undo. A-right returns at 4–10 with its settings and selection restored, and the viewport reveals it.
4. Tap Undo again. The original A at 0–10 returns, selected at position 4.
5. Tap Redo. The split is reapplied. Tap Later: position becomes 4.1 seconds without clearing redo. Tap Redo: deletion is reapplied and recorded post-delete state is restored.
6. Tap bottom Back to Projects, then reopen. Arrangement and session context remain. Standard edge Back must reach the same destination.

Alternative branch: after step 4, move inside A and commit a new Split. The previous redo branch is cleared. Scrubbing alone never clears it.

This is a worked specification trace; it was not executed in an app.

## Acceptance checks and status

**Passed — static specification review:** all four supplied barriers have explicit replacements; every editing/navigation action has a sequential single-tap route; destructive scope and exact inverses are defined; system gestures are preserved; availability, cancellation, failure, narrow-layout behavior and session boundaries are specified. The worked state trace agrees with the action/history contract.

**Failed:** no failure identified in the static specification checks. This is not a runtime pass.

**Not executed — implementation acceptance:**

| Check | Pass condition |
|---|---|
| Discoverability and one-handed task | Without gesture coaching, select a clip, position, split, delete, undo, redo and return using either hand and sequential taps; test representative small/large iPhones. No held second touch or velocity threshold. |
| Gesture separation | Slow/fast drags in both directions only scrub; canceled drag restores position; no recognizer handles a three-finger circle. Live playhead feedback remains responsive. |
| System boundaries | Edge Back, canceled interactive Back, Home, overlays and accessibility shortcuts retain system behavior; bottom and top Back reach the same parent without losing edits. |
| Editing bounds | No selection, locked clip, empty project, clip endpoints and project boundaries yield the specified disabled state and guidance. Interior valid-frame Split preserves source and settings. |
| History correctness | Execute the worked trace, new-edit branch, repeated undo/redo and offscreen restoration. Clip identity/ranges/settings/position and selection restore exactly. Selection/scrub/step create no history entries. |
| Failure and lifetime | Failed edits leave arrangement and stacks unchanged; retry commits once. Duplicate activation cannot duplicate edits. Autosave and leaving/reopening preserve session history; session close/restart preserves saved arrangement and begins new history. |
| Geometry and text | Measure actual hit regions ≥44 × 44 pt and gaps ≥8 pt. At 200% text and landscape, all labels/actions remain reachable without overlap or clipping, with identifiable selection and position. |
| Assistive input | On an Apple environment, complete the same task using VoiceOver, Switch Control, Voice Control, AssistiveTouch and Full Keyboard Access. Names, values, disabled states and outcomes are exposed and actionable. |
| Native undo | Standard three-finger undo/redo and supported shake use the same stack; shake wording does not duplicate system-provided Undo/Redo. |

## Evidence and limits

Read the installed root `.agents/skills/apple-hig/SKILL.md` explicitly, then searched `references/topic-index.md`. Read each selected family, its routed topic procedure, then the supporting guide, using one file per shell command. Routes consumed:

- Inputs → Gestures → `references/gestures.md`.
- Menus and actions → Buttons and Toolbars → their respective reference guides.
- Foundations → Accessibility → `references/accessibility.md`.
- Patterns → Undo and redo → `references/undo-and-redo.md`.
- Presentation → Alerts → `references/alerts.md`, to resolve deletion confirmation.

All paths above resolve inside the installed apple-hig package. Official links identify the sources recorded by those local guides; no web browsing or live-source verification occurred. The package describes its articles as derived local guidance with a 2026-10-25 snapshot, not SDK documentation or proof of independent review.

Only a short text brief was supplied. No app implementation, screenshots, SDK, simulator, GUI, device measurements or accessibility execution were available or performed. Static review cannot establish native rendering, gesture recognition, latency, hit geometry, focus order, contrast, physical reach, comfort, compilation or runtime accessibility. These remain implementation acceptance work. No code changes or execution tests are claimed.
