# Revised interaction specification

Scope: optional leaderboards and asynchronous friend challenges for the iOS/tvOS puzzle game described in `interface.md`. This is a framework-agnostic design contract, not an SDK implementation. Existing solo puzzle mechanics remain the primary task. Scoring details below are explicit product decisions because the brief provides no scoring rules.

## Decisions and source basis

1. **Solo play is immediately available.** Home offers Play Solo first, then Leaderboards and Challenges. A launch-time capability/sign-in status check may initialize an available integration, but never waits in the solo path or repeatedly presents authentication. Authentication is offered when the player selects a social action. Cancel, unavailable authentication, and no network return to usable solo play. This reconciles the guide's launch initialization advice with a smooth start; initialization is not a login gate. [Game Center — Accessing Game Center](https://developer.apple.com/design/human-interface-guidelines/game-center#Accessing-Game-Center).
2. **Only verified, acknowledged results receive a rank.** Local scores are labelled Local result; pending submissions say Awaiting verification. Never infer “global champion” from a local score or a successful upload request. This validation policy is a product integrity decision, not an asserted HIG server-security requirement. Classic boards support lasting best scores; recurring boards give renewed opportunities. [Game Center — Leaderboards](https://developer.apple.com/design/human-interface-guidelines/game-center#Leaderboards).
3. **Friend challenges use short, comparable attempts.** Use a fixed puzzle/rules version, approximately three-minute attempts, and the latest completed eligible attempt, not lifetime progress or personal best. Invitations resolve to that exact challenge after necessary teaching. [Game Center — Challenges](https://developer.apple.com/design/human-interface-guidelines/game-center#Challenges).
4. **Publish a public player alias, never private real names.** Explain what becomes visible before the first publication. Request no contacts access for this design; an available provider-owned friend picker supplies authorized recipient identifiers. Minimize collection and maintain accurate privacy disclosures. Alias-only display is this product's concrete application of the privacy guidance. [Privacy — Best practices and Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices).
5. **Keep social UI outside active gameplay.** Prefer a supported provider-owned Game Center entry in main/settings menus; reserve its collapsed/expanded area. Pause before opening social UI from a pause menu and require explicit Resume afterward. iOS integration may open an overlay; tvOS uses a full-screen dashboard. If no integration exists, expose an honest unavailable state rather than simulated sign-in. Use official localized Game Center names and unchanged artwork if supplied. [Game Center — Integrating the access point and Using custom UI](https://developer.apple.com/design/human-interface-guidelines/game-center#Integrating-the-access-point).

## Screens and transitions

**Home:** Play Solo, Leaderboards, Challenges, Settings. Show current public alias only when authenticated; otherwise “Playing locally.” Play Solo opens/resumes the local puzzle regardless of social state.

**Social entry:** If unavailable, show “Online competition is unavailable. You can still play solo,” with Retry, Play Solo and Back. If signed out, show “Sign in to view rankings and challenge friends,” with Sign In, Play Solo and Back. Sign In invokes the supported authentication adapter. Cancellation returns here without another prompt. Successful authentication returns to the requested board/challenge, not Home. No custom screen impersonates a system permission alert; any actual protected-data permission uses its proper system flow.

**First publication:** Before submitting or sending an invitation, show an ordinary publication review: “Share as [public alias]. Your alias and verified score will be visible on this leaderboard,” or “Your alias and challenge results will be visible to invited players.” Show the actual audience and actions Submit Score/Send Challenge and Cancel. This is a product sharing choice, not a pre-permission prompt. Cancel preserves the local result/draft. Do not silently expand the audience later.

**Leaderboards:** Start with “Weekly Puzzle,” current date range, explicit “Global” or “Friends” scope, rules summary, last updated timestamp, and the player's verified row if available. A secondary “All-Time” board retains best eligible scores for its own fixed ruleset. Rows contain rank, public alias, score and “You” where applicable. Empty means “No verified scores yet”; missing player rank means “No verified result for this board,” never rank zero. Loading, unavailable, empty and loaded are distinct states. Retry is explicit; Back always works. Cached boards say “Saved rankings · updated [time]”; cached ranks cannot trigger a new winner celebration.

**Puzzle completion:** Show local score and Next Puzzle first. Offer Submit Score when authenticated/online, Sign In to Submit when signed out, or “Offline · result saved locally.” Only explicitly approved submissions can retry automatically; unapproved local history is never backfilled. Signing in later does not publish earlier games. Rejected results remain local with “This result could not be verified” and Play Again; transport failures offer Retry without claiming verification failed.

**Challenge creation:** Challenges → New Challenge → choose supported puzzle → choose authorized friends → review puzzle, rules, alias, recipients, and closing time → Send Challenge. Proposed duration: 24 hours, fixed by the server at creation. No invitation is sent until Send succeeds; loading disables duplicate sends and preserves Cancel/Back. Failure keeps the draft and says “Not sent”; retries use the same operation identifier. Empty friend list offers Back and a supported Add Friends route if available, with no demand for contacts permission.

**Challenge invitation:** Resolve a stable challenge ID to authoritative details. Show inviter's public alias, puzzle, rules, time remaining and audience, with Play Challenge, Decline and Back. Never auto-start. If first-time teaching is necessary, say “Learn the rules, then continue to [challenge]”; retain the destination and recheck availability afterward. Expired/deleted/inaccessible invitations show their specific state and offer Play Solo and Back, never an unrelated challenge. If a solo puzzle is underway, preserve it and enter the challenge only from a safe pause/confirmation point.

**Challenge play/results:** Start a server-issued eligible attempt online. Offline users may Practice the same downloaded puzzle, clearly excluded from rankings. Completed attempts say Awaiting verification until acknowledged. After confirmation, show “Latest verified attempt: [score]” and provisional standing with timestamp. A failed newer submission does not replace an older verified score; show both states explicitly. At closing, show final standings only after the server confirms closure and validation. Equal scores share rank. “No completed attempt” is distinct from zero. Rematch creates a new challenge, never reopens an expired one.

## Scoring and asynchronous state contract

Product scoring choice: one point per correctly solved puzzle cell at completion; no speed tie-break. Same puzzle seed, rule version, time allowance and declared assistance category compete together. Solo remains usable with accommodations; differing competition rules use separate boards with clear labels. Server-authorized competitive rules must be finalized before release.

Weekly board: best verified score during the displayed server-defined UTC week; show localized dates/time zone. All-Time: best verified score for that board's rules version. Challenge: latest completed eligible attempt ordered by server-issued attempt sequence, not network arrival order. An abandoned attempt is not completed. A newer lower score replaces the older score after verification. The attempt lasts at most three minutes and must complete before the challenge deadline; explain this before starting. Server enforcement and any recovery allowance require implementation validation.

Abstract operations (no assumption of GameKit or any Apple SDK):

```text
socialCapability = unavailable | signedOut | authenticated(playerId, generation)
submission = local | approved | sending | awaitingVerification |
             verified(score, boardId, rankSnapshot, snapshotTime) |
             transportFailed | rejected(reason)

startSolo(): openLocalPuzzle()  // no dependency on socialCapability
openSocial(destination): preserve destination; check capability; render appropriate state
submit(result, audience): require explicit approval + bound authenticated identity
  send once using stable submissionId and attemptId
onResponse(response):
  ignore if identity/generation differs from current session
  update only the corresponding submission; never infer a rank
  render rank only from an authoritative verified ranking snapshot
onRetry(): reuse operation ID; do not create another attempt or invitation
onViewerChange(): increment generation; cancel old requests; hide old personal data;
  partition caches, drafts and outbox by identity; load matching profile or local guest
```

Backend requirements: authenticate ownership; validate puzzle/rules/attempt eligibility and score; reject duplicate/replayed or altered results; enforce deadlines and deterministic ranking. Verification rejection and network failure are different outcomes. Reconnecting processes only approved, identity-bound, still-eligible operations. Never send another household member's queued result under the new viewer. On an unresolved timeout, query the operation ID before reporting “Not sent” or enabling a duplicate invitation.

## Platform interaction and access contract

| Concern | iOS | tvOS |
|---|---|---|
| Primary interaction | Touch; labeled actions with 44 × 44 pt activation areas as the default design target | Siri Remote directional navigation and deliberate Select press; 66 × 66 pt default control target |
| Navigation | Preserve system Back/swipe-back; explicit Back available without a custom gesture | Back opens parent; gameplay Back pauses; Back from pause resumes; explicit Exit to Menu leaves play; root Back and holding Back retain system behavior |
| Restoration | Preserve puzzle, board scope/scroll, challenge destination and draft across interruption/orientation | Preserve route and focus within the current profile; viewer changes clear personal social content before showing the new profile |
| Presentation | Frequent actions toward comfortable middle/lower reach; reflow portrait/landscape | Large legible rows, room for focus enlargement; no pointer hover dependency |

Sources: [iOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices), [tvOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos#Best-practices), [Remotes](https://developer.apple.com/design/human-interface-guidelines/remotes), [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility). These targets retain the guide's platform units and default scope, rather than treating smaller stated minima as recommended density.

TV focus map: Home is a vertical list starting at Play Solo. Up/Down moves one action; Select enters. Board screen is a vertical sequence: scope control → board selector → scrollable rows → Retry when relevant → Back. Left/Right changes focus among scope options; Select commits the scope and refreshes. Moving focus alone does not send, authenticate or switch scope. Challenge review is a vertical sequence of recipient controls → Send → Cancel. All branches have a parent exit; return restores the invoking control. Distinguish focused, pressed, selected and unavailable. If a focused row disappears during directional navigation, choose its nearest surviving neighbor; asynchronous refresh must otherwise avoid stealing focus. [Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices).

Labels and status must survive at least 200% text sizing; rows expand vertically instead of clipping aliases, scores or actions. Use 17 pt iOS and 29 pt tvOS default body sizes as starting points from the supplied guide. Status uses text, not color/sound alone. Reading order is heading, rules/audience, result/status, primary action, secondary actions. Every control exposes a meaningful name, role, state and activation; rows expose rank, alias, score and whether they represent the player. Persistent failures do not disappear on a timer. Validate contrast in both appearances and Increase Contrast, and test the complete flow with supported assistive input. These are requirements to test, not claims of accessibility execution. [Accessibility — Vision, Mobility and Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility).

## Data-purpose contract

| Data | Purpose and exposure | Boundary |
|---|---|---|
| Local puzzle/progress | Solo restoration on device | No social upload without approval |
| Provider player identifier | Ownership/authorization | Internal only; not a displayed real name |
| Public alias | Public board or named challenge audience | Use only provider-authorized public alias; absent alias becomes “Player”; never fall back to private real name/email |
| Score, rules version, attempt ID, validation evidence | Verify and rank approved attempt | Publish only alias/score/rank; keep validation evidence private |
| Authorized friend IDs, challenge membership | Deliver selected invitations and limit result visibility | No bulk contacts collection or public membership list |

Do not fetch private real names for this feature. Apply the alias-only projection to rows, invitations, error text, cached payloads and analytics; redact personal identifiers in logs. Retention/deletion rules and privacy disclosures must be completed against the eventual backend before release; this specification does not assert a legal retention period or guarantee removal from provider-owned records.

## Worked before → after

**Before (supplied proposal):** An offline player must log in before playing solo. A local score is posted as global champion without verification, with a private real name visible publicly.

**After (illustrative score 42):** Launch offline → Play Solo immediately → complete puzzle → “Local result: 42” and Next Puzzle. Reconnect → select Submit Score → authenticate or cancel without losing the result → review “Share as PuzzleFox · visible globally” → approve → Awaiting verification. A network timeout shows Retry, retaining the operation ID. Verification succeeds and an authoritative snapshot reports “Weekly Puzzle · Global · tied rank 8 · 42 · updated [time].” No champion claim appears. If verification rejects the score, it stays local. A later friend invitation opens its exact puzzle and uses the latest verified attempt for that challenge; it does not import the 42-point weekly best.

## Acceptance checks and evidence limits

**Passed — static specification checks:** The supplied brief was read; all three observed defects have explicit replacements. This document defines solo/auth separation, verified ranking, alias-only public identity, challenge routing, offline/cancel/failure recovery, and iOS/tvOS differences. Installed root, selected family procedures, topic procedures and supporting local guides were read in that order per route. Official links above identify source guidance; they were not browsed.

**Failed — supplied proposal at specification level:** Solo availability under failed authentication; truthful ranking for an unverified result; private-name protection. These findings follow directly from `interface.md`, not a runtime test.

**Not executed — implementation acceptance scenarios:**

- Cold launch with network/auth unavailable: Play Solo completes a puzzle; cancelling login returns to the original social destination without prompting again.
- Submission timeout, duplicate retry and delayed response: one submission exists; no unverified rank appears; rejected and transport-failed states differ.
- Verified scores tied at the top: show tied rank 1 only for the identified board/period and timestamp, never an unqualified global champion.
- Newer lower challenge attempt arrives before an older attempt response: latest eligible attempt wins by sequence; older responses do not overwrite it.
- Invitation during solo play, first-use tutorial, expiration during tutorial, and offline entry: preserve solo state, retain exact destination, recheck deadline, offer explicit practice/exit where applicable.
- Cancel/send timeout/retry: no unintended invitation or duplicate; recipients and public alias match the review.
- Change tvOS viewer with a request in flight: prior personal content disappears, old response is ignored, old outbox cannot publish as the new viewer.
- Inspect all public payloads and presentation paths with a fixture containing private names/email: neither leaks; missing public alias uses “Player.”
- Traverse every TV direction/Select/Back route, including empty/error screens and row removal; focus is visible, reachable, distinct from selection, and does not trigger actions by movement.
- Resume after interruption and rotate iOS; enlarge text to 200%; verify essential content/actions, state restoration, activation geometry, contrast, remote legibility and supported assistive-input completion.

Only a brief and local guidance were supplied. No executable app, backend, screenshots, SDK, device, GUI, authentication session, remote or accessibility execution was used. Backend validation, provider feature availability, focus engine behavior, system UI, touch comfort, contrast, geometry and assistive technology remain unverified. The installed guides are dated local summaries (retrieval stated as 2026-10-25), not API documentation or independently verified current platform support. Integration must capability-check real support and verify APIs on the eventual target; this contract remains usable when no Apple SDK is available.
