# Invitation and access repair

Patched `interface.md` in place, replacing the original one-line problem statement with a concrete authorization, invitation, management, and offline recovery contract. iPadOS is primary; the supplied macOS scope is preserved.

## Decisions and patch summary

- Separate Collaborate from Send a Copy. Default to invited people with Viewer access; forwarding a link grants nothing. Explain copy permanence.
- Define owner/editor/viewer capabilities and server enforcement across every command path.
- Separate invitation lifecycle, effective role, and presence; pending invitees cannot appear active.
- Confirm permission changes through the server, reconcile uncertainty, and refresh open windows. Access loss clears shared surfaces while preserving unsynced personal writing privately.
- Revalidate before offline replay; preserve both versions and require explicit review for conflicts.
- Specify iPad/Mac sharing distinctions, command progress, confirmation copy, cancellation, and dismissal behavior.

The [Collaboration and sharing guidance](https://developer.apple.com/design/human-interface-guidelines/collaboration-and-sharing#Best-practices) supports explicit permissions, copy/access separation, and persistent management. [Privacy guidance](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices) supports precise exposure. The exact defaults, role matrix, expiry, and recovery algorithm are product decisions; article links for controls and presentation appear in the patched specification.

## Worked before/after

Before: Morgan shares a link and Alex silently gains edit access. Alex appears active before accepting, can delete writing despite a viewer label, and continues seeing access after revocation. Offline changes have no defined recovery.

After: Morgan sees “Only invited people · Can view · Only owner can invite,” selects Alex as Viewer, and sends. After server confirmation, Alex appears under Pending Invitations as “Invited · Can view.” Only explicit acceptance by the bound account creates Viewer membership. Delete commands are unavailable and direct mutation requests fail. Morgan confirms Remove Access; the UI says “Removing access…” until acknowledgment. Alex's connected windows clear shared content and show “Your access was removed.” If Alex had previously been an editor with offline writing, reconnect checks access first and preserves that writing privately without replay. If still authorized but revisions differ, both versions survive for merge review.

## Acceptance checks

Passed — static specification review only:

- All five supplied failures map to explicit replacement behavior.
- Recipient scope, snapshot payload, invitation acceptance/expiry/cancel, persistent management, and object-specific links are defined.
- Pending, success, failure, uncertain completion, retry, cancellation, dismissal, reconnect, and permission races have defined outcomes.
- Platform distinctions and source links are explicit.

Failed: no outstanding specification check identified. This is not an implementation pass.

Not executed — implementation acceptance scenarios:

| Scenario | Required outcome |
| --- | --- |
| Forward link to uninvited/wrong account | No grant/content; account switch or access request route. |
| Viewer deletes via UI, keyboard, or direct request | No mutation; role explanation and server denial. |
| Open pending invitation without accepting | No membership or active presence count. |
| Accept twice or after expiry/cancel/replacement | At most one valid membership; invalid tokens grant nothing. |
| Send times out then retries | Reconciliation prevents duplicate invitations. |
| Revoke/downgrade while editing in two windows | Role refreshes, unauthorized writes fail, unsynced writing stays private. |
| Revocation fails | Last confirmed state remains; no false success. |
| Revoke during offline editing | Cached access is unverified; reconnect blocks replay and clears shared cache. |
| Concurrent edits and repeated merge conflict | Both versions survive; publication checks latest revision. |
| Copy, sharing cancellation, link disabling | Independent clean snapshot; cancellation grants nothing; invalid links fail while accepted membership remains. |
| Dismiss/reopen, compact layout, alert keyboard cancellation | Draft retention, single presentation, and no mutation on Cancel. |
| Device/assistive checks | Verify names, focus, enlarged labels, target geometry, status announcements, and native sharing/presentation. |

## Route audit and evidence limits

Explicitly read the installed `.agents/skills/apple-hig/SKILL.md` from disk, then searched its topic index. Read owning family, topic procedure, and supporting reference in order for Patterns → Collaboration and sharing; Menus and actions → Activity views and Buttons; Foundations → Privacy; Presentation → Alerts, Popovers, and Sheets. Every file read used a separate `cat` command with a path resolved beneath the installed package. No web browsing occurred; official links come from the local 2026-10-25 snapshot.

Evidence consists of the original `interface.md` and installed instructions. No app code, backend, screenshot, executable prototype, SDK configuration, or minimum deployment version was supplied. No live invitations were sent or permissions changed. No device, SDK build, GUI, accessibility execution, measured target geometry, delivery test, or backend authorization test was performed. This repairs the specification; runtime acceptance remains pending implementation and execution.
