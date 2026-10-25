# Optional puzzle competition: revised interaction specification

## Decisions and source basis

Targets: iOS/tvOS from interface.md. This is a framework-agnostic interaction contract, not an SDK implementation. The supplied proposal contains no screens, scoring rules, backend or code. Concrete scoring and validation choices below are product decisions, not claims about Game Center APIs.

1. **Play Solo is always available.** Home orders Play Solo, Leaderboards, Challenges, Settings. Include a playable puzzle locally. Check social authentication/capability at launch without waiting to enable play; defer interactive authentication to an explicit social action in a safe menu. Canceling or failing authentication returns to solo without repeated prompts. This reconciles checking at launch with a smooth start. [Games: first play](https://developer.apple.com/design/human-interface-guidelines/designing-for-games#Jump-into-gameplay), [Game Center access](https://developer.apple.com/design/human-interface-guidelines/game-center#Accessing-Game-Center).
2. **Social play is opt-in.** Browsing a board does not enroll the player or upload historical solo scores. Prefer supported system Game Center UI/access point when an adapter can provide it; place access in main/settings menus with room for expanded forms, never gameplay or splash/tutorial screens. Pause gameplay before opening social UI. Without an integration, explain competition is unavailable and retain solo. Never imitate system authentication. [Access point guidance](https://developer.apple.com/design/human-interface-guidelines/game-center#Integrating-the-access-point).
3. **Local score is not a rank.** Client calculations remain “Local score.” Only authoritative acceptance and a separate scoped rank response permit “Rank 1 · Weekly board · updated [time].” Never label an unverified score “Global champion.” Verification and this wording are product decisions addressing the brief.
4. **Public identity uses only a service-authorized public alias.** Never derive it from private names, contact labels or email. Missing alias renders “Player.” This alias-only policy is a product decision applying [privacy data minimization](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices).

## Revised screens and routes

**Solo:** Home → Play Solo → puzzle → result. Result prioritizes Next Puzzle and Play Again, with optional Leaderboards/Challenges below. Save puzzle progress on interruption. Solo results stay local; competition uses separately started attempts under disclosed rules.

**Leaderboards:** Show board name, rules/difficulty, scoring direction, period/time zone and last refresh time. Product decision: default Weekly board runs Monday 00:00 UTC to next Monday and retains the best verified competitive attempt. A separate classic All-Time board retains the best verified result indefinitely. Never mix incompatible rules or unequal puzzle difficulty. Rows show rank, public alias, score and “You” for the current player. Friends/Everyone scopes are explicit where supported. Empty state: “No verified scores yet,” with Play Ranked Puzzle when available. Recurring versus classic types follow [leaderboard guidance](https://developer.apple.com/design/human-interface-guidelines/game-center#Leaderboards).

**Play Ranked Puzzle:** Before Start, display exact puzzle, scoring, period, public identity and submission visibility; offer Back. Product scoring choice: fixed seed and rules version; fewest moves wins; equal scores share rank. Purchases and lifetime progress cannot affect the result. Start records a unique attempt ID and replayable move sequence. No retroactive solo upload.

**Challenges:** List received invitations and joined challenges with puzzle, inviter’s public alias, deadline with time zone, latest verified attempt and status. Create Challenge chooses a fixed puzzle designed for approximately 1–5 minutes, eligible friends via an authorized selection flow, then Review. Product deadline: 24 hours after creation. Review shows recipients, puzzle, score rule, deadline and sender alias; Send Challenge is deliberate. Cancel discards the unsent draft; failure retains it for retry. No contacts import is needed.

Invitation links contain an opaque challenge ID resolved against authoritative details. They open that exact challenge, never generic Home. Detail offers Accept and Play, Not Now, Decline. If teaching is needed, say “Learn the moves, then play this challenge,” preserve destination, finish the local tutorial and return to detail for Start. Authentication never automatically begins an attempt. Expired/invalid links explain the state and offer Solo/Home.

Challenge participants receive the same puzzle and rules. Use the **latest completed, verified attempt**, even if worse, rather than lifetime or personal-best scores. Starting or abandoning a retry does not replace the prior result. Before retry: “Your next verified result replaces your current challenge score.” Ties share rank. Product deadline rule: authority must receive a valid completed attempt before the deadline; disclose this before Start. Offline completions remain practice unless received and accepted in time. Do not announce a winner until final standings are confirmed. Short skill attempts, latest-attempt scoring and precise destinations follow [challenge guidance](https://developer.apple.com/design/human-interface-guidelines/game-center#Challenges).

## Availability and score state contract

| State | UI and recovery |
|---|---|
| Checking | Solo enabled; social view says “Checking competition availability…” and retains Back. No blocking launch overlay. |
| Signed out | “Sign in to Game Center to compare scores and challenge friends.” Sign In / Back to Solo. Cancel preserves originating context. |
| Authentication failure | Plain failure message, Try Again / Back to Solo. No automatic prompt loop. |
| Offline | Solo enabled. Cached boards say “Offline · last updated [time].” No fresh-rank claims. Uncached view offers Retry / Back. |
| Available | Load exact selected board/challenge; distinguish loading, empty and error states. |
| Unsupported integration | “Competition isn’t available in this version.” Keep solo. Do not fabricate system UI. |

Framework-neutral pseudocode:

    competitiveAttempt = {
      id, ownerToken, viewerEpoch, puzzleID, rulesVersion,
      boardOrChallengeID, moves, localScore, status
    }
    status = local | pendingVerification | accepted | rejected | expired

    onComplete:
      save locally first
      if authenticated owner matches and network available:
        submit using attempt.id as idempotency key
      otherwise label local; offer eligible retry

    onResponse:
      ignore visible update if viewerEpoch no longer matches
      pending/timeout -> "Submission pending"; query same attempt ID
      rejected -> "Score not counted" + safe reason + Play Again
      expired -> "Deadline passed — saved as practice"
      accepted -> "Score submitted"; fetch authoritative scoped rank
      rank unavailable -> "Rank unavailable"; never infer it locally

Authority validates rules, replay, ownership and deadline; it never trusts client-supplied rank or score alone. Deduplicate retries. Order challenge completions authoritatively so delayed responses cannot replace newer results. Offline ranked/challenge starts are explicitly practice unless a trusted eligibility mechanism is actually implemented. These are required product/backend contracts, not capabilities established by HIG.

## Data and shared-viewer boundaries

| Data | Purpose and boundary |
|---|---|
| Authorized public alias and optional avatar | Competition display; preview before first submission. No private-name fallback. |
| Opaque account/attempt IDs | Ownership and deduplication; never public names. |
| Puzzle, rules, move replay, score | Competitive verification only; solo remains local. |
| Selected friend identifiers | Deliver the reviewed invitation only; no unrelated friend export. |
| Real names, email, contacts | Not needed; do not collect, persist or render for this feature. |

Feature copy: “Competition shares your public player alias and verified score. Solo results stay on this device.” This is ordinary feature information, not a fake permission pre-alert. Ask for any genuinely required access at the relevant action. Define retention/deletion and update privacy disclosures before release; the brief establishes neither. [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy).

On tvOS viewer change: pause play, immediately clear visible social content, recipients, drafts and pending invitation destinations; increment viewer epoch, cancel old requests and reload for the new viewer. Never submit old queued attempts under a new account. Partition prior progress by owner; offer the new viewer their own saved/new solo puzzle. [tvOS viewer guidance](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos#Best-practices).

## Platform interaction contract

| iOS | tvOS |
|---|---|
| Touch activates labeled actions; retain direct puzzle manipulation. Primary actions remain reachable; preserve swipe-back and puzzle/selection/draft across interruption and orientation changes. | Siri Remote alone completes the flow: directional movement targets tiles/actions, deliberate Select activates. No controller required. |
| Use at least 44 × 44 pt touch targets, safe areas and stacked actions for enlarged text. | Start from games guidance defaults of 29 pt text and 66 × 66 pt buttons; validate across-room legibility and room for enlarged focus. |

The local games source has a 28 pt table minimum versus 44 pt iOS touch prose; choose the conservative 44 pt. These units are platform points, not CSS pixels. [Game display guidance](https://developer.apple.com/design/human-interface-guidelines/designing-for-games#Look-stunning-on-every-display), [iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices).

TV focus map: Home vertical actions in the stated order. Social screens arrange Back → scope choices → content rows → eligible primary/recovery action. Up/Down traverses vertical groups; Left/Right traverses horizontal choices; no region traps focus. Select activates scope changes; focus alone never changes context. Persistent selected scope remains distinct from focused/pressed state. Unavailable actions are inactive and skipped with a visible explanation. Empty/error screens retain Back and recovery. Restore initiating focus on return; if removed during directional navigation, use a nearby one-step neighbor.

Back opens the hierarchy’s parent; during gameplay it opens Pause, and Back from Pause resumes. Pause exposes Resume, Restart, Exit to Home. Hold-Back remains system-owned. Controller menus use conventional activation/cancel mappings and glyphs for the active controller. This component-focus model is specified for tvOS, not iOS touch. [Focus](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection), [Remotes](https://developer.apple.com/design/human-interface-guidelines/remotes), [Game controls](https://developer.apple.com/design/human-interface-guidelines/game-controls).

## Worked before / after

**Before, from the supplied proposal:** Offline signed-out Ari cannot enter solo because login blocks it. A client score is posted as global champion and exposes private real names.

**After:** Ari launches offline and immediately completes a solo puzzle in 24 moves. Result says “Local score: 24 moves,” with Next Puzzle first. Leaderboards shows Offline and publishes nothing. Later Ari deliberately signs in, reviews the public alias TileFox and starts the weekly ranked puzzle. A 22-move completion remains “Submission pending” through a timeout. Retrying the same attempt ID receives verified acceptance; a separate ranking response displays “Rank 7 · Weekly board · updated 14:32 UTC.” A friend invitation opens its exact puzzle. Ari’s latest verified challenge attempt of 26 moves replaces an earlier 24-move attempt as disclosed; the weekly best remains governed by its separate rule. A TV viewer switch clears TileFox’s social content before loading the new viewer.

## Acceptance checks and evidence limits

**Passed — specification inspection only:** unconditional solo route; local/pending/accepted distinction; alias-only public identity; exact invitation destination; latest challenge versus best leaderboard scoring; offline/authentication recovery; viewer ownership; platform input and return paths are defined. Installed root, owning families, selected topic procedures and their local references were explicitly read. No web browsing occurred.

**Failed — supplied proposal against this contract:** login gates solo, unverified score claims global champion, private real names appear publicly. These are proposal defects stated in interface.md, not runtime observations.

**Not executed — implementation acceptance checks:**

- Disable networking and sign out: complete a shipped solo puzzle; cancel social sign-in and retain puzzle/context.
- Inject timeout, duplicate/reordered responses, invalid replay and expired submission: no invented ranks, duplicate attempts or stale overwrite.
- Exercise ties, better weekly results and worse latest challenge attempts: verify distinct aggregation using authoritative fixtures.
- Open new-player, expired and invalid invitations: exact valid destination after teaching, or recoverable explanation.
- Seed private names/emails and omit alias: inspect public UI, payloads and logs for leakage. Switch TV viewers during pending requests: no cross-account content or submission.
- Physically traverse every TV state with Siri Remote, including empty/error and disappearing-item cases; verify focus enlargement, Back/Pause, puzzle completion and across-room readability. Test active-controller prompts separately.
- On iOS, check orientations, enlarged text, safe areas, interruption/resumption and touch reach. Perform assistive-technology reading/activation checks once screens exist.
- Validate real authentication, system overlay/dashboard, invitation transport, SDK availability and server verification in supported environments before release.

Evidence is limited to interface.md and the installed dated HIG summaries. Official links identify source sections; they were not fetched. No device, SDK, GUI, backend, network, security or accessibility execution occurred. The specification does not certify accessibility or security. Backend verification, identity-field availability, privacy retention/deletion and integration feasibility remain unproven dependencies. Product scoring and deadline choices are explicit design proposals; HIG does not establish that those services already exist.
