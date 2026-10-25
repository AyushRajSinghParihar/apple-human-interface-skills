# Sound-recognition repair

Patched `interface.md` in place from a one-paragraph defect brief into an implementable iPhone specification. Recognition is now optional, explicitly started, bounded and cancellable. The specification separates possible match, ambiguity, no match, unavailable service and authorization failures. It clears stale candidates, rejects late callbacks, provides manual browsing throughout, and prevents repeated permission requests after denial.

## Decisions and source support

- Sampling stops when sufficient, with a proposed 10-second maximum; processing has a separate proposed 15-second timeout. Neither timing is an Apple requirement or a measured performance result. [ShazamKit — Best practices](https://developer.apple.com/design/human-interface-guidelines/shazamkit#Best-practices) supports stopping after the needed sample.
- Ask through the system only when Identify Exhibit needs access. Denial offers voluntary Settings navigation and browsing; returning never starts listening. Purpose copy names microphone use and its museum benefit. [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission) supports contextual requests and specific explanations; the exact denial recovery is a product decision.
- Treat recognition as complementary, reactive and visible, with privately captured environmental audio. The model's update cadence is unknown; the design promises no training from corrections. Possible Match and a maximum of three ambiguous candidates replace asserted certainty. Confidence percentages and ranking remain withheld pending validation. Manual selection corrects the current task immediately and remains revisable. [Machine learning — Confidence, Corrections and Limitations](https://developer.apple.com/design/human-interface-guidelines/machine-learning) supports this recovery and uncertainty treatment.
- Persistent visual state, accessible control contracts and manual lookup remove reliance on hearing a result or acting quickly. The chosen iPhone target is 44 × 44 pt and the text enlargement check is 200%. [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) supplies these platform defaults and enlargement guidance. [Buttons — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS) supports keeping activity feedback in the initiating button.
- Sample buffers are transient, and no analytics/training reuse is introduced. Remote processing remains an explicit release dependency, not an invented claim of local processing. [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices) supports minimization and preferring on-device work.

## Worked before/after

Before, a visitor launches the app and it listens indefinitely. It guesses “Steam Engine” as certain. At the next exhibit, no match leaves “Steam Engine” visible. After denial, the app repeatedly opens permission requests.

After, launch shows Ready with no capture. The visitor taps Identify Exhibit and grants the contextual system request. One sample ends as soon as sufficient, no later than the proposed cap. Two candidates yield “Several exhibits may match,” with gallery and exhibit numbers; the visitor explicitly opens Steam Engine. At the next exhibit, Try Again clears the previous recognition candidate. A completed attempt with no useful candidate shows No Match with Try Again and Browse Exhibits. Steam Engine remains only in ordinary navigation history. A late callback cannot replace No Match. If access is later revoked, the next action shows Permission Denied, with explicit Settings navigation and manual browsing, without another system request.

## Acceptance checks and results

**Passed — static specification inspection:** The patched artifact contains all four requested repairs, explicit entry/exit transitions, cancellation, bounded capture/processing, ambiguity and unavailable paths, current-attempt identity, permission branches, correction semantics, data boundaries and manual fallback. These are contract checks only.

**Failed:** No specification check failed during this inspection. This is not a runtime pass.

**Not executed — implementation acceptance:**

| Scenario to exercise | Required outcome |
| --- | --- |
| Cold launch, then first Identify tap | No launch capture/prompt; system request only on tap; no capture before grant. |
| Deny, relaunch, retry, return from Settings | No repeated request; browse works; authorization rechecked; grant requires a fresh Identify tap. Restricted status does not promise a Settings fix. |
| Sufficient sample / no sample / slow processing | Capture stops early when sufficient and by 10 seconds otherwise; processing resolves or reaches Unavailable by 15 seconds; no infinite listening. Measure with instrumentation. |
| Cancel, navigate away, lock, background, interruption, revocation | Capture resource released; attempt invalidated; delayed callbacks ignored; no automatic restart or narration. |
| Match A, new attempt, no match; inject old callback | No current A title/image/link/spoken result survives; old callback cannot restore it. History can still contain the manually opened page. |
| Single, multiple, empty and failed recognition responses | Possible Match, Ambiguous, No Match and Unavailable remain distinct; no fabricated certainty, percentages or causes. |
| Choose Another Exhibit, revisit and correct again | User selection opens immediately, remains in history and is revisable; no implied training or silent replacement. |
| Duplicate activation and timeout races | One active attempt; one terminal outcome; no duplicate sessions or stale outcomes. |
| Sound off; enlarged text; assistive input | Task completes without hearing; text/actions survive 200% enlargement; targets measure at least 44 × 44 pt without overlap; VoiceOver, Switch Control and Full Keyboard Access reach/activate required actions. |
| Data inspection and service audit | Capture/transfer/retention match the contract; no raw-audio logging or training reuse; actual processing destination and privacy disclosures verified. |

## Evidence limits and routing audit

Only the supplied brief and installed local guidance were used. The root `apple-hig/SKILL.md` was explicitly read first; relevant topic-index rows were searched. Then the technologies, foundations, and menus-and-actions family procedures were read, followed by the ShazamKit, Machine learning, Privacy, Accessibility and Buttons topic procedures, each before its corresponding source guide. All were resolved beneath `.agents/skills/apple-hig/`; each read used one file per command. The installed guides identify a 2026-10-25 snapshot. Official links above are attribution, not evidence of browsing or current SDK verification.

No code, recognizer, catalog, calibrated confidence, screenshots, device or SDK environment was supplied or tested. No GUI, microphone, permission prompt, accessibility execution, native rendering, contrast measurement, target measurement or build is claimed. Recognition quality must be evaluated with representative museum audio, noise, overlapping sources, unknown exhibits and catalog versions; inspect wrong matches and no-match rates by exhibit, not just aggregate accuracy. Sampling caps, catalog completeness, offline behavior and service data handling require implementation validation before release. ShazamKit is relevant guidance, not proof of framework selection or platform/API feasibility.
