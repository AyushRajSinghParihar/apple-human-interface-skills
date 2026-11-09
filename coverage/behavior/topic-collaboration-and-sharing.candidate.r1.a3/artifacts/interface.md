# Shared writing project: invitations and access

Platform: iPadOS first, with the same access semantics on macOS. This specification replaces silent link grants, viewer mutations, misleading invitation status, stale revocation claims, and unspecified offline conflicts. No framework or backend is supplied.

## Authorization model

The server owns project identity, membership, invitation lifecycle, permission version, and content revision. Authorize every read, write, invitation acceptance, and queued replay. UI restrictions supplement server enforcement. Use idempotency keys for mutations; permission changes and writes carry their expected permission/content versions. Reject stale operations and return current permitted state rather than silently broadening access.

| Role | Read | Edit text/delete sections | Invite/change roles/revoke | Delete project |
| --- | --- | --- | --- | --- |
| Owner (one) | Yes | Yes | Yes | Yes |
| Editor | Yes | Yes | No | No |
| Viewer | Yes | No | No | No |
| Pending/declined/expired/revoked/nonmember | No | No | No | No |

Owner transfer is outside scope; the owner cannot remove themselves. Viewers see “View Only” and “Only editors can change this project.” Remove editing actions from their editing surfaces; disable remaining standard commands with that explanation. Enforce the same restrictions for keyboard commands, context actions, drag/drop, and direct requests.

## Share versus copy

Use standard Share in the document toolbar with distinct **Collaborate** and **Send a Copy** modes and supported system sharing presentation. Default collaboration to **Only invited people · Can view · Only owner can invite**. Show the full summary before sending or copying a link. This revision supports invited-account access only; do not offer “Anyone with the link.”

The owner selects a recipient and Viewer or Editor before **Send Invitation**. Draft changes grant nothing. Editors/viewers can copy a restricted URL but cannot create invitations. Explain “Only invited people can open this link.” Forwarding a URL never grants membership or changes its bound recipient.

Links resolve to the exact project/invitation after sign-in and fresh authorization. Validate the account and invitation before exposing project title, inviter, and offered role. A wrong account sees “This invitation is for a different account” and **Switch Account**. An unauthorized link shows “You don’t have access,” **Request Access**, and **Back to Projects**, without content or participant details. Requests notify the owner without granting access. Updates link to the relevant project view rather than a generic home screen.

**Send a Copy** exports the currently authorized, synchronized revision as a UTF-8 text file. Show its revision time before handoff. Exclude participant identities, invitation tokens, comments, and history. If writing is unsynced, disable this export and say “Sync changes before sending a copy.” The snapshot is independent and carries no ongoing access grant. Explain that revocation cannot recall copies. Canceling sharing creates no new grant and leaves existing membership unchanged. Include only relevant activities, avoid duplicate system actions, and do not prescribe system destination ordering.

## Invitation lifecycle

Track invitation status separately from effective role and online presence. Presence is online/away/unknown and never establishes membership. Invitations expire seven days after server creation, a product choice.

| Event | State and visible result |
| --- | --- |
| Send requested | Sending; show “Sending…” in the activating button and prevent duplicates. No member yet. |
| Server confirms creation | Pending Invitations row: name, “Invited · Can view/edit,” expiry date; owner can Resend Invitation or Cancel Invitation. Destination handoff does not prove delivery. |
| Send fails/times out | “Invitation not confirmed” and Retry; preserve recipient/role draft and reconcile the idempotency key before retry. |
| Valid recipient opens | Show offered role with Accept Invitation and Decline. Signing in does not accept. |
| Accept succeeds | Atomically validate recipient, expiry, cancellation, and current offered role; create membership once, move row to Members, and open project. Report presence independently. |
| Accept fails | No membership. Explain expired/canceled/unavailable state with Request New Invitation or Retry as applicable. |
| Decline/expiry/owner cancellation | No access; corresponding status appears in owner invitation history. |

Resend creates a new token and invalidates the previous one. Changing a pending invitation's role creates a replacement invitation and invalidates the old token, so an old link cannot accept an obsolete edit grant. Pending invitees never appear in active avatar counts or “editing now.”

## Management and revocation

After sharing starts, show Collaboration prominently next to Share. Separate Members, Pending Invitations, and invitation history. Put participants/communication at the top, essential recent project activity in the middle, and **Manage Access** at the bottom. Members can inspect their own role; the owner alone sees management controls and pending recipient addresses.

Owner commands: **Change to Viewer**, **Change to Editor**, **Remove Access**, **Cancel Invitation**, **Disable Existing Links**. Role changes identify the person and resulting role before submission. Disable Existing Links rotates link generation and invalidates outstanding invitation links while preserving accepted memberships; explain this distinction before confirmation. New invitations use new tokens.

Removal alert: “Remove Alex’s access?” Message: “Alex will no longer be able to open this shared project. Copies already sent can’t be recalled.” Actions: **Cancel** and **Remove Access**, using semantic removal styling and no Return default to require deliberate choice. This is a product choice; HIG permits a normal default for deliberately requested destruction. Escape or Command-Period cancels where supported. Cancel sends no request.

During submission show “Removing access…” or “Updating role…” and block duplicates. Label the last confirmed role as pending; never claim completion early. On acknowledgment show the new role or remove membership and record “Access removed.” On failure retain confirmed state, show “Access change not confirmed,” and offer Retry after reconciliation. Access changes require connectivity and are never queued offline.

Server revocation immediately rejects subsequent reads/writes. Push refreshes all open windows; foreground, reconnect, and permission errors also trigger revalidation. Downgrade stops editing and quarantines unsynced writing. Revocation stops sync, clears shared content/presence surfaces, and shows “Your access was removed” with Back to Projects. Preserve only the person's unsynced writing in a private recovery draft labeled “Not shared”; never replay it or automatically export the project after revocation. Previously exported copies remain outside revocation control.

## Offline and conflict recovery

Offline status reads “Offline · Access last checked [time].” Cached permission is unverified. Previously confirmed owners/editors can write into a local pending draft; viewers cannot. Show “Saved on this iPad · Not synced.” Invitation sending/acceptance, access management, and shared export wait for connectivity. Previously received cached content cannot be remotely erased while the device remains disconnected; clear its shared cache when revocation is learned.

Reconnect first revalidates authorization, then compares the draft's base revision. Revoked/downgraded users retain private recovery writing without publishing it. Authorized matching revisions submit once with idempotency keys; show “Synced” only after acknowledgment. If revisions differ, retain both and show “Changes need review.” Never silently overwrite using last-writer-wins.

Open a dedicated conflict workspace with base, latest shared text, and local changes. **Save Merged Version** submits the reviewed result against the latest revision; another concurrent edit returns to review without losing either draft. **Keep Private Draft** leaves shared text unchanged. Closing retains unresolved work. Do not mark synced while queued changes remain unresolved.

## Presentation and controls

Use system controls, short outcome labels, and text for roles/status. Give Share and Collaboration symbols matching accessible names. On iPad use separated button hit regions of at least 44 × 44 pt. Delayed commands show progress in the initiating button; inline errors offer Retry. Routine updates do not interrupt with alerts. A button animation or share dismissal never establishes server success.

In wide iPad layouts anchor Collaboration to its toolbar control and keep project context visible. Show one popover at a time, without cascades. Outside dismissal retains invitation drafts and confirmed changes; explicit Cancel discards only the unsubmitted draft. At compact widths use a scoped sheet with standard centered iPad sizing where appropriate, leading Cancel and trailing Send Invitation. Retain unfinished input across gesture dismissal so reopening resumes it; Cancel explicitly discards. Dismissing a submitted request does not cancel server work: reconcile status in Collaboration on reopening. Restore document selection on exit.

On macOS use supported toolbar/context-menu sharing and sharing popovers, not a claimed Mac activity-view component. Retain native control sizing and continuation ellipses where further input is required. Permission and sync semantics remain identical. No SDK integration is asserted.

## Basis and scope

Explicit collaboration/copy choices, concise permissions, persistent management, and project links apply [Collaboration and sharing — Best practices](https://developer.apple.com/design/human-interface-guidelines/collaboration-and-sharing#Best-practices). Sharing mechanics/platform distinctions follow [Activity views](https://developer.apple.com/design/human-interface-guidelines/activity-views). Minimized exposure follows [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices); application roles are not OS privacy prompts. Labels, targets, and pending states follow [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons); confirmations follow [Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts). Adaptation and dismissal follow [Popovers](https://developer.apple.com/design/human-interface-guidelines/popovers) and [Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets).

Invited-only access, viewer default, owner-only management, seven-day expiry, server version checks, private recovery, and conflict policy are product decisions applying the local guidance, not universal Apple requirements. Backend, SDK support, deployment versions, delivery, and runtime behavior require implementation verification.
