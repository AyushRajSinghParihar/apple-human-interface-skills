# Cross-window specimen transfer audit

## Scope and evidence

The supplied `interface.md` is a behavioral brief for iPadOS/macOS, not an executable interface. Its five statements are the verified documentary evidence below; none was independently reproduced. Priority reflects likely user impact, not measured frequency. The requested iPad archive is primary; Mac-specific behavior is qualified separately. No SDK or framework is assumed.

Read the installed apple-hig root, searched its topic index, and followed Patterns → Drag and drop → supporting guide. Also followed Patterns → Undo and redo → guide, and Foundations → Accessibility → guide for recovery and the alternative transfer route. All paths were resolved under `.agents/skills/apple-hig/`. Official links below identify the sources represented by these local snapshots; no web access was used.

## Ranked verified findings

| Rank | Evidence from interface.md | Effect and decision | Source |
|---|---|---|---|
| 1 · Critical | “a canceled drag deletes the source” | Cancellation destroys archive content without a completed transfer. Cancel/reject/failure must preserve source records, relationships, and selection. Defer source removal until a move commits; make a completed internal transfer reversible. | [Drag and drop: Best practices](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop#Best-practices), [Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#Best-practices) |
| 2 · High | “moving multiple selected items transfers only one” | The requested set and resulting set differ. Freeze all selected specimen identities when dragging a selected item, include subsequently gathered iPad items, and validate/commit the complete batch. | [Drag and drop: Best practices](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop#Best-practices), [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop#iOS-iPadOS) |
| 3 · High | “copying to another app strips useful representations” | Receiving apps lose useful content or editability. Advertise available representations richest to simplest, always copy interapp, and let the destination choose its richest supported representation and relevant fields. Exact lost formats and fields are unspecified. | [Drag and drop: Accepting drops](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop#Accepting-drops) |
| 4 · Medium | “drop regions do not indicate acceptance” | People cannot predict a valid destination. Show eligible/rejected state and operation, clear it on exit, and revalidate on release. Feedback is a proposal, never proof of acceptance. | [Drag and drop: Providing feedback](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop#Providing-feedback) |
| 5 · Medium | “Drag preview is a blank square” | The preview loses specimen identity and batch context. Use recognizable specimen content or a labeled fallback; maintain preview continuity and show a batch count. | [Drag and drop: Providing feedback](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop#Providing-feedback) |

These are evidence-backed findings about the brief. No evidence establishes whether alternate commands, undo, scrolling, accessible semantics, or Mac modifier handling currently exist; their absence is not an additional verified defect.

## Corrected behavior and decisions

**Operation contract.** A window is presentation context, not a container identity. Generally move within one logical container and copy between distinct containers; always copy to another app. An explicit “Move to…” command may move between archive containers. If drag-to-move between archive collections is desired, document that exception and its data-loss rationale before adopting it. This specification uses copy between collections by default. Moving a collection membership must not silently delete the underlying specimen globally. These defaults follow [Drag and drop](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop).

**Payload.** Carry one entry per specimen with stable identity, revision, source container, display label, preview, and lazily provided representations. Suggested archive formats, subject to the real data model: lossless specimen package with metadata/assets; portable structured metadata; available vector/PDF or lossless image; compatible image; plain-text summary and stable reference. Do not claim unavailable conversions. Internal reordering preserves identity; copying creates a new destination identity with provenance. A receiving field imports only relevant fields. Finder export on Mac should offer a format the archive can reopen, or an appropriate clipping. These choices apply the guide’s richest-to-simplest and relevant-fields guidance; the exact schema is a product decision.

**Feedback and completion.** Show a translucent recognizable preview after about 3 pt of movement, with a flock/count for a batch. Label a valid target, for example “Copy 3 specimens to Review”; provide a non-color rejection cue for an incompatible/read-only target. Clear cues on exit. Autoscroll near an edge only while inside the destination. Slow drops retain placement placeholders and progress; success appears only after commit. Failed drops return visually to the source or fade without implying placement. After success, select the dropped batch; deselect source content for intercontainer transfers and originals for in-container copies. Cancellation preserves the prior selection. See [Providing feedback](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop#Providing-feedback) and [Accepting drops](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop#Accepting-drops).

**Input and recovery.** Support adding specimens during an active iPad drag. On Mac, inspect Option at release for an in-container forced copy; releasing Option restores move. Permit useful background-window dragging without forcing activation. Provide labeled “Copy to…” and “Move to…” actions with a destination chooser using the same validation/transaction path. Give sources and targets meaningful names and operation/count states, and make the full alternative path keyboard and assistive-input operable. These are requirements of this proposed design, not verified implementation properties. See [Drag and drop: platform considerations](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop#Platform-considerations) and [Accessibility: Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility).

One committed batch is one undo unit: “Undo Move Specimens” or “Undo Copy Specimens.” Restore memberships/order/selection on undo and reveal affected content; redo reapplies the batch. A new edit after undo clears the redo branch. Integrate with existing meaningful history rather than resetting it at each drag; save/open history policy remains to be specified with the archive’s persistence model. Preserve standard platform undo access, including Mac Edit commands and Command-Z/Shift-Command-Z. Do not promise to undo another app’s completed import; external copies preserve the source and reversal belongs to the receiver. See [Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo).

## Framework-agnostic transaction model

Batch atomicity and idempotency below are proposed engineering safeguards, not additional quoted HIG rules.

```text
beginDrag(anchor, selection):
    ids = anchor in selection ? all(selection) : [anchor]
    session = snapshot(ids, revisions, memberships, order, selection)
    state = dragging                       // no source deletion

gather(id):
    add unique id and its snapshot to session; refresh count

hover(target):
    proposal = negotiate(session, target, currentInput)
    show eligible operation/count OR unavailable cue
    // no data mutation; exit clears cue

release(target, inputAtRelease):
    freeze batch; revalidate permissions, revisions, capacity, representations
    operation = resolve(containerIdentities, appBoundary, inputAtRelease)
    if rejected: restore presentation/selection; finish rejected
    else:
        state = pending; show placeholders/progress
        stage all destination entries using richest accepted representations
        if interapp:
            expose copy payload; never delete source
            finish only with actual available completion evidence
        else:
            atomically commit destination + source changes for move
            // cross-store implementation needs a recoverable transaction journal
            // if atomicity cannot be guaranteed, reject move before mutation
            record one inverse; select destination batch; finish committed

cancelOrFailBeforeCommit():
    discard staging; clear cues/placeholders; preserve source snapshot
    show cancellation or actionable failure without success animation

retryOrDuplicateCallback(sessionId):
    resume journaled outcome or return existing outcome; never duplicate commit
```

Cancel-versus-commit races must resolve to one terminal outcome. After a durable commit, recovery is undo, not a misleading “canceled” result. A stale/deleted specimen or one unsupported batch item rejects the entire internal batch with an explanation; partial import would need a separately specified, explicit outcome.

## Worked before/after

Illustrative specimens A, B, C are selected in Intake in window 1; Review in window 2 is a different collection.

**Before, as reported:** dragging shows a blank square and no acceptance cue; a requested multi-item move transfers only one. Canceling deletes source content. Copying externally strips useful representations. The brief does not establish whether the other selected items survive or which formats are lost.

**After, proposed:** the preview shows A’s thumbnail/label and “3 specimens.” Review proposes “Copy 3 specimens to Review.” Releasing stages all three, commits three copies, retains all three Intake records, selects the Review copies, and deselects the Intake selection. Undo removes those copies as one action and reveals the affected context. Canceling before commit leaves Intake unchanged. Explicit “Move to Review” transfers all three memberships atomically and supports undo. Copying to another app offers every available representation; a rich receiver chooses the lossless package, while a text-only receiver chooses the summary. Neither external path removes Intake records.

## Acceptance checks and status

**Passed — documentary checks:** read interface.md; traced all five reported defects to the ranked findings; read installed router, selected families, topic procedures before their supporting guides; produced explicit operation, payload, feedback, reversal, and selection contracts. This is specification coverage, not a runtime pass.

**Failed — supplied behavior against the proposed contract:** cancellation preserves source; selected batch transfers completely; useful representations survive export; eligible targets provide feedback; preview identifies content. Each failure is reported by the brief only.

**Not executed — implementation acceptance:**

| Check | Required observable result |
|---|---|
| Cancel, outside release, rejected/read-only target | Zero source/destination mutations; prior selection retained; cues cleared. |
| Same-container move/copy and cross-window collection copy | Correct operation by container identity; exact batch count, identities/provenance and final selection. |
| iPad gathering | Added unique specimens join payload and count; entire gathered batch transfers. |
| Slow, failing, stale, duplicate, and interrupted transfer | Placement/progress while pending; no false success, lost source, half batch, or duplicate commit; recover after restart. |
| Mixed-format batch and external receivers | Rich receiver retains supported metadata/assets; simple receiver receives relevant fallback; source preserved for every interapp outcome. |
| Target enter/exit and edge scrolling | Eligible/rejected cues follow current target; scrolling only inside edges; release revalidates. |
| Mac Option held then released before drop | In-container copy when held at release; move when released; background drag preserves appropriate window/selection context. |
| Undo/redo sequence | One batch reversed/restored, visible offscreen recovery, correct identities and selection; new edit clears redo branch. |
| Alternative transfer route | Complete copy/move without dragging; named source, destination, operation and status reachable/activatable with keyboard and assistive input. |

## Evidence limits

Only a short textual brief and installed guidance were supplied. No source code, specimen schema, screenshots, receiver matrix, persistence model, or runtime results establish actual implementation details. No device, GUI, SDK build, native drag, Universal Control, accessibility execution, contrast, geometry, or physical-comfort test was performed. Platform-specific behaviors above are acceptance requirements, not demonstrated support. Accessibility, alternative-route availability, undo history, transaction durability, exact representation fidelity, and API feasibility remain unverified. Local guidance is a dated snapshot; linked official pages were not fetched and no current-release verification is claimed.
