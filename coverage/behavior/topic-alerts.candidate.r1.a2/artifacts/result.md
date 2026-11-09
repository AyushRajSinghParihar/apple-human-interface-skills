# Mac research archive alert audit

Scope: specification review of `interface.md`; no screenshot, implementation, or running app supplied. Findings below are verified against the brief, not observed on a device. Severity ranks reflect potential consequence, not measured incident frequency.

## Ranked verified findings

| Rank | Evidence and effect | Decision and source |
| --- | --- | --- |
| 1 — High | Irreversible archive deletion uses title `Error`, body `Something happened`, and `Yes` / `No`. Neither the affected archive nor permanent loss is explained; generic answers conceal the outcome. | Keep a consequential confirmation, name the target and permanence, and replace answers with `Cancel` / `Delete Archive`. A deletion request is not itself an error. [Alerts: Best practices, Content, Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Content); [Buttons: Content](https://developer.apple.com/design/human-interface-guidelines/buttons#Content). |
| 2 — High | A sync failure presents a second alert over the first. Competing decisions interrupt the original task and obscure which action is being resolved. | Never stack alerts. Record the sync failure and expose it in context; if immediate action is genuinely needed, serialize its alert after the active decision closes and revalidate relevance. [Modality: Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices). |
| 3 — Medium | Every routine successful save triggers an alert, forcing interruption without a necessary decision. | Remove this alert. Show a quiet `Saved` state near the document only after save completion is confirmed. Track sync separately. [Alerts: Best practices](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices); [Feedback: Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices). |
| 4 — Medium | The harmless save alert defaults to `Cancel`, misrepresenting completion as abandonment. Its handler and other buttons are unknown. | Removing the alert resolves this. If a separate, justified completion acknowledgment is retained, a single default completion button is `Done`; purely informational acknowledgment can use `OK`. Cancel abandons a pending task and must not be the alert default. [Alerts: Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons); [Buttons: Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role). |

No finding claims that deletion currently lacks a cancellation handler, uses red styling, or has an unsafe Return mapping: none is supplied.

## Corrected behavior and decisions

For this specification, assume the user explicitly invokes deletion of one identified archive. The brief does not establish the actual entry point or deletion scope; verify both before implementation. Do not imply removal of source files, backups, or remote copies unless the product actually does that.

Show one confirmation before irreversible work begins:

- Title: `Permanently delete archive “{archiveName}”?`
- Body: `This permanently deletes this research archive. This action cannot be undone.` Add a concise factual scope sentence if the archive contains or references separately managed data.
- Mac horizontal order: `Cancel` leading, `Delete Archive` trailing. Cancel has cancellation semantics and never deletes. Delete Archive commits only the identified archive.
- Default: none, so an unfocused Return does nothing. This is a deliberate-reading product choice allowed by the guidance, not a universal prohibition on destructive defaults. Cancel is not default. Explicit focus plus activation can choose either button.
- For explicitly requested deletion, a normal Delete Archive button is permitted; the alert-specific exception allows a normal default that Return confirms. This specification chooses no default. If deletion is an unexpected consequence of another action, explain that consequence and use destructive styling. Do not infer prior intent from button color. [Alerts: Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons).
- Cancel, Escape, and Command-Period dismiss without mutation and return to the archive context. Outside clicks never confirm deletion. Keep a visible Cancel regardless of keyboard support.
- No routine caution symbol, suppression checkbox, text field, or Help control is needed for this confirmation. These are product choices; Mac supports optional accessories. Reserve a caution symbol for exceptional attention such as unexpected loss. [Alerts: macOS](https://developer.apple.com/design/human-interface-guidelines/alerts#macOS).

For sync failure, use an in-context `Sync failed` state with a verified cause when known and a `Retry Sync` action. Do not claim `Saved on this Mac` unless local persistence has actually succeeded. Retry starts sync, and only confirmed remote completion changes status to `Synced`. Immediate blocking treatment depends on consequences absent from the brief; lack of connectivity alone does not establish urgency. [Feedback: Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices).

## Worked before/after

Example archive name `Field Notes` is illustrative.

**Before:** A successful save opens an alert defaulting to Cancel. While it remains visible, a sync error opens another alert. Deleting an archive produces `Error` / `Something happened` / `Yes` / `No`.

**After:** A completed save updates nearby status to `Saved`. A sync failure adds `Sync failed` and `Retry Sync`, without covering any confirmation. Choosing deletion opens `Permanently delete archive “Field Notes”?` with the body above and `Cancel` / `Delete Archive`, neither default. Return alone leaves the archive intact. Escape closes the confirmation with no mutation. Reopening and explicitly activating Delete Archive starts one deletion of Field Notes. Confirmed success removes it from the archive view; failure reports the known result rather than claiming success or promising restoration. Any still-relevant sync issue remains in context.

## Framework-agnostic state contract

The concurrency and target-validation details below are engineering recommendations, not additional HIG rules.

```text
state = idle | confirming(targetId, version) | deleting(operationId, targetId)
activeAlert = none | oneAlert

on saveSucceeded(confirmedPersistenceScope):
    update nearby save status truthfully; do not open alert

on requestDelete(target):
    if state != idle: ignore duplicate request
    capture stable target ID, displayed name, and version
    state = confirming(target.id, target.version)
    present one confirmation with no default

on Cancel or Escape or CommandPeriod while confirming:
    dismiss confirmation; state = idle; restore archive context
    run no delete operation

on Return while confirming and no button explicitly targeted:
    do nothing

on explicit DeleteArchive activation while confirming:
    validate target identity/version and actual deletion scope
    if validation fails:
        close confirmation; state = idle
        explain changed target; require a new request/confirmation
    else:
        dismiss confirmation before showing any other alert
        state = deleting(new operationId, targetId)
        initiate exactly one deletion; prevent duplicate submission

on deleteResult(operationId, result):
    ignore stale/duplicate callbacks
    reconcile actual archive state; state = idle
    if success: update archive view; choose a remaining context target
    if failure: show truthful failure and recovery supported by storage
    if outcome unknown: reconcile before enabling retry; do not claim success

on syncFailure(issue):
    retain latest relevant issue; update in-context sync status
    never open an alert over an active alert
    if consequences truly require an urgent decision:
        queue/coalesce issue; after active alert closes, revalidate and
        present at most one relevant alert, preserving archive task state
```

Deletion cannot be cancelled after irreversible commitment unless the storage contract explicitly supports it; do not leave a misleading Cancel control during that phase. Preserve the current selection on cancellation, and return to an available archive context after successful deletion. Actual focus behavior remains unverified.

## Acceptance checks and status

**Passed — document inspection:** macOS scope identified; all supplied controls inventoried (deletion Yes/No and save Cancel); root, selected families, topic procedures, then supporting guides read from the installed package. Corrected specification supplies exact copy, roles, ordering, default, triggers, exits, and outcomes.

**Failed — supplied specification:** meaningful deletion title/body/action labels; no stacked alerts; routine-save interruption policy; completed-save default label. These are static failures established by `interface.md`.

**Not executed — implementation acceptance:**

1. Open deletion for archive A. Verify displayed target and scope. Return without explicit targeting performs no deletion; Cancel, Escape, and Command-Period each preserve A and restore its context.
2. Explicitly activate Delete Archive. Verify exactly one operation for A, truthful pending/result states, and no mutation of B. Change A or its scope before activation; require renewed confirmation.
3. Inject save success, delayed save, and failed save. Only confirmed persistence may show Saved; none generates a routine success alert. Sync success/failure remains separately truthful.
4. Inject sync failure while confirmation is open, including repeated failures. Alert count never exceeds one; confirmation remains actionable; later feedback is coalesced, relevant, and recoverable without reopening obsolete dialogs.
5. Exercise deletion failure, ambiguous outcome, duplicate activation, and stale callbacks. No false success or unsafe blind retry; reconcile actual storage state first.
6. On the eventual Mac interface, inspect button names, ordering, keyboard targeting, focus restoration, increased text sizes and long archive names for clipping or overlap. Verify assistive-technology operation separately; these checks have not run.

## Evidence limits and source trail

Only `interface.md` and installed instructions/guides were used; no web access. Official links above identify the articles behind the local guidance, not live-verified pages. The local references identify their snapshot as 2026-10-25.

Installed package root: `.agents/skills/apple-hig/`. Read `SKILL.md`, searched `references/topic-index.md`, and followed these routes before their source guides:

- Presentation family → `.topics/apple-hig-alerts/SKILL.md` → `references/alerts.md`.
- Menus and actions family → `.topics/apple-hig-buttons/SKILL.md` → `references/buttons.md`.
- Patterns family → `.topics/apple-hig-modality/SKILL.md` and `.topics/apple-hig-feedback/SKILL.md` → their respective references.

No screenshot, app source, storage contract, handler execution, GUI, Apple device, SDK compilation, accessibility execution, target geometry, visual styling, or enlarged-text rendering was available. The proposed state model is unexecuted pseudocode. Platform facts and the deliberate-destruction default exception come from the installed snapshot; product choices and engineering recommendations are identified above. The supplied evidence does not establish deletion's current default, prior intent, exact data scope, actual sync urgency, or whether deletion succeeds.
