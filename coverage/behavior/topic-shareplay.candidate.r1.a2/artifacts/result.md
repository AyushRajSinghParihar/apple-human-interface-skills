# Shared movie watching: revised interaction specification

This design replaces the behaviors stated in `interface.md` for iOS, tvOS, and visionOS where shared watching is supported. It is a framework-agnostic contract, not an SDK implementation. Product choices below apply the installed HIG snapshot; exact labels, state arbitration, and recovery policies are design decisions rather than quotations of Apple requirements.

## Decisions and source basis

1. **Joining never starts microphone capture or transmission.** Watching works without microphone permission. This version uses communication controls owned by the system call experience; it does not add an app microphone channel. Joining or leaving the movie must not change an existing call's mute state or end that call. Explain on entry: “Joining shares movie playback. Your call and microphone controls stay separate.” If an app-owned voice feature is added later, it needs a separate explicit action, permission at that moment, and a specific purpose string before capture. This follows data minimization and contextual permission requests in [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission). The no-auto-broadcast policy is this design's stronger product decision.
2. **Late arrivals follow the current group position.** Join, rejoin, access recovery, and buffering completion never emit a restart, seek, or pause command. Playback position, play/pause, and explicit seeks are shared; volume, captions/subtitle language, audio description preference, and other accessibility settings remain personal. Explain shared transport effects and identify the initiator, for example “Alex paused for everyone.” See [SharePlay — Best practices](https://developer.apple.com/design/human-interface-guidelines/shareplay#Best-practices) and [Designing shared activities](https://developer.apple.com/design/human-interface-guidelines/shareplay#Designing-shared-activities).
3. **Leave affects only the departing person, including the initiator.** There is no app “End for Everyone” command in this revision. The group continues until the last participant leaves or the underlying session ends externally. A last-person leave closes the empty activity. This avoids the supplied ambiguous, group-wide exit; clear leave/rejoin is supported by the same SharePlay guidance. Removing group termination is a product scope decision, not a claim that HIG prohibits it.
4. **Check each participant's access.** An invitation does not grant a rental, purchase, subscription, or regional license. Necessary prerequisites are dismissible; optional profiles and onboarding wait. See [SharePlay — Best practices](https://developer.apple.com/design/human-interface-guidelines/shareplay#Best-practices). Existing customers get sign-in/restore before repurchase; any paid offer must show actual localized terms and use the genuine purchase confirmation, following [Apple In-App Purchase](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Making-signup-effortless). No prices or availability are supplied, so this specification invents none.

## Screens and action contract

**Entry:** Movie details offer a recognizable **SharePlay** action. Invitations from app UI, a supported system route, or a link resolve to the specific movie and activity, never a generic home screen. The invitation includes accurate artwork, movie title, and “Watch together.” Prepare the movie-detail return destination immediately, including for a quick exit.

**Join view:** Show title/artwork, available participant context, session status, and “Playback controls affect everyone. Volume and captions are yours.” The primary **Join Movie** action is available after access and capability checks. **Not Now** dismisses to the originating context without joining. Do not request microphone access. A loading access check reads “Checking access…” and retains an exit; it must not pretend access is denied while unresolved.

**Access required:** Replace Join with the applicable **Sign In**, **Restore Purchases**, or **View Access Options** action. Show “You need access to [movie] to watch together.” Any actual offer must identify included content, complete billed amount and duration, trial/subsequent billing where relevant, and Terms/Privacy. **Not Now** remains available. Canceling authentication or purchase returns here without joining or altering the group. Successful recovery rechecks entitlement and session existence, then returns to a ready Join view. Unsupported device/content/region gets an accurate explanation and **Back to Movie**; never charge for access that cannot enable this session.

**Joining:** Join becomes **Joining…**, with activity feedback and duplicate activation suppressed. Keep **Cancel Joining** available. Obtain the latest group snapshot after readiness, then align locally before showing synchronized playback. Do not show an old resume position as the group's position. If the session has ended, show “This watch session ended” with **Watch on My Own** (only with access) and **Back to Movie**. Solo playback is a fresh explicit choice, not an automatic fallback.

**Watching:** Standard playback controls remain familiar; prefer a system player when an eventual implementation can supply one. Keep a discoverable **Session Details** button within one action of playback. It opens an in-app destination containing status, participants, the shared-controls explanation, and **Leave Movie**. **Back to Movie** returns to the player without leaving. These are navigation destinations, not permission pre-alerts. See [Playing video — Best practices](https://developer.apple.com/design/human-interface-guidelines/playing-video#Best-practices).

**Leaving:** Session Details says “Leave this movie? Others will keep watching. Your call stays connected.” **Leave Movie** is a secondary, explicitly activated local command; it is not bound to a generic Back or automatic default activation. It needs no additional confirmation because it affects only the person and allows rejoin. Immediately stop local movie output, detach shared transport, and return to movie details. Show persistent status “You left the movie” with **Rejoin Movie** while the session exists and **Watch on My Own** when entitled. Neither starts automatically. Rejoin uses the same checks and current group position as Join. Local saved position is updated without writing it to the group.

All action labels are also their accessible names; actions have button semantics, enabled/busy states, visible focus and activation feedback. One primary action per destination; secondary exits stay reachable. Delayed actions retain context and resolve to success or an actionable error. These choices follow [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Style).

## State and concurrency contract

```text
states = outside, checking, accessRequired, ready, joining,
         watching, reconnecting, left, ended, unavailable
shared = {sessionId, movieId, revision, position, rate, timestamp, participants}
personal = {volume, captions, audioDescription, accessibilityPreferences,
            returnRoute, savedSoloPosition}

openInvitation -> checking -> ready | accessRequired | ended | unavailable
JoinMovie when ready -> joining (new attempt token)
onReady(token):
  reject if token was canceled or superseded
  revalidate access; fetch current session snapshot
  align local player to snapshot; attach as participant -> watching
  emit no group transport command
CancelJoining:
  invalidate token; detach any provisional membership -> ready
  late callbacks cannot attach or start output
explicitPlayPauseOrSeek when watching:
  submit ordered command(sessionId, expectedRevision, actionId, actor)
  apply authoritative accepted snapshot; never replay stale commands after reconnect
LeaveMovie:
  invalidate attempts; stop local output; disable command submission
  detach local membership idempotently -> left
  emit no group end, pause, restart, or seek command
```

The session coordinator serializes simultaneous transport commands and increments revisions; participants follow its accepted order. Joiners do not become transport authorities merely by arriving. Show actor attribution for accepted shared changes; keep current status available in Session Details rather than relying only on a fleeting message.

On connection loss, stop stale local playback, show “Reconnecting…” and offer Leave Movie. Reconnection fetches the latest snapshot and aligns locally; it never replays old transport requests. A failed join shows **Retry** and **Back to Movie**. A failed remote detach still leaves local playback and command submission disabled; retry cleanup idempotently and show “Disconnected locally; session update pending” until acknowledged. If content access expires, stop that person's output, detach them, and offer access recovery without a group command. A player integration that necessarily pauses the group during buffering must disclose and attribute that behavior; do not claim it is eliminated without runtime evidence.

## Platform presentation

| Platform | Entry, navigation, and return |
| --- | --- |
| iOS | Touch-accessible Join and exits; preserve swipe-back and selected movie through rotation/interruption. Back from Session Details returns to playback without leaving. Support continuing shared video in Picture in Picture where available. Preserve session and personal settings on app switching. |
| tvOS | Large readable destinations with visible focus. Join view focus order: Join/access action → Not Now; directions reverse to return. Session Details: Back to Movie → Leave Movie; return focus to Session Details in the player. Back dismisses Session Details; Back out of playback opens movie details while membership remains visibly active with Resume Movie and Session Details. Never terminate the group through Back. Actual remote behavior remains to be verified. |
| visionOS | Entry and session management use an ordinary movable window; playback begins by choice in a modest resizable window. No forced immersion or custom seating is added. Standard-window sharing is screen mirroring through the window-bar Share button; do not conflate that with synchronized, independently entitled movie playback. Expose this flow only when the actual capability supports it. Any later immersive/volume SharePlay design needs a separate spatial arrangement and consent specification. Resting indirect input and supported pointer alternatives must reach every action. |

Platform basis: [iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices), [tvOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos#Best-practices), [visionOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos#Best-practices), and [SharePlay platform considerations](https://developer.apple.com/design/human-interface-guidelines/shareplay#Platform-considerations). Missing platform-specific guidance does not prove feature availability.

For custom controls, design activation areas of at least 44 × 44 pt on iOS, 66 × 66 pt on tvOS, and 60 × 60 pt on visionOS, without overlap. The tvOS value uses the local accessibility guide's platform default rather than the buttons guide's general 44 pt floor. Keep visionOS control centers at least 60 pt apart. These are specification targets, not measured results. At 200% text size, reflow entry/status/actions without truncating essential copy. Pair status symbols/colors with text; preserve personal caption and description preferences. Follow [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) and [Buttons — visionOS](https://developer.apple.com/design/human-interface-guidelines/buttons#visionOS).

## Worked before/after

**Before, from the brief:** Alex and Bo are watching. Casey joins late: Casey's microphone broadcasts and everyone's playback restarts. Casey leaves: everyone's session ends without warning. Dana lacks content access; no recovery behavior is supplied.

**After, illustrative trace:** Alex and Bo are at 32:10. Casey opens their invitation, sees the specific movie and shared-control explanation, passes access checks, and selects Join Movie. Readiness completes when the group is at 32:14; Casey aligns to that current point with no restart command and no microphone change. Casey's captions remain enabled while Bo's remain off. Alex explicitly pauses; everyone follows the accepted pause and sees “Alex paused for everyone.” Casey opens Session Details and selects Leave Movie. Casey returns to movie details; Alex and Bo remain paused in their existing session, and Casey's separate call is unchanged. Rejoining follows the group's then-current position. Dana sees Access Required, can sign in/restore or inspect real access options, and can dismiss without affecting anyone. This is a specified walkthrough, not an executed multi-device test.

## Acceptance checks and evidence limits

**Passed — static specification inspection:** Each of the brief's three harmful behaviors has an explicit replacement. Entitlement failure, dismissal, duplicate joins, canceled late callbacks, reconnect, expired access, initiator departure, last-person departure, and ended sessions have defined outcomes. Shared versus personal state and platform return paths are stated. The worked trace is consistent with these contracts.

**Failed — supplied behavior against the revised contract:** Automatic microphone broadcast; restart on late join; group termination on individual leave. These failures are established by `interface.md`'s description, not observed runtime execution. No access-recovery defect can be established beyond its missing specification.

**Not executed — implementation acceptance gates:**

- With two established viewers and one late joiner, assert no join/rejoin/cancel path emits a shared transport mutation; the joiner aligns to the newest revision, including a concurrent seek.
- Exercise microphone permission denied, previously granted, and an already active call. Joining neither captures audio nor changes call mute state; watching remains usable. Leaving the movie leaves the call unchanged.
- Leave as initiator, ordinary participant, and last participant. Only local membership/output stops; others retain position, transport, and personal settings. Rejoin reaches current group state.
- Test missing/expired entitlement, canceled purchase, restored access, unsupported region/device, stale invitation, network loss, and rapid duplicate activation. No unexpected charge, playback, stale attachment, or group restart occurs.
- Traverse every destination with remote and supported assistive inputs; verify names, states, focus order, Back behavior, focus restoration, and no unreachable exits. Check 200% text, real hit geometry, contrast in light/dark and Increase Contrast, and captions/audio descriptions. No essential information may depend on color, sound, speech, or a timed message alone.
- On iOS test portrait/landscape, PiP, interruption/resumption, and quick exit. On tvOS test across-room legibility and remote traversal. If interactive overlays pause media, honor the video guide's minimum 0.5-second delay and verify shared consequences. On visionOS test resting input, pointer alternatives, window sharing versus actual synchronized playback, and comfort without forced immersion.

Only supplied local text and installed instructions were read; no web browsing occurred. Official links identify the source articles cited by the local snapshot, not independently checked current pages. There is no implementation, SDK availability evidence, entitlement service, device, GUI, accessibility execution, audio-capture inspection, or synchronization measurement in this work. All runtime gates remain pending; source existence does not establish independent source review or platform feasibility.
