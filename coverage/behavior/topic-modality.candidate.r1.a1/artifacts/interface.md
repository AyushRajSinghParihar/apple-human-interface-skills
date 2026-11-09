# Draft composer — iOS and iPadOS

## Task and presentation

Create and save one draft, optionally adding attachments and draft-specific settings, then return to Browse. A single modal composer blocks its originating Browse view to keep this scoped task focused. Global app settings belong in ordinary navigation after closing the composer; they never open above it.

Use a large-only sheet on iPhone for writing space. On iPad, prefer a standard centered page/form sheet over a dimmed parent; adapt within the available window, including compact multitasking widths. Keep the same task and data contract at every size. Size changes must not recreate the draft or add a presentation. If writing becomes a substantial multi-task workspace, reevaluate modality rather than extending this flow indefinitely.

## State and ownership

One coordinator owns `presentation = none | composer`, `step = editor | attachments | draftSettings`, and `decision = none | discardConfirmation`. These are exclusive values, not independent presentation flags. Attachment and settings screens are internal navigation within the composer. At most one composer and one necessary confirmation are visible; never stack sheets or alerts.

The draft store, independent of view lifetime, owns a stable draft ID, text, attachment references and upload statuses, draft settings, revision, and last durably saved revision. Selection/caret and scroll position are retained for this session. Pending attachment selections are isolated until Add; navigation never mutates or erases the writing. Retain local attachment files until explicit removal, successful transfer of ownership, or confirmed draft discard.

Persist accepted changes as local draft revisions. Display Saving until durable storage acknowledges the latest revision; only then display Saved. Closing waits for that revision to be durable. On storage failure, remain in the composer with text intact and an inline explanation plus Retry; never report success or discard as a fallback. Relaunch restores the last durable revision and marks interrupted uploads retryable. Unacknowledged changes cannot be promised after abrupt process termination; foreground/background transitions flush pending changes where execution permits.

## Titles, controls and navigation

- Editor: title New Draft (Edit Draft on resume), leading Close, trailing Done. Done means save draft and close, never send or publish. Explain this with nearby text: “Done saves this draft.” Provide Attachments and Draft Settings entry rows and a clearly labeled Discard Draft action.
- Attachments: title Attachments, leading Back, trailing Add enabled only for a valid selection. Back abandons only unadded selections, returns to the editor and restores its entry control focus. Add commits the selection to the draft, returns to the editor and starts uploads. Existing attachments and writing survive both routes.
- Draft Settings: title Draft Settings, leading Back. Changes update the draft immediately; Back returns to the editor. Do not show an unrelated Done/Cancel pair here.
- Close is always discoverable in the editor. From either substep, Back leads there. Do not show Back, Close and Done together. Preserve editor text, caret and scroll when returning.

## Transition and exit contract

| Event | Data and state result | Destination |
| --- | --- | --- |
| Compose from Browse | Create one stable draft ID; ignore repeated presentation requests during transition | Composer/editor; focus writing field |
| Resume from Browse draft row | Load durable draft; reset transient decision and substep | Composer/editor; restore session caret if available |
| Open Attachments / Draft Settings | Preserve draft; change internal step only | Named internal screen |
| Done from editor | Persist latest revision; disable duplicate completion while saving; on success update Browse exactly once | Browse, focus originating control or saved draft row |
| Close, completed swipe dismissal, supported Escape/Command-Period, or product navigation away | Same shared exit handler from any step: persist accepted draft changes before dismissal; unadded file selections are abandoned; no writing is discarded | Browse; restore originating focus |
| Clean/empty exit | No confirmation; remove an untouched empty placeholder after successful close | Browse |
| Cancelled interactive swipe | No dismissal or deletion; retain current step and input | Current composer screen |
| Home/app switch/background | Preserve draft and flush where possible; this is interruption, not discard | Resume current session state; relaunch uses editor with durable content |
| Discard Draft | Present one confirmation: “Discard this draft?” / “This deletes the writing and attachments in this draft.” Buttons Cancel and destructive Discard | Composer remains underneath |
| Cancel confirmation, supported keyboard cancellation, or outside dismissal if offered | No deletion; clear decision | Editor with Discard Draft focus restored |
| Confirm Discard | Atomically remove draft and owned attachment files; cancel/invalidate its uploads; close only after success. Failure keeps content and offers inline Retry | Browse on success |

Interactive dismissal must route through the exit handler before the composer vanishes. If the framework cannot pause that dismissal for persistence, prevent completion until saving succeeds while retaining Close/Done. No gesture may bypass this rule. On iPad, any offered outside-click dismissal uses the same handler. Escape cancels a visible confirmation first; it must not also close the composer. While a decision or save/discard transition is pending, coalesce repeated exits and prevent competing transitions.

## Upload recovery and presentation arbitration

Show upload failures beside the affected attachment: “Upload failed. Your draft is saved.” only when the saved status is true; otherwise show the actual saving status. Offer Retry and Remove inline. Tapping the error reveals inline details, never an alert. Retry is single-flight per attachment; repeated taps do not start duplicate uploads. Removing an attachment preserves writing.

All events go through the coordinator serially. Duplicate confirmations are ignored. Upload callbacks update attachment state without opening presentations, including while a confirmation is visible. Callbacks carry draft ID, attachment ID and attempt generation; ignore stale callbacks after removal, discard or retry. Closing preserves pending/failed attachment records for resume. Reopening begins at editor, not an obsolete error or settings presentation.

A future necessary blocking alert must use this same exclusive decision slot: defer it until the existing decision has dismissed, revalidate its relevance, then present it. Complete dismissal before presenting any replacement composer. Never queue obsolete alerts for later replay.

## Design basis

These are product decisions informed by the supplied local HIG snapshot, not SDK API guarantees. [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices) supports clear task titles, familiar exits, protecting created content and avoiding stacked presentations. [Sheets — Anatomy, Best practices, and iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/sheets) distinguishes Back from completion, recommends one sheet, describes large composition sheets and preferred iPad page/form styles. [Alerts — Best practices and Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts) supports contextual status and specific actions with a cancellation route for destruction. Automatic draft retention and the exact persistence/coordinator model above are application policy; they eliminate routine loss rather than requiring a save/discard prompt for every exit.
