# Launch and resume repair

Patched interface.md in place with a concrete iPhone state specification. It removes the repeated 12-second animation, replaces misleading launch content with a static appearance-matched structure, restores reading context, and defines usable cached, sample, pending, partial-success and failure states.

## Decisions and rationale

- Launch ends at useful interaction, not completion of an animation. Refresh and images run independently. This applies [Launching: Best practices](https://developer.apple.com/design/human-interface-guidelines/launching#Best-practices) and [Loading](https://developer.apple.com/design/human-interface-guidelines/loading).
- The system launch screen has no fake Sign In button or yesterday headline. Actual dated content belongs in the running app. This applies [Launching: Launch screens](https://developer.apple.com/design/human-interface-guidelines/launching#Launch-screens).
- Foreground entry preserves the open article and position; process restart restores saved IDs/anchors. A fresh external destination wins over saved navigation. The detailed precedence and missing-record fallback are product decisions applying the restoration guidance in [Launching](https://developer.apple.com/design/human-interface-guidelines/launching).
- Cached text stays readable offline and during failed refreshes. Bundled, clearly labeled sample stories give first-install offline users something usable; they never masquerade as current news. This follows the initial-content guidance in [Onboarding: Additional content](https://developer.apple.com/design/human-interface-guidelines/onboarding#Additional-content).
- No new tutorial or account funnel is introduced. Any later optional tutorial must remember Skip and remain available in Help, following [Onboarding: Best practices](https://developer.apple.com/design/human-interface-guidelines/onboarding#Best-practices). Public reading without an account is an explicit product assumption, not evidence about an existing backend.
- The 15-second request deadline, one automatic recovery attempt, stable-anchor fields and staged feed reordering are proposed engineering/product policies. HIG does not prescribe these numbers or algorithms. They make waits finite and preserve task continuity.

## Worked before/after

Scenario: a person is halfway through cached article A, backgrounds the app, loses connectivity, then returns.

Before, according to the supplied specification: every foreground entry imposes an unskippable 12-second animation. The launch screen depicts Sign In and yesterday's headline. Offline launch stays blank despite cached stories. The supplied text says nothing about restoration, so loss of article position cannot be asserted as an observed behavior.

After, by the revised contract: a warm resume keeps article A at its reading anchor without an app-owned splash. Its cached text remains readable, with an offline saved-content status and truthful dates. If the process was terminated, a cold launch uses the static system launch screen and then restores A and its anchor from local state. Refresh failure never removes A. If this entry instead requests article B through a fresh link, B takes precedence; when uncached and offline, B's unavailable state offers Retry and access to saved stories rather than silently opening A.

## Acceptance checks

Status below distinguishes document inspection from execution. All runtime cases remain required implementation checks.

| Check | Expected result | Status |
|---|---|---|
| Required artifact edit | interface.md replaced with concrete revised transitions, dependencies and recovery policy | Passed: file inspection |
| Original defects addressed | No timed foreground animation; no fake launch controls/headline; cached offline content specified | Passed: file inspection |
| Cold and warm start | First-use feed/sample content; warm screen preserved; terminated process restores article/feed anchor | Not executed |
| Offline and slow network | Cache remains usable; first install has labeled samples; missing-content failure has Retry; deadline resolves pending wait | Not executed |
| Partial success and refresh | Text available before images; failed update retains content/date; success replaces status truthfully | Not executed |
| Retry and interruption | One active request; repeated failures recover to Retry; late responses cannot overwrite newer destination | Not executed |
| Restoration exceptions | Missing anchor uses defined fallback; missing article explains loss; fresh external target wins | Not executed |
| Appearance and rotation | System launch and initial screen match in light/dark and every supported orientation | Not executed |
| First/returning/skipped users | No mandatory startup tutorial; any future tutorial honors persisted Skip and Help access | Not executed; future tutorial conditional |
| Optional setup denied | No startup permission prerequisite or repeated optional prompt; reading remains available | Not executed |
| Timing | Measure cold launch to first useful interaction and warm resume on actual supported hardware, online/offline | Not executed; no measured launch time |

Failed checks: none established by execution. The original supplied specification contains the three reported design defects; the revised document's inspection checks pass. Runtime pass status is not implied.

## Evidence and limits

Only local files were used; no web browsing occurred. Explicitly read the installed apple-hig root SKILL.md, searched references/topic-index.md, then read the Patterns family, Launching/Loading/Onboarding topic procedures, and their corresponding source guides, in that order before composing the revision. Each file read used a separate cat or rg command. Paths resolve under `.agents/skills/apple-hig/`; the source guides record snapshot date 2026-10-25. Official links above identify the source guidance; they were not fetched or independently checked for current changes.

The original interface.md was a single paragraph. It provides no framework, code, screenshots, cache schema, supported orientation set, account policy, timing trace, or runtime evidence. Sample packaging and account assumptions need implementation follow-through. This work changes a specification only: no device, SDK build, GUI, network simulation, native rendering, accessibility, VoiceOver, or persistence execution was performed. Accessibility and interaction quality require subsequent implementation validation; this report makes no accessibility conformance claim.
