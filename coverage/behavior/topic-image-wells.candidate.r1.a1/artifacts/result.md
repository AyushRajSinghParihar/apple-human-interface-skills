# Revised Mac contact-card portrait well

## Scope and decisions

The supplied `interface.md` establishes three defects: the square preview does not communicate editability, any file is accepted before silent failure, and replacement cannot be undone. It also establishes optional portraits and multiple-contact selection. It supplies no implementation or rendered screen.

Use an **editable image well**, retaining the square preview. A persistent “Portrait” label and visible “Choose Portrait…” action make editing discoverable without hovering. Show “Drop an image here” beneath the well when empty and “Drop an image to replace” when populated. A bezel identifies the editable container; selection, keyboard focus, and eligible-drop outlines are visually distinct. These presentation details are product decisions, not prescribed HIG geometry. The component choice and direct-drop/selected-command behavior follow [Image wells](https://developer.apple.com/design/human-interface-guidelines/image-wells#Best-practices).

Portraits are optional. Clearing removes the custom portrait and shows an initials placeholder, or a generic person silhouette if initials are unavailable. The placeholder represents “No portrait”; it is never copied as if it were a custom image. If a future product requires portraits, clearing must instead restore an appropriate default, as qualified in the image-well guidance. No operation deletes or changes the source file.

Editing is restricted to exactly one writable contact. With no contact selected, show “Select a contact to edit its portrait.” With multiple contacts selected, show a neutral group placeholder and “Select one contact to edit its portrait.” Disable Choose, portrait editing commands, and drops; never choose an arbitrary contact or silently apply a batch change. For a read-only contact, display its portrait and “This contact is read-only”; allow Copy of a custom portrait but disable mutations. These are explicit product policies.

## Input, validation, and feedback contract

Accept exactly one JPEG or PNG image, supplied as decoded image data or a local file representation. For this revision, other formats, directories, multiple items, file lists with mixed content, and remote URLs are unsupported. Validate actual content rather than trusting the extension. Product limits: at most 20 MiB of encoded input and 40 million decoded pixels, with positive dimensions; reject safely before allocating beyond those limits. Decode using bounded resources. The same validation applies to Choose, Paste, and Drop. A file chooser filters for supported images but still validates the chosen content.

When multiple representations describe the same dragged image, select the richest usable representation within this accepted set; do not treat those representations as multiple images. Import a copy into contact-owned storage. A portrait drop always copies, including from another app; Option does not turn it into a move. This field-specific copy policy prevents source loss. See [Drag and drop — Best practices](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop#Best-practices).

| Event or state | Required behavior |
|---|---|
| Pointer click on editable well | Select and focus the well; do not change the portrait. |
| Choose Portrait… | Open image selection; successful validation commits one replacement; cancel leaves data and history unchanged and returns focus to the invoking control. |
| Drag enters an unselected well | Prior selection is unnecessary. Inspect advertised content and contact eligibility. Highlight only a provisionally eligible target with a copy cue; this is not a success indication. |
| Known unsupported drag | Show unavailable feedback; do not highlight as accepted. On attempted drop, explain the rejection. |
| Drag exits or is canceled | Remove drop feedback; preserve portrait, selection, and history. |
| Provisionally eligible drop | Recheck target and payload; validate asynchronously if needed. Select the target well, retain the old portrait, and show “Checking image…” beside it. Do not show the new image as saved yet. |
| Valid image | Persist owned image data and portrait reference atomically, then show the new preview, select the well, and announce “Portrait updated.” |
| Invalid input or read/decode/storage failure | Keep the old portrait and history. Show a persistent inline explanation, for example “Couldn’t use this image. Choose one JPEG or PNG image, up to 20 MiB and 40 million pixels.” For storage failure use “Couldn’t save portrait. Your previous portrait is unchanged. Try again.” Provide Dismiss; retry through Choose, Paste, or Drop. |
| Contact selection changes during validation | Cancel/invalidate the pending operation. Never apply its result to the newly selected contact or commit later to the old one. |
| Pending operation | Disable further portrait mutations; keep Cancel available. Cancel preserves data/history. Copy can still copy the current committed portrait. |

Feedback uses text and outline/icon changes rather than color alone. A small fixed well needs no internal autoscroll; an enclosing scrollable card may scroll only while the pointer remains within its eligible scrolling region. Failed drops must not animate or announce success. These follow [Drag and drop — Providing feedback and Accepting drops](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop#Providing-feedback); validation limits and exact wording are product choices.

Display the complete image proportionally within the square, with neutral padding where necessary. Do not distort or silently crop faces. No crop editor is introduced in this revision.

## Commands and accessible operation

The selected/focused well owns portrait commands; merely selecting a contact does not redirect Delete from the contact list to its portrait. If focus is in a text field, its editing commands retain their ordinary scope. Undo/Redo use the contact window’s history regardless of current field focus.

| Command | Eligibility and effect |
|---|---|
| Edit > Copy, Command-C | Selected well with a committed custom portrait, including read-only contacts. Copy image data; never copy the entire contact or placeholder. |
| Edit > Paste, Command-V | Selected editable well, no pending operation, and exactly one apparently compatible image. Run full validation before committing. Disable for known incompatible/empty pasteboard content; report later decode failures without loss. |
| Edit > Cut, Command-X | Selected editable well with a custom portrait. Copy first; only after successful pasteboard write, remove portrait as one undoable edit. Failed copy leaves portrait intact. |
| Edit > Delete; Delete key | Selected editable well with a custom portrait. Remove without changing the pasteboard; show placeholder. Never delete the contact or source file. |
| Remove Portrait (visible beside Choose) | Same eligibility and effect as Delete; offers an explicit removal route. |
| Edit > Undo / Redo | At the top of Edit; Command-Z / Shift-Command-Z. Use action-specific labels described below. |

Disable inapplicable commands rather than leaving deceptively enabled actions. Use the platform host’s standard menu ordering and shortcut dispatch when available; the framework must provide equivalent application-menu behavior if it does not supply it automatically. The specification requires these behaviors without assuming AppKit or another Apple SDK. See [Edit menus — Best practices](https://developer.apple.com/design/human-interface-guidelines/edit-menus#Best-practices).

Expose the well as a focusable, selectable editable-image container with name “Portrait for {contact name}”, value “Custom portrait” or “No portrait”, selected/busy/read-only states, and an accessible description of replacement. Expose Choose, Remove, Cancel, and Dismiss as named actions with standard button semantics. A group placeholder is described as “Multiple contacts selected; select one contact to edit portrait.” Do not announce decorative initials separately. Keyboard navigation follows card order: well, Choose, Remove when available, then following contact fields; pending/error controls occur next to the well. Keyboard/assistive activation must complete selection, replacement, removal, error recovery, and undo without dragging.

Use visible focus, labels that remain readable at 200% text scale, and layout that reflows the controls below the image rather than clipping them. Start with macOS’s documented 28 × 28 pt default activation area, with sufficient separation; do not treat the smaller minimum as the design target. Check light/dark and Increase Contrast appearances with actual rendered colors. Do not require animation or sound to understand results. These requirements follow [Accessibility — Vision, Mobility, and Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). Actual geometry, contrast, and assistive behavior remain to be measured.

## State and history model

Maintain `selectionContext`, `committedPortrait[contactID]`, `wellSelection`, and an optional pending token. Store portrait contents or durable owned references in history, including the previous absence of a portrait. Never rely on an external source path remaining readable.

```text
beginImport(payload):
    require exactly one writable contact and no pending import
    capture contactID, selectionRevision, new token
    keep committed portrait visible
    validate and prepare owned image off the UI thread
    if canceled or token/context no longer matches: discard prepared data
    if validation/storage fails: show error; do not mutate history or portrait
    else atomically commit ChangePortrait(contactID, before, after)

ChangePortrait.apply / undo / redo:
    update only stored contactID, using retained image data or absence
    publish preview only after successful persistence
    if persistence fails: preserve current value and history cursor; report failure
    reveal affected contact and well, with visible result and status
```

Each successful Choose/Paste/Drop is one history entry, labeled “Undo Change Portrait” / “Redo Change Portrait”. Remove and Cut are “Undo Remove Portrait” / “Redo Remove Portrait”; undoing Cut restores the portrait but does not rewind the clipboard. No-op changes, rejection, cancellation, focus changes, and contact selection create no entries. New successful edits after undo discard the redo branch. Retain the meaningful sequence for the open contact window, including across successful saves; closing the window ends this revision’s history session. No arbitrary shallow cap is specified. External deletion of a target must produce an explicit unavailable-history error rather than restoring into another contact.

If undo targets a different contact from the current selection, reveal/select that contact and its well so restoration is visible. Preserve unrelated contact data. Ordinary reversible replacement/removal needs no confirmation. These decisions apply [Undo and redo — Best practices and macOS](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#macOS).

## Worked before / after

**Before, from the brief:** Alex’s square portrait offers no visible editing cue. Dropping a PDF is accepted and silently fails. Replacing Alex’s portrait with a valid photo cannot be undone. Multiple-contact behavior is unspecified.

**After:** Alex’s card shows Portrait, its editable bezel, Choose Portrait…, and replacement guidance. Dragging a PDF produces unavailable feedback; attempting the drop shows the supported-image explanation and leaves Alex’s original portrait intact. Dropping `alex-new.png` without selecting the well first shows a copy cue, then Checking image… while retaining the original. Successful validation and persistence replace it in one transaction. Command-Z, labeled Undo Change Portrait, restores the exact prior portrait; Shift-Command-Z restores the replacement. Remove Portrait shows No portrait and an initials placeholder; Undo Remove Portrait restores the image. Selecting Alex and Sam together disables mutation and explains how to proceed, without modifying either portrait.

This is a specified outcome, not a record of executed UI behavior.

## Acceptance checks and evidence status

**Passed — document inspection only:** Read `interface.md`; explicitly read the installed root skill; searched its topic index; read the selection/input, patterns, foundations, and menus/actions family procedures, their selected image-well, drag/drop, undo/redo, accessibility, and edit-menu topic procedures before their supporting guides. The revised contract covers all three stated defects and both empty/multiple-selection cases. Official links above are citations from local guides, not web verification.

**Failed — supplied behavior, reported by the brief:** Editability is not distinguishable; unsupported drops silently fail; replacement lacks undo. These are brief-backed findings, not independently reproduced failures.

**Not executed — implementation acceptance checks:**

1. Drop a valid JPEG/PNG onto an unselected well. Confirm copy semantics, source preservation, visible eligibility, one commit, and resulting well selection. Exit/cancel a drag and confirm feedback disappears with no mutation. Check Option pressed/released: import remains a copy.
2. Try a PDF, renamed non-image, corrupt PNG, directory, remote URL, two images, empty clipboard, and oversized/over-pixel-limit images. Check rejection, explanation, no success feedback, unchanged committed image, and no history entry. Test valid multiple representations of one image separately from multiple images.
3. Simulate slow decode, read/storage failure, cancellation, selection change, and stale completion. Verify old portrait remains until commit, retry is possible, and no result reaches another contact.
4. With the well selected, exercise menu and keyboard Copy/Paste/Cut/Delete. Verify copied content, Cut failure safety, Delete’s unchanged clipboard, disabled empty/read-only commands, and no command acting on a contact list or text-field selection by mistake.
5. Start with no portrait; add A, replace with B, remove. Undo through B, A, and absence; redo through all states. Undo then import C and verify redo is cleared. Save and repeat undo. Navigate elsewhere before undo and confirm the correct contact is revealed. Verify failed undo persistence leaves history/value consistent.
6. With zero, one, read-only, and multiple selected contacts, verify every displayed state and command/drop eligibility. Ensure neither an arbitrary target nor bulk change occurs.
7. Complete choose, paste, remove, failure recovery, undo, and redo using keyboard and supported assistive input. On the Mac, test VoiceOver, Full Keyboard Access, and Switch Control; inspect names, roles, states, navigation order, and announcements. Check 200% text, light/dark, Increase Contrast, measured text contrast, activation geometry, and visible focus.

## Evidence limits

Only local text files and installed instructions were used. The local guidance is a dated 2026-10-25 snapshot derived from Apple HIG, not an SDK reference or proof of independent source review. No web access, source-code implementation, native pasteboard/drag execution, build, SDK compilation, GUI, Apple device, or accessibility execution was performed. No rendered dimensions, contrast values, timing, or assistive order were measured. Limits, accepted formats, labels, single-contact scope, placeholder, history lifetime, and fit-with-padding policy are explicit product decisions awaiting implementation and the checks above; they are not claimed as universal Apple requirements.
