# Revised iPad laboratory notebook interaction specification

## Scope and decisions

This is a framework-agnostic design contract for the iPadOS notebook described in `interface.md`. Apple Pencil is optional. The supplied artifact is a behavior description, not an implementation. Requirements below are proposed product decisions; HIG support is cited separately. No Apple SDK is assumed.

| Supplied behavior | Revised decision | Reason and source |
|---|---|---|
| Typing is disabled when Pencil is nearby | Proximity changes neither text availability nor focus, selection, keyboard visibility, or document content. Typing, paste, touch, and Pencil can alternate within the same task. | Pencil should support ordinary control activation and mixed writing tasks; hover must never activate content. [Pencil: Best practices, Hover](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble) |
| Specimen IDs require handwriting | Store IDs as editable text. Offer onscreen keyboard, hardware keyboard, paste, and optional handwriting-to-text. Never require recognition to complete entry. | Text fields suit short specific values; preserve keyboard entry and familiar editing. [Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields), [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards) |
| One gesture erases ink and deletes pages | Erasing affects ink only. Remove the page-deletion interpretation entirely. Provide a separate labeled “Delete page” action with cancellation and recovery. | Keep gestures predictable and provide visible alternatives; Pencil hardware gestures should be nondestructive and reversible. [Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures), [Pencil: Double tap, Squeeze](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble) |
| Text boxes are custom canvases | Retain a drawing surface for ink; replace short-value text canvases with semantic editable text controls, or an adapter satisfying the text contract below. Rendering text on a canvas alone is insufficient. | Standard editable text supports Scribble automatically in supported environments; custom fields need explicit handwriting behavior. This does not establish support in the eventual framework. [Pencil: Scribble](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble), [Accessibility: Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility) |

## Surface and data contract

A page contains a persistently labeled “Specimen ID” text field and a separate labeled “Ink notes” drawing region including useful margins. Keep their hit regions distinct: writing in the ID region edits text; writing in the drawing region creates ink. No stroke may fall through from a field into the drawing region. A stroke retains its original target until it ends. Other existing text content must retain its values when migrated out of canvas rendering.

Use visible Pen, Eraser, Undo, Redo, and Delete page actions. Show the active drawing tool with both a name and selected state. Pencil can activate these controls. Finger dragging in the drawing region scrolls by default; an explicit “Draw with finger” option enables finger marking for people without Pencil. While that option is active, provide a visible Scroll action to restore navigation. Essential text and page operations never depend on drawing ability.

For controls, start with iPadOS activation areas of 44 × 44 pt, with separation preventing overlap; this is a product target based on the guide’s default, not a claim about measured geometry. Keep tools clear of either writing hand and allow repositioning. Use body text at the iPadOS 17 pt default with semantic sizing or equivalent. At 200% text scale and supported larger accessibility sizes, grow and stack controls and labels; preserve full ID access through editing/scrolling rather than ellipsis alone. [Accessibility: Vision, Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [Typography: Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography)

### Specimen ID field

- Representation: an exact text string, not a number; preserve leading zeros, case, punctuation, and entered Unicode. Disable automatic capitalization, spelling correction, and smart punctuation for this identifier. Offer an alphanumeric entry layout where available, never a digits-only restriction.
- Purpose: persistent “Specimen ID” label; placeholder is optional and hides as writing begins. A trailing “Clear specimen ID” control clears only the draft and is undoable.
- Editing: caret, range selection, copy, cut, paste, deletion, and undo work across input methods. Changing inputs preserves the draft, caret, selection, and committed value. Handwriting recognition updates the same draft; it does not silently commit an ID.
- Commit: explicit “Apply specimen ID” or Return validates and commits. Leaving the field retains the draft without silently applying it. “Cancel ID edit” restores the last committed value and ends editing. Page navigation retains drafts so a failed or interrupted edit is recoverable.
- Validation: require a nonempty, non-whitespace-only value on Apply. Keep the draft and show “Enter a specimen ID” next to the field if invalid; do not clear it or trap focus. Apply stays available so its failure can be explained. No laboratory format, length limit, uniqueness rule, or registry is supplied; impose none in this specification. A whitespace-containing nonblank ID is preserved, not trimmed. Any later laboratory rule must have explicit corrective feedback before commit.
- Long values remain editable end to end without clipping data. Locale/input-source changes never parse the ID as a localized number or transform its characters. These are ordinary identifiers; no supplied evidence establishes a need for password-style masking.

These validation and commit rules are product decisions, informed by [Text fields: Best practices](https://developer.apple.com/design/human-interface-guidelines/text-fields).

## Interaction and state model

Track independently: `textDraft`, `committedID`, `textSelection`, `focusedTarget`, `drawingTool`, `activeStrokeTarget`, `pendingTranscription`, `pageDeletionState`, and reversible document edits. Pencil availability is capability metadata, never an edit lock.

| Event/context | Required transition and feedback |
|---|---|
| Pencil approaches, leaves, disconnects, or hovers | Preserve all editing state. Supported hover may preview the likely ink mark inside the ink region only; never write, commit, focus, erase, or delete. |
| Tap ID with finger/Pencil; keyboard navigation enters ID | Enter text editing. A finger tap offers the onscreen keyboard when appropriate; hardware typing remains available. Pencil activation must not disable the explicit keyboard route. |
| Pencil writes in ID target, handwriting supported | Begin without a preliminary focus tap. Hide placeholder. Freeze field position, transcription position, and writing-area geometry while writing/selection is active. Convert into editable draft text; defer reflow or scrolling until a writing pause and selection has ended. |
| Handwriting unavailable or recognition fails | Keep existing text intact. Offer “Use keyboard” and paste. Explain unavailable handwriting without presenting the field as unavailable. Do not create a fake transcription or silently save raw strokes as the ID. |
| Pencil contacts ink region with Pen | Begin drawing immediately without first selecting Pen for every stroke. Initial drawing tool is Pen; an explicitly chosen Eraser remains active until changed. Feedback follows contact; useful margins also accept marks. |
| Eraser stroke | Remove only intersecting ink strokes on the current page, grouped as one undoable edit per eraser stroke. Never remove text, page metadata, or the page, even when all ink is gone. |
| Pending handwriting plus another edit/Apply | Serialize edits to avoid late recognition overwriting newer typing. Apply waits for the active text composition to finish; show “Finishing handwriting…” while pending. Cancel invalidates its recognition token. Discard late results for canceled or superseded drafts. |
| Tool change during a stroke | Queue the change until stroke end; do not reinterpret an in-progress stroke. |
| Undo / Redo | Reverse/reapply the most recent edit in the active editing context; the action label identifies the operation, such as “Undo erase ink.” Field undo edits its draft. Outside field editing, document undo includes ink edits and page deletion. |

If supported by actual hardware, honor the person’s preferred Pencil double-tap tool mapping when applicable, including no action. Do not add a custom override by default. Squeeze may show quick tool choices near the tip as one discrete action; it never deletes or erases content directly. Barrel roll may affect a meaningful mark property, never navigation. Pressure and tilt may affect mark qualities, but neither is required for a legible mark or essential action. All hardware features require capability checks and have visible alternatives. [Pencil guidance](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble)

### Separate page deletion

Activating “Delete page” identifies the current page and asks “Delete this page and its contents?” with Cancel and Delete page actions. Cancel is the initial safe action and preserves the page, draft, selection, and drawing tool. Confirmed deletion moves a complete page snapshot, including drafts and ink, into a recoverable deleted-pages store; it does not permanently purge it. Select the next page, otherwise the previous page, otherwise an empty-notebook view with Add page. Expose a persistent “Page deleted” status with Undo and a labeled “Deleted pages” recovery route. Recovery is not dependent on a timed toast. Undo restores the page at its prior position with its content; Redo repeats the recoverable deletion. Permanent purge is outside this specification.

This confirmation and recovery policy is a product choice to protect notebook content, not a universal HIG requirement. In an eventual Assistive Access adaptation, any difficult-to-reverse deletion must follow the local guide’s two-confirmation condition. [Accessibility: Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility)

## Keyboard, gesture, and alternative access contract

Preserve ordinary text gestures and system undo/redo, copy/paste, app switching, edge navigation, and multitasking gestures. Do not reuse the former ambiguous erasing gesture for a second operation. Eraser is an explicit tool; no hidden page-deletion gesture remains. Offer visible Undo and Redo even when a compact drawing palette omits them. [Gestures: iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/gestures)

Use Command-C/X/V/A for normal text selection editing and Command-Z / Shift-Command-Z for Undo/Redo in context. Delete/Backspace in text edits text only; outside text it never deletes a page. Escape cancels a pending deletion or ID edit. Do not introduce a page-deletion shortcut. Keep the standard editing commands discoverable without overriding system accessibility shortcuts. [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards)

Ordinary iPad keyboard content navigation enters the page content group with Specimen ID as its primary item. Tab/Shift-Tab traverse logical content groups; arrows navigate within appropriate custom groups and retain text-caret semantics inside the field. Full Keyboard Access must separately reach and activate every tool, Apply, Cancel, Clear, Delete, confirmation, and recovery control. Ordinary content focus alone is insufficient evidence of that access. Focus must remain distinct from selected drawing tool and selected page. Return from canceled deletion restores its invoker. [Focus and selection: iPadOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection)

Expose the ID as an editable-text role with label, exact value, required state, and associated validation feedback. Expose actions with names, button roles, availability, and selected tool state where applicable. Ink notes has a named drawing region; tool and recovery actions remain reachable without drawing gestures. Error and deletion statuses use text, not color or sound alone. Complete the ID-entry and page-recovery task with keyboard and supported assistive input; handwriting is optional. Detailed spoken order and actual assistive behavior remain implementation verification work. [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

## Worked before/after

Example data `AB-0017` is illustrative, not an inferred laboratory format.

**Before (from the brief):** A researcher reaches for Pencil while entering the specimen ID. Proximity disables typing; the ID must be handwritten into a custom canvas. An attempt to erase an incorrect mark uses a gesture that also means delete page. The brief does not specify how that conflict is resolved or whether recovery exists.

**After (specified):** The researcher types `AB-00` with Pencil nearby, then writes the remaining `17` in the ID field. Its geometry stays still during writing; recognition inserts text into the same draft. If recognition produces `AB-00I7`, the researcher selects `I` and types `1`, then applies `AB-0017`. The committed identifier remains exact text. A Pencil mark in Ink notes appears immediately. Selecting Eraser and crossing that mark removes only the ink; the ID and page survive. Undo restores the mark. Separately activating Delete page opens the explicit confirmation. Cancel changes nothing; confirmation moves the complete page to recovery, and Undo restores it.

## Acceptance checks and evidence status

**Passed — specification inspection only:** Read `interface.md`; mapped all four supplied behaviors to revised contracts; explicitly read installed root, selected Inputs / Selection and input / Foundations family procedures, routed Pencil, keyboards, gestures, fields, focus, accessibility, and typography topic procedures before their supporting local guides. The specification contains input alternatives, independent states, validation, recovery, and observable failure criteria.

**Failed — supplied behavior against the revised contract:** Pencil proximity disables typing; handwriting is mandatory for IDs; erase and page deletion share a gesture. These failures are established by the brief, not device execution. Custom canvas text is a risk requiring semantic and editing verification; the brief alone does not prove it lacks accessibility semantics or Scribble support.

**Not executed — implementation/device acceptance:** Every check below is required before claiming the revised behavior works.

| Check | Pass condition |
|---|---|
| Mixed input | Type, paste, and edit with Pencil nearby/hovering; remove or disconnect Pencil mid-edit. Draft, caret, selection, and keyboard access remain intact. Finish without Pencil. |
| ID values | Empty and whitespace-only Apply show contextual error and preserve draft. Partial `AB-` remains editable. `00017`, mixed case, punctuation, Unicode, long values, and changed input locale preserve exact text. Cancel restores the committed ID. |
| Scribble | Write into an unfocused field without a preliminary tap. No target/transcription movement mid-stroke or during selection; reflow waits for a pause. Correct recognition using keyboard; late/canceled transcription cannot overwrite newer edits. Test unsupported handwriting fallback. |
| Ink | First Pen stroke and margin strokes draw directly. Eraser removes intersecting ink only; erasing the last mark leaves page and ID intact. Undo/Redo restores/reapplies precisely that edit. Tool change mid-stroke does not reinterpret it. |
| Hardware | Hover never changes content. Test each available double-tap preference and supported squeeze; neither deletes content. Test hand occlusion, palm rejection, latency, pressure/tilt, and both handednesses on relevant devices. No numeric latency claim is made. |
| Deletion | Gesture, hover, squeeze, Backspace, and ink erase cannot delete page. Explicit Cancel preserves all state. Confirm/Undo/Redo and Deleted pages restore exact ink, committed text, drafts, and order, including the last-page case. |
| Keyboard | Complete enter–correct–apply–delete–cancel–recover task with hardware keyboard; verify ordinary focus separately from Full Keyboard Access. Text shortcuts retain meanings; test international layouts and system gesture conflicts. |
| Alternative input | Complete ID editing and page recovery using supported VoiceOver, Switch Control, and AssistiveTouch paths; labels, values, errors, and state are exposed and essential actions are reachable without handwriting. |
| Layout | At 200% text and supported larger sizes/Bold Text, essential labels and actions remain usable, full IDs remain accessible, and handwriting geometry stays stable. Measure activation areas and contrast in light/dark and Increase Contrast. Test keyboard occlusion and compact iPad window sizes. |

## Evidence limits

Only local supplied files and installed skill instructions/references were used. Official links above identify the sources represented by the local snapshot; no website was opened or checked. The references identify a 2026-10-25 snapshot and are application guidance, not an SDK reference or independent validation of current Apple behavior.

No application code, screenshots, devices, SDK, GUI, accessibility tools, recognition engine, or laboratory identifier policy was provided or executed. No native control availability, compilation, rendering, accessibility conformance, hardware comfort, latency, recognition accuracy, or persistence correctness is claimed. Custom text adaptation and optional handwriting remain feasibility work in the chosen stack; lack of an Apple SDK does not justify blocking typing. Laboratory retention, regulated audit trails, identifier schema, and permanent-deletion policy need separate product requirements before implementation can claim those properties.
