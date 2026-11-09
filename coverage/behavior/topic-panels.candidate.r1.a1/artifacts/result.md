# Image-inspector repair result

Updated `interface.md` in place from a three-sentence defect report to an implementable macOS presentation, target, lifecycle, persistence, and keyboard contract.

## Decisions and patch summary

- Replace the per-click document-modal sheet with one reusable standard Color Inspector panel so inspection and image editing can coexist. Include a movable title bar, show/hide route, activation behavior, and full-screen acceptance requirements. [Panels](https://developer.apple.com/design/human-interface-guidelines/panels#Best-practices) supports contextual tools; [Modality](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices) calls for a clear benefit before blocking work.
- Interpret “inspector” as following the active document, with each document retaining its own selected sample. The brief does not establish a requirement to pin one image across activation changes. A stable-object view would instead require a regular Info window under the [Panels guidance](https://developer.apple.com/design/human-interface-guidelines/panels#Best-practices). The patch explicitly identifies the target and handles absent/invalid selections and late results.
- Separate hiding a tool from document saving. Read-only inspection cannot dirty a document; closing the panel cannot save unrelated edits. Preserve existing document autosave or manual-save policy, dirty state, save-error recovery, and document-local undo. This is a product-level repair informed by [File management](https://developer.apple.com/design/human-interface-guidelines/file-management#Saving-work) and [Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#macOS), not a blanket prohibition on autosave.
- Add a menu and keyboard path, explicit panel-key versus document-key command targeting, and a conditional keyboard sampling fallback. [Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Best-practices) and [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards#Standard-keyboard-shortcuts) support discoverable commands and keyboard workflows. No new editing controls, framework migration, or storage system is specified.

## Worked before/after

**Before, from the supplied brief:** Clicking a color opens a document-modal sheet, blocking comparison with the image. Activating another document loses the target. Closing the inspector saves unrelated edits. The brief supplies no exact values, file names, implementation, or runtime trace.

**After, proposed scenario:** A contains an unsaved crop and selected sample at (24, 18). Inspecting that sample opens Color Inspector while A remains editable. A second sampling click updates the same panel. Activating B shows B's name and its retained sample, or the selection prompt; A's crop and sample remain in A. Returning to A restores (24, 18) and reads its current color. Closing the panel leaves A's crop unsaved under a manual-save policy and does not save B. Reopening follows the current document. Undo in A reverses A's crop rather than panel visibility. With autosave enabled, its independent policy still applies; dismissal never initiates Save All.

## Acceptance checks

All rows below are implementation acceptance scenarios, **not executed**. Use two documents with distinct samples and separate unsaved edits; observe readouts, document identities, undo histories, and save-handler calls/file writes.

| Check | Expected outcome |
|---|---|
| Inspect repeatedly; edit, pan, zoom, compare | One panel; image remains interactive; no sheet or inspection-induced dirty state. |
| A → B → panel focus → A | Correct labeled target at every step; per-document samples and edits retained; panel focus does not retarget. |
| B has no sample; sample invalidated; all documents closed | Explicit empty state; no stale readout or accidental fallback sample. |
| Delayed A result arrives after B activation or A closure | Result rejected; B/empty state remains correct. |
| Close control, Hide menu, Option-Command-I, panel-key Command-W, clean and edited documents | Same hide-only result; no save call, dirty-state change, discard, or history reset. Reopen follows current context. |
| Document-key Command-W; File > Save while panel key; no document | Normal document-close protection; Save targets the active document only; unavailable without a document. Failed save retains unsaved state. |
| Manual saving and autosaving configurations | Hide never initiates saving; manual dirty work stays dirty; independent autosave continues. Reopen saved files to verify actual durability. |
| Edit A, edit B, undo/redo A; grouped continuous edit; new edit after undo | Correct document and meaningful undo unit; visible reversal; only A's redo branch invalidated. Save/hide do not reset history. |
| Hide/reopen; switch apps and return | Samples preserved; visible panel hides over other apps and returns; intentionally hidden panel stays hidden. |
| Close target document; resize/move windows; enter/leave full screen | No dangling target; usable image comparison and commands; no forced modal presentation, panel minimization, or document-list entry. |
| Complete sampling/show/hide/save using keyboard; Escape during sampling; close focused panel | Reachable task, no shortcut collisions, cancellation preserves prior sample, sensible focus return. Check international layouts and Full Keyboard Access separately. |

## Evidence and limits

**Passed — static artifact review:** Read the revised `interface.md` after writing it. It contains a nonmodal presentation, explicit document/sample ownership, selection and activation transitions, all specified hide paths, no-target handling, persistence separation, undo ownership, keyboard route, and official guidance links. The worked scenario is consistent with those written rules. This establishes specification coverage only.

**Failed:** No executed implementation checks failed, because no implementation was supplied or run. The original brief reports the three defects above; those are reported behavior, not independently reproduced failures.

**Not executed:** All acceptance scenarios, macOS GUI/device behavior, native panel key/main behavior, actual save/undo execution, SDK compilation, multi-display/full-screen behavior, keyboard layout tests, Full Keyboard Access, and assistive-technology checks. No accessibility execution or conformance is claimed.

The only product evidence supplied was the original `interface.md`. No application code, screenshots, SDK version, controls inventory, persistence implementation, or runtime was available. The contextual target model and read-only inspector scope are stated design assumptions. No exact color values, visual measurements, SDK API guarantees, or native rendering results are inferred.

Instruction audit: explicitly read the installed `.agents/skills/apple-hig/SKILL.md`; searched its topic index for inspector/panel/modality/keyboard and file/undo concepts; read the Getting started, Presentation, Patterns, and Inputs family instructions. Read each selected topic procedure before its source guide: Designing for macOS, Panels, Modality, File management, Undo and redo, and Keyboards. Every instruction/source read used a separate `cat` command for one file. Guidance came only from that installed package's local snapshots; official links above are attribution, not browsed verification. No web browsing was performed.
