# Invitation and access repair

Patched interface.md in place, replacing the short defect statement with an implementable specification for iPadOS and consistent macOS access semantics.

## Decisions and changes

- Split Collaborate from Send a Copy; describe payloads, cancellation, background work and platform presentation boundaries.
- Replace silent public editing with identity-bound, invited-only access and Viewer as the invitation default. Define Owner, Editor and Viewer permissions with service enforcement across every command path.
- Separate Invitations from accepted participants and presence. Define accept, decline, expiry, resend, cancellation, failures and acknowledgement loss.
- Keep Collaboration management available after sharing. Report removal and role changes only after acknowledgement; revalidate old links and stale clients.
- Preserve unsynced contributions locally, label unverified offline access honestly, and require permission/revision checks before upload. Conflicts require review rather than silent overwrite.

The least-access default, invitation lifecycle, operation IDs, recovery model and conflict algorithm are product decisions. HIG supports explicit permission choices and management but does not prescribe this backend or role taxonomy.

## Worked before/after

Before, an owner sends a link to Maya. It silently grants Editor access to anyone who receives it. Maya appears active before joining. A Viewer can delete writing. After removal, Maya’s UI continues claiming access, and reconnecting offline edits may overwrite other writing.

After, the owner chooses Collaborate, sees “Only invited people” and explicitly invites Maya as Viewer. Maya appears under Invitations. Forwarding the link to Leo grants Leo nothing. Maya signs in as the invited identity and accepts; only acknowledged acceptance moves her to accepted participants, labeled Viewer. Delete commands are unavailable and direct mutation requests are denied. The owner may explicitly promote her to Editor. If she writes offline, the app says “Saved on this iPad — not shared.” If removal commits before reconnect, authorization fails and only her unsynced contributions remain in a local recovery draft; no upload occurs. If she remains Editor but another writer changed the base revision, reconnect opens review and preserves both versions. Closing review does not discard her work.

## Acceptance checks

Static specification review — passed:

| Check | Evidence in interface.md |
| --- | --- |
| No access broader than described | Invited-only summary, identity-bound links and authoritative role table. |
| Copy cannot be mistaken for shared access | Separate operation, snapshot payload, no sync/credentials and explicit recall limit. |
| Pending is not accepted or online | Separate Invitations section and acknowledgement-based acceptance. |
| Viewer destructive paths are blocked | All input paths and direct requests subject to service permissions. |
| Management remains reachable | Persistent Collaboration entry with owner actions and failure/retry states. |
| Revocation has honest pending/success/failure states | Removing label, server acknowledgement, stale-link denial and client revalidation. |
| Offline uncertainty and conflicts are represented | Last verification time, local save labels, permission-first reconnect and conditional revision review. |
| Recipient and update destinations are concrete | Invitation/project/passage routing with authorization and unavailable fallbacks. |
| Sharing dismissal/cancellation is defined | Dismissal does not establish acceptance/delivery; continuation remains visible. |

Runtime acceptance scenarios — not executed; required for implementation:

1. Invite Viewer, forward link to another identity, attempt acceptance under wrong account: no content disclosure or grant; correct identity can accept once. Repeat after expiry, decline, cancellation and resend; invalidated tokens fail.
2. As Viewer, attempt deletion through touch, keyboard, menu, drag/drop and direct service calls; all shared mutations fail without changing text. Repeat a stale Editor request after downgrade.
3. Drop the connection after acceptance/removal commits but before acknowledgement; retry/reopen reconciles one operation and accurately reflects membership.
4. Remove an online Editor, then reuse old invitation/project/update links and stale write requests: no renewed access. Verify cache removal and recovery contains only unsynced personal contributions.
5. Remove an offline Editor, then reconnect: no queued upload; local writing survives. Repeat without removal and with a changed server revision: review preserves both versions; a second concurrent edit prevents stale application.
6. Cancel sharing, fail export, dismiss during background work and use unsupported destinations: no false delivery/acceptance status; task context and recovery remain available.
7. On iPad and Mac, verify actual system sharing presentation, management availability, keyboard behavior, readable states and assistive-technology navigation with the chosen framework.

Failed checks: none identified in the static specification review. Runtime checks are unexecuted, not passes.

## Guidance and evidence limits

Read the installed apple-hig root SKILL.md explicitly, then Patterns family → Collaboration and sharing topic procedure → its source guide. Followed its routes through Foundations → Privacy procedure → Privacy guide and Menus and actions → Activity views procedure → Activity views guide. Each file was read individually by cat from this installed package. Sources were local snapshots; no web browsing occurred.

Material support: [Collaboration and sharing, Best practices](https://developer.apple.com/design/human-interface-guidelines/collaboration-and-sharing#Best-practices) for copy/access distinction, permission summaries and persistent management; [Activity views](https://developer.apple.com/design/human-interface-guidelines/activity-views) for contextual sharing and Mac surface limits; [Privacy, Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices) for precise access and data minimization. Links identify official sources; they were not fetched or independently verified.

Only the supplied one-paragraph interface brief and installed guidance were available. No app, backend, screenshot, framework, identity implementation or OS deployment target was supplied. No invitation was sent and no live permission was changed. No device, SDK build, GUI, accessibility, network or security execution was performed. System integration, token enforcement, cache isolation, recovery extraction, revision handling and assistive-technology behavior require implementation evidence. Existing copies and information already viewed cannot be recalled, and offline devices cannot immediately observe remote revocation. This specification does not certify security, accessibility or SDK availability.
