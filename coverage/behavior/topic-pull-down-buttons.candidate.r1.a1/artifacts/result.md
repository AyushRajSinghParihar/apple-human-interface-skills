# Selected report: revised interaction specification

## Scope and decisions

Input: `interface.md` describes an iPadOS chooser that displays the last command as state, mixes Share/Duplicate/Delete with theme settings, executes its first item on opening, and sometimes has no selected report. These are supplied observations, not runtime findings. No implementation or report data was supplied.

Replace the chooser with an ordinary **Report Actions** pull-down. Its label stays constant after every command; opening only reveals commands. No command is checked, selected as a stored value, or executed by opening. Use a text list rather than icon-only actions. Three related report commands justify this reveal step. Keep viewing/selecting the report directly available in the main content; do not move the report's main task into the menu. The brief does not establish whether Share is primary: retain any existing direct Share entry point, and use the standard Share button for that route.

This follows [Pull-down buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons#Best-practices) and [Menus — Labels and Organization](https://developer.apple.com/design/human-interface-guidelines/menus#Labels). Ordering below is a product decision; usage frequency was not supplied.

| Order | Item | Role and outcome | Enabled when |
| --- | --- | --- | --- |
| 1 | Share… | Requires a destination; close menu and initiate sharing for the captured report | Exactly one existing report is selected and shareable; no report operation is pending |
| 2 | Duplicate | Immediate command; create one independent copy, preserve original | Exactly one existing report is selected and duplication is permitted; no operation is pending |
| separator | | Separate destruction from ordinary work | |
| 3 | Delete… | Destructive; close menu and request intent confirmation for the captured report | Exactly one existing report is selected and deletion is permitted; no operation is pending |

All three remain visible, dimmed and nonactivatable when unavailable. The parent remains openable even when all are disabled. With no selection, show nearby text **Select a report to use report actions.** Never fall back to the first, previously selected, or last modified report. Zero or multiple selections cannot enable a single-report command. This applies the ordinary-menu availability guidance in [Menus — Labels](https://developer.apple.com/design/human-interface-guidelines/menus#Labels).

Move theme settings to a separate, labeled **Theme** single-choice control in appearance settings. Preserve the existing theme options and stored value; their names, default and storage scope are not provided. Show the actual stored theme as the control value, mark only that option, commit an explicitly chosen option, and leave it unchanged on dismissal. Rechoosing the same value is idempotent; external theme changes update its displayed value. Theme stays usable without a report. Never put report commands in this value list. A compact pop-up is appropriate if the existing options form a flat mutually exclusive set; otherwise retain an appropriate separate settings control. See [Pop-up buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons#Best-practices).

## Command and presentation contract

**Scope:** Show the selected report's title in the surrounding report header. On opening, capture its stable ID and revision. If selection or eligibility changes while the menu is open, close it and require a fresh opening. Revalidate the captured ID, revision and permission on activation and immediately before mutation. Never retarget a pending command to the current selection. A stale or missing report yields an inline explanation and no mutation.

**Share:** Capture the report's current saved content as a read-only share payload with its title and supported content type. Do not invent a public link or change access permissions. Close the action menu before opening the platform sharing surface through a host adapter. Offer compatible destinations only; do not duplicate built-in actions or claim control over system ordering. Canceling sharing changes neither report nor selection. Preserve the snapshot until sharing ends. Payload format and host sharing capability require implementation verification; this specification does not assume an Apple SDK. See [Activity views — Best practices](https://developer.apple.com/design/human-interface-guidelines/activity-views#Best-practices).

**Duplicate:** Use an idempotent operation token to create exactly one new report with a new ID and a distinguishable title such as “Quarterly Review Copy” (uniqueness suffix as needed). After success, select and display the copy. On failure, keep the original selected and show an inline error with an explicit retry. These naming/selection choices are product decisions.

**Delete:** After choosing Delete…, replace the menu with a confirmation popover anchored to Report Actions in a wide iPad layout. Do not cascade it from an open menu. Title: **Delete “Quarterly Review”?** Substitute the captured report name. Offer **Delete Report** with destructive semantics first, then **Cancel**. The title identifies the object; do not claim permanent deletion or recoverability without backend evidence. No implicit default action; Return alone does not delete. Explicitly activating Delete Report revalidates and submits one deletion. Cancel, outside dismissal, Escape, system dismissal or changing selection performs no deletion. Dismissal restores focus to Report Actions when that control remains available.

The [pull-down-specific guidance](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons#Best-practices) explicitly calls for destructive intent confirmation using an iPadOS popover. General [Alerts — Best practices](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices) says common undoable deletion generally needs no confirmation, while [Popovers — Best practices](https://developer.apple.com/design/human-interface-guidelines/popovers#Best-practices) reserves warnings for alerts. Apply the component-specific confirmation here as a deliberate post-command choice, not a warning-only popover. Recovery is unknown, so do not waive confirmation on an assumed undo capability. Unexpected critical failures need a separately designed alert rather than relying on this transient surface.

In compact iPad windows, use an adapted action-sheet confirmation with the same named target, destructive action and safe cancellation; do not force a wide-layout popover into insufficient space. Keep one temporary surface at a time and preserve the source context where space permits. Fit content, allow long report names to wrap, and accommodate enlarged text without hiding choices. See [Popovers — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/popovers#iOS-iPadOS) and [Action sheets — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/action-sheets#iOS-iPadOS).

On successful deletion, clear selection if it still refers to the deleted report and show the empty-selection state. On failure, retain the report and selection, end pending state, and show an inline error; retry requires a fresh explicit command and confirmation. Do not optimistically erase the report or promise Undo without a supported recovery model.

## Framework-agnostic state model

```text
state = Closed | Menu(targetSnapshot?) | ConfirmDelete(target) | Pending(op, target)

openActions:
  state = Menu(snapshotOfSingleSelectionOrNull)
  render commands with current eligibility
  // no command dispatch, value update, or theme change

activate(command):
  require state is Menu and command is enabled
  target = captured snapshot
  require target still exists, matches selection/revision, and is eligible
  close menu
  if Delete: state = ConfirmDelete(target)
  if Share: prepare snapshot payload; open host sharing adapter
  if Duplicate: state = Pending(Duplicate, target); submitOnce(token, target)

confirmDelete:
  require state is ConfirmDelete
  revalidate captured target and permission
  state = Pending(Delete, target); submitOnce(token, target)

dismissMenuOrConfirmation:
  state = Closed; restore trigger focus; mutate nothing

selectionOrEligibilityChanges:
  close Menu or ConfirmDelete; require fresh invocation
  // Pending keeps its original target; selection never redirects a request

operationCompletes:
  apply outcome only to captured target; clear pending state
  apply command-specific selection outcome; show inline failure if needed
```

The host must support ordinary menu touch activation and keyboard navigation: opening focuses a navigable item without executing it; only explicit activation invokes an enabled item. Escape dismisses. Disabled entries never dispatch. Repeated trigger activation toggles the menu without executing a command. During pending operations disable report commands to prevent duplicate submissions. These are acceptance requirements, not evidence of keyboard or assistive-technology behavior.

## Worked before/after

**Before, as described:** With “Quarterly Review” selected, opening the chooser executes its first item. Choosing Duplicate makes “Duplicate” look like a persistent value. Theme options occupy the same list. With no report selected, target behavior is unspecified.

**After:** The header shows “Quarterly Review”; the trigger reads Report Actions. Opening reveals Share…, Duplicate, a separator, and Delete… with zero side effects. Choosing Duplicate creates one copy and displays it; the trigger still reads Report Actions. Reopening and choosing Delete… names that copy in a separate confirmation; Cancel leaves both reports intact. Clearing selection leaves the menu openable with all three commands dimmed and the selection prompt visible. Choosing Theme elsewhere changes only the stored appearance choice.

## Acceptance checks and evidence limits

**Passed — static specification inspection:** command/state separation, stable trigger label, three scoped commands, independent theme value, no-selection handling, explicit destructive confirmation and cancellation, captured-target checks, pending/error transitions, and wide/compact presentation contracts are all specified above. Root, family and topic procedures were read before their supporting guides from the installed package. Only local files were used; links identify source articles and were not fetched.

**Failed — supplied design against this contract:** opening executes a command; last command is displayed as state; theme settings share the report-command list. These failures come solely from the supplied prose. The no-selection condition exposes a missing contract, not proof of a wrong-target execution.

**Not executed — implementation acceptance:**

- Open/dismiss/reopen, including repeated trigger activation: zero report mutations and zero theme changes.
- Select each enabled item: correct captured report, exactly one outcome; disabled items and all-disabled menu dispatch nothing.
- Change selection, remove the report or revoke permissions during menu/confirmation: close or reject safely; no command reaches a replacement report.
- Duplicate twice through two deliberate invocations: two separate copies; repeated delivery of one token: one copy. Failure preserves the original.
- Delete then cancel through every supported exit: no deletion. Confirm: only named report removed; failed deletion leaves it available.
- Share uses actual selected content; cancellation preserves data; unsupported destinations are excluded and preparation failure does not open an empty sharing surface.
- Theme reflects persisted state after selection, dismissal, reopening, repeated selection and external updates; empty report selection has no effect on theme eligibility.
- Long/localized labels, enlarged text, narrow windows and layout changes preserve readable labels, reachable choices and correct anchoring without stacked popovers.
- Touch, pointer and keyboard open/select/dismiss behavior, focus restoration, disabled semantics and assistive-technology announcements match the contract on the target host.

No device, GUI, SDK compilation, host sharing integration, native menu rendering, accessibility execution, backend recovery or physical interaction was tested. The local guidance is a dated snapshot (2026-10-25), not an SDK reference or proof of current platform behavior. Theme inventory, report format, permissions and recovery remain integration facts to establish before implementation can pass these checks.
