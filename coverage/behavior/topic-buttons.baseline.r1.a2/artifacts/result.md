# iPad field-report export controls: correction plan

## Scope and decisions

This is a specification audit of `interface.md`, not an inspection of a rendered interface. Preserve Publish, Preview, Save Draft, and Delete as four direct button functions. Use framework-independent semantic buttons with press feedback, accessible names, roles, and enabled/busy states. No Apple SDK is assumed.

Make Publish the single prominent action when the report is eligible for publication. Keep Preview and Save Draft secondary. Keep Delete visibly separate, explicitly labeled, and semantically destructive; it must not be the editor's primary/default action. This choice of Publish as the preferred action is a product recommendation based on the export task, not evidence about usage frequency. Explicit activation should trigger publishing; ordinary Return in report text must continue editing text.

## Ranked verified findings

Ranks reflect likely harm and task blockage, rather than measured incident rates. All observations below come from `interface.md`.

| Rank | Verified observation and effect | Correction and source |
|---|---|---|
| 1 — High | Delete is primary/default. Accidental default activation risks report loss; reversibility is unspecified. | Remove its editor default/primary role. Give it a destructive role and a text label. Buttons guidance generally assigns primary to a likely nondestructive action. [Buttons: Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role) |
| 2 — High | An 8-second Publish upload produces no change; repeated taps create duplicate uploads. People cannot tell that work started and can repeat its effects. | Immediately show an activity indicator inside Publish, label it “Publishing…”, and guard the operation against reentry. Show outcome/recovery in place. The in-button indicator is iOS/iPadOS guidance; transaction deduplication is an engineering correction derived from the observed defect. [Buttons: iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS), [Progress indicators: Best practices](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices) |
| 3 — High | Glyph-only Preview has no accessible name, obscuring its function for assistive navigation. | Prefer visible “Preview” text and expose the accessible name “Preview” with button semantics. A familiar glyph may accompany it. [Accessibility: Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [Buttons: Content](https://developer.apple.com/design/human-interface-guidelines/buttons#Content) |
| 4 — High | Every hit region is 20 × 20 pt, with 2 pt gaps. Small, tightly packed targets increase selection errors, especially near Delete. | Specify nonoverlapping hit regions at least 44 × 44 pt, with clear surrounding separation. Use an initial 12 pt gap between bordered controls and a larger separation before Delete; validate these layout choices rather than treating 12 pt as a universal minimum. Wrap into multiple rows when necessary. [Buttons: Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), [Accessibility: Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility) |
| 5 — Medium | Four equally prominent filled buttons obscure the preferred action and give destruction equal emphasis. | Use one prominent Publish button; secondary Preview and Save Draft; separated destructive Delete. Preserve comparable target sizes rather than expressing importance through size. HIG advises one or two prominent buttons per view. [Buttons: Style](https://developer.apple.com/design/human-interface-guidelines/buttons#Style) |

**Numerical qualification:** The installed Buttons article says general hit regions should be at least 44 × 44 pt. Accessibility lists iOS/iPadOS controls as 44 × 44 pt default and 28 × 28 pt minimum. These are different stated scopes, not a single interchangeable minimum. The supplied 20 × 20 pt falls below both. This plan conservatively chooses 44 × 44 pt hit regions and comfortable separation for this touch footer. Do not substitute macOS's 20 pt minimum or visionOS's 60 pt targeting rules.

## Corrected behavior

### Idle and deletion

Use visible labels “Publish”, “Preview”, “Save Draft”, and “Delete”. Maintain a logical focus order and equivalent touch, pointer, keyboard, and assistive activation paths. Adapt the footer to narrow iPad windows and enlarged text without clipping labels or overlapping targets. Preserve visible focus and avoid communicating destructive or disabled states through color alone. These are proposed acceptance requirements, not verified capabilities. [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

Deletion behavior depends on reversibility, which the supplied file does not establish. Prefer recoverable deletion with an accessible Undo route. Common undoable deletion generally needs no confirmation. If deletion is uncommon and irreversible, use an explicit confirmation naming the report and consequence, with “Delete” and “Cancel”; consider no default to require deliberate selection. The editor's destructive button rule does not imply that every explicit destruction confirmation must forbid a default: the installed Alerts guide allows a normal default confirming deliberately requested destruction. Never silently turn every delete into a mandatory alert. If Assistive Access is supported, account for the separately stated two confirmations for difficult-to-reverse actions in that mode. [Alerts: Best practices and Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts), [Accessibility: Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive)

### Slow Publish operation

On the first activation, synchronously acquire a publication guard before starting asynchronous work. Keep button geometry stable, replace any image with an in-button activity indicator, and show “Publishing…”. Expose busy/unavailable state and an accessible status update without moving focus. The label change is optional HIG advice adopted here for clarity. Do not wait eight seconds to acknowledge activation.

Use indeterminate activity when completion is unknown. If reliable whole-operation progress is available, show honest determinate progress in a consistent nearby status region, including final server processing. Do not invent percentages or swap the button spinner into a differently shaped bar midtask. Show “Published” only after authoritative completion. For a stall, explain what is known and provide recovery; do not infer failure merely because eight seconds elapsed. [Progress indicators: Best practices](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices)

For this plan, capture the current report revision for publication. Keep Preview and Save Draft available for local work; clearly identify which revision is being published if editing continues. Temporarily disable Delete while the publish result is unresolved, with a reason available to assistive users. These concurrency policies are proposed engineering decisions requiring implementation support, not HIG mandates. Offer cancellation only if the operation can be safely cancelled; do not claim that aborting a network request retracts a server publication. If cancellation discards useful partial work, consider pause and explain the consequence as the progress guidance recommends.

Framework-independent pseudocode:

```text
state = idle | publishing | reconciling | succeeded | failed
activeOperation = none

on Publish activation:
    atomically:
        if state in {publishing, reconciling}: return
        snapshot = currentReportRevision()
        activeOperation = persist(reportID, snapshot, newIdempotencyKey())
        state = publishing
    renderBusyPublishAndAnnounceOnce()
    submit(snapshot, activeOperation.key)

on authoritative success(operation, receipt):
    if operation != activeOperation: return
    state = succeeded
    showAndAnnounce("Published", receipt.revision)

on authoritative failure(operation, explanation):
    if operation != activeOperation: return
    state = failed
    preserveDraftAndOperation()
    showAndAnnounce(explanation, recovery = "Retry")

on timeout or lost response(operation):
    if operation != activeOperation: return
    state = reconciling
    showStatus("Checking publication status…")
    queryStatus(operation.key)  // do not start another publication

on Retry for the same unresolved attempt:
    reconcileOrResubmitUsingSameKeyAndSnapshot()
```

The backend must enforce idempotency for each operation key and return the same publication result on retries. A disabled button alone cannot protect against concurrent activation, reconnects, or lost responses. Persist unresolved operations across reloads if the implementation permits reload/resume. A later intentional publication of a new revision gets a new operation identity. If status lookup/idempotency is unavailable, expose the uncertainty and require resolution before another submission; this plan cannot promise duplicate prevention from frontend styling alone.

## Worked before/after

**Before:** The author taps Publish at t=0. All four filled 20 pt buttons remain unchanged. At t=2 seconds the author taps again because nothing appears to happen; another upload starts. At roughly t=8 seconds the first finishes, with duplicate work already in flight. Delete is still the default and Preview remains unnamed.

**After:** At t=0, a guard captures revision 17 and operation key K; Publish immediately shows an activity indicator and “Publishing…”. Preview, Save Draft, and Delete retain their functions and labels; Delete is temporarily unavailable with an explanation. At t=2, another activation cannot start an upload. At t=8, confirmed success changes the status to “Published” for revision 17 and releases the pending state. If the response is instead lost, the UI says “Checking publication status…” and checks K; retrying K cannot create a second publication. Preview and Save Draft remain secondary, while Delete has no editor default role. The eight-second duration is the supplied example, not a timeout threshold.

## Acceptance checks

These checks are specified for future implementation; none were executed against an app.

- All four functions remain discoverable and operable. Publish alone is prominent; Delete has destructive semantics and is never the editor default. Return in text does not delete or publish.
- Each target measures at least 44 × 44 pt in iPad layout coordinates, with no hit-region overlap and clear separation. Check narrow windows, multiline labels, and 200% text enlargement; reflow rather than shrink targets.
- Inspect the semantic tree: Preview is named “Preview”; all controls expose button role, enabled state, and applicable busy state. Verify focus order and activation with VoiceOver, Voice Control, Full Keyboard Access, pointer, and Switch Control on a suitable implementation.
- Simulate an eight-second upload. Busy feedback appears on first activation before the asynchronous wait; focus stays stable; repeated touch, keyboard, and assistive activation produces one operation and one server publication.
- Test measurable and unknown-duration work. Percentages derive from real whole-operation progress; unknown work remains indeterminate. Success is announced only after confirmation, and pending, success, and failure are understandable without animation or color alone.
- Test definitive failure, offline interruption, lost success response, retry, and reload during pending work. Preserve the draft; reconcile the persisted operation identity; prove that retries cannot duplicate publication. Distinguish confirmed failure from unknown outcome.
- Test deletion according to the chosen recovery policy: Undo restores the report, or irreversible deletion names the consequence and offers Cancel. Cancel preserves data and returns focus. Verify any supported Assistive Access behavior separately.

## Evidence and limits

Auditable local reads followed this route: installed `apple-hig/SKILL.md` → `subskills/apple-hig-menus-and-actions/SKILL.md` → `references/buttons.md`; root → status family → `references/progress-indicators.md`; root → foundations family → `references/accessibility.md`; root → presentation family → `references/alerts.md`. The complete topic index was searched for exact component names. All paths resolve inside `.agents/skills/apple-hig/`; the selected family files routed directly to these articles and supplied no additional topic procedure. The Buttons article's alert-specific exception prompted the presentation/Alerts read before prescribing deletion confirmation behavior.

Only `interface.md` and the installed instructions/guides informed this review. Official links above identify the guides' sources; they were not opened. Local guidance is a dated 2026-10-25 snapshot derived from HIG, not an independently verified current Apple manual or SDK reference. No web, media, device, SDK, GUI, build, runtime, or accessibility execution occurred. No rendered app was supplied. Actual contrast, typography, focus behavior, press feedback, publication architecture, deletion recoverability, and cancellation support remain unknown. They are validation needs, not additional verified defects. The operation protocol, layout spacing, snapshot policy, and recovery choices are proposed corrections, not claims about existing implementation or universal HIG requirements.
