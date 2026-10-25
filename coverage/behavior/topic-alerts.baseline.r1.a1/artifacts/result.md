# macOS research archive alert audit

## Scope and decisions

This is a specification audit of [interface.md](interface.md), not an executed app review. Keep confirmation for irreversible archive deletion; remove routine successful-save alerts; never stack alerts. Use clear deletion consequences and explicit actions. Choose **no default button** for the irreversible-delete confirmation, with Cancel available. This is a product decision supported by the HIG option to require deliberate reading, not a universal requirement for all deletion confirmations.

## Ranked verified findings

Rank reflects potential harm and disruption, not measured incident frequency.

| Rank | Verified observation | Effect and guidance | Correction |
|---|---|---|---|
| 1 — High | Irreversible deletion uses title **Error**, body **Something happened**, and **Yes / No**. | Conceals the pending destructive decision and its consequences. HIG advises against bare error titles, calls for useful contextual text, prefers outcome labels over Yes/No, and says destructive actions must have Cancel. [Alerts: Content and Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Content) | Name the archive and irreversible consequence; use **Cancel** and **Delete Archive**. Do not describe a confirmation as an error. |
| 2 — High | Sync failure presents a second alert over the first. | Creates competing modal decisions and obscures context. HIG explicitly says never to stack multiple alerts. [Modality: Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices) | Keep one alert active. Record sync failure and show contextual status; if immediate attention is genuinely required, present a still-relevant alert only after the current alert closes. |
| 3 — Medium | Every routine successful save triggers an alert. | Repeatedly interrupts work without a decision to make. HIG reserves alerts for immediate attention and puts informational status in context. [Alerts: Best practices](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices) | Complete the save without a modal. If feedback is useful, show unobtrusive **Saved** status near the document/archive context. |
| 4 — Low | The harmless save alert defaults to **Cancel**. | A success acknowledgment has nothing to cancel. HIG says a single default acknowledgment should be Done rather than Cancel. The supplied description does not establish the full button set, so the single-button rule is conditional. [Alerts: Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons) | Removing the alert resolves this. If a separate, justified informational acknowledgment is retained, use **Done** as its single default action. |

Deletion confirmation itself is appropriate for irreversible destruction. The description does **not** establish the deletion alert's current default, button order, styling, icon, keyboard behavior, or focus. These are requirements below, not additional verified defects.

## Worked before / after

Illustrative archive name: **Field Notes**. The name is an example, not supplied app data.

**Before — supplied behavior**

```text
Routine save succeeds → alert (default: Cancel)
Irreversible deletion → Error
                        Something happened
                        [Yes] [No]
Sync fails while an alert is open → another alert above it
```

**After — proposed behavior**

```text
Routine save succeeds → in-context “Saved” status; continue working

Explicit request to delete Field Notes → one confirmation:

    Permanently delete “Field Notes”?
    This archive will be permanently deleted. This action cannot be undone.

    [Cancel]                         [Delete Archive]
    No default button

Sync fails while confirmation is open → retain failure state;
    no second alert; offer contextual “Sync failed” status and Retry
    where relevant, without dismissing or answering the confirmation.
```

The message deliberately makes no claim about deleting linked files, remote copies, collaborators' data, or backups. If deletion affects those resources, revise the message to state the verified scope before shipping. Local save success and sync success must remain distinguishable; use “Saved locally” only if the product actually guarantees a local save.

## Framework-agnostic behavior specification

```text
onDeleteRequested(archive):
    capture stable archive identity and current deletion scope
    present one confirmation through the alert coordinator
    title = Permanently delete “{archive display name}”?
    message = verified deletion scope + irreversibility statement
    actions = [Cancel, Delete Archive]
    defaultAction = none
    cancelAction = Cancel

onCancel / Escape / Command-Period:
    dismiss confirmation
    do not delete or queue deletion
    return focus to the invoking context

onDeleteArchiveChosen:
    validate captured identity, scope, and current permission
    if the intended scope changed: require a fresh informed decision
    otherwise dispatch deletion once; prevent repeated submission
    reflect actual completion or failure in the archive context
    never report success before the operation succeeds

onRoutineSaveSucceeded:
    update contextual save state; do not present an alert

onSyncFailed(failure):
    retain relevant failure state and expose contextual recovery
    if immediate attention is necessary:
        enqueue/deduplicate an alert request
        show only when no alert is active and request remains relevant
    never automatically answer or dismiss a deletion confirmation
```

The coordinator, identity validation, duplicate prevention, focus return, and Retry treatment are proposed implementation safeguards, not independently verified HIG violations. Serialization applies to every alert presentation path; stale queued failures must not reappear after recovery.

Use the expected/default action at the trailing end of a row, with Cancel generally leading; do not infer a universal layout across platforms. Here the macOS row has Cancel leading and Delete Archive trailing. Support Escape and Command-Period cancellation. With no default, Return in the newly opened alert must not implicitly delete; explicit keyboard activation of the focused Delete Archive control remains available. Initial focus should allow safe reading and cancellation, without preselecting destructive activation. These interaction details need implementation verification. [Alerts: Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons)

Do not require red styling solely because deletion is irreversible. The local guidance applies destructive styling to consequences the person did not deliberately request; an explicitly requested destructive confirmation can retain normal styling and a normal default. The trigger is unspecified here, so this proposal assumes an explicit delete request and chooses no default. Reassess styling if destruction is an unexpected consequence. Do not prescribe a caution icon without evidence of unexpected loss; macOS guidance reserves it for situations requiring extra attention. [Alerts: Buttons and macOS](https://developer.apple.com/design/human-interface-guidelines/alerts#macOS)

## Acceptance checks — specified, not executed

1. Save successfully several times: no alert appears, editing continues, and any visible status reflects actual save state.
2. Request irreversible deletion: exactly one confirmation identifies the intended archive and explains verified scope and irreversibility; buttons are Cancel and Delete Archive.
3. Cancel by button, Escape, and Command-Period: archive remains intact, no deletion is queued, and focus returns sensibly.
4. Open confirmation and press Return without choosing an action: no implicit deletion occurs. Keyboard users can reach and explicitly activate both actions.
5. Confirm deletion: exactly one operation targets the captured archive. Double activation cannot dispatch a second operation; failure is not reported as success.
6. Change selection or deletion scope while confirmation is pending: no different archive or expanded scope is silently deleted.
7. Fail sync during the confirmation: maximum simultaneous alert count remains one. Cancel and confirm still resolve the original decision; no deferred deletion is triggered by sync handling.
8. Recover sync before a queued failure alert is eligible: stale failure alert is discarded. Persistent failure exposes a meaningful recovery route without alert stacking.
9. Review rendered text, long archive names, keyboard focus, and assistive-technology announcement in the eventual implementation: identity, consequence, and actions remain available and understandable. This audit supplies no visual or accessibility pass result.

## Evidence and limits

Read order from the installed package: root `apple-hig/SKILL.md` → `subskills/apple-hig-presentation/SKILL.md` → alert entry in `references/topic-index.md` → presentation `references/alerts.md`; then modality index entry → `subskills/apple-hig-patterns/SKILL.md` → patterns `references/modality.md`. Each file was read in its own shell command. The selected families route directly to these article guides; no separate topic procedure was identified in those routes.

The guides identify their snapshot as 2026-10-25 and describe themselves as guidance derived from Apple sources. Official links above provide attribution; they were not fetched. Findings rely exclusively on the supplied textual description and installed instructions. No screenshot, source implementation, app execution, device, SDK, GUI, keyboard test, or accessibility execution was available or performed. Visual hierarchy, contrast, sizing, actual focus/default behavior, deletion scope, and sync recoverability remain unverified. Acceptance checks are future validation criteria, not test results.
