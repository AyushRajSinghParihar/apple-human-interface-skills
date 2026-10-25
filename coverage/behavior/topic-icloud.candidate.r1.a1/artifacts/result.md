# Revised sync and conflict interaction specification

Scope: the iOS/iPadOS sketch notebook on a shared iPad and its macOS counterpart on a personal Mac. This is a framework-agnostic design contract, not an SDK implementation. `interface.md` supplies only three existing behaviors; no screens, backend contract, authentication implementation, or runtime were supplied. A shared device does not imply a shared account or collaborative notebook.

## Decisions and evidence

1. Save locally before attempting sync. Keep drawing available without an account or network. Distinguish durable local storage from confirmed cloud storage. The local HIG snapshot recommends unobtrusive offline behavior and preserving local work ([iCloud, Best practices](https://developer.apple.com/design/human-interface-guidelines/icloud#Best-practices)); truthful nearby feedback follows [Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices).
2. Automatically reconcile only demonstrably equivalent revisions. For divergent sketch content, preserve both and invite a choice promptly. Do not use timestamps as the winner or flatten strokes automatically. Differentiated versions and understandable conflict choices follow [iCloud](https://developer.apple.com/design/human-interface-guidelines/icloud#Best-practices). The conservative merge rule, revision protocol, and recovery retention below are product decisions, not prescribed Apple algorithms.
3. Require sign-in for cross-device sync, not sketch creation. Explain that benefit at the sync entry point ([Managing accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Best-practices)). Partition ownership on the shared iPad; never transfer one person's work to the next account implicitly. This is a product safeguard informed by data minimization and established protection guidance in [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices).
4. Keep routine status inline. Conflict review is an explicit navigation destination associated with a notebook, not an unsolicited blocking alert. Clear verbs and remedies follow [Writing](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices). No routine sync banners, sound, or haptics are required.

## State and status contract

Track independent dimensions: local persistence, account/owner, connection, pending revisions, last confirmed server head, and unresolved conflicts. “Synced” means this device's current revision is durably acknowledged by the service, all known remote heads are incorporated, and no work is pending. It cannot promise another device has downloaded the content.

Place a persistent text status beside the notebook title, exposed as a labeled Sync details action. Notebook-list rows expose the same state. Details show current destination account when signed in, pending notebook count, last successful check, and a remedy. Never display internal revision IDs as primary copy. App-wide details list affected notebooks; a conflict in one notebook does not stop others.

| Condition / truth source | Inline copy | Details and available action |
|---|---|---|
| Local commit pending | Saving on this device… | Drawing remains available; do not claim saved yet. |
| Local commit failed | Couldn’t save on this device | “Keep this notebook open. Free storage and try again.” Retry save; offer Export copy when an export destination is available. Preserve in-memory work; never claim export succeeded before confirmation. |
| Guest, local commit succeeded | Saved on this device | “Sign in to sync across devices.” Sign in; continue sketching. |
| Account-owned content, credentials expired | Saved on this device · Sign in to sync | Sign in to the owning account. Expiry alone does not discard cached work. |
| Offline with pending changes | Saved on this device · Waiting for connection | “Changes will sync when connected.” No repeated error prompt. |
| Online, pending changes | Saved on this device · Sync pending | Background retry is scheduled. Sync now requests one immediate attempt. |
| Request in flight | Saved on this device · Syncing… | Text only; no invented percentage or perpetual animated spinner. |
| Remote write and head check confirmed | Synced | “Saved to [account]. Last checked [localized time]. Other devices update when connected.” |
| Previously confirmed, now offline | Saved on this device · Offline | “Last synced [time]. Checking for changes when connected.” |
| Service failure / quota rejection | Saved on this device · Couldn’t sync | State the known cause: e.g. “Cloud storage is full.” Retry sync, or Manage storage if a real destination exists. Unknown cause: “Try again when the service is available.” |
| Divergent heads retained | Two versions need review | “Both versions are saved on this device.” Review versions; other editing remains available. |

Local saving failure takes visual priority, then unresolved conflict, account/network failure, pending work, and confirmed state. Details retain every applicable condition. A conflict label must not conceal failed local persistence. Never say both versions are saved until their durable commits succeed. No stale response may replace a newer status.

On connectivity restoration, foregrounding, or successful authentication, retry eligible pending work automatically. Use bounded exponential backoff with jitter; collapse duplicate manual retries into one request. A stalled request times out into pending/failure with recovery, rather than remaining “Syncing…” indefinitely. Exact timeout/backoff values require service measurements and are not HIG requirements.

## Persistence and concurrency pseudocode

Each immutable revision carries notebook ID, owner namespace, content, parent revision IDs, and an idempotency key. Device name and edit time are descriptive metadata, never ordering authority.

```text
onEdit(edit):
  update canvas in memory
  transactionally persist revision + pending outbox entry
  if persistence fails: expose local-save failure; retain memory; stop upload
  else: expose saved-locally state; schedule sync if eligible

sync(notebook, authenticatedOwner):
  require notebook.owner == authenticatedOwner and locallyDurable
  capture ownerSessionGeneration and local revision
  fetch service heads
  if heads equivalent or ancestors of local revision:
    compare-and-set service heads to captured revision (idempotent write)
  else if local revision is ancestor of service head:
    durably fetch remote revision; apply only at a safe edit boundary
  else:
    durably retain every divergent head; record conflict; invite review
  if compare-and-set rejects: refetch; repeat reconciliation
  if response belongs to old owner session: never render/apply it to new session
  remove only acknowledged outbox entries
  show Synced only after confirming current heads and no newer local edits
```

A remote update must not interrupt an active stroke, reset zoom/selection, or erase uncommitted input. Finish and persist the stroke before reconciliation. Crash recovery restores the outbox and conflicts. A newer edit during upload stays pending after the older acknowledgement. Server-side conditional writes, revision retention, and idempotency are implementation prerequisites; if unavailable, this contract needs backend changes before release.

## Conflict review and recovery

Review versions opens a dedicated notebook review view, preserving canvas position and return destination. Show: “This notebook changed on two devices. Choose a version to continue with, or keep both.” Each version has a full preview with zoom, origin device label, localized edit time, page count, and available textual page titles/descriptions. Call them “Version from Shared iPad” and “Version from Personal Mac,” adding a unique readable suffix if device names match. Avoid “latest,” since clocks can disagree. For more than two heads, show all versions.

On a wide Mac or iPad view, show previews side by side. At narrow widths or enlarged text, stack them without losing labels or actions. Selection is explicit, with no preselected winner. Actions:

- **Keep both notebooks**: create independent, clearly named notebooks for the retained heads; preserve the original notebook ID for the version last open locally and create stable IDs for the others. Record the resolution against all reviewed heads.
- **Use selected version**: require selection. Adjacent copy: “The other versions remain in Recovered versions.” Create a new revision with all reviewed heads as parents and the selected content; retain all source snapshots.
- **Back**: leave the conflict unresolved with all versions intact. Return focus to Review versions. Closing the window, navigation away, or process interruption has the same data consequence.

Commit the resolution and recovery snapshots atomically locally before returning to the canvas. Show “Saved on this device · Sync pending” until confirmed. If another head arrives during review, preserve the selection but show “Another version arrived. Review it before continuing”; refresh the choices and require a new explicit commit. Never apply a stale decision over unseen edits.

Recovered versions is a persistent notebook action, with no automatic expiry in this specification. Open any retained snapshot and choose Restore as new notebook; restoration creates a pending revision without replacing current work. Keep recovery copies when signed out, scoped to their owner. This flow offers no destructive discard action; deletion and retention policy changes require a separate cross-device deletion specification and confirmation. Storage exhaustion remains an explicit save failure, never silent pruning.

## Shared-device ownership and offline access

Guest mode opens a clearly labeled “On this device” workspace: “Sketches here can be seen by other people using this device.” It is not a private account. Sign-in cancellation returns here without losing edits. On sign-in, open that account's separate workspace; guest sketches stay local. An explicit account-level action, “Copy device notebooks to [account],” explains that all guest notebooks will upload and become available on that account's devices; cancel leaves them local. This avoids per-document storage prompts while preventing automatic guest upload.

Explicit sign-out first commits local work, invalidates the active sync session, hides account notebooks, previews, search entries, and recovery records, and opens the guest workspace. Pending account work remains retained for the same account; copy reads “Unsynced changes stay on this device for [account] until you sign in again.” If local persistence fails, explain that sign-out cannot safely finish yet and offer Retry save or return to the notebook. Account B cannot view, retry, or upload A's queue. A late response for A cannot appear in B's interface. Returning to A restores its pending work and review state. Local caches require established encrypted storage and authentication protections; hiding UI alone is not a security boundary. Guest copying and explicit sign-out are product choices, not asserted iCloud account APIs.

| Data | Purpose and boundary |
|---|---|
| Sketch content and recovery snapshots | Local creation/recovery; transfer only within an enabled owner workspace or explicit guest-copy action. |
| Owner identifier and credentials | Route and authorize sync; isolate namespaces; protect credentials with established secure storage. |
| Device label, revision ancestry, edit times | Differentiate conflicts and detect concurrency; do not collect contacts, location, camera, or microphone for sync. |

## Worked before / after

Alex opens the same notebook on a shared iPad and personal Mac. Both start at revision R0. Offline on the iPad, Alex adds a tree (I1); the Mac adds a house (M1) and uploads it.

**Before, as described by the brief:** the iPad calls I1 “Synced” after a local save. Reconnection silently overwrites one concurrent edit. Signed-out use is blocked. Which version wins is unspecified.

**After:** the iPad shows “Saved on this device · Waiting for connection.” On reconnection it discovers M1 diverges from I1, retains both, and shows “Two versions need review” without interrupting drawing. Alex opens Review versions, compares labeled previews, and chooses Keep both notebooks. The tree remains in the current notebook; the house appears as a second notebook named with its origin. Both remain available locally while pending upload. Only confirmed service heads permit “Synced.” Explicit sign-out hides Alex's notebooks but permits a new guest sketch; another person's sign-in never uploads Alex's tree. Signing back into Alex's account restores any unsynced recovery work.

## Acceptance checks and evidence limits

**Passed — static specification checks:** the three supplied failures have explicit replacement behavior; every status has a truth source and remedy; conflict choices preserve both sources; cancellation and stale-resolution handling are defined; guest and account data have separate ownership. Installed root, selected families, topic procedures, and supporting guides were read from this package, including the iCloud procedure's routed Writing topic. Official links above identify source sections; no web browsing occurred.

**Failed — supplied design against this contract:** local save labeled Synced; silent overwrite of concurrent edits; signed-out offline sketching blocked. These are findings from the brief, not reproduced runtime failures.

**Not executed — required implementation acceptance checks:**

1. Edit offline, restart, reconnect: exact strokes survive; no Synced label precedes acknowledgement. Inject disk-full failure: no false saved claim and no upload of an undurable revision.
2. Upload R1 while creating R2: R1 acknowledgement leaves R2 pending. Drop acknowledgement and retry: one logical revision results. Inject timeout, quota failure, and recovery: truthful actionable status without repeated blocking prompts.
3. Create divergent strokes on two clients: neither disappears. Exercise each recovery action, Back, window close, restart, and a third concurrent head. All source versions remain recoverable and stale choices cannot overwrite unseen heads.
4. Sign out with pending edits, sign in as another account, and deliver an old response: no cross-account content, search results, thumbnails, or uploads. Sign back into the original account: pending edits and conflicts return. Cancel guest copying: no upload occurs.
5. Complete review using keyboard and supported assistive input. Specify focus order as title/explanation, each labeled version and selection, resolution actions, Back; return focus to the initiating control. Status changes are semantic text updates announced without stealing focus or announcing each stroke. No essential information depends solely on color, sound, previews, or gestures; supply author-entered sketch descriptions where available and explicitly label undescribed previews.
6. At 200% text size, long localized labels, narrow iPad windows, light/dark appearance, and increased contrast: retain every state and action with scrolling/reflow. Start with activation areas of 44 × 44 pt on iOS/iPadOS and 28 × 28 pt on macOS, as the local guide's platform defaults, not its smaller minima. Measure actual contrast and geometry. These targets follow [Accessibility: Vision, Mobility, and Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility).

No device, SDK compilation, GUI, service propagation, security, localization, contrast measurement, or accessibility execution was performed. No Apple framework or cloud provider is assumed. The installed guides are dated derivative HIG snapshots, not API documentation or independently verified current Apple text. There is no source-backed automatic sketch merge algorithm here; reliable comparison for complex undescribed drawings, backend guarantees, encrypted owner isolation, and recovery storage capacity remain implementation and user-validation dependencies.
