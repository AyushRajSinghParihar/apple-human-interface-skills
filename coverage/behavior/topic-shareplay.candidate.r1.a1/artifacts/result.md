# Shared movie watching: revised interaction specification

Scope: design for iOS, tvOS, and visionOS where the required capability is available. This is a framework-agnostic contract, not SDK code. The only product evidence is `interface.md`; it describes behavior, not screens or implementation. Labels, role policy, and recovery rules below are proposed product decisions.

## Decisions and source support

1. **Join deliberately and quietly.** Opening an invitation shows the specific movie, artwork, inviter, session status, and “Join SharePlay.” It never captures or broadcasts microphone audio. After joining, show “Your microphone is off” and an optional communication control. Joining and watching must work without microphone permission. Request permission only when the person chooses to speak. This applies privacy guidance on minimum necessary access and permission timing; the default-off policy is our design choice. [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission).
2. **Join the current moment.** A late join reads the current shared timeline and seeks only the joining player. It must not emit restart, seek-to-zero, pause, or play commands to the group as a side effect of joining. Show “Joining at 24:18” using the actual current position. Revalidate the timeline immediately before playback. SharePlay supports synchronized viewing and direct content entry; this exact late-join policy is our correction. [SharePlay — Best practices](https://developer.apple.com/design/human-interface-guidelines/shareplay#Best-practices).
3. **Check each person's access.** The invitation does not confer a subscription or purchase. Resolve capability, sign-in, entitlement, and content availability before group membership commits. Defer optional profile setup. Required prerequisites remain dismissible. [SharePlay — Best practices](https://developer.apple.com/design/human-interface-guidelines/shareplay#Best-practices).
4. **Separate leave from end.** “Leave SharePlay” removes only this person; even an organizer can leave without ending others' viewing. A separate organizer-only “End for Everyone” requires confirmation. Clear leave/rejoin is source-backed; organizer authority and continuity are product policy requiring implementation feasibility validation. [SharePlay — Designing shared activities](https://developer.apple.com/design/human-interface-guidelines/shareplay#Designing-shared-activities).
5. **Keep personal settings personal.** Shared state is movie identity, playback position/rate, play/pause, session revision, and membership. Volume, subtitles, audio description, other accessibility preferences, microphone intent, and local presentation remain per-person. A deliberate shared pause displays “Alex paused for everyone.” The app must also explain system-originated group pauses accurately rather than falsely assigning an actor. [SharePlay — Best practices and visionOS](https://developer.apple.com/design/human-interface-guidelines/shareplay).

## Entry and access contract

Use ordinary navigation to a movie-specific invitation page, not a blocking onboarding flow. In-app SharePlay, an external invitation, or a supported system entry all resolve to the same session/movie identity. The invitation uses a concise title and description, such as “Watch Ocean Lights with Alex.” Returning from a prerequisite restores this destination, not the catalog.

| State | Visible content and actions | Transition and side effects |
|---|---|---|
| Invitation | Movie, inviter, live/ended status; Join SharePlay; Close | Close returns to originating context, without joining or changing playback. |
| Checking | “Checking access…”; Cancel | Cancel invalidates pending requests. No group mutation. |
| Access required | “You need access to Ocean Lights to watch together.” Sign In, Restore Purchases, View Access Options, Close as applicable | No forced purchase and no host-entitlement assumption. Preserve invitation while resolving access. |
| Access unavailable | Specific known reason, such as regional unavailability; Close; Retry only when useful | Do not offer a purchase that cannot unlock this movie. Unknown/network errors must not be labeled missing entitlement. |
| Ready | Movie and current session position; Join SharePlay | Explicit activation commits joining after a fresh access/session check. Repeated activation produces one join. |
| Joining | “Joining…”; Cancel | Fetch latest timeline; prepare local player; no group restart. |
| Watching | Movie, shared status, personal settings, Leave SharePlay, optional speaking control | Membership acknowledgment precedes shared playback controls. |
| Ended or failed | “This session has ended,” or actionable connection error; Watch Alone if entitled, Return, Retry when applicable | No silent creation of a replacement session or automatic solo playback. |

If entry checks finish immediately, Join SharePlay can proceed through Ready without requiring a duplicate activation; never introduce a second consent tap solely because the check was fast. If access resolution interrupted the action, return to Ready for an explicit join.

Access options use the existing commerce system. No prices or offer terms are supplied, so this specification does not invent a paywall. Before any purchase, show the actual localized total, included access, duration, and applicable renewal/trial terms; offer sign-in/restore to existing purchasers. On tvOS, prefer supported companion-device/code entry. Successful access acquisition rechecks the live session and returns to Ready; canceled or pending purchases do not join. [Apple In-App Purchase — Making signup effortless](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Making-signup-effortless).

## Microphone and data boundary

| Data | Purpose | Boundary |
|---|---|---|
| Movie/session identifier, membership, playback revision | Locate and synchronize the activity | Share only the necessary session state; do not broadcast purchase history. |
| Entitlement result | Authorize local playback | Keep account credentials and detailed purchase records outside participant-visible state. |
| Microphone audio | Optional live conversation | No app capture/transmission until explicit speaking intent and authorization; stop immediately on mute or departure. No recording is proposed. |
| Personal playback preferences | Individual viewing needs | Local to each person; never overwritten by a join or another viewer's settings. |

For app-owned audio, “Turn On Microphone” requests the real system authorization if needed. Suggested purpose: “Use your microphone so other participants can hear you during shared watching.” On denial, remain watching with audio transmission off; show an inline explanation and optional settings recovery. Recheck that the person is still joined and still requesting speech when authorization returns. A stale grant cannot enable capture after cancellation. Muting is immediate and does not pause the movie.

For system-owned FaceTime/communication audio, use the supported system control and accurately display its ownership; do not claim the app muted an existing call or invent access to call controls. Joining must never unmute that call. If the communication state cannot be read, say “Manage microphone in your call” rather than asserting it is off. Capability support and these handoffs remain implementation questions. Update privacy disclosures to match actual collection. [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices).

## Leaving, ending, and recovery

“Leave SharePlay” is a direct action with nearby explanation: “Others will keep watching.” It disables app-owned audio transmission immediately, disables shared controls, and requests local membership removal. On acknowledgment, show the movie page with “You left SharePlay,” Rejoin if still live, and Watch Alone if entitled. Solo playback begins only on request, at the departure position; it has no shared effects. Leaving does not end a separate call. Closing player controls or navigating Back is not an implicit group-end command.

The organizer's separate End for Everyone action opens one consequential confirmation:

- Title: “End SharePlay for Everyone?”
- Message: “Shared playback will stop for all participants. You can leave instead to let others keep watching.”
- Actions: Cancel (cancellation role), End for Everyone (explicit termination role). No default activation, so Return alone does not end the group. Use platform placement rather than fixed cross-platform geometry. This conservative no-default policy is permitted application advice, not a universal HIG requirement for deliberate destruction.
- Cancel, supported keyboard escape, and tvOS remote cancellation dismiss without changing playback. Restore the initiating control. Only deliberate confirmation submits the end command; never stack duplicate alerts.

The confirmation blocks only its local parent. Other participants continue playing until termination is acknowledged. Validate organizer authority again on commit. If authority changed, explain inline and retain Leave SharePlay. On success all participants stop shared playback and see “Alex ended SharePlay,” plus deliberate solo/return choices. End failure must not report success; retry after checking session status. [Alerts — Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons), [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices).

On connection loss, show “Reconnecting…” locally and prevent stale shared commands. Reconnect to the latest timeline without rewinding others, retaining personal settings and keeping app-owned microphone off until explicit reactivation. Leaving while offline closes local media/audio immediately and invalidates reconnect attempts; reconcile remote membership when possible. Organizer loss/departure does not terminate the session: transfer organizer authority using a deterministic service policy. If the backend cannot provide continuity, that is an unresolved implementation blocker, not permission to silently end everyone.

```text
join(attempt):
  require currentAttempt(attempt) and capability and entitlement and liveSession
  membership = joinOnce(sessionID, attempt)
  if canceled(attempt): leaveMembershipIfCreated(membership); return
  timeline = latestTimeline(sessionID)
  localPlayer.align(timeline)       // never a shared seek
  appMicrophone.transmit = false

leave():
  invalidateJoinAndReconnectAttempts()
  appMicrophone.stopImmediately()
  disableSharedControls()
  removeOnlyLocalMembershipOnce()  // no end-session fallback on error

confirmEnd():
  require explicitConfirmation and currentOrganizerAuthority
  endSessionOnce(sessionID, commandID)
```

## Platform contract

| Platform | Entry, viewing, and return |
|---|---|
| iOS | Keep primary join/leave actions reachable and context intact through orientation, enlarged text, and interruptions. Support shared video continuing in Picture in Picture where supported; returning restores the movie/session rather than onboarding. Backgrounding is not a group-end action. [iOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices), [SharePlay — iOS](https://developer.apple.com/design/human-interface-guidelines/shareplay#iOS-iPadOS-macOS). |
| tvOS | Show legible across-room movie and access status with visible focus. Invitation focus order: Join → Close; access page: applicable recovery actions → Close; player session controls: Leave → organizer-only End. Reverse movement returns through those controls. Remote cancellation exits the current prerequisite/confirmation without ending the group. Actual directional traversal remains to be tested. Viewer changes recheck the new profile's access. [tvOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos#Best-practices). |
| visionOS | Entry, access, and leaving use a standard window in Shared Space. Ordinary window mirroring via the window-bar Share button must not be confused with adopting SharePlay for volumes/immersive content. This design does not require Full Space or custom seating. If spatial participation is implemented, prefer side-by-side media viewing, stable participant locations on departure, and contact-image/2D alternatives where Personas are unavailable. Any later immersion change needs deliberate permission; leaving returns to windowed context where possible. [visionOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos#Best-practices), [SharePlay — visionOS](https://developer.apple.com/design/human-interface-guidelines/shareplay#visionOS). |

## Worked before/after

Before, Alex and Bea are 24 minutes into a movie. Casey joins: their microphone broadcasts automatically and everybody restarts at zero. Casey leaves, ending the session for Alex and Bea. Drew lacks content access; the brief does not describe any recovery.

After, Casey opens an invitation directly to that movie. Access is verified; Join SharePlay aligns Casey to the latest group position, now 24:18, with app-owned microphone off. Alex and Bea continue uninterrupted. Casey's subtitles remain on. Choosing Leave SharePlay stops Casey's transmission and membership only; Alex and Bea continue. Casey can rejoin at the new current time. Drew sees the access prerequisite, can sign in/restore or review actual access options, and can close without affecting anyone. If Alex deliberately chooses End for Everyone, the explicit confirmation explains its group effect before any termination is sent.

## Acceptance checks and evidence limits

**Passed — static specification inspection:** all four brief concerns have explicit revised contracts; join/cancel/access failure/leave/rejoin/end paths have outcomes; shared and personal state are separated; the pseudocode contains no join-time shared seek or leave-time session-end fallback. These are document checks only.

**Failed — supplied baseline against this specification:** automatic microphone broadcast, late-join group restart, and leave-triggered group termination. These failures are reported from `interface.md`, not observed on devices. Lack of content access is a known condition; a defective recovery UI cannot be inferred because none was supplied.

**Not executed — implementation acceptance scenarios:**

1. Join with microphone permission absent, denied, and already granted: app-owned audio remains off and viewing works. Cancel during permission resolution: no late capture. Existing system call: join never changes its mute state.
2. Join while two other players advance: only the newcomer seeks to the latest timeline; group receives no restart. Deliberate shared pause identifies its actor; personal volume/subtitle changes affect only their owner.
3. Missing entitlement, restored purchase, purchase cancellation/pending, regional restriction, and network error follow distinct paths. Access success after the session ends offers no stale join.
4. Cancel a slow join, then deliver its success callback: no lingering membership or audio. Repeat Join/Leave/End requests: one logical operation each.
5. Participant and organizer each leave: others continue. Rejoin uses current position and preserved personal preferences. Offline leave cannot reconnect or unmute in the background.
6. End confirmation: Cancel, keyboard escape, remote cancellation, and Return without selection do not terminate. Explicit confirmation ends once; stale organizer authority and network failure recover honestly.
7. iOS interruption, rotation, enlarged text, and Picture in Picture preserve context. tvOS remote traversal has visible focus and no dead ends; viewer change clears previous account access. visionOS entry/return works in a window with resting indirect input; optional spatial participation keeps positions stable and supports non-Persona participants.

No implementation, SDK compilation, entitlement transaction, synchronization, device, GUI, native input, assistive-technology, or accessibility execution occurred. Physical comfort, focus behavior, rendering, permission prompts, and platform/API availability remain unverified. The local HIG articles are derived snapshots dated 2026-10-25, not SDK references or proof of independent source review. Only local files and installed instructions were consulted; official links identify provenance and were not browsed. No newer-release or commercial-policy claim is made.
