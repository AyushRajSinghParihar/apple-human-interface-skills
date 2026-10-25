# Revised iPad legal annotation workspace

This is an interaction specification, independent of framework or Apple SDK. The supplied `interface.md` describes a fixed fullscreen landscape canvas, editing tools hidden on keyboard connection, and selection reset on resize. Those are the observed requirements/problems; no implementation or screenshots were supplied. The revision supports a compact window through full screen without interrupting legal annotation.

## Decisions and source basis

1. **Use available window space.** Full screen, portrait, landscape and multitasking are layouts of the same editing session. Never require rotation or fullscreen to edit. Base pane placement on usable width and height after safe regions, bars and keyboard occlusion. Apple supports adaptation to actual environmental space and preserving functionality across size classes: [Layout — Adaptability and Size classes](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability).
2. **Keep tools beside the document when useful; collapse their presentation when necessary.** The document is primary; the supporting pane contains tool choices and properties of the selected annotation, not an unrelated destination. Preserve a logical compact route back to the document. See [Designing for iPadOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados#Best-practices) and [Split views — iPadOS](https://developer.apple.com/design/human-interface-guidelines/split-views#iPadOS).
3. **Separate editing state from presentation.** Resizing, rotation, keyboard attachment and switching inputs cannot clear selection, draft, active tool or undo history. Focus is an interaction target, not the selected annotation: [Focus and selection — Best practices and iPadOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices).
4. **Keep editing commands visible with accessories attached.** Hardware keyboard and pointer add routes to the same actions. Essential actions never depend on hover. See [Keyboards — Best practices](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices) and [Pointing devices — iPadOS](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#iPadOS).

All numeric layout values below are provisional product choices in logical points, not Apple requirements or measured device limits. Framework adapters must map these units and environmental values correctly.

## Layout and navigation contract

The workspace has a document toolbar, canvas, and optional supporting tools pane. Toolbar leading region identifies the document and provides the existing return-to-documents route; center exposes frequent tools; trailing region exposes Tools and completion of any active edit. Shorten the displayed document title before removing essential controls; make the full name available through document information.

Let `W` be usable workspace width. Reserve a provisional 480 pt canvas, 280 pt tools pane and 16 pt separation for simultaneous editing. Use these initial states:

| State | Fit condition | Arrangement and routes |
|---|---|---|
| Compact | W < 600 pt | Canvas fills available space. Tools opens a replacement tools view within this workspace. Its Back to Document control returns to the same page and selection. |
| Intermediate | 600 ≤ W < 776 pt | Canvas stays primary. A compact tools strip exposes frequent choices; Tools opens the same replacement view for properties. Do not squeeze a full pane beside an unusable page. |
| Expanded | W ≥ 776 pt and measured content fits | Canvas plus trailing 280 pt supporting pane when tools are requested. Tools toggles that pane. Hiding it gives the space to the canvas. |

A replacement view is a route in the same workspace, not a new document or an assumed sheet/popover API. It shows document name, selected annotation summary, tool controls, and Back to Document. Tool changes apply immediately; returning does not commit an unfinished annotation. Any explicit Done for an annotation remains separate from Back to Document.

Width alone is insufficient: larger labels, text settings or localized controls that do not fit cause the next simpler layout. Let rows grow/wrap and make the tools view vertically scrollable. With little height, move the intermediate strip into the tools view. Keep essential toolbar routes visible, using a second wrapping row when necessary. A usable canvas may scroll in both axes rather than shrinking text and controls. At widths below the provisional compact test size, retain these scroll/reflow routes; do not silently crop required controls or enforce fullscreen.

Do not stretch document pages. Preserve page aspect ratio. Default to fit width when first opening; after manual zoom, retain document scale through resizing. Store a document-space viewport anchor, preferably the selected annotation or caret, and its relative position. Restore it in the remaining canvas, clamping only at page boundaries. Fit-width mode recomputes scale while retaining the anchor. Software keyboard occlusion scrolls the caret into view, not the whole document back to its beginning.

On expansion, an open replacement tools view becomes the adjacent pane. On collapse, an open pane becomes a replacement view only if the person was actively operating it; otherwise show the canvas with Tools available. Preserve the pending return route. Explicitly hiding tools persists across later resizing; attaching a keyboard never changes that preference.

## Commands and input contract

Proposed core tools are Select, Highlight, Pen and Note; these are design assumptions, not an inventory recovered from code. One command registry supplies all surfaces and enabled states.

| Command | Visible route and outcome | Keyboard / availability |
|---|---|---|
| Select | Tool choice; tap/click annotation to select, document text to establish a range | Content arrows navigate candidates, activation selects; focus movement alone does not change selection |
| Highlight | Tool choice; apply to selected text range | Activate the same tool via keyboard-accessible controls; disabled with explanation when no valid range |
| Pen | Tool choice with current color/width in tools view | Keyboard can choose/configure it; freehand drawing itself needs touch or Pencil |
| Note | Tool choice; create a note at selected document anchor and edit its draft | Keyboard activation opens the same draft editor; Done commits, Cancel discards that draft |
| Undo / Redo | Persistent toolbar controls, including compact mode | Command-Z / Shift-Command-Z; disabled when the corresponding history is empty |
| Copy | Selection action | Command-C; text editing retains ordinary copy semantics |
| Tools / Back to Document | Show/hide supporting tools or return from replacement view | Keyboard-accessible controls; Escape returns from tools without changing document state |
| Done / Cancel edit | Visible while a draft is active | Keyboard-accessible controls; Escape cancels an active manipulation first, otherwise returns from tools, otherwise cancels a draft; never discards committed annotations |

Toolbar priority: navigation and edit completion first; then Undo/Redo and Tools; then individual tool shortcuts; then secondary properties. Tools always exposes every tool even if its shortcut leaves the toolbar. If the host supplies automatic toolbar overflow, use it without an additional manual overflow. Otherwise provide one overflow mechanism for secondary toolbar commands, never a competing second one. Do not hide the toolbar on keyboard connection. This applies [Toolbars — Best practices and Item groupings](https://developer.apple.com/design/human-interface-guidelines/toolbars#Best-practices) without claiming native overflow exists in an unspecified framework.

- **Touch:** Select mode taps select and drags text-range handles. Pen mode draws with one finger; two-finger pan and pinch navigate/zoom. Outside Pen mode, ordinary page dragging scrolls. Provide visible Zoom In, Zoom Out and Fit Width controls in Tools, plus a scroll route. Keep system edge, multitasking and three-finger editing gestures available. [Gestures — Best practices](https://developer.apple.com/design/human-interface-guidelines/gestures#Best-practices).
- **Pencil:** Contact draws immediately with the remembered ink tool in document/margins, without requiring Pen selection each time; explicit eraser or text-selection choice overrides that default. Finger scrolling remains available. Pencil can activate all controls. Hover previews only and never writes. Optional hardware gestures respect supported capabilities and preferences; no squeeze/double-tap deletes content. Fixed-document ink colors remain stable across appearance changes. [Apple Pencil and Scribble — Best practices, Hover and Custom drawing](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble#Best-practices).
- **Pointer:** Click selects, drag adjusts a text range or annotation position, scroll navigates. Show text targeting for text and restrained highlight feedback on toolbar controls; avoid scaling that obscures neighbors. Selection handles remain touch-operable. Secondary click may accelerate existing actions but cannot be their only route. No essential tool is hover-only.
- **Keyboard:** Preserve standard text editing when a note editor owns focus; an arrow key there cannot move a page annotation. Content focus groups are canvas and tools content, with Tab/Shift-Tab between groups and arrows within an appropriate collection. Entry returns to the remembered content target. Full Keyboard Access separately covers all toolbar buttons and completion controls; ordinary content focus alone does not establish that coverage. Expose shortcut names alongside commands where supported; do not assume an SDK discoverability overlay. Test standard bindings in context rather than copying the source's legacy/system shortcuts wholesale.

Input switching retains selection and active edits. On connection/disconnection update capabilities and actual occlusion only. If a focused control disappears on resize, retain its semantic target for restoration; hide its focus indicator instead of choosing another annotation. On the next explicit keyboard navigation, enter the corresponding visible group/control. Keep persistent selection styling separate from focus styling.

## State and transition pseudocode

```text
session = {documentID, pageID, selectionIDsOrTextRange,
           draftTextAndCaret, activeTool, inkProperties,
           undoHistory, redoHistory, zoomMode, scale, documentAnchor}
presentation = {layout, toolsRequested, activeRoute, focusTarget, returnRoute}

onEnvironmentChanged(size, safeRegions, textMetrics, occlusion, capabilities):
    anchor = captureDocumentAnchor()
    nextLayout = chooseLayoutFromUsableSpaceAndMeasuredFit()
    if activeStrokeOrComposition:
        retain draft samples/text in document coordinates
        finish current input transaction before relocating its target
        // New geometry may clip temporarily; never reinterpret samples as new ink.
    reconcileToolsRoute(presentation, nextLayout)
    relayoutWithoutReplacingSession()
    restoreDocumentAnchor(anchor)
    retainSemanticFocusOrHideIndicator()
    // No selection-clear, history-reset or keyboard-triggered hide-tools action.

onExplicitSelectionChanged(target):
    if draft belongs to another target:
        require visible Done or Cancel before changing target
    else:
        update selection and contextual tools

onDoneDraft(): commit once to document history; clear draft only
onCancelDraft(): discard draft only; retain prior committed selection/context
```

Resize is never an undoable document edit. An interrupted stroke remains a recoverable draft until its transaction ends; do not lose it or commit it twice. If the selected annotation is actually removed by a document operation, clear that invalid selection with feedback; resize alone is never that operation.

Cross-app import/export is outside the supplied editing brief. If later supported, inbound drops must preview an insertion destination and create/import content explicitly, never silently replace the current legal document. No inter-app behavior is claimed here.

## Worked before/after

Illustrative fixture: page 12 of “Contract A”, selected text range “termination”, an unfinished note “Check notice period”, caret at its end, and three undoable edits. Begin at usable 1024 × 768 pt, then attach a keyboard and resize to 520 × 700 pt before returning to 1024 × 768 pt.

**Before, per brief:** keyboard connection hides every editing tool; resizing resets selection. The brief does not establish whether draft text or undo history is lost, so no such defect is asserted.

**After:** keyboard connection leaves the tool routes intact. At 520 pt the canvas occupies the workspace; Tools opens the replacement tools view. Page 12, the exact text range, note draft/caret, tool and three history entries survive. The user returns with Back to Document and commits via Done, producing one new history entry. Expansion restores the tools pane if requested and the same document anchor. Undo reverses only that note commit, not the window transition. The person can perform this sequence using touch controls or keyboard-accessible commands; Pencil and pointer remain usable without reconnecting or resetting the session.

## Acceptance checks and evidence limits

**Passed — static specification checks:** the supplied brief and installed root skill were read; topic index concepts were searched; selected family and topic procedures were read before their source guides. This document provides compact/intermediate/expanded routes, persistent state, command priorities, input mappings, a worked example and explicit runtime checks. These passes describe the artifact, not app behavior.

**Failed — supplied design against the revised contract:** fixed fullscreen landscape assumption; loss of tool access on keyboard connection; selection reset on resize. These are brief-reported failures, not reproduced test results.

**Not executed — implementation/device acceptance:**

| Check | Required observable result |
|---|---|
| Resize sequence at usable widths 320, 520, 599, 600, 775, 776 and 1024 pt; include heights 320 and 700 pt | Every command reachable; correct state/fit fallback; no overlapping controls; no fullscreen demand |
| Cycle compact → intermediate → expanded → compact repeatedly, with tools open/closed and focus in tools/canvas | Correct return route and user hide preference; identical page, selection, draft/caret, tool and history |
| Run worked fixture and resize during ink/text composition | No lost draft/samples, duplicate commits or selection reset; Undo reverses the edit only |
| Rotate, show/hide onscreen keyboard, attach/detach hardware keyboard, then switch touch/Pencil/pointer | Controls remain available; caret visible; anchor stable; no accidental marks or changed selection |
| Larger text, long translated labels, both reading directions, safe-area obstructions | Measured-fit fallback, wrapping/scrolling and all required actions usable; document itself undistorted |
| Keyboard-only completion with ordinary focus and Full Keyboard Access tested separately | Enter content groups, select, open tools, create note, Done, Undo and return without pointer; no traps or text shortcut conflicts |
| Touch and pointer equivalents, system gestures and optional Pencil capabilities | Hover never commits; no hidden-only commands; reserved gestures work; visible feedback tracks manipulation |
| Fullscreen long-session use, left/right hands, supported Pencil models | Comfortable reach, readable document, stable ink visibility, acceptable latency and unobstructed controls |

Only local files and installed guidance were used. Official links above are attribution from the local snapshot (dated 2026-10-25); no web verification or independent source/media review was performed. No app code, Apple SDK, build, GUI, iPad, assistive-technology session or hardware execution was available or claimed. Layout thresholds, physical comfort, native focus/overflow, accessibility execution and Pencil latency remain unvalidated. The local guidance names Apple frameworks, but this specification requires behavior rather than assuming those frameworks are installed. No source conflict was identified in the selected passages; absence of another platform subsection is not proof of support.
