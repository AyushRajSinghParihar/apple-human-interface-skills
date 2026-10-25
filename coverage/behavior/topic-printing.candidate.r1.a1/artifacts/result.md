# Revised Mac badge printing interaction specification

## Scope and evidence

The complete supplied interface describes macOS, immediate printing of every attendee, invisible selected range and paper size, attendee deletion on cancellation, and possible missing-printer/job-rejection failures. No implementation, screenshots, badge dimensions, printer capability data, or runtime is supplied. These are reported behaviors from `interface.md`, not independently reproduced defects.

This specification is framework agnostic. A printing adapter must expose configuration, preview, submission, and observable job outcomes. Prefer standard macOS system printing in the eventual Mac client; this document neither assumes an Apple SDK on this server nor substitutes a custom implementation for verified system capabilities. If integration cannot provide the contract, treat that as an implementation gap, not successful printing.

## Decisions and interaction contract

1. **Separate intent, review, and submission.** File > Print… (Command-P) opens configuration and preview; it never submits immediately. Page Setup… precedes Print… and handles document-level paper size, orientation, and scaling. Preserve familiar Mac command placement and unavailable commands as dimmed items. [Printing, Best practices and macOS](https://developer.apple.com/design/human-interface-guidelines/printing#macOS), [File menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#File-menu).
2. **Use system-owned common choices.** The print presentation owns printer, copies, page range, and supported printer features. Add only a clearly named “Badges” category for attendee scope; do not create competing copies or page-range controls. Paper size remains visibly summarized in preview even when edited through Page Setup. Retain committed document setup at least while the event is open. [Printing](https://developer.apple.com/design/human-interface-guidelines/printing).
3. **Treat printing as read-only access to attendees.** No preparation, submission, cancellation, rejection, or completion may delete or modify attendee records. A job history is separate from the attendee database. This is a product safety decision responding directly to the supplied destructive cancellation, rather than a prescribed HIG database architecture.
4. **Use one scoped, parent-attached print presentation.** It blocks that event window while other app windows remain usable. Configuration, preview, and corrections stay in this presentation; do not stack a custom preview sheet over a print sheet. A necessary failure alert may appear above it, one at a time. Cancel is always visible; outside clicks do not dismiss. [Sheets, macOS](https://developer.apple.com/design/human-interface-guidelines/sheets#macOS), [Modality, Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices).

### Entry and availability

Print… is enabled only with printable attendees and a known available printer. When discovery is pending, show “Checking printers…” in context and keep submission disabled. With no printer, dim Print… and show an event-level message: “No printer is available. Add or reconnect a printer to print badges.” Provide “Check Again”; do not alert repeatedly. Page Setup and a separate “Preview Badges…” command remain available without a printer so review is possible. Preview Badges… uses the same renderer and settings in the event workspace; it cannot submit. With zero attendees, show “Add attendees to preview or print badges.” All routes recheck availability before submission. This follows the local printing guide’s explicit missing-printer dimming rule; preview availability is a product decision.

### Preview and settings

- Header: event name, “Print Badges”, attendee scope, total badges, total sheets, and copies. Default scope is “Selected attendees (N)” when the event has a selection; otherwise “All attendees (N)”. A visible scope choice allows switching, without altering the event selection. Never infer that filtering means selection.
- Show actual page composition, printable boundary, badge boundaries, and “Sheet X of Y”. Provide previous/next and zoom; zoom affects viewing only. Keep a visible summary such as “Selected attendees: 12 · Sheets 1–2 of 2 · A4 · Portrait · 100% · 1 copy”. Values here are examples, not assumed stock dimensions.
- Label attendee scope separately from system “Pages”: selecting pages prints sheets of the chosen attendee set. Show how many badges fall within that page range and list their names in a preview details view. Stable ordering follows the captured event ordering, disclosed in details.
- Changing scope, paper, orientation, scaling, copies, or page range regenerates the preview and totals. Disable Print until the current settings have a valid preview. Out-of-order asynchronous render results cannot replace the latest preview.
- Reject empty/out-of-bounds ranges with a nearby remedy: “Choose pages between 1 and Y.” Explain incompatible media/settings beside the affected choice. If badge content clips or a layout exceeds printable bounds, block submission with “Badges do not fit this paper. Change paper size or badge layout.” Do not silently shrink physical badge dimensions. Exact stock dimensions and supported scaling require product/printer validation.
- Opening Page Setup from this flow replaces the current presentation after preserving its draft. Apply returns to a regenerated preview; Cancel returns to the unchanged draft. Canceling the overall print task discards uncommitted print choices. Previously applied Page Setup settings remain document settings. No exit changes attendee data.

Preview effects, supported options, incompatibility explanation, and document setting retention follow [Printing, macOS](https://developer.apple.com/design/human-interface-guidelines/printing#macOS). Specific badge summaries, clipping policy, and defaults above are product decisions.

### Commit, cancellation, and recovery

Print is the trailing affirmative action; Cancel leads it. Return activates Print only when enabled and configuration is valid, never while editing a field that consumes Return. Escape and Command-Period cancel before submission. Cancel, supported close requests, and keyboard cancellation share one handler: discard the uncommitted print draft, preserve attendees and event selection, return to the event, and restore focus to the initiating control (or attendee list if it no longer exists). No discard alert is needed for disposable print configuration. Visible pending feedback says “Preparing preview…” or “Sending job…” as appropriate; these are ordinary inline status messages.

On Print, freeze attendee IDs, rendered content, settings, and preview revision into an immutable job snapshot. Disable repeat submission immediately. Revalidate printer and capabilities; if changed, return to configuration with the reason and regenerate preview. A late preview or callback from an older attempt cannot change the active attempt.

| Observed outcome | Presentation and exact recovery | Data and next state |
| --- | --- | --- |
| Printer disappears before submission | Inline “The selected printer is unavailable. Choose another printer or reconnect it.” Keep Print disabled; offer Check Again and printer selection. | Keep draft and preview; no submission. |
| Confirmed rejection with no accepted job | One alert: “The printer rejected the badge job.” Message: “No job was accepted. Check the printer or choose another printer, then try again.” Append a verified reason when available. Buttons: Cancel (leading, cancellation role), Review Settings (trailing, default, non-destructive). | Cancel closes task; Review Settings returns to preserved configuration. Retry requires a fresh explicit Print. |
| Submission timeout or acceptance unknown | One alert: “The badge job’s status is unknown.” Message: “The printer may have received it. Check the print queue before sending another job to avoid duplicate badges.” Buttons: Cancel (leading), Review Job (trailing, default). | Preserve snapshot and attempt ID. Review Job shows available queue evidence or honestly says status unavailable; no automatic retry. A later explicit “Print Again…” returns to preview with duplicate-risk text before submission. |
| Queue confirms acceptance | Close print presentation; inline event status “Badge job sent to [printer].” Provide job details/queue route when supported. | Record accepted job separately. Do not claim badges physically printed. |
| Confirmed post-acceptance failure | Inline job status “Badge job failed” with available reason and Review Job. | Preserve accepted job identity; never auto-resubmit. Partial output requires the person to inspect output/queue and explicitly choose badges to reprint. |
| Cancel before submission | Close without sending. | Preserve all attendees and event selection. |
| Cancel request during submission | Request adapter cancellation only if supported; show “Cancel requested” until confirmed. Otherwise explain it is already being sent and offer job details. | Never equate dismissal or cancellation request with proof that nothing printed. Track late acceptance/rejection in job history. |

Alerts use meaningful actions and safe exits, with no automatic retry as a default action. Repeated errors update the existing failure context instead of stacking alerts. No suppression checkbox hides failures requiring recovery. Button roles/order, Return/default behavior, and alternate cancellation follow [Alerts, Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons); contextual remedies follow [Writing, Best practices](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices). Job identity, duplicate prevention, and uncertainty handling are product decisions.

## Framework-agnostic state sketch

```text
onOpenPrint(event):
    require printableContent(event) and printerAvailable
    draft = copy(lastAppliedSettings, currentSelectionOrAll)
    state = configuring
    regeneratePreview(draft, revision++)

onPreviewReady(result, revision):
    if revision != currentRevision: ignore
    preview = result
    canPrint = preview.valid and printerAvailable and not submissionPending

onPrint():
    require canPrint
    submissionPending = true             // synchronous double-submit guard
    job = freeze(content, attendeeIds, draft, preview.revision, newAttemptId())
    revalidateAndSubmit(job)              // adapter; no attendee write capability

onResult(attemptId, outcome):
    updateSeparateJobHistory(attemptId, outcome)
    if attemptId != activeAttempt: return // never reopen obsolete UI
    transitionAccordingToOutcomeTable(outcome)

onCancelBeforeSubmit():
    invalidatePendingPreviewCallbacks()
    discardPrintDraft()
    closeAndRestoreFocus()
```

After submission, cancellation follows the outcome table, not the pre-submit handler. Definitive no-acceptance results permit a fresh attempt; uncertain results require explicit review. Adapter delivery cannot be assumed exactly once across a printer boundary.

## Worked before/after

Illustrative fixture: an event has 120 attendees, 12 selected, and a validated layout fitting 10 badges per A4 sheet.

**Before, from the brief:** choosing Print sends all 120 badges immediately. Scope and paper are invisible. Cancel removes attendees. A missing printer or rejected job has no specified recovery.

**After:** choose File > Print…. The presentation shows “Selected attendees (12)”, two sheets, A4, portrait, actual badge placement, and one copy. Nothing has been sent. Change to sheet 2: the preview and details show the remaining two badges and the summary changes to “2 badges · Sheet 2 of 2”. Cancel returns to the same 12 selected attendees; all 120 records remain. Reopen, review both sheets, and choose Print. If the printer definitively rejects the job, Review Settings preserves the 12-person scope and paper choices. Choose another available printer, validate its printable area, review the regenerated two-sheet preview, then explicitly Print. Acceptance produces “Badge job sent”, not “120 attendees printed”. If acceptance is unknown, use Review Job before deciding whether to print again.

## Acceptance checks and audit status

**Passed — specification inspection only:** the brief’s immediate-submit, hidden scope/paper, destructive cancel, missing-printer, and rejection cases each have explicit revised behavior. The table separates accepted, rejected, and unknown outcomes. All pre-submit exits preserve attendee data. Root, owning families, routed topic procedures, and supporting guides were read locally in that order per route; the topic index was searched. No web access was used.

**Failed — supplied design against this contract, based on the brief:** immediate submission bypasses review; range/paper are hidden; cancellation deletes attendees. These are brief-level findings, not executed failures. Missing-printer and rejection behavior is unspecified, so it is an evidence gap rather than a demonstrated runtime defect.

**Not executed — implementation acceptance checks:**

| Check | Required observable result |
| --- | --- |
| Open, cancel, Escape, Command-Period, close; repeat after changing options | No job before explicit Print; identical attendee records/count and restored event selection; defined draft retention and focus return. |
| Zero attendees, no printer, pending discovery, reconnect | Correct disabled commands and contextual remedy; preview remains usable when content exists; availability rechecked. |
| Selection versus all, sheet subset, copies, paper changes | Correct badge membership, totals, pagination, and physical layout; summary matches preview and submitted snapshot. |
| Invalid ranges, incompatible media, clipping | Specific remedy, disabled submission, no silent scaling. |
| Rapid changes and delayed preview callbacks | Only newest revision is shown and printable. |
| Double activation, rejection, timeout, late callback | One attempt per explicit activation; no automatic resend; preserved draft and accurate known/unknown status. |
| Accepted job, cancellation race, partial output | Queue acceptance distinguished from physical completion; no deletion or automatic reprint; late result retained. |
| Multiple event windows, hidden toolbar, repeated errors | Correct active-event scope; File command works independently of toolbar; other windows usable; no stacked sheets/alerts. |
| Keyboard, resizing, long text, assistive access | Every setting/action reachable and labeled; readable preview alternatives and error text; no clipped actions; focus enters and returns predictably; default Return never bypasses validation. |

## Evidence limits and handoff

Only local text was inspected and this specification was produced on the headless Linux server. No Mac GUI, physical printer, SDK compilation, queue integration, keyboard execution, screen-reader execution, accessibility conformance, rendering, or printed dimensions were tested. The final acceptance row describes required behavior, not established accessibility results. Validate interactive Mac behavior on the MacBook; run source/build work on the server as appropriate.

The installed guides are independent, dated HIG summaries (snapshot/retrieval 2026-10-25), not SDK references or proof of current platform support. Official links above are provenance copied from those local guides; they were not visited. Printer discovery, cancellation, job queries, printable bounds, stock dimensions, adapter support, and PDF output remain implementation-dependent. The local guide explicitly dims Mac Print when no printer exists; this specification conservatively does so and keeps preview separate rather than asserting an unverified PDF exception. No source conflict was identified in the material used. Native system integration and any fallback must be validated before claiming the specified Mac behavior works.
