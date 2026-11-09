# Shared writing: invitation and access specification

Platform: iPadOS/macOS; iPad is the primary interaction context. Framework, backend, OS minimums, and screen layouts are unspecified. This is a design contract requiring implementation verification.

## Share and manage

Use the standard Share entry in the project toolbar and supported system presentation. iPad uses the system share sheet/popover; Mac uses supported sharing entry points, not a macOS activity-view component. Preserve project and writing position on dismissal. Do not prescribe system destination ordering.

Offer Collaborate and Send a Copy as distinct modes:

- Collaborate defaults to “Only invited people · Can view · Only owner can invite.” Owner selects Can View or Can Edit for each named recipient before Send Invitation. This release has no anyone-with-link access. Forwarding or copying a link grants nothing.
- Send a Copy exports the current project's text as a UTF-8 plain-text file named after the project, without participant identities or invitation metadata. Explain “Independent copy. Changes won't sync. Copies can't be recalled.” Label unsynced exports Local Draft. Export only already authorized content; do not export from a revoked-access screen. Copy transfer creates no membership.

Invitation setup shows recipient identity, project, and proposed role. Cancel or dismiss before Send Invitation creates nothing. Sending creates a pending invitation only after server acknowledgment, never after transport handoff alone. Failed creation retains inputs with Retry. An uncertain response is reconciled using a request ID before retry to avoid duplicates.

Once invitations or members exist, show Collaboration prominently beside Share. Group People and Invitations separately, each with identity and role/status text; show essential communication options where supported and Manage Access at the bottom for owners. Pending-only copy is “1 invitation pending,” not “1 collaborator.” Nonowners see their role and owner contact route without management commands. Use system management when the eventual infrastructure supplies this model; otherwise implement it explicitly. Done closes management without altering access.

## Capabilities and enforcement

| Capability | Owner | Accepted editor | Accepted viewer | Pending / removed / unknown identity |
| --- | --- | --- | --- | --- |
| Read | Yes | Yes | Yes | No new server content |
| Edit text or delete sections | Yes | Yes | No | No |
| Delete shared project | Yes | No | No | No |
| Invite, change roles, remove others | Yes | No | No | No |

Server authorization is required for every read, write, export fetch, acceptance, and management operation. Bind invitations to authenticated identity and project. A link alone must not expose content. UI availability does not substitute for authorization.

Viewer screens say “Can view” and explain “You have view access.” Editing and destructive commands are unavailable through toolbar, keyboard, context menu, drag, and batch paths. A rejected stale editor command applies the returned role, preserves unsent authored work separately, and never retries as an authorized edit.

## Invitation, membership, and presence states

Store invitation lifecycle, accepted role, live presence, and sync status independently. Sending is neither acceptance nor presence.

| State / transition | Management display | Recipient behavior |
| --- | --- | --- |
| Creating → acknowledged | Sending invitation… → Invited · Can view/edit | No content before authenticated acceptance |
| Pending → accepted | Move from Invitations to People after server acceptance | Show inviter, project, account, role; Accept Invitation joins; Decline creates no membership |
| Pending → expired / declined / canceled | Explicit terminal status; owner can invite again | Explain terminal status; no content; contact owner for a new invitation |
| Accepted | Can view/edit; Editing now only from fresh presence | Open specific project with current role |
| Role changing → confirmed | Changing access… → confirmed role | Apply event or refresh; stop editing on downgrade |
| Removal pending → confirmed | Removing access… → Access removed | Stop editing/subscriptions and show access-ended state |

Product policy: invitations expire seven days after creation. Resend creates a new token and invalidates the old one. Cancel invalidates an unaccepted invitation. Serialize acceptance/cancellation: if acceptance wins, show the accepted person and require Remove Access. Offline members remain accepted; unknown presence never means Editing now.

## Removal and stale access

Remove Access opens an important confirmation: “Remove Alex's Access?” / “Alex will lose access to this shared project. Previously saved copies can't be recalled.” Provide Cancel and destructive Remove Access, with no default action as a deliberate product choice. Cancel, Escape, or Command-Period sends no request. Do not stack alerts. Owner-only Delete Project similarly names the project and warns that everyone loses the shared project, with Cancel and Delete Project.

During a request, show pending status and disable duplicate activation. Failure says “Couldn't remove access” with Retry, retaining last confirmed membership. Unknown outcome says “Checking access…” until reconciled. Never claim removal before acknowledgment. Offline management is unavailable with “Connect to change access”; do not silently queue permission changes.

After confirmed removal, deny future server reads/writes and invalidate that membership's invitation tokens. Connected clients apply revocation events immediately; revalidate on foreground, reconnect, and link opening. A disconnected client cannot know revocation: show “Offline · Access not verified” and last checked time, never an assertion of current access. On learning removal, hide shared content, clear that client's shared caches, and show “Your access to [project] ended,” Back to Projects, and already-known owner contact information. Preserve unsent user-authored changes as a separate local recovery draft, never writable shared content. Revocation cannot recall external copies or erase an unreachable device.

Invitation and activity links resolve to the specific object after authentication and authorization. Wrong identity shows “This invitation is for another account” with Switch Account and Back. Invalid links show an unavailable state without content. Accepted members open without accepting again; removed people see access ended. Custom infrastructure must implement universal-link routing; working integration is not assumed.

## Offline drafts and conflicts

Accepted owners/editors may write durable local drafts offline, labeled “Offline · Changes on this device · Access not verified.” Viewers remain read-only. Shared section deletion, project deletion, and access management require connection. Keep the base server revision and unique operation IDs; restore draft and status after closing/relaunching.

Reconnect revalidates identity and role before fetching or uploading. Removal uses the access-ended recovery state. Downgrade preserves the authored draft separately and opens server content read-only. For an authorized editor, submit against the base revision; matching revision commits once. Show Syncing… while pending and Saved only after acknowledgment. Network failure retains the draft with Retry.

Concurrent revision changes retain local and server versions and show “Changes need review.” Present conflicting passages with Keep Server Version, Use My Version, and Edit Combined Draft as draft decisions. Back retains both versions. Apply Reviewed Changes explicitly commits against the latest revision and permission. Another concurrent change restarts review against the new server version while preserving reviewed work. Never silently overwrite or replay destructive operations. Recovery drafts can be saved separately as authored text, without newly fetched content after removal.

## Control contract and guidance

Prefer system buttons with specific labels, visible availability and pending feedback. Send Invitation, Accept Invitation, Retry, and Apply Reviewed Changes show activity in the activating iPad button and deduplicate requests. Give the Share symbol the name Share. iPad targets are at least 44×44 pt with separation; Mac retains native sizing and uses ellipses for commands requiring further input. Status uses text rather than avatars or color alone. Verify native rendering, focus, enlarged labels, keyboard actions, and actual target geometry during implementation.

Source basis: [Collaboration and sharing — Best practices](https://developer.apple.com/design/human-interface-guidelines/collaboration-and-sharing#Best-practices) supports copy/access separation, concise permissions, prominent collaboration management, and object-specific update links. [Activity views](https://developer.apple.com/design/human-interface-guidelines/activity-views) informs system handoff and Mac distinctions. [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices) informs precise exposure and data minimization. [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons) and [Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts) inform labels, pending feedback, and consequential cancellation. Owner-only management, expiry, server guards, and conflict policy are product decisions applying this guidance, not Apple API guarantees.
