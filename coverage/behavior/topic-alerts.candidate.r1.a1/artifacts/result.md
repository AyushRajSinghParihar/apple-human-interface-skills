# Mac research archive: irreversible-delete alert audit

This is a specification review of `interface.md`, not an executed app audit. Rankings reflect potential consequence first, then interruption frequency. All four findings below are verified against the supplied description; implementation outcomes remain unverified.

## Ranked findings and decisions

| Rank | Verified evidence | Effect and correction | Source |
| --- | --- | --- | --- |
| 1 — High | Irreversible deletion is titled `Error`, says `Something happened`, and offers `Yes` / `No`. | Conceals the affected object, permanence, and action outcomes. Replace with a contextual deletion question, explicit irreversible consequence, and `Cancel` / `Delete Archive`. A deletion confirmation warrants interruption. The described buttons also lack the explicit Cancel label required alongside destruction; their actual handlers are unknown. | [Alerts: Best practices, Content, Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Content) |
| 2 — High | Sync failure presents a second alert over the first. | Competing modal decisions obscure the active task. Keep at most one alert; retain the deletion decision and record sync failure for in-context display, or present a necessary recovery alert only after the first closes and after revalidating relevance. | [Modality: Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices) |
| 3 — Medium | Every routine successful save triggers an alert. | Repeatedly blocks work without a consequential decision. Remove the alert; show a nonblocking `Saved` status in the archive context when useful. Do not infer sync success from local save success. | [Alerts: Best practices](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices) |
| 4 — Medium | The harmless save alert defaults to `Cancel`. | Cancel implies abandoning a task that already succeeded and is an inappropriate default. Removing this alert resolves the defect. If a separately justified completion acknowledgment is retained, use a single default `Done`; purely informational acknowledgment may use `OK`, with no invented cancellation effect. | [Alerts: Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons), [Buttons: Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role) |

These are source-backed findings. The exact copy, no-default choice, status treatment, and scheduling model below are product design decisions applying that guidance.

## Corrected behavior and control contract

Entry assumption: the person explicitly requests deletion of the selected archive. The brief does not establish the initiating command or deletion scope. Bind the confirmation to a stable archive identifier and display its actual name; verify the scope before shipping. Do not invent claims about attachments, backups, or deletion from other devices.

Proposed worked example, using the illustrative archive name “Field Notes”:

| | Before (supplied) | After (proposed) |
| --- | --- | --- |
| Trigger | Irreversible archive deletion; initiating action unspecified | Person invokes deletion for Field Notes; no data changes yet |
| Title | `Error` | `Permanently delete “Field Notes”?` |
| Body | `Something happened` | `This will permanently delete this archive. You can’t undo this action.` |
| Actions | `Yes`, `No`; mappings/default unknown | Horizontal Mac row: `Cancel` leading, `Delete Archive` trailing |
| Default | Unknown | No default; unfocused Return does nothing |
| Cancel outcome | Unknown | Close confirmation; preserve archive, selection, and unfinished work |
| Delete outcome | Irreversible deletion described; handlers unseen | Explicit activation commits deletion of the confirmed archive only; update archive view after confirmed success |
| Concurrent sync error | Second alert above first | Record/coalesce error; no overlay alert; surface current sync status after dismissal |

`Cancel` has cancellation semantics. `Delete Archive` performs destruction, but for the assumed explicitly requested deletion it uses the alert-specific deliberate-destruction exception: normal visual styling is permitted. Choose no default here to encourage reading the irreversible consequence; do not make Cancel the default. If the real flow exposes unexpected destruction instead, use destructive styling and explain that unexpected consequence. A normal Delete default allowing Return is permitted for deliberate destruction; it is not a verified violation in this interface. See [Alerts: Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons).

Escape and Command-Period cancel the pending confirmation with the same data policy as Cancel. Focused-button activation remains available through the chosen toolkit’s ordinary keyboard interaction; no default does not mean disabling keyboard access. Do not bind bare Return globally to deletion. Restore focus to the initiating control after cancellation; after success, move to a meaningful remaining archive-list location. Focus behavior is a proposed contract requiring runtime verification.

Use Mac-appropriate standard button sizing and distinct, nonoverlapping targets; allow the archive name and translated labels to wrap or expand without hiding the permanent-loss message. Prefer system styles where available, but no Apple SDK is assumed. Do not add a caution symbol merely because this is a routine explicitly requested deletion. No suppression checkbox is proposed for this confirmation. See [Buttons: macOS](https://developer.apple.com/design/human-interface-guidelines/buttons#macOS) and [Alerts: macOS](https://developer.apple.com/design/human-interface-guidelines/alerts#macOS).

## Framework-agnostic transition specification

```text
state = idle | confirming(targetID, revision, returnContext) | deleting(targetID)
activeAlert = none | deleteConfirmation | recovery
pendingSyncIssue = none | latestRelevantIssue

on routineSaveSucceeded:
    update local save status to Saved without opening an alert
    leave sync status independent

on requestDelete(target):
    if state != idle or activeAlert != none: do not open another confirmation
    capture target ID, revision, display name, and return context
    state = confirming(...)
    activeAlert = deleteConfirmation
    block changes in the affected parent; do not globally block unrelated work
    render exact copy and buttons above, with no default action

on Cancel / Escape / Command-Period while confirming:
    dismiss confirmation; clear activeAlert; state = idle
    preserve data and restore return context
    reconcilePendingSyncIssue()

on explicitly activate Delete Archive while confirming:
    revalidate target identity, revision, and deletion eligibility
    if changed: close stale confirmation without deleting;
                explain changed target in context; require a fresh request
    otherwise:
        atomically leave confirming so repeated activation cannot submit again
        dismiss confirmation; clear activeAlert; state = deleting(targetID)
        perform deletion once; indicate pending work in context
        on success: update archive view; state = idle; restore meaningful focus
        on failure or uncertain result:
            reconcile actual archive state; never claim successful deletion
            state = idle; explain known failure and available recovery
        reconcilePendingSyncIssue()

on syncFailure(issue):
    pendingSyncIssue = coalesceByAffectedArchive(issue)
    if activeAlert == none and state == idle: reconcilePendingSyncIssue()

reconcilePendingSyncIssue():
    discard resolved or obsolete issues
    show relevant sync failure in context, with supported recovery actions
    if immediate user decision is genuinely necessary:
        wait until activeAlert == none and state == idle
        revalidate issue; then present one contextual recovery alert
    never stack alerts or replay duplicate stale errors
```

The scheduling and revalidation rules are proposed safeguards, not evidence of existing backend behavior. No retry or local-copy guarantee is promised without implementation evidence. A failed sync must not silently reinterpret the archive being confirmed. A later recovery alert must describe the actual problem and available actions rather than reuse `Error` / `Something happened`.

## Acceptance checks and results

**Passed — static audit only:** platform and irreversibility are explicit in the supplied brief; an irreversible-deletion confirmation is justified. The proposed specification names outcomes, provides safe cancellation, defines a no-default policy, and prevents stacked alerts on paper. These passes do not establish runtime compliance.

**Failed — supplied behavior:** consequential title/message clarity; specific action labels and explicit Cancel; routine-success interruption policy; save acknowledgment default; single-alert presentation policy. These failures come from the brief, not observed device execution.

**Not executed — implementation acceptance checks:**

1. Invoke deletion for a named archive: show the specified name and permanent-loss warning before mutation. Return with no focused button does not delete. Deliberately activate Delete Archive by keyboard and pointer: exactly one deletion request targets the confirmed ID.
2. Test Cancel, Escape, and Command-Period independently: no deletion, preserved work and selection, useful focus restoration. Test supported window-close/navigation paths: they must not bypass confirmation or commit deletion.
3. Change or remove the archive while confirmation is open: reject stale confirmation; never substitute another archive. Repeat activation during pending deletion: no duplicate request. Simulate success, failure, and uncertain completion: report only verified state.
4. Complete repeated routine saves: no alert or focus theft; Saved status reflects local success only. If a justified acknowledgment exists elsewhere, test its intended Done/OK behavior and default separately.
5. Trigger sync failure during confirmation, during deletion, and repeatedly: at most one alert; deletion choice remains understandable; errors are coalesced, revalidated, and surfaced without stale replay. Canceling deletion must not erase a relevant sync issue.
6. Render long names, enlarged text, and translated labels: no clipped consequence or overlapping controls. Verify actual focus order, button names, keyboard activation, and assistive announcement in the target implementation. Measure selectable regions from real layout/runtime evidence; no size defect is established by this brief.

## Evidence and limits

Only `interface.md` and installed local guidance were used. No screenshot, implementation, executable, Apple SDK, device, GUI, keyboard, or accessibility execution was available. Button geometry, actual roles/styles, delete default, Yes/No handlers, deletion scope, focus behavior, sync urgency, and persistence/recovery guarantees are unknown. No such unknown is ranked as an observed defect. The worked archive name is illustrative.

Instruction route read explicitly, with one file per shell command: installed `apple-hig/SKILL.md`; Presentation family → Alerts procedure → `presentation/references/alerts.md`; Patterns family → Modality procedure → `patterns/references/modality.md`; Menus and actions family → Buttons procedure → `menus-and-actions/references/buttons.md`. All paths were resolved within `.agents/skills/apple-hig/subskills/` for family material. Alerts owns confirmation/default/copy; Modality owns competing presentations/exits; Buttons covers each supplied Yes/No/Cancel control, including questions whose implementation is unseen.

The installed source guides identify a 2026-10-25 snapshot and are derived guidance, not SDK documentation or proof of independent source review. Official links above are attribution from those local guides; no web content was fetched. General button guidance prefers nondestructive defaults; the more specific alert guidance permits a normal default for deliberately requested destruction. This specification preserves that exception and selects the documented no-default option rather than asserting that deletion can never be default.
