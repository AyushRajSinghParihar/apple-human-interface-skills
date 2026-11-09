# Sketch notebook: sync status and conflict recovery

## Scope and decisions

The supplied `interface.md` specifies iOS/macOS, a shared iPad and personal Mac, and three current behaviors: every local save says “Synced,” concurrent edits overwrite silently, and signed-out users cannot work offline. Treat the iPad experience as iPadOS; retain a compact iOS layout if iPhone is supported. No implementation, storage model, authentication service, or sync provider is supplied.

This specification replaces those behaviors. Local persistence and remote synchronization have separate truth sources. Drawing remains available without connectivity or an account. Concurrent versions are preserved until a safe merge or an explicit choice. Account ownership remains distinct from the identity of a device’s current user.

HIG supports quiet offline continuity, automatic conflict resolution where possible, and clearly differentiated versions when a choice is needed ([iCloud, Best practices](https://developer.apple.com/design/human-interface-guidelines/icloud#Best-practices)). This is experience guidance applied to an unspecified sync provider, not a requirement to adopt iCloud or an Apple SDK. Revision tokens, transactional storage, retry timing, and recovery history below are product engineering decisions.

## Persistence and status contract

Each notebook has an immutable ID and owner namespace (`guest-device` or account ID). Each revision records its parent revision(s), content, device label, and display timestamp. Device names and wall-clock timestamps help identify versions; they never decide which edit wins. Persist content and pending operations atomically, including referenced sketch assets, before reporting a local save. Autosave completed drawing operations and flush when leaving the notebook or backgrounding. A failed flush must remain visibly unsaved; closing a view must not clear its in-memory recovery state. Reopening recovers the last durable revision and pending operations.

This follows autosave and truthful document-state guidance ([File management, Saving work](https://developer.apple.com/design/human-interface-guidelines/file-management#Saving-work)). Exact crash-durability guarantees require implementation testing.

Show a compact text status immediately below the notebook title and in notebook-list metadata. Its adjacent “Sync Details” button opens an inline details region containing local-save result, last server confirmation time, pending work, account destination, and recovery actions. Never require opening details to discover a failure or conflict. Use notebook-scoped status; a collection summary says, for example, “2 notebooks need review,” rather than implying all notebooks are current.

| Condition | Visible status | Details / next action |
|---|---|---|
| Current edit has not committed locally | Saving on This Device… | No claim of durability or cloud success |
| Local commit fails | Couldn’t Save on This Device | “Recent changes haven’t been saved. Free storage, then retry.” Retry Save; Save a Copy to a chosen destination if available; keep original draft |
| Guest local commit succeeds | Saved on This Device | “Not connected to an account. These sketches are available to people using this device.” Sign In for Sync |
| Account-owned local commit, offline | Saved on This Device · Offline | “Changes will sync when a connection is available.” No spinner or blocking prompt |
| Session expired | Saved on This Device · Sign In to Sync | Sign In; drawing continues within the current unlocked workspace until explicit sign-out |
| Connected, queued | Saved on This Device · Waiting to Sync | Pending operations retained; automatic retry |
| Request actively running | Syncing… | Local save status remains in details; indeterminate activity, no percentage |
| Current durable revision confirmed by server, no pending work/conflict | Synced | “Confirmed with the service at [time]. Another device may still be offline.” |
| Transport/service failure or stall | Saved on This Device · Sync Paused | Specific known cause; Retry Sync; never suggest signing in for an unrelated network failure |
| Concurrent versions retained | Versions Need Review | “Two versions were saved. Review them when ready.” Review Versions |

Local-save failure has highest status priority; conflict, authentication/offline/failure, active sync, queue, and confirmed status follow. Details retain every applicable condition: a conflict does not hide an unsaved edit. “Synced” means server confirmation of the current revision and assets; it cannot promise delivery to every device. A new edit invalidates that status immediately, even if an older upload succeeds later.

Routine save/sync transitions stay near the notebook without banners, sounds, or repeated announcements. Persistent actionable text handles errors and conflicts ([Feedback, Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices)). Use a fixed small activity region only during actual work; remove activity on completion, failure, offline, or authentication expiry. No invented percentage. For this product, a request with no progress for 30 seconds becomes paused, with automatic retries at 5, 15, then 60 seconds, capped at 60 seconds while foregrounded. Background scheduling may defer attempts. Retry Sync requests one immediate attempt; coalesce repeated activation. Late responses remain subject to revision/account checks. These timings are proposals, not HIG values ([Progress indicators, Best practices](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices)).

## Conflict recovery

1. Fetch remote changes without replacing unacknowledged local edits. If one revision descends from the other, fast-forward safely. Otherwise retain both immutable branches and their common ancestor. Initial implementation offers manual review for divergent sketch content; automatic merge is permitted later only with demonstrated semantics for strokes, erasures, layers and ordering. Never merge by timestamp or blindly overlay drawings.
2. Show “Versions Need Review” promptly without opening a modal automatically. Continue drawing on the local branch and syncing unrelated notebooks. Review Versions opens a short sheet attached to this notebook. Snapshot the latest local branch on entry; temporarily suspend editing this notebook while the comparison is open. Other notebooks remain usable after dismissal; other Mac windows remain usable.
3. Title: “Review Versions.” Body: “This notebook changed on two devices. Both versions are saved.” Show labeled previews: “This iPad — [date/time]” and “Mac — [date/time],” each with page count, page selector, and changed-page summary relative to the common ancestor when computable. Use “Other device” if provenance is missing. Identical-looking previews retain distinct labels. Allow inspecting every page at useful scale without switching to an editing tool.
4. Prominent default: **Keep Both**. It creates two independently editable notebooks with distinct IDs and names such as “Field sketches — iPad version” and “Field sketches — Mac version.” **Use iPad Version** and **Use Mac Version** choose the active notebook content; the unselected branch remains in that notebook’s **Recovered Versions** region with Open and Restore as Copy actions. Never call this deletion or silently discard the alternative. State that preservation next to these actions. **Cancel** dismisses with no resolution. On Mac, entry commands requiring further input use ellipses, such as “Review Versions…”.
5. Commit the resolution locally as one transaction, retaining originals and recording a unique resolution ID. If offline, close with “Saved on This Device · Waiting to Sync” (or Offline). If online, upload conditionally against the reviewed remote revision. Do not show Synced until confirmation. Duplicate activation or retry reuses the resolution ID and cannot create extra copies.
6. If the remote head changed during review, preserve the choice as a local draft, refresh the comparison and show “Another version arrived. Review the updated versions.” Require a new explicit choice; never overwrite the unseen revision. Recovered versions remain until a separately specified explicit deletion flow exists; no automatic expiry in this revision.

Cancel, Escape on Mac, supported swipe dismissal on iOS/iPadOS, and presentation closure all preserve both branches and return to the same page, zoom and selection. No resolution occurs on dismissal. After commit, return to the chosen notebook; after Keep Both, open the local-derived copy and expose the other in the list. Focus returns to Review Versions if unresolved, or the notebook heading after resolution. App interruption preserves the branches; reopening review rebuilds comparison from current revisions rather than committing a stale choice.

A short choice belongs in a scoped sheet; substantial manual merging is excluded. One sheet at a time; authentication replaces the sheet only after preserving context. Mac sheets block their parent, while iPad uses a centered, adequately sized sheet; compact iOS uses a large sheet. Resizing can stack previews vertically while preserving labels and actions. These decisions follow [Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets#Platform-considerations) and [Modality](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices).

## Signed-out and shared-device behavior

New Sketch always works in a guest workspace. No launch-time sign-in gate. Sign In for Sync explains: “Sync account notebooks across your devices. Sketches on this device stay local unless you add them.” After successful authentication, show the account destination and offer **Add Device Sketches to Account** or **Keep on This Device**. Adding is an explicit bulk copy, preserving guest originals and assigning new account-scoped IDs. Guest sketches never silently upload to the next person’s account. Guest storage is visibly shared-device storage, not a private vault.

Explicit Sign Out first stops uploads, invalidates in-flight request context, flushes edits and seals the account workspace. Copy: “Account notebooks will be hidden on this device. Unsynced changes will stay here for this account. Device sketches remain available to anyone using this device.” If local persistence fails, retain the recovery buffer behind the account access boundary and report failure on return; do not expose it in guest mode or claim it was saved. Sign-out must still revoke access. Account-owned cached content, previews, search results, recovered versions and queues remain inaccessible until that same account authenticates again. A different account cannot adopt those queues. Returning to the same account resumes pending work and rechecks remote revisions. No cross-device deletion is implied by signing out.

Authentication cancellation/failure returns to the same guest notebook or locked account entry, with its saved work intact. No authentication method or biometric capability is promised. This permits useful unregistered access ([Managing accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Best-practices)) and applies data minimization and established protection principles ([Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Protecting-data)). Account isolation and retention behavior are proposed requirements, not proven security properties.

## Framework-agnostic transition rules

```text
on edit(operation):
  append to in-memory draft; invalidate current synced claim
  commit content + assets + pending operation in owner-scoped transaction
  if failed: show local-save failure; retain draft
  else: schedule sync only if owner matches authenticated session

on sync attempt:
  capture(owner, sessionEpoch, localRevision, expectedRemoteHead, operationID)
  conditionally upload durable revision and assets
  on response:
    reject UI/account mutation if owner or sessionEpoch no longer matches
    if remote divergence: durably retain branches; require review
    if accepted: acknowledge only captured revision and operationID
    recompute status from current revision, remaining queue and conflict state

on resolve(choice, reviewedHeads):
  atomically preserve branches + create resolution draft with stable ID
  conditional publish against reviewed remote head
  if remote moved: preserve draft; require updated review
  if accepted and no newer edits: mark confirmed
```

## Platform, controls and access

On iPad, touch reaches every recovery action; Pencil is optional for drawing and never required for recovery. On Mac, expose File > Sync Details… and File > Review Versions… for the active notebook, with the same availability and target as onscreen buttons. Provide a full keyboard path; Escape cancels review, and Return activates only the focused action or the nondestructive Keep Both default. Retry is enabled when its prerequisite exists; otherwise show why, such as “Connect to retry.” No hidden hover-only commands.

At wide widths previews sit side by side; at narrow widths they stack in one scroll region with completion reachable. Rotation, resizing, background/foreground and switching apps preserve notebook, page and draft. This follows the [iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados#Best-practices), [macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Best-practices), and compact [iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices) guidance.

All actions have matching visible and accessible names, button roles, enabled/busy state and press feedback. Status is readable text, never color alone. Reading order is title, status, explanation, labeled versions, actions. Announce a newly encountered failure/conflict once without moving focus; do not announce each autosave. Preview descriptions include device, date, page and available change summary, without pretending to describe arbitrary drawing content automatically. Recovery requires no timed response, sound, or complex gesture. Use 44 × 44 pt activation regions for these recovery buttons on both platforms as a conservative product choice: the local Buttons guide gives a general 44 pt recommendation, while Accessibility lists macOS default 28 pt and minimum 20 pt. Do not misstate 44 pt as a universal Mac minimum. Use platform default text sizing, support at least 200% enlargement, reflow labels, and measure actual light/dark contrast before release. See [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision), and [Writing](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices).

## Worked before/after

Mira opens “Field sketches” at revision R on the shared iPad and her personal Mac. Offline, the iPad adds shading A while the Mac erases a line B.

**Before:** Both local saves say Synced. The last reconnect silently replaces the other drawing. Signing out on the iPad prevents the next person from sketching offline.

**After:** The iPad says “Saved on This Device · Offline.” The Mac’s upload B receives server confirmation and says Synced. When the iPad reconnects, its conditional upload detects that A and B diverge from R; both survive and the iPad says “Versions Need Review.” Mira opens labeled previews, chooses Use iPad Version, and sees that the Mac version remains under Recovered Versions. The resolution saves locally, then says Synced only after server confirmation. She can restore B as a separate copy. If the Mac edits again during review, the stale choice cannot overwrite it. After Mira signs out, her private notebook disappears from the guest list, pending account work stays account-bound, and the next person can create a device-only sketch offline.

## Acceptance checks and evidence limits

**Passed — static specification review only:** The revised contract separates local save from server confirmation, defines all review exits, retains concurrent branches and rejected resolution drafts, permits guest offline drawing, and forbids cross-account queue adoption. The worked scenario traces the three supplied defects to specific replacement behavior. Installed root, selected families, topic procedures and local source guides were read; no web browsing was used.

**Failed — supplied baseline contract:** Its three stated behaviors fail truthful status, conflict preservation and signed-out offline access. These findings come from `interface.md`, not observed execution. No revised runtime was tested, so no revised runtime failures or passes are asserted.

**Not executed — required implementation acceptance:**

| Scenario | Pass condition |
|---|---|
| Local commit succeeds, network unavailable | Local status only; drawing/reopen retains edits; no spinner while offline |
| Disk full / asset-write failure / app killed during commit | No Saved or Synced claim; previous durable revision survives; retained draft recovery follows documented storage guarantees |
| Old upload completes after a newer edit | Current notebook remains pending; old acknowledgement cannot mark it Synced |
| Long upload, server rejection, timeout, retry | Honest activity; paused recovery; no duplicate operations; no false percentage or success |
| Divergent edits, erase-versus-draw, repeated reconnect | Both branches remain; no silent winner; unrelated notebooks continue |
| Cancel, Escape, swipe, resize, app interruption | No resolution committed; both versions retained; page/context restored |
| Each resolution choice offline and online | Correct active content/copies; alternative recoverable; remote confirmation required for Synced |
| New remote revision arrives during review or resolution retry | Stale publish rejected; draft retained; updated review required; no duplicate copies |
| Account A signs out; account B signs in; late A response arrives | No A content, thumbnails, search results or queued upload enters B; A can recover pending work on return |
| Guest sign-in canceled, failed, or completed | Guest draft survives; upload only after explicit account-copy choice |
| Narrow/wide iPad, compact iOS, resizable Mac, 200% text | Labels and all actions remain readable/reachable; selected page and draft persist |
| Keyboard and assistive input, no color/sound, light/dark | Named controls and status reachable in task order; focus restored; contrast and hit regions measured; no essential gesture-only action |

The only product evidence is a one-sentence brief. No app, backend, SDK, device, GUI, accessibility runtime, storage durability test, or multi-device service run was available or executed. Local guides are dated 2026-10-25 application guidance derived from HIG; official links identify provenance and were not opened. They do not establish current API availability, security enforcement, legal compliance, native rendering or assistive-technology behavior. Synchronization transport, encryption, account authentication and crash-safe persistence must be selected and verified during implementation. General document browser, export, account creation/deletion and cloud deletion flows are outside this revision; no capabilities for them are inferred.
