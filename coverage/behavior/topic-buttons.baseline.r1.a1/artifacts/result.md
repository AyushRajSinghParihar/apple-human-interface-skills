# iPad report editor export-control correction plan

This is a specification audit of [interface.md](interface.md), not an execution audit. Preserve Publish, Preview, Save Draft, and Delete. All four remain direct, discoverable footer actions; no Apple SDK is assumed.

## Ranked verified findings

Priority reflects likely harm and task blockage; it is a product judgment, not an Apple severity scale. “Verified” means explicitly stated in interface.md.

| Rank | Observed evidence and effect | Correction and guidance |
| --- | --- | --- |
| 1 — High | During the eight-second Publish upload, nothing changes and repeat taps create duplicate uploads. People cannot tell whether activation worked and can accidentally publish repeatedly. | Immediately show an activity indicator inside Publish, replacing any image, with “Publishing…”; prevent additional submissions while active. HIG explicitly describes in-button activity for delayed iOS/iPadOS actions; duplicate prevention is the engineering decision that makes this safe. [Buttons: iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS), [Progress: best practices](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices). |
| 2 — High | Delete is the primary/default action. A dangerous operation receives the expected-action emphasis and default activation. Actual deletion reversibility and keyboard behavior are unknown. | Remove Delete’s primary/default role; give it destructive semantics and a clear text label. Make Publish the preferred nondestructive footer action. [Buttons: role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role). |
| 3 — High | Every hit region is 20 × 20 pt, with 2 pt gaps. These targets are below both locally documented iPadOS size references and are tightly packed. | Use hit regions at least 44 × 44 pt, with clear separation and no overlap. Adopt 12 pt edge-to-edge gaps as this plan’s starting layout value, to validate at actual sizes. [Buttons: best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), [Accessibility: mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility). |
| 4 — High | Glyph-only Preview has no accessible name. Its purpose is unavailable through its name to assistive interaction. | Display “Preview” and expose accessible name “Preview” and button semantics. If a glyph is retained, treat it as decorative alongside that label. [Buttons: content](https://developer.apple.com/design/human-interface-guidelines/buttons#Content), [Accessibility: vision and mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |
| 5 — Medium | All four buttons have equally prominent fills. The footer fails to distinguish a preferred next action. | Use one prominent filled Publish button; use quieter Preview and Save Draft controls and a separated, lower-emphasis destructive Delete control. HIG advises one or two prominent buttons per view; selecting Publish is a product decision based on this export task. Review the rest of the editor before finalizing view-wide emphasis. [Buttons: style](https://developer.apple.com/design/human-interface-guidelines/buttons#Style). |

Size qualification: Buttons says general hit regions should be at least 44 × 44 pt; Accessibility lists 44 × 44 pt as the iOS/iPadOS default and 28 × 28 pt as its minimum control size. These are distinct statements, not a universal 44-pt minimum claimed from both. Use the conservative 44-pt target here. The 20-pt regions fail either reference. The supplied guidance suggests around 12 pt padding for bezelled elements; it does not establish an exact mandatory inter-button gap. Our 12-pt gap is a design decision.

## Corrected interaction decisions

Use consistent control heights and distinguish importance through style, not unequal button sizes. Suggested reading order: Preview, Save Draft, a separated Delete, then prominent Publish at the trailing end. Keep all actions visible. At narrow editor widths or enlarged text, wrap into labeled rows rather than shrinking targets or truncating action names. Provide visible press feedback for custom controls. Use semantic roles, adaptable colors and text, and an accessible interaction tree through whatever framework the project provides. Destructive meaning must be conveyed by “Delete” and semantics as well as color. [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons), [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility).

Primary styling does not mean intercepting Return anywhere in the editor. Return in report text must keep its editing behavior. Any default-action keyboard binding must be scoped to an appropriate action context; Delete receives no implicit default binding. Preserve explicit focused-button activation and complete keyboard navigation. This scoping is an implementation decision supporting the editor task.

Publish feedback starts when activation is accepted, before awaiting network work. Preserve its dimensions and context; expose busy/unavailable state and announce “Publishing report” without moving focus. Ignore repeated touch, keyboard, and assistive activations through a shared command guard, not just visual disabling. Keep Preview and Save Draft usable against the current local document. Publish uses a captured revision; subsequent edits must not silently change the upload. Temporarily make Delete unavailable for this report while publication is unresolved, with a discoverable explanation, “Publication in progress.” These concurrency choices are product decisions.

Use an indeterminate indicator when completion is unknown. If reliable whole-operation progress is available, display it honestly in a stable adjacent status area; do not invent percentages from the eight-second example or switch a spinner into a differently shaped bar. Include final server processing in completion status. On confirmed success, remove the indicator and report “Report published”; if edits occurred, identify that newer edits remain unpublished. On definite failure, retain the report, remove busy state, and offer “Retry Publish” with a useful failure explanation. Status belongs in context, not a routine modal alert. [Progress: best practices](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices), [Alerts: best practices](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices).

An unusually slow upload remains visibly active with “Still publishing…” and a useful recovery/status route. Eight seconds is the supplied scenario, not a universal HIG timeout. Do not infer failure from elapsed time. Support cancellation only if the transport and publication service can establish a safe outcome; do not relabel an active Publish button “Cancel” without explaining the changed action. If cancellation can discard useful partial work, consider pause and explain consequences. Cancellation support is unverified and is not promised by this plan. [Progress](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices).

For Delete, first establish whether recovery exists. A common undoable deletion can proceed with a real Undo opportunity; an irreversible report deletion gets a deliberate confirmation explaining loss, with Delete and Cancel. Choose no default in that confirmation to require deliberate activation. Do not claim HIG universally requires Cancel to be default: the alert guidance says not to make Cancel default and permits a normal default for deliberately requested destruction. That exception applies to the confirmation, not the standing editor footer. If supporting Assistive Access, the local accessibility guide specifies two confirmations for difficult-to-reverse actions in that mode. [Alerts: best practices and buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons), [Accessibility: cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive).

## Framework-agnostic command contract

```text
publication = idle | uploading | resolving | succeeded | failed
operation = { key, reportId, capturedRevision, payload }

onPublish():
    atomically:
        if publication in {uploading, resolving}: return
        operation = captureImmutableReportAndPersistentOperationKey()
        publication = uploading
    renderBusyPublishAndAnnounce()   // before awaiting upload
    send(operation.payload, operation.key)

onConfirmedSuccess(operationKey):
    if operationKey != currentOperation.key: return  // stale response
    publication = succeeded
    showPublishedRevisionAndAnyNewerUnpublishedEdits()

onDefiniteFailure(operationKey, reason):
    if operationKey != currentOperation.key: return
    publication = failed
    retainDocumentAndOfferRetry(reason)

onTimeoutOrConnectionLoss():
    publication = resolving
    showOutcomeUnknownAndReconcileUsingCurrentOperationKey()
    // Do not create a new publication while this outcome is unresolved.

onRetrySameOperation():
    resendSamePayloadWithSameKeyOrQueryItsStatus()
    // Changed content requires a new operation after resolving the old one.
```

The service must atomically deduplicate the operation key and return the same outcome for retries. Persist the key before sending so reconnects/restarts can reconcile it. A UI guard alone cannot guarantee exactly one publication after an ambiguous network failure. If the existing service cannot support this contract, retain the guard and expose outcome uncertainty, but treat reliable retry deduplication as unfinished engineering work. No service implementation was supplied.

## Worked before/after: slow Publish

**Before:** At t=0 a person taps Publish; no visual change occurs. At t=1 they tap again because the first tap appears ineffective. The specified behavior creates duplicate uploads. At t=8 there has been no in-flight feedback; completion feedback is unspecified.

**After:** At t=0 the command captures revision R7 and records operation K. Publish immediately shows its in-button indicator and “Publishing…” with a busy state announcement. A second tap at t=1 is ignored by the command guard. Preview still opens the local report; Save Draft still saves it. If the person edits to R8, K continues publishing R7. During all eight seconds the footer retains its layout and ongoing status. On confirmed completion at t=8, the indicator clears and status says “Report published. Newer edits are not published.” Exactly one publication of R7 exists for K. If the response instead goes missing, show “Publication status unknown — checking…” and reconcile K; do not claim success or submit a fresh publication.

## Acceptance checks to execute during implementation

- Inspect all four functions at normal, narrow split-view, and at least 200% text enlargement: labels remain readable, targets remain at least 44 × 44 pt, gaps remain clear, and hit regions never overlap. Measure actual hit bounds in pt, not just glyph bounds.
- Verify Publish is the sole prominent footer action; Delete has destructive semantics and no editor default binding. Return in report text inserts a newline. Focused buttons remain operable by keyboard.
- Inspect accessible names, roles, busy/unavailable states, focus order, and status exposure. Execute Preview through VoiceOver and Voice Control; test keyboard, pointer, Switch Control, and AssistiveTouch where available. Confirm status announcements do not steal focus or repeat on every animation frame.
- With an injected eight-second delay, verify immediate in-button feedback and exactly one accepted command for rapid taps and mixed input activations. Check that Preview and Save Draft work and Delete explains its temporary unavailability.
- Test definite failure, long delay, dropped response after server commit, reconnect, and restart. Verify retained drafts, truthful status, stable layout, stale-response rejection, and a single server publication when the same operation key is retried.
- Edit during upload: verify the uploaded revision is the captured one and newer edits remain saved and clearly unpublished. Confirm success is announced only after server acknowledgment.
- Exercise the chosen deletion branch: real Undo restores the report, or irreversible deletion requires deliberate confirmation with Cancel. Check focus returns appropriately after cancellation. Verify Assistive Access behavior separately if supported.

These are proposed checks, not reported passes.

## Evidence and limits

Read locally, in order: installed apple-hig/SKILL.md; menus-and-actions, status, and foundations family SKILL.md procedures; their Buttons, Progress indicators, and Accessibility source guides; then presentation/SKILL.md before Alerts. The package topic index was searched for the relevant article paths. Paths resolve under `.agents/skills/apple-hig/`; the linked official articles above identify the guidance, but were not fetched. The installed guides describe a 2026-10-25 snapshot and are derived guidance, not SDK documentation.

Only interface.md and the installed local instructions/guides support this audit. No rendered app, source implementation, backend contract, screenshot, dimensions beyond those stated, or runtime was supplied. No device, SDK, GUI, accessibility tool, network, or end-to-end execution occurred. Contrast, actual text scaling, real focus behavior, deletion reversibility, upload cancellation, service deduplication, other view-level primary actions, and product publishing semantics remain unverified. These unknowns are implementation validation work, not additional verified defects. The delivered artifact is this correction specification, not an implemented or tested interface.
