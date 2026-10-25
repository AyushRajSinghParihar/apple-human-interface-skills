# macOS image inspection — revised specification

## Task and scope

Inspect a selected image color while continuing to edit and compare the image. Replace the reported document-modal sheet on every click with one reusable, nonmodal floating **Color Inspector**. Retain the existing editor and document format; this change does not add color-adjustment controls or a new storage system.

The supplied brief reports three defects: blocked comparison, lost inspection target after document activation, and unrelated edits saved on inspector close. The following is the replacement behavior contract, not evidence of a running implementation.

## Presentation and commands

- Use a standard macOS panel with a movable title bar titled Color Inspector. Keep it compact, repositionable, and visually subordinate to the image. Do not dim or disable the document. Avoid HUD styling, disable minimization, and exclude it from the Window menu's document list.
- Window > Show Color Inspector / Hide Color Inspector toggles the same instance; Option-Command-I invokes that command. Showing it again does not create another panel. A color-inspection click opens it if hidden and updates its contents if visible; ordinary editing clicks retain their existing meaning.
- The close control, Hide command, and Command-W when the panel is key all hide the panel. They do not close a document, save, discard, apply changes, or clear inspection state. Command-W when a document is key retains normal document-close behavior. There is no Done or Save button in this read-only inspector.
- Keep documents interactive while the panel is open: selection, zoom, pan, editing, and document activation remain available. Repositioning the panel must allow unobscured image comparison. Full screen must retain access to the inspector command, inspector, image, and editing commands without a modal fallback.

## Target and lifecycle contract

This is a contextual inspector, not a pinned Info window. It follows the active document and that document's selected sample. Preserve a separate sample location/selection per document so returning to a document restores its inspection context.

Store document identity and sample identity/location explicitly; never infer ownership from whichever window happens to be key. Focusing the panel does not change the active document. Display the document name and sample location alongside the existing color readout; disambiguate duplicate names with location information. Refresh the readout when edits change the sampled content. Inspection itself never dirties a document.

| Event | Required result |
|---|---|
| Inspect a sample in A | Bind to A and that sample, show/update the single panel; A remains editable. |
| Inspect another sample in A | Replace A's selected sample immediately; no sheet, nested presentation, or save. |
| Activate B | Retain A's selection; atomically show B's retained selection and readout. If none exists, show B and “Select a color in the image.” Never leave A's values labeled as B. |
| Focus panel | Preserve the current document target; focusing the tool is not document activation. |
| Return to A | Restore A's sample and recompute its current readout; preserve A's image view and edits. |
| Selection becomes invalid | Clear the stale readout and show the selection prompt; do not silently choose another sample. |
| No eligible document | Show “No image selected” with no stale color values. |
| Target document closes | Release its target/state, then follow the remaining active document or the empty state. Reject late updates from the closed document. |
| Hide/close and reopen panel | Retain per-document selections; reopen on the current document, not the document active when hidden. |
| App deactivates/reactivates | Hide the panel over other apps; preserve visibility intent and all document state. On return, restore a previously visible panel in front of app windows and refresh the active target. An intentionally hidden panel stays hidden. |

Bind asynchronous readouts to a document/sample revision token; discard results that no longer match the current target. This is a proposed safeguard against stale context, not an observed implementation defect.

## Editing, persistence, and recovery

All image edits remain owned by their document and use its existing undo history and saving policy. Switching documents or hiding the inspector neither commits a separate editing session nor rolls back edits. Any existing continuous edit is finalized to its original document before rebinding; queued edit events cannot be redirected to the newly active document.

Inspection, show/hide, close, and activation handlers must not invoke Save, Save All, or clear dirty state. This does not disable independent document autosave. If autosave exists, it continues on its own document lifecycle/schedule; panel dismissal is not its trigger. If autosave is off, dirty documents retain their unsaved indication and normal document-close/quit save protection. Save failure retains unsaved state. File > Save (Command-S) saves only the targeted document, including when the panel is key; disable it with no document target.

Preserve document-local Edit > Undo / Redo (Command-Z / Shift-Command-Z). Inspection and panel visibility do not enter edit history. One existing continuous adjustment is one meaningful undo unit; undo reveals the affected image and refreshes the inspected value. New edits after undo invalidate redo in that document only. Panel dismissal does not reset history.

## Keyboard path and return

From a document, invoke Show Color Inspector through the menu or Option-Command-I. Preserve the editor's keyboard selection path; if sample selection currently has only a pointer route, supply a keyboard sampling mode: arrows move the sample one image pixel and Return selects it, Escape cancels movement and restores the prior sample. This is a proposed fallback, not a claim about existing controls.

Allow standard keyboard navigation between document and panel. Opening for inspection need not steal keyboard focus from the image. Closing a focused panel returns focus to the active document's prior valid focused view; with no document, use the app's normal empty workspace. Escape cancels a current sampling/editing action without saving or dismissing unrelated work. Verify ordinary keyboard navigation and Full Keyboard Access separately on macOS.

## Guidance basis

The panel choice and contextual-versus-fixed distinction follow [Panels — Best practices](https://developer.apple.com/design/human-interface-guidelines/panels#Best-practices). Reduced interruption follows [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices). Multiwindow context and menu access follow [Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Best-practices). Shortcut choices follow [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards#Standard-keyboard-shortcuts). Document saving and recovery follow [File management](https://developer.apple.com/design/human-interface-guidelines/file-management#Saving-work) and [Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#macOS).

These are locally read snapshot sources. Exact target tokens, empty-state copy, keyboard sampling fallback, and dismissal/save separation are product decisions applying that guidance; Apple does not prescribe this complete state model. Runtime acceptance scenarios and evidence limits are recorded in result.md.
