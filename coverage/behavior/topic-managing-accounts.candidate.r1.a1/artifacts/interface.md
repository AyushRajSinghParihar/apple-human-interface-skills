# Revised account specification

Platform: macOS. This is an implementable product contract, not evidence of running code. Use the existing app stack and native system controls where available.

## Ownership and launch

Local budgeting works without an online account. On launch show “On This Mac” budgets immediately, including offline; offer a labeled “Sign In…” button with “Sign in to sync budgets and collaborate with your family.” Request authentication only for account sync, sharing, or access to account-owned private budgets. Do not substitute an online login wall for local access.

Distinguish an on-device workspace from each authenticated account workspace. Every budget, draft, queued change, sync job, and restored window is keyed to a stable owner ID; names and email addresses are display labels, never ownership keys. “On This Mac” belongs to the current macOS user and is not uploaded on sign-in. Account A’s cached data stays private to A, including while signed out. This is app account switching, not switching macOS users; storage and credentials must respect macOS user boundaries.

Do not automatically assign legacy unowned data to the next person who signs in. Preserve it locally and require verified ownership before exposing it to an account; ambiguous legacy account data remains quarantined with an explanation and support recovery route. Migration must not delete originals.

## Account controls

Replace the unlabeled trash glyph beside the avatar with a labeled “Account…” button opening a nonmodal Account view in the current window. Show active identity (name and email), workspace name, and textual sync state (“Saved on This Mac”, “3 changes waiting to sync”, or “Sync failed”). The avatar is decorative when redundant with identity text.

The Account view contains labeled native push buttons:

| Control | Availability and outcome |
| --- | --- |
| Sign In… | Signed out; starts the existing supported authentication flow. Cancel leaves local work unchanged. Do not advertise unverified passkey, biometric, or provider support. |
| Switch Account… | Signed in; authenticates the target before committing the switch. Never merges or uploads data between owners. |
| Sign Out | Signed in; persists work locally, ends credentials/session, and returns to On This Mac. Does not delete account or budgets. |
| Delete Account… | Signed in, in a separate “Delete Account” section below ordinary session actions; opens the irreversible-deletion confirmation. Never an avatar-adjacent shortcut. |
| Back to Budgets | Returns to the current workspace without changing session or data. |

Use normal roles for session/navigation commands and a destructive role for deletion. Ellipses indicate further input, not waiting time. No default shortcut invokes account deletion. Retain system control sizing and states, distinct nonoverlapping targets, and readable wrapping labels. Provide complete keyboard navigation and accessible names matching visible labels. Status must remain understandable without color or sound.

## Switch and sign-out transitions

1. Before switching or signing out, durably save editor drafts and queued operations under the current owner, including edits in all app windows. If persistence fails, stay in the current session, preserve the editor, and show “Your changes couldn’t be saved on this Mac. Try again before signing out or switching accounts.” Offer Retry and Cancel; never silently discard.
2. For switching, show persistent text in the Account view: “Your unsynced changes will stay saved for [A email]. They will sync when you sign in to that account again.” Allow Cancel throughout target authentication. Authentication failure or cancellation restores A’s workspace and focus, without changing ownership or uploading anything to B.
3. After successful authentication, atomically stop A’s sync, detach A’s credentials, clear A’s content from every app window, and display B’s workspace. Fence late responses and queued work by owner and session generation; A’s pending writes must never execute with B’s credentials. Restore B’s own navigation context only. Do not show A’s budget titles, search results, thumbnails, or undo history in B’s workspace.
4. Sign Out does not wait for network sync. After the durable save, stop/fence sync and remove session credentials; show On This Mac with “Signed out. Your account changes are saved on this Mac. Sign in to [A email] to sync them.” Account data is retained in protected storage but not available from the signed-out workspace. Returning to A restores its pending edits and resumes sync; conflicts must preserve both versions for resolution rather than overwrite silently.
5. If interrupted or relaunched during a transition, recover one coherent owner/session state. Never restore a private window under a different owner. While a transition commits, disable duplicate session commands with an inline explanation; do not stack authentication or confirmation flows.

No cross-account merge is part of this repair. Local budgets remain local after sign-in. Any future transfer/import requires a separately designed explicit source, destination, preview, and consent contract.

## Delete Account

Deletion is real account deletion, distinct from sign-out or deactivation. It is available in-app without contacting support or canceling an external subscription first. Authenticate the current account using the actual supported method if the service requires recent authentication; cancellation changes nothing. Bind the request to the displayed stable account ID, not whichever account later becomes current.

Before confirmation, fetch an authoritative deletion summary. Show the account email, owned budgets and unsynced-change count, effects on shared budgets and other family members, expected completion time, and any required retention with reason and duration. If this summary cannot be obtained, retain the data and offer Retry or Cancel; do not guess consequences or timing. Product policy for this repair: delete the account’s owned budgets and its local cached copies/queued edits; remove its memberships in others’ budgets, leaving those owners’ budgets intact. Clearly state that collaborators will lose access to budgets owned by the deleted account. On This Mac and other accounts remain untouched. Service enforcement of this policy is a release requirement.

Use one native macOS confirmation alert attached to the initiating window:

- Title: “Delete account for [email]?”
- Message: “This will permanently delete your account, its [N] owned budgets, and [M] unsynced changes on this Mac. Family members will lose access to your owned budgets. Budgets owned by others and On This Mac budgets will remain.” Follow with the verified timing and retention summary. Zero counts must be accurate; never omit unsynced loss when present.
- Actions: Cancel (cancellation role, leading) and Delete Account (destructive role, trailing). Choose no default action so Return alone does not delete; focus starts on the explanatory content. Escape and Command-Period cancel, preserve all work, and return focus to Delete Account…. Outside clicks do not confirm. Do not add a suppression checkbox or an arbitrary typed phrase.

The no-default choice is a product precaution for financial data; HIG also permits a normal default in confirmations of deliberately requested destruction. Do not claim that destructive defaults are universally forbidden.

On confirmed deletion, submit an idempotent request once and show persistent “Deleting account…” status. Do not claim success or erase recoverable data merely because the request was sent. Block edits/sync for this owner while the outcome is pending; other owners’ data remains separate. If the connection is lost or the app closes, persist the request ID, reconcile status on return, and prevent duplicate submission or reupload. A confirmed request cannot be canceled by closing the view; explain that fact before submission.

On confirmed completion, remove this account’s local data and credentials, revoke provider tokens where applicable (including Sign in with Apple if actually supported), return all affected windows to On This Mac, and show persistent “Account deleted” with the completion receipt. Provide the service’s completion notification through its verified channel. On a definite rejection, retain work and session where valid, show the reason and Retry; an unknown outcome stays “Deletion status unavailable” with Check Status, never “Deleted.” Legally retained records must be separately identified and excluded from active product use according to verified policy.

If billing exists, show “Deleting your account does not cancel your subscription” and the actual subscription-management route before confirmation. Apple auto-renewable subscriptions require separate cancellation; external purchases must not block deletion. Do not invent billing, retention periods, provider support, or completion guarantees. Verified summary, timing, notification, and billing behavior are implementation prerequisites, not established capabilities of the supplied app.

## Acceptance contract

Trace launch offline, clean and dirty switching, authentication cancellation/failure, sign-out offline, disk-save failure, relaunch, late sync responses, and multiple open windows. None may lose work or expose/upload one owner’s data to another. Trace deletion with and without pending edits, canceled confirmation, repeated activation, server rejection, unknown outcome, relaunch while pending, and confirmed completion. Only confirmed deletion may remove the targeted account’s data.

On a Mac implementation, verify keyboard-only operation, Return/Escape/Command-Period behavior, focus return, VoiceOver names/status, Full Keyboard Access, 200% text enlargement, and light/dark/Increase Contrast appearances. Measure targets and contrast in the actual UI; a small glyph alone is not evidence of a small hit area. No runtime or accessibility pass is implied by this document.
