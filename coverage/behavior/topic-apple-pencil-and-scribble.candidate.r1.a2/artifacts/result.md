# Revised iPad laboratory notebook interaction specification

This specification replaces the behavior described in `interface.md`. Target: iPadOS, with optional Apple Pencil, touch, software keyboard, and hardware keyboard. It specifies observable behavior independently of any framework or Apple SDK. “Must” below defines the proposed product contract; it does not imply every decision is an Apple requirement.

## Decisions and source support

| Supplied behavior | Revised decision | Basis |
|---|---|---|
| Typing is disabled whenever Pencil is nearby | Proximity never changes text editability, focus, selection, or keyboard availability. Input changes according to the action and target. | Pencil is an additional input for drawing, handwriting, and ordinary controls; see [Apple Pencil: Best practices and Scribble](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble#Scribble). Proximity independence is our product rule. |
| Specimen IDs require handwriting | Use an actual short text field, accepting typing, paste, and optional supported handwriting conversion. Always offer a visible **Type** action. | [Text fields: Best practices](https://developer.apple.com/design/human-interface-guidelines/text-fields#Best-practices) and [Pencil: Scribble](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble#Scribble). |
| Text boxes are custom canvases | Separate structured text from ink. Prefer standard editable text primitives where the chosen stack supplies them; otherwise implement equivalent text semantics and editing. A drawing surface is not sufficient for a text field. | [Text views: Best practices](https://developer.apple.com/design/human-interface-guidelines/text-views#Best-practices). Automatic Scribble support described for standard controls is not promised for a custom implementation. |
| One gesture erases ink and deletes a page | Eraser affects ink only. A separate labeled **Move page to Trash** action removes a page recoverably; **Trash → Restore** remains available after navigation/relaunch. No permanent deletion in this scope. | [Gestures: Best practices and Custom gestures](https://developer.apple.com/design/human-interface-guidelines/gestures#Custom-gestures). Trash retention and recovery are product choices. |

## Surface and data contract

Each page contains a persistently labeled **Specimen ID** field, **Notes** multiline editor, and a distinct **Ink** region including useful margins. Boundaries must distinguish writing destined for text conversion from retained ink. Text controls take priority over overlapping expanded handwriting hit areas; expanded areas must never intercept Ink or another control. A stroke's initial target owns it until completion.

Store `specimenId: string`, `notes: string`, and `ink: strokes` separately. Keep raw text exact: preserve leading zeros, case, punctuation, and Unicode; never silently substitute O/0 or I/1, uppercase, trim, or autocorrect identifiers. Disable automatic spelling replacement/capitalization and smart punctuation for IDs where supported. Offer a general text keyboard with letters, digits, and punctuation, rather than a numeric-only pad. Notes use ordinary language entry and multiline Return. IDs use **Done** to commit. Hardware input and paste use the same validation path. These configurations follow [Virtual keyboards: Best practices](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#Best-practices); exact preservation is a notebook-specific integrity decision.

The brief supplies no specimen format or length constraint. Proposed baseline: ID is required when explicitly committing the specimen record; reject empty or whitespace-only values with “Enter a specimen ID.” Accept other nonempty values unchanged until a laboratory schema is supplied. Do not invent a format regex, uniqueness scope, or maximum length. Retain invalid/partial drafts locally, visibly distinguish **Draft** from **Committed**, and leave an existing committed value unchanged after failed validation. Blur retains the draft without committing. **Cancel edit** restores the value at edit start; **Done** validates and commits. Notes retain draft edits on blur. Show **Saved locally** only after persistence succeeds; on failure retain the draft and show **Not saved — Retry**. This is a proposed local persistence contract, not a regulatory audit-trail claim.

ID fields provide a trailing **Clear specimen ID** action affecting only the draft, reversible with Undo. IDs and Notes support caret placement, selection, copy, cut, paste, and undo/redo. Long IDs scroll within the editable field; a read-only full-value view wraps and permits copying without ellipsis-only access. Notes reflow and grow within the page's main scroll region; avoid a second independently scrolling prose editor. The page scrolls to reveal caret and completion actions when needed.

## Input and state transitions

Maintain independent states:

```
focusedText = none | specimenId | notes
textPhase = idle | editing | handwritingActive | awaitingTranscription
inkTool = pen | eraser                  // default pen
pageState = active | trashed
```

| Event / target | Required result |
|---|---|
| Pencil proximity changes | No content, focus, tool, or keyboard change. |
| Touch tap / keyboard focus / Type on text | Place or restore caret, begin edit; Type requests software keyboard. Hardware keyboard entry works regardless of Pencil presence. |
| Pencil begins writing in text target | Where handwriting conversion is supported/enabled, accept without an extra focus tap. Hide placeholder at writing start; persistent label remains. Otherwise retain Type/paste routes and explain that handwriting conversion is unavailable. |
| Handwriting active | Freeze target bounds, transcription position, and app-driven scrolling/reflow. Reserve writing space before writing or during a pause. Queue layout changes until writing/selection pauses. Recognition updates the draft, never the committed ID. |
| Recognition pending + Done | Wait for the current recognition result before validation; show pending status. Do not commit incomplete text. Type switches after pending recognition resolves or is explicitly canceled, retaining resolved text. |
| Pencil contacts Ink | Begin pen mark immediately, without a preliminary Draw-mode selection. With eraser selected, erase only intersected ink strokes. One contact sequence is one undoable transaction. A contact canceled by interruption is rolled back. |
| Finger drag in page / Ink | Scroll the page; no accidental ink or page deletion. Explicit ink selection plus **Delete selected ink** provides a non-Pencil erase route. |
| Pencil taps ordinary control | Activate the control normally; never interpret it as ink. |
| Hover, if available | Preview likely ink only, without changing content, focus, or committing any action. |
| Double tap, if available | Respect the person's meaningful preferred tool mapping, including no action. Show the active tool. Never erase content or remove a page directly. |
| Squeeze, if available | One discrete nondestructive tool-picker action near the tip; no sustained/repeated pressure requirement. |
| Barrel roll, if available | May vary a supported mark, never navigate or delete. No essential task depends on it. |
| Move page to Trash | Finish/persist any pending transaction first; if saving fails, keep the page active. Persist a recoverable page snapshot including drafts, ink, and page position before removal. Show persistent Trash access and a labeled Undo action. |
| Restore / Undo page removal | Restore exact content and page position; return focus to the restored page heading. If no pages remain, show an empty state with Create page and Trash. |

Tool placement must be movable or otherwise clear either hand. Pen and Eraser are visibly named with selected state. Provide visible Undo/Redo even in compact layouts; preserve standard system undo/redo gestures rather than reusing them for deletion. The existing unspecified dual-use gesture is retired, with no hidden page-deletion mapping. Standard text editing gestures remain text editing inside text targets; an ink-erasing drag only erases in Ink with Eraser active. These choices apply [Pencil: Best practices, Hover, Double tap, Squeeze, and Custom drawing](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble) and [Gestures: iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/gestures#iOS-iPadOS). Feature availability must be detected for the actual iPad/Pencil pair; the specification does not require Pencil Pro hardware.

## Layout and alternative access

Keep the focused text target and Done/Cancel actions clear of docked, floating, or moved software keyboards using available occlusion geometry, with hardware-keyboard operation independent of it. Prepare handwriting space before entry; if a window/layout change cannot wait, end or cancel the current recognition transaction visibly before relocating the target. Do not shift a field beneath an active stroke. See [Virtual keyboards: iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#iOS-iPadOS).

Use semantic heading, body, field-label, and status roles. Start body text at the iPadOS 17 pt default or an equivalent semantic style; support text enlargement of at least 200%, larger accessibility text sizes, and Bold Text. Stack labels/actions and wrap notes/errors rather than clipping them. Reflow after handwriting pauses. Use 44 × 44 pt activation areas as the iPadOS default starting point with sufficient separation, and verify actual geometry. Tool state and save/error status use words alongside visual distinctions. These are sourced from [Accessibility: Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility) and [Typography: Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type).

Expose text field/editor names, values, editability, errors, button roles, and tool selected states to the chosen accessibility layer. Task order: page heading → Specimen ID → its Type/Clear actions → Notes → its Type action → ink tools/selection actions → Undo/Redo → Move page to Trash → Trash. Tab follows text-entry order, Shift-Tab reverses it; supported keyboard and assistive navigation must reach and activate every essential action without drawing or speech. After validation failure keep focus at ID and associate its error. Removing a page moves focus to the next page heading or empty-state heading. These are requirements for later verification, not assertions of assistive execution. See [Accessibility: Mobility and Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility).

## Worked before/after

Illustrative value, not an assumed laboratory format: `LAB-0071-A`.

**Before, from the brief:** A researcher leaves Pencil nearby and attempts to type the ID. Typing is disabled, so handwriting is mandatory. The same erase gesture can also remove an entire page. The brief does not establish how recognition errors, saves, or recovery currently behave.

**After, proposed trace:** With Pencil nearby, the researcher taps Specimen ID and types or pastes `LAB-0071-A`, preserving `0071`. Alternatively they write directly in the field. If recognition yields `LAB-OO71-A`, that remains an editable draft; the researcher selects `OO`, types `00`, and presses Done to commit `LAB-0071-A`. No automatic ambiguity correction occurs. They immediately draw a diagram in Ink, select Eraser, and remove one stroke. Undo restores that stroke; the page and ID remain intact. They then activate Move page to Trash deliberately. Trash → Restore returns the ID, Notes, and diagram together, including after relaunch once persisted.

## Acceptance checks and current results

**Passed — specification inspection only:** The supplied brief was read; all four described behaviors have explicit replacements above. The revised state model leaves typing available with Pencil present, confines erasure to ink, provides text alternatives and page recovery, and requires draft review before ID commit. Installed root, owning families, topic procedures, and supporting local guides were read. No implementation behavior is established by these passes.

**Failed — supplied design against this revised contract:** Proximity disables typing; IDs lack a typing route; a shared erase/page-delete gesture crosses destructive scope. Custom text canvases are a capability risk requiring replacement or demonstrated equivalent semantics; their existence alone does not prove every editing/accessibility feature is missing.

**Not executed — implementation/device acceptance:**

| Scenario | Observable pass condition |
|---|---|
| Pencil absent, nearby, connected, disconnected; software/hardware typing and paste | Same editable ID and Notes; no value/focus loss or forced handwriting. |
| Empty, whitespace-only, partial, valid, Unicode, long ID; locale change | Draft survives; empty/whitespace commit gets the stated error; other nonempty values preserve exact characters. No locale coercion or invented format restriction. |
| Write without focus; placeholder; long transcription; delayed result | Writing starts directly where supported; label persists; target remains stationary; Done waits; recognized text remains correctable. |
| Mixed text/ink/control strokes and border crossing | Initial target owns the stroke; controls activate; text does not become page ink; eraser never removes text/pages. |
| Pen, Eraser, selected-ink deletion, Undo/Redo | Immediate attached feedback; selection deletion works without Pencil; one Undo restores the last relevant transaction. |
| Hover, double tap, squeeze, roll on supported hardware | Hover never activates; preference mappings respected; squeeze is nondestructive; roll affects marks only; absent features do not block work. |
| Standard system gestures and app edges | Undo/redo, copy/paste, navigation, and multitasking retain their system meanings; retired gesture never deletes a page. |
| Trash, restore, final page, relaunch; persistence failure | Exact snapshot recovers; empty-state focus/actions work; failed persistence prevents removal and does not falsely report Saved. |
| Keyboard docked/floating/moving; narrow window; long Notes and ID | Active target and completion remain reachable, full content can be read/copied, no field movement mid-stroke. |
| 200% enlargement, largest supported accessibility text, Bold Text | Labels/errors/actions remain complete and operable, Notes reflow, full ID remains available. Measure target geometry and contrast in light/dark and Increase Contrast. |
| Keyboard, Full Keyboard Access, VoiceOver, Switch Control, AssistiveTouch | Complete ID entry/correction/commit, Notes entry, ink selection deletion, page removal and restore without a required Pencil gesture; names, values, states, errors, focus return are usable. |
| Left/right-handed iPad/Pencil use | Tools clear the writing hand; test palm rejection, precision, fatigue, latency, and stable transcription in actual use. |

## Evidence limits

Only the short local `interface.md` brief and the installed apple-hig package were used. Routing: root → topic-index search → Inputs (Pencil/Scribble, Gestures), Selection and input (Text fields, Virtual keyboards), Content (Text views), and routed Foundations (Accessibility, Typography); procedures preceded their source guides. No screenshot/animation was supplied, so no visual-example route was needed.

Official links identify the articles behind the local guidance; they were not fetched. The package identifies its references as derived guidance dated 2026-10-25, not an SDK reference or independently verified current Apple manual. No source conflict was identified in the consulted passages. No web browsing, implementation, SDK compilation, device, GUI, accessibility, recognition, persistence, latency, contrast, or physical-comfort execution occurred. Standard-control Scribble behavior does not establish support in the eventual stack. Laboratory identifier schema, deployment versions, hardware, retention policy, and any regulated audit requirements remain unspecified; the proposed baseline must be reconciled with those before implementation is considered ready for laboratory deployment.
