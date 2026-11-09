# Revised undo history specification — Mac vector editor

## Scope and decisions

The supplied `interface.md` reports that Undo sometimes reverses server sync instead of the last user edit, Redo survives divergent edits, and Delete shape is unrecoverable. It also requires attention to selection and document identity across windows. No implementation or screenshots were supplied. This specification replaces that behavior; it does not describe verified runtime behavior.

**History follows meaningful user edits in one document.** Undo reverses the latest committed edit in the routed document, regardless of sync timing or current selection. Redo reapplies the most recently undone edit. A successful new edit after Undo discards that document's redo branch. Sync acknowledgments, saving, selection changes, focus changes, pan, and zoom never create history entries or clear Redo. These are product rules implementing predictable recovery; Apple's guidance supports meaningful grouping and visible results, but does not prescribe this data model. [Undo and redo — Best practices](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#Best-practices)

**One history per stable document ID, shared by its open views.** Window IDs and file names are not document IDs. Rename or move retains identity; a duplicated document receives a new ID and an empty history. Different documents never share stacks. Two windows on the same document share edit order but retain separate selections and viewports. Closing one view leaves history intact while another remains open. Closing the last view ends the session; reopening begins an empty history on the saved document. Save/autosave does not clear either stack. Retain the full session's meaningful history, including edits preceding saves; use disk-backed storage if necessary rather than a fixed entry-count limit. The session/identity policy is a product decision. [Windows — macOS window states](https://developer.apple.com/design/human-interface-guidelines/windows#macOS-window-states), [Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo)

## Command surface and routing

At the top of Edit, in order:

| Command | Shortcut | Availability and effect |
|---|---|---|
| Undo Move Shape, Undo Change Fill, Undo Delete Shape, etc. | Command-Z | Enabled when the routed history has an applicable top undo entry |
| Redo Move Shape, Redo Change Fill, Redo Delete Shape, etc. | Shift-Command-Z | Enabled when the routed history has an applicable top redo entry |
| Separator, then supported standard editing commands, including Delete in standard order | Existing standard bindings | Delete requires an editable, nonempty selection with all targets deletable |

Empty stacks show disabled `Undo` and `Redo`; commands remain visible. Names describe the recorded operation, not a newly selected object. Use plural labels for multiple shapes, such as `Undo Delete 3 Shapes`. No ellipses: these actions require no further input. Menu activation and shortcuts invoke the same dispatcher. No dedicated toolbar controls or history panel are required. [Undo and redo — macOS](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#macOS), [The menu bar — Edit menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Edit-menu), [Menus — Labels](https://developer.apple.com/design/human-interface-guidelines/menus#Labels)

Resolve the command target once at invocation:

1. A focused editable text control owns Undo/Redo for its text session, including a document's shape-text editor or an inspector input. Never let an empty text history fall through to an unrelated shape edit. A committed document text change becomes one document entry after that session ends; an inspector commit becomes one property-change entry.
2. Otherwise use the active document view. A document-owned floating inspector routes object commands to its explicit owner document/view, even while the inspector is key and the document is main.
3. A window without a document owner has no shape-history target: disable these document commands. Never fall back to the most recently edited document.

Opening Edit temporarily takes menu focus but preserves this command context. Recompute labels and enablement on document activation, focus change, commit, undo, redo, and permission change. Revalidate at dispatch so a stale menu cannot affect a different document. Read-only documents disable mutation commands, retaining descriptive labels when history exists. Text editing must retain familiar shortcuts. [Keyboards — Standard keyboard shortcuts](https://developer.apple.com/design/human-interface-guidelines/keyboards#Standard-keyboard-shortcuts)

## Reversible edits and grouping

Each entry stores `documentID`, stable target IDs, operation label, exact forward/inverse payloads, before/after selection IDs, affected artboard/layer, and bounds sufficient to reveal the result. Capture and validate the inverse before making the edit visible. Do not offer an edit whose recovery data cannot be retained.

| User intent | One entry and inverse |
|---|---|
| Drag or resize one/multiple shapes | Pointer-down through pointer-up is one Move/Resize entry; restore exact pre-gesture geometry and transforms, not accumulated inverse deltas |
| Continuous fill/opacity adjustment | Begin adjustment through release/commit is one Change Fill/Opacity entry; restore previous values for every target |
| Held arrow nudge | Key-down/repeats through key-up is one Move entry; another key press begins another entry |
| Delete selected shapes | One Delete entry for the full selection; restore the same IDs, geometry, styles, text, assets, parent/group relationships, stacking order, and dependent links |
| Create or duplicate shapes | Undo removes created IDs; Redo recreates those same IDs with captured content and order |
| Commit shape-text or inspector edit | One meaningful committed change; inverse restores the previous value/text |

Do not group across documents, target sets, operation types, focus changes, or separate completed gestures. An interrupted gesture cancels its preview and restores its initial state; Escape likewise cancels with no entry. No-op and rejected edits neither add history nor discard Redo. Undo/Redo invoked during a gesture first cancels its uncommitted preview, then processes the existing stack. An active text session instead follows the text-owner rule above.

Delete removes without modifying the clipboard; Cut additionally copies to the clipboard. Both must be recoverable when offered. Ordinary reversible deletion needs no confirmation. Empty selection, locked targets, or read-only content disables Delete; do not silently delete only an editable subset. [Edit menus — Best practices](https://developer.apple.com/design/human-interface-guidelines/edit-menus#Best-practices)

## State model and asynchronous work

Framework-agnostic pseudocode; all document mutations are serialized and atomic:

```text
commitUserEdit(context, intent):
    doc = resolveAndFreezeTarget(context)
    cancelOrFinishPreviewAccordingToRules(context)
    entry = prepareExactReversibleEntry(doc, intent)
    if entry is rejected or has no content change: return
    transaction(doc):
        validate(entry.forward)
        apply(entry.forward)
        doc.redo.clear()
        doc.undo.push(entry)
        updateDirtyStateAgainstSavedContent()
    revealAndSelect(context.view, entry.afterSelection, entry.afterBounds)
    enqueueSync(doc.id, freshMutationID(), entry.forward)

undo(context):
    doc = resolveAndFreezeTarget(context)
    entry = doc.undo.peek()
    if absent or not applicable: explainUnavailable(); return
    transaction(doc):
        validate(entry.inverse)
        apply(entry.inverse)
        doc.undo.pop(); doc.redo.push(entry)
        updateDirtyStateAgainstSavedContent()
    revealAndSelect(context.view, entry.beforeSelection, entry.beforeBounds)
    enqueueSync(doc.id, freshMutationID(), entry.inverse)

redo(context):
    # Same atomic process, forward payload, redo -> undo,
    # afterSelection/afterBounds; do not call commitUserEdit.

syncAcknowledgment(documentID, mutationID):
    markDeliveryOnly()  # never push, pop, replay an edit, or switch windows
```

If validation, inverse storage, or application fails, roll back the transaction and leave both stacks unchanged. Do not skip the blocked top entry and undo an older one. Show an inline explanation and recovery action, for example `Can't undo Move Shape because its layer is unavailable. Restore the layer to continue.` Retain the data for retry.

Sync represents delivery of document changes, not an edit intention. Undo before acknowledgment changes the local document immediately and queues a causally ordered compensating mutation; retries are idempotent by mutation ID. A late acknowledgment cannot resurrect deleted content or reverse the compensation. Offline and failed delivery retain local history and show pending/failed synchronization with Retry. Do not call a local restoration a reversal of already delivered external effects. [Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo), [Feedback — Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices)

Assumption: server sync acknowledges this editor's mutations. The brief does not establish collaborative editing. If incoming server content changes the document, it must pass through the same serialized mutation gate and revalidate affected entries. Never blindly apply whole-document snapshots over newer content. If an inverse conflicts, block it with an explanation and retain history; collaborative rebasing/merge semantics need a separate design before support can be claimed.

## Selection, focus, and visible restoration

Undo/Redo targets recorded IDs, never whichever shapes happen to be selected now. In the invoking view, restore the entry's before/after selection, filtered to IDs that exist in the resulting document. Undo Delete therefore restores and selects the deleted shapes; Redo Delete clears them. Other views retain their own selections, dropping IDs that cease to exist. They update content without changing focus or viewport. Undo from another view of the same document is valid and reveals the result there.

Keep input focus on the invoking canvas or inspector; restoring selection does not move keyboard focus into an object. If a focused shape disappears, retain the canvas input owner and remove its obsolete object indicator. Persistent selection and focus remain distinct. [Focus and selection — Best practices](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices)

In the invoking view, keep the viewport unchanged if affected content is visible. Otherwise reveal its artboard and pan minimally; fit the affected bounds only if they cannot be shown at the current zoom. For deletion, reveal the old bounds and show a temporary outline plus text such as `Redid Delete Shape`; this provides visible evidence even though no object remains. A restored hidden-layer object gets a visible bounds overlay and text identifying its layer, without silently changing stored layer visibility. Do not activate another window. Routine changes use selection/outline and nearby status text, without modal success alerts or sound-only feedback. [Undo and redo — Best practices](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#Best-practices), [Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)

## Worked before/after

Start with `Poster` open in windows A1/A2 and `Logo` in B. Poster contains shape S at x=10 with blue fill. All stacks are empty; A1 selects S.

| Step | Revised result |
|---|---|
| A1 drags S through 50 pointer updates to x=70 | One Move Shape entry; Undo Move Shape enabled |
| Server acknowledges an earlier save | No history change; next Undo still targets S's move |
| A1 changes S to red, then deletes S | Stack is Move, Change Fill, Delete; S is absent |
| Activate B; press Undo | B's empty history means disabled Undo; Poster is untouched |
| Activate A2, whose viewport is on another artboard; Undo | Restore the same S at x=70, red, in its original layer/order; select and reveal S in A2; Redo Delete Shape enabled |
| Undo again | S becomes blue at x=70; next Redo is Change Fill |
| Make a new resize in A2 | Add Resize after Move; discard both undone entries; Redo disabled |
| Attempt Redo or receive delayed delete acknowledgment | Neither changes S or restores the discarded branch |
| Undo Resize, then Undo Move | Restore original size, then x=10; sync events are never history targets |

Before: the brief reports unpredictable sync reversal, stale Redo, and permanent loss on Delete. After: this sequence has a deterministic target, exact recoverable deletion, document isolation, shared-view order, and branch invalidation. The sequence is a specification walkthrough, not an executed test.

## Acceptance checks and evidence status

**Passed — static specification review only:** all three reported defects have explicit replacement rules; target routing includes same-document and different-document windows; grouping, inverses, save/open boundaries, selection, offscreen reveal, failures, and sync ordering are specified. The worked sequence is consistent with the stated stack transitions.

**Failed — supplied baseline report:** wrong-target Undo, persistent Redo after divergent changes, and unrecoverable deletion are reported in `interface.md`. They were not independently reproduced.

**Not executed — implementation acceptance scenarios:**

1. Replay the worked sequence; assert content, exact IDs, stack labels, availability, selections, and unchanged unrelated document after each step.
2. Undo/Redo a drag with 50 updates, a held nudge, and a slider adjustment: each is one entry; separate gestures stay separate. Cancel and no-op preserve Redo.
3. Delete a group with linked assets and ordering dependencies; Undo restores exact content/IDs/order and Redo removes it without clipboard changes. Empty/locked/read-only selection never mutates content.
4. Switch among A1, A2, B, an owned inspector, a text editor with empty local history, and an unowned window. Each command acts only in its declared context; no text shortcut falls through to shapes.
5. Undo offscreen deletion and redo it; reveal is visible in the invoking view, hidden-layer recovery has an overlay/text cue, and other windows retain focus and viewport.
6. Save between edits and traverse history across the save point. Close one shared view and continue. Close the last view and reopen: saved content survives with empty session history. Rename retains identity; Duplicate isolates history.
7. Delay/reorder acknowledgments, disconnect, retry, and Undo before delivery. No history entry is created by sync, compensation remains ordered, and no duplicate mutation or late acknowledgment resurrects content.
8. Inject inverse-storage failure and a conflicting incoming change. No partial mutation or stack movement occurs; blocked commands explain why and retain retry data. Successful new edits alone discard Redo.
9. On a Mac implementation, exercise menu and keyboard routes with the toolbar hidden, document switching, text editing, Full Keyboard Access, and supported keyboard layouts. Verify dimmed commands, accurate labels, reachable menu items, focus return, and interpretable visual/text feedback.

Only local files and installed skill guidance were read. Root skill, owning families, and topic procedures were read before their supporting guides. Routes used: Patterns → Undo and redo / Feedback; Inputs → Focus and selection / Keyboards; Menus and actions → The menu bar / Edit menus / Menus; Presentation → Windows. Official links above identify source sections from the installed dated snapshot; no web verification was performed. No device, SDK, GUI, accessibility, native menu, network protocol, or executable history implementation was tested. Actual server protocol, memory/storage budget, document schema, supported text editor behavior, and collaborative editing capabilities remain unknown; the specified model requires implementation and verification in the project's chosen stack.
