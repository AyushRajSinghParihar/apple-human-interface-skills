# Repair result

Patched interface.md in place, replacing the one-paragraph defect description with an implementable macOS specification. The deliverable is a specification repair, not an application-code fix.

## Decisions and patch summary

| Supplied problem | Revised contract | Guidance and decision boundary |
| --- | --- | --- |
| All windows share a hidden unsaved buffer | Stable document IDs own content/revisions/save destinations; window IDs own frame/selection/scroll. Different documents remain independent; repeated Open reuses the existing file window. | [Windows — Best practices and macOS](https://developer.apple.com/design/human-interface-guidelines/windows#macOS) supports parallel context and normal window behavior. The exact ownership schema and one-window-per-document policy are product decisions. |
| Closing one window discards another document's edits | Per-document autosave, durable Untitled drafts, revision-aware completion, atomic saving, and close/quit blocked by unresolved persistence failures. | [File management — Saving work](https://developer.apple.com/design/human-interface-guidelines/file-management#Saving-work) supports autosave on periodic and consequential exits. Save intervals, draft retention and failure transitions are concrete engineering choices. Autosave-off dirty-dot advice is conditional; this design enables autosave and uses Edited without dirty dots. |
| Restored windows forget size/selection | Versioned per-window restoration records, correct-document loading before selection, stale-range clamping and visible-display frame fallback. | [Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Best-practices) and [Multitasking — macOS](https://developer.apple.com/design/human-interface-guidelines/multitasking#macOS) inform continuity. Record fields and fallback rules are product decisions. |
| Tiny fixed window clips enlarged labels | Resizable primary windows, proposed 900 × 650 pt initial / 480 × 360 pt minimum content size, wrapping/stacking/scrolling and 100–200% app text scaling. | [Layout — Adaptability](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability), [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision), and [Typography — macOS](https://developer.apple.com/design/human-interface-guidelines/typography#macOS). Dimensions are unmeasured product starting values. macOS has no Dynamic Type; custom accommodation is explicit. |
| Settings duplicates as a document | One reusable auxiliary Settings window, app-menu access, persistent app-wide values; no document buffer, dirty state or document save target. | [Settings — macOS](https://developer.apple.com/design/human-interface-guidelines/settings#macOS). Singleton reuse is a product choice to prevent clutter; stable pane behavior follows local guidance. |

The patch also defines active-window command scope, no-document availability, standard shortcuts, native state cues and menu access when the bottom edge is offscreen. See [The menu bar](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar) and [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards). No framework replacement or unverified SDK calls are prescribed.

## Worked before/after

**Before (illustrative trace from the supplied defect report, not an executed reproduction):** Open “Gateway” and “Storage.” Edit Gateway's retry paragraph, then Storage's replication paragraph. Both windows use the hidden buffer; closing Gateway can discard Storage's work. Relaunch loses the prior frame and selection. Settings creates another apparent document, and enlarged labels cannot fit the fixed window.

**After (required behavior):** Gateway has document ID A/window ID WA; Storage has B/WB. A's retry edit advances A to revision 8, B's replication edit advances B to revision 13. WA is 900 × 650 pt; WB is 700 × 500 pt with selection [120, 18]. Closing WA persists A8 and closes only WA. B13 and WB's selection remain intact, even if A's save finishes after B's edit. A failed save instead keeps WA open and offers Retry/Save As without clearing either document.

Quit persists B13 and WB's view record. With system restoration enabled, relaunch reopens WB at 700 × 500 pt and [120, 18]; WA remains closed. Open Recent can reopen A with its last view state. Command-comma repeatedly focuses the same Settings window. Selecting 200% text reflows app-owned labels and note display without editing either note. If WB's display is disconnected, its frame moves into the visible work area while its document and valid selection survive.

## Acceptance checks

All runtime checks below are **not executed**. Run builds/tests on THINKBOOK as applicable to the eventual stack; use the MACBOOK for native macOS interaction and accessibility verification. There is no supplied runnable app in this task evidence.

| Check | Observable pass condition |
| --- | --- |
| Independent edits and asynchronous saves | Edit A and B, delay/reorder A's completion, close A; B's bytes, revision, selection and destination remain unchanged. A's old save completion cannot clear A's later edit. |
| Repeated opens and naming | Open the same file twice, including minimized state: one editable window activates. Open two same-named files in different folders: independent content and distinguishable titles. New twice produces independent drafts. |
| Close, reopen, failed persistence | Close named and Untitled documents, then reopen: latest successfully persisted content returns. Inject disk-full/permission failure: affected window remains open, Edited/error persist, retry or alternate destination succeeds without losing the previous file. Cancel Save UI: draft and selection survive. |
| Quit and recovery | Quit with A/B open, including a failing save: quit aborts until resolved. Successful quit/relaunch restores only the open set when requested by system policy. Interrupted-process recovery returns the latest persisted draft, without asserting recovery of never-written edits. |
| View restoration | Resize/move each window, select different ranges and scroll; close/reopen and relaunch preserve each window independently. Disconnect a display, shorten text externally, corrupt a view record or remove a file: safe frame/range/fallback/unavailable state appears without replacing content. |
| Activation and commands | Switch A → B → another app → back; native key/main/inactive cues and each selection persist. Save targets B only. With Settings key, document saves are disabled and Close affects Settings only. With no documents, New/Open/Settings work; closing the last window does not quit. |
| Layout and enlargement | At 480 × 360, 900 × 650, 1440 × 900 pt content areas, intermediate sizes and full screen, test 100% and 200%, long labels and long paragraphs. Labels wrap/stack, content scrolls, selection survives and essential actions remain available. Repeat when available display area is below the nominal minimum. Dimensions are test proposals, not measured results. |
| Settings | Invoke repeatedly: one window, no new document IDs. Change Text Size, close/reopen and relaunch: value persists, notes stay unmodified. Closing Settings changes no note/save state. |
| Keyboard and accessibility | Complete New → edit → Save → switch windows → close → reopen → Settings using keyboard/menu routes; repeat with Full Keyboard Access. Confirm focus and essential actions remain reachable at 200%. Use Accessibility Inspector and native assistive-input testing; verify labels/states rather than inferring them from this prose. |

## Audit and evidence limits

**Passed — static specification review:** interface.md now contains explicit contracts for all five supplied failures, creation/open/reuse/close/quit transitions, save failure, restoration fallback, sizing, enlarged text, Settings scope and command availability. The worked trace is consistent with the one-window-per-document policy. Official links identify the local guidance basis.

**Failed — supplied baseline:** the original interface.md reports shared mutable state, cross-document data loss, lost restoration state, fixed-layout clipping and duplicated Settings documents. These are reported defects; no runtime reproduction was available. No executed runtime pass or failure is claimed for the revision.

**Not executed:** compilation, SDK/API availability checks, storage durability/fault injection, GUI rendering, menu integration, native window management, multi-display/full-screen transitions, actual font/geometry measurement, keyboard execution, Accessibility Inspector, VoiceOver or other accessibility execution. The specification cannot prove these outcomes or establish accessibility conformance.

Audit route: explicitly read the installed `.agents/skills/apple-hig/SKILL.md`, then Presentation family and searched `references/topic-index.md`. Read Getting started → Designing for macOS, Presentation → Windows, Foundations → Layout/Accessibility/Typography, Patterns → File management/Settings/Multitasking, Inputs → Keyboards, and Menus and actions → The menu bar. Each family/topic procedure was read before its supporting guide using separate file-reading commands resolved under the installed package. Consulted each corresponding local reference; the relevant Typography introduction/macOS section was reread separately after large output truncation. No screenshots, visual demonstrations, application code or SDK documentation were supplied or evaluated. No web browsing occurred.

Sources are the installed English HIG-derived snapshot dated 2026-10-25, not a live verification of Apple documentation or an independently validated SDK reference. No material conflict affects these decisions; the menu guide's unrelated custom-menu ordering ambiguity does not determine this standard-menu subset. Proposed policy details and numeric product dimensions must be validated in implementation.
