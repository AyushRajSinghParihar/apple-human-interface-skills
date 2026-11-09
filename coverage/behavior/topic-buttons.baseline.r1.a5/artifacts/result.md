# Export-control correction plan

Scope: iPadOS field-report editor, reviewed from [interface.md](interface.md). All four functions remain: Publish, Preview, Save Draft, Delete. Findings below are verified against the supplied description, not a rendered or running app. Priority reflects potential harm and task blockage; it is a review judgment.

## Ranked findings and decisions

| Rank | Verified observation and effect | Correction and source |
|---|---|---|
| 1 — High | An 8-second Publish upload produces no UI change; repeated taps create duplicate uploads. People cannot tell whether publishing started and can repeat the side effect. | Immediately acknowledge activation; show an activity indicator **inside Publish**, replacing any image, with “Publishing…”; reject repeat activation while pending. Add operation-level deduplication and recovery as specified below. [Buttons: iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS); [Progress indicators: Best practices](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices). Deduplication is an engineering decision supporting this behavior, not an HIG API requirement. |
| 2 — High | Delete is primary/default in an editor. Accidental default activation can select destruction. Actual deletion reversibility and confirmation behavior are unknown. | Remove its editor default binding and primary emphasis; expose a labeled destructive Delete action separately from Publish. Make Publish the sole prominent action, assuming completing the report is the likely task. HIG generally assigns primary to a likely nondestructive action. [Buttons: Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role). |
| 3 — High | Every hit region is 20 × 20 pt with 2 pt gaps. Small, crowded controls increase missed and neighboring activations, including Delete. | Give every action a nonoverlapping hit region at least 44 × 44 pt and clear surrounding space. Use 12 pt between bordered control hit regions as a project layout starting point, with a larger group separation before Delete; validate layout rather than shrinking targets. [Buttons: Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices); [Accessibility: Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility). |
| 4 — High | Glyph-only Preview has no accessible name. Its purpose is unavailable through its accessible label. | Display “Preview” and expose that accessible name, button role, enabled state, and keyboard activation. Do not rely on a glyph or tooltip alone. [Accessibility: Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision); [Buttons: Content](https://developer.apple.com/design/human-interface-guidelines/buttons#Content). |
| 5 — Medium | Four equally prominent filled actions compete for attention and obscure the expected next step. | One prominent filled Publish; secondary Preview and Save Draft; lower-emphasis destructive Delete, retaining a visible label and destructive semantics. Keep comparable control sizing; distinguish priority by style. [Buttons: Style](https://developer.apple.com/design/human-interface-guidelines/buttons#Style) advises one or two prominent buttons per view, rather than requiring exactly one. |

Numerical qualification: the local Buttons guide says general hit regions should be at least 44 × 44 pt. Accessibility lists iOS/iPadOS default controls at 44 × 44 pt and minimum controls at 28 × 28 pt. These statements differ in scope; 20 × 20 pt falls below both. This plan conservatively chooses 44 × 44 pt hit regions. Accessibility's approximate padding suggestions are not a universal inter-button gap requirement; the proposed 12 pt gap is a product decision, not a claimed HIG minimum.

## Corrected behavior specification

These are immediate-action buttons, not toggles or selection controls. Provide visible press feedback even when an operation finishes quickly. Prefer semantic controls with built-in states when the implementation environment offers them; otherwise implement equivalent behavior without assuming an Apple SDK.

Idle footer, reading order: **Preview**, **Save Draft**, **Publish**, then a spatially separated **Delete** group. Publish alone has primary visual emphasis. Do not bind Return globally to Publish while editing multiline text; explicit focused-button activation works. Delete is never the editor's default action. At narrow iPad window widths or enlarged text, wrap into logical rows without truncating labels, overlapping targets, or changing reading order. Destructive meaning must be available through text and semantics as well as color.

- **Preview:** opens the report preview without publishing or changing saved content; return restores editor context.
- **Save Draft:** saves the current revision and acknowledges success only when persistence succeeds. If saving is asynchronous, give it its own pending feedback and duplicate guard. Preserve unsaved content on failure and offer retry.
- **Delete:** determine actual reversibility before release. For ordinary undoable deletion, provide a usable Undo path; HIG says such deletions generally need no confirmation. For uncommon irreversible deletion, require a confirmation naming the report and explaining actual loss, with Delete and Cancel. Choose no default to require deliberate activation; Cancel dismisses without changes. The alerts guide permits a normal default for explicitly requested destruction, so this is a conservative product choice, not a universal prohibition on destructive confirmation defaults. If Assistive Access is supported, its separate two-confirmation guidance for difficult-to-reverse actions must also be addressed. [Alerts: Best practices and Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices); [Accessibility: Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive).
- **Publish:** capture an immutable revision, synchronously acquire a pending guard, and start one logical publish operation. Keep Preview and Save Draft usable against clearly identified revisions. Editing may continue; publication always refers to the captured revision. Disable Delete while publication is pending to avoid deletion/publication races, with an accessible explanation. New edits remain a draft and are never silently included in the upload.

### Upload state and recovery

| State | Visible and accessible behavior | Allowed transition |
|---|---|---|
| Ready | Publish enabled; no progress UI | Activate → pending immediately |
| Pending | Indicator inside button + “Publishing…”; busy/unavailable semantics; stable button bounds. Announce start once. | Authoritative success, definite failure, or uncertain outcome |
| Slow/stalled | Keep indicator active; stable inline status such as “Publishing is taking longer than usual.” Do not claim failure from elapsed time alone. | Continue reconciliation; offer safe recovery according to transport capabilities |
| Succeeded | Remove indicator; show and announce “Report published” for the captured revision. Keep status available until dismissed or superseded. | Re-publishing an unchanged revision returns existing result; changed draft can start a new operation |
| Definite failure | Remove indicator; preserve report; show actionable reason and Retry | Retry the same logical operation with its original identity |
| Outcome unknown | “Publication status is unavailable. Check status before retrying.” No success claim or fresh publish operation | Check/reconcile by operation identity, then success or safe retry |

Use indeterminate activity when total completion is unknown. If reliable whole-operation progress exists, show honest determinate progress in a stable location, accounting for final server processing; bytes uploaded alone must not imply publication is complete. Do not replace an in-button spinner with a differently shaped bar midtask. No invented percentage or eight-second countdown. A 10-second slow-status threshold is a proposed product tuning value, not an HIG rule. [Progress indicators: Best practices](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices).

Allow cancellation where safe. No cancellability is evidenced here: do not offer “Cancel Upload” unless the service can establish whether publication was prevented. If supported, keep the operation pending while cancellation is acknowledged; explain consequences and preserve the draft. A request to cancel does not itself prove cancellation. Pause is appropriate only if resumable partial work exists. These capabilities require backend verification.

Framework-agnostic pseudocode (the service contract below is proposed, not supplied):

```text
activatePublish():
    atomically:
        if operation is pending or outcomeUnknown: return
        snapshot = captureCurrentRevision()
        operation = findOrCreateDurableOperation(reportID, snapshot.revision)
        operation.state = pending
    renderBusyBeforeStartingNetworkWork()
    publish(snapshot, idempotencyKey=operation.id)

onPublishResult(operationID, result):
    if operationID != currentOperation.id: return  // ignore stale callbacks
    if authoritativeSuccess(result): state = succeeded
    else if definiteNoncommitFailure(result): state = failed
    else: state = outcomeUnknown
    renderAndAnnounceStateChange()

retryOrCheck():
    reconcile(currentOperation.id)
    // If safe to retry, reuse the SAME identity and immutable payload.
    // Never create a fresh operation because a timeout occurred.
```

The service must atomically deduplicate requests by operation identity and return the existing publication result for repeats; persist the client identity before sending so reconnection/restart can reconcile it. UI disabling alone cannot prevent retries, concurrent activation paths, or lost-response duplicates. Same revision must resolve to one logical operation. Release requires confirming this service contract or implementing equivalent guarantees. Retain pending guards across all input paths, not just touch.

## Worked before/after

**Before:** A reporter finishes revision 12. Four filled 20 × 20 pt controls have 2 pt gaps; Delete is default. The reporter taps Publish at t=0, t=2 and t=4 during an eight-second wait. No feedback appears; three uploads are created. A person navigating by accessible names cannot identify Preview.

**After:** The footer contains named, separated targets at least 44 × 44 pt; Publish is visually primary and Delete has no editor default binding. At t=0, Publish captures revision 12, locks operation R12, and immediately shows an in-button indicator with “Publishing…”. The accessible state announces publishing once. Taps at t=2 and t=4 create no additional request. At t=8, an authoritative success removes the indicator and presents “Report published.” Exactly one publication exists. If the reporter edited revision 13 while waiting, status identifies revision 12 as published and revision 13 remains a draft. If acknowledgment was lost instead, the UI shows uncertain status and checks R12; retry reuses R12 and cannot create another publication.

## Acceptance checks (specified, not executed)

1. Inspect every idle, pressed, disabled and pending action: all four functions exist; one prominent Publish; secondary Preview/Save Draft; destructive Delete has no editor default binding. Focused controls activate with keyboard; Return in report text inserts a newline.
2. Measure actual hit regions in iPad layouts: each ≥44 × 44 pt, nonoverlapping, with clear separation and isolated Delete. Test narrow windows, rotation and at least 200% text enlargement without lost labels or targets.
3. Inspect accessibility semantics and then test with VoiceOver, Voice Control, Full Keyboard Access and Switch Control: Preview is named; all buttons expose roles and state; busy, success and failure are perceivable without relying on color or animation. Focus remains predictable when states change. These require later runtime evaluation.
4. Inject an eight-second upload. Observe immediate in-button activity and press feedback; repeated touch, keyboard and assistive activation produce one operation. At success, activity ends and success status remains available. Test the proposed slow-status threshold separately with a longer delay.
5. Inject definite rejection, no connectivity, lost acknowledgment, repeated callbacks, reconnection and restart. Draft content survives; uncertain status never reports success; all retries use the same operation identity; the service creates at most one publication. Verify final processing is included in any determinate progress.
6. Edit during upload and verify the captured revision is published, later changes remain draft, Preview/Save Draft work consistently, and Delete is unavailable with a reason until the operation resolves. Verify late callbacks cannot overwrite a newer operation's UI.
7. Verify deletion policy against actual persistence: Undo really restores an undoable deletion; otherwise irreversible confirmation explains the exact scope and Cancel changes nothing. Test optional cancellation only if its service guarantee exists.

## Evidence and limits

Only interface.md and installed skill guidance were used; no web browsing. Official URLs above are source attribution from local snapshots, not evidence of live-site verification. The installed root SKILL.md was explicitly read first. Routing then read menus-and-actions, status, foundations and presentation family SKILL.md files before their selected article references: buttons.md, progress-indicators.md, accessibility.md and alerts.md. The topic index was consulted for exact components. These families routed directly to articles and specified no additional topic procedure. All paths were resolved within `.agents/skills/apple-hig/`; each file read used its own command.

The sources are a dated local snapshot (2026-10-25), not SDK documentation or proof of independent source review. No screenshot, source implementation, service contract, rendered app, runtime, Apple SDK, device, GUI, accessibility tree or assistive-technology execution was supplied or performed. Consequently contrast, actual target geometry, focus behavior, adaptation, network semantics and accessibility execution remain unverified. Missing upload feedback, duplicate creation and the stated controls are description-backed findings; the state machine, idempotency contract, spacing choice, revision policy and recovery copy are proposed corrections. Deletion reversibility, publication side effects and safe cancellation remain implementation questions, not additional verified violations.
