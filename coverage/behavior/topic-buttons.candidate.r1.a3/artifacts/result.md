# iPad field-report editor: export-control correction plan

This is a review and framework-agnostic behavior specification, not an implementation. Preserve Publish, Preview, Save Draft, and Delete. Fix accidental destruction and duplicate publishing first, then target access, naming, and visual hierarchy. All verified findings below come from `interface.md`; none were observed in a running app.

## Ranked verified findings

| Rank | Verified condition and effect | Decision and source |
| --- | --- | --- |
| 1 — Critical | Delete is the primary/default action in an editor. Default activation risks unintended data loss. Actual deletion and recovery semantics are unspecified. | Remove Delete's primary/default role. Use a destructive role and explicit activation. The normal editor's likely nondestructive action is the default candidate. This follows [Buttons: Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role); it is not a claim that destruction can never be default in a deliberate-deletion alert. |
| 2 — High | During the eight-second Publish upload, nothing changes and repeated taps create duplicate uploads. People cannot tell whether activation registered and can publish more than intended. | Immediately show activity inside Publish and prevent another operation for the same report revision. Define success and recovery explicitly. In-button activity is supported by [Buttons: iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS). Duplicate protection and the recovery model below are product engineering decisions, not a claimed HIG network protocol. |
| 3 — High | Every actual hit region is 20×20 pt with 2 pt gaps. All four actions are difficult to select accurately; proximity to Delete increases consequence. | Give each target at least 44×44 pt and nonoverlapping hit regions. The local guide says general hit regions should be at least 44×44 pt and calls for sufficient separation ([Buttons: Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices)). Use an initial 8 pt gap and a distinct gap before Delete as product choices; the source supplies no fixed iPad gap minimum. |
| 4 — High | Glyph-only Preview has no accessible name. Its action cannot be identified through that name. | Prefer visible “Preview” and accessible name “Preview”; if retaining a glyph, still provide that name. The installed Buttons procedure explicitly requires an action name for an icon-only button. Short action labels follow [Buttons: Content](https://developer.apple.com/design/human-interface-guidelines/buttons#Content). Actual assistive-technology behavior remains untested. |
| 5 — Medium | Four equally prominent filled buttons provide no useful hierarchy. | Make Publish the sole prominent action; use lower-emphasis Preview and Save Draft, and a separated lower-emphasis destructive Delete. Prefer one or two prominent likely actions, and use style rather than unequal peer sizes ([Buttons: Style](https://developer.apple.com/design/human-interface-guidelines/buttons#Style)). Choosing Publish as most likely is a proposed product decision, not evidence about usage frequency. |

## Corrected action contract

All four are commands, not persistent selections; retain buttons. Use the existing framework's suitable semantic controls when available, otherwise implement the specified roles, names, focus, disabled states, and perceptible press feedback. No Apple SDK is required by this plan. Custom press feedback follows [Buttons: Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices).

| Control and accessible name | Outcome and affected object | Role, placement, and availability |
| --- | --- | --- |
| Publish | Publish a captured revision of the current report; completion requires authoritative confirmation. | Primary, filled, at the end of the routine-action group. Enabled only for a publishable revision with no unresolved publication operation. It is the sole default candidate in the editor, but Return in a text field must continue editing rather than publish. |
| Preview | Open a read-only preview of the current report; closing restores editor state and focus to Preview. | Normal, lower emphasis, text label preferred. Remains available during upload; distinguish current edits from the revision being uploaded. |
| Save Draft | Persist the current report as a draft without publishing; report success only after persistence succeeds. | Normal, lower emphasis. Remains available during upload. A failed save retains edits and offers retry; do not imply Publish has saved newer edits. |
| Delete | Delete the current report through an explicit destructive path. | Destructive, lower emphasis and spatially separated; never the editor default. Disabled while publication is pending or its outcome is unknown, with the reason “Resolve publishing before deleting this report.” |

Use equal peer target heights of at least 44 pt and widths of at least 44 pt, enlarged for labels. Keep all four discoverable. Reflow into two rows when available width, enlarged text, or localization requires it; do not shrink targets or clip labels to preserve one row. Color alone must not convey Delete's consequence: retain its text and semantic destructive role.

Deletion reversibility is unknown. Before implementation, establish what Delete removes, whether published content is affected, and whether restoration is reliable. If reliably reversible, provide a clear Undo/recovery path restoring the affected report. If irreversible, specify an explicit confirmation naming the report and loss before committing, with a safe exit that changes nothing and restores focus. This is a provisional product safeguard, not a verified alert-specific HIG prescription. Exact alert ordering/default behavior needs the missing Alerts procedure and recovery requirements; never transfer the editor's default mapping blindly into that surface.

## Slow-upload state contract

Keep the initiating button in place and its dimensions stable. On activation, synchronously guard the operation before starting network work; render an activity indicator inside Publish, replacing any image, with “Publishing…” as the visible label and accessible name. Expose busy/unavailable state and an accessible status update without moving focus. Do not show a fabricated percentage for an eight-second wait. The local Buttons guide supports contextual in-button activity and optionally changing its label; the status announcement and guard are proposed implementation contracts.

```text
on Publish(report, revision):
    if revision is not publishable: explain validation; return
    atomically:
        if operation exists for (report.id, revision.id): return
        persist operation with stable idempotency key and captured revision
        state = publishing
    render Publish(activity, "Publishing…", unavailable)
    send captured revision using operation.key

on confirmedSuccess(operation, publicationReceipt):
    state = published
    record receipt and published revision
    remove activity; show "Published" status
    prevent republishing that unchanged revision
    if newer edits exist: explain "Published revision X; newer edits remain"
    enable Publish only for a new publishable revision

on confirmedFailure(operation, reason):
    state = failed
    remove activity; retain report and edits
    show actionable failure and "Retry Publish"
    enable retry only when no operation remains in flight

on timeout / lost response / interrupted connection:
    state = outcomeUnknown
    remove activity when no request is actively waiting
    show "Publication status unknown" and "Check Status"
    reconcile operation.key with the service before a new publication
    retry the same logical operation only with deduplication guarantees
```

The service should enforce one publication result per stable operation key, including retries after lost responses and process restarts. Client tap suppression alone cannot guarantee that. If service reconciliation/idempotency is unavailable, keep an unknown result unresolved and explain recovery rather than launching another blind upload. Retry must preserve the captured revision; publishing newer edits is a separate operation. A new key must not be generated just because a response was lost.

No cancel button is specified because upload cancellation capabilities are unknown. Preview and Save Draft remain usable; do not block the whole editor for this upload. Preserve local changes on every failure path. Persistence, service guarantees, and concurrent-edit behavior are requirements to implement and verify, not supplied capabilities.

## Worked before/after

**Before:** A field worker taps Publish at t=0. Four filled controls remain unchanged. At t=1 and t=2 they tap again because there is no feedback. The brief says those taps create duplicate uploads. Delete remains the default throughout.

**After:** At t=0 the first tap acquires the operation guard and Publish shows an in-button indicator with “Publishing…”. Taps at t=1 and t=2 do nothing; the transport receives one logical operation. Preview and Save Draft remain available; Delete explains its temporary unavailability. At t=8 a confirmed receipt changes the status to “Published”, records the revision, and removes the indicator. The same revision cannot be published again accidentally. If the response is lost instead, “Publication status unknown” offers Check Status; reconciliation finds the existing result without creating another publication. If the service confirms rejection, preserve the draft and offer Retry Publish with an actionable reason. These timings illustrate the supplied eight-second case; they are not a measured execution.

## Acceptance checks and current status

**Passed by static inspection:** The specification preserves all four functions; assigns labels, roles, outcomes, geometry, and pending/resolved behavior; and includes unknown-outcome recovery. The source brief explicitly establishes each ranked condition. The installed Buttons procedure and supporting guide were read.

**Failed in the supplied design description:** Safe editor default; duplicate prevention; upload feedback; minimum target dimensions; accessible Preview naming; meaningful prominence hierarchy. “Failed” here means contradicted by the brief, not a runtime test failure.

**Not executed — implementation acceptance checks:**

1. At normal and enlarged text sizes, and narrow iPad editor widths, inspect actual hit geometry: each target is at least 44×44 pt, targets do not overlap, labels remain legible, and all four functions remain discoverable. Evaluate whether chosen gaps are comfortable on a device.
2. Confirm each command reaches its named outcome. Preview dismissal preserves edits and returns focus. Save Draft does not publish. Delete requires explicit activation, respects the selected recovery policy, and restores the correct report through Undo if offered.
3. Verify keyboard focus and activation mappings, including Return in editor text and on focused controls. Unfocused/default activation must never invoke Delete. Verify perceptible pressed and disabled states.
4. With an eight-second simulated upload, rapid touch, keyboard, and programmatic activation produce one logical operation and one publication. Activity and busy status appear at initiation and clear only on a defined transition.
5. Exercise success, rejection, lost response after server commit, disconnection, restart, and retry. Verify stable operation identity, reconciliation, revision capture, no data loss, and no duplicate service result. Check that newer edits are never represented as already published.
6. Inspect the accessibility tree and execute assistive-technology checks on an appropriate environment: Preview has its name, controls expose roles and availability, status updates are perceivable without focus theft, and reading/focus order follows the layout.

## Evidence and routing limits

Only local files and installed instructions were used; no web browsing occurred. Official links above identify sources from the local snapshot, not pages verified online. No rendered app, implementation, transport, service, device, SDK, GUI, or accessibility execution was supplied or performed. Actual deletion scope, undo support, save durability, input mappings, contrast, focus order, rendered geometry, and network guarantees remain unknown.

Read order used the installed package at `.agents/skills/apple-hig/`: root `SKILL.md`; Menus and actions family; its `.topics/apple-hig-buttons/SKILL.md`; then its `references/buttons.md`. The Status family routed to `.topics/apple-hig-progress-indicators/SKILL.md`, and Presentation routed to `.topics/apple-hig-alerts/SKILL.md`; both procedure files were absent at those installed paths. A package file search and `references/topic-index.md` supplied no alternate procedure path. Their supporting source guides were deliberately not substituted for the missing prerequisite procedures. Slow-upload recommendations therefore use the available Buttons iPadOS guidance; deletion confirmation remains conditional and no progress- or alert-specific compliance is claimed. Reading the missing procedures and validating the implemented behavior are outstanding evidence tasks, not completed checks.
