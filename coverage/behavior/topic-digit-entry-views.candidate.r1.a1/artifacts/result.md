# Pairing-code specification repair

Patched [interface.md](interface.md) in place. The original one-line tvOS specification required swipes, hid focus, erased all digits after a mistake, and ended at “Invalid”. The replacement defines a complete entry, correction, submission, recovery, cancellation, and success contract.

## Decisions and basis

- Use fullscreen six-digit numeric entry with a purpose-specific title and prompt. Preserve leading zeroes and mask this credential. [Digit entry views — Best practices](https://developer.apple.com/design/human-interface-guidelines/digit-entry-views#Best-practices) supports the presentation and masking; exact length and string handling come from this task.
- Separate the editing slot from the focused control; define directional routes, press feedback, and Select activation. Directional presses complete the task without swipes. [Focus and selection — tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS) and [Remotes](https://developer.apple.com/design/human-interface-guidelines/remotes) support visible focus, reachability, and deliberate activation. The keypad layout and correction mechanics are product decisions.
- Preserve entered digits after rejection or connection failure. Explain what happened and expose Pair, Get a New Code, and Cancel. These recovery rules and explicit submission are application decisions, not a HIG authentication protocol. Outcome-specific labels and system button styles follow [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons).
- Provide in-app new-code instructions and a deliberate Enter New Code reset. No issuer or resend endpoint exists in the supplied evidence, so the screen does not pretend to send a code. The source of a replacement code remains an integration dependency; the specification gives an actionable return route without inventing a companion app.
- Use tvOS-specific 29 pt text and 66 × 66 pt control defaults, enlarged text reflow, non-color focus/status cues, and assistive-operation checks. These come from [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility); the 66 pt platform default is the conservative choice over the buttons guide’s general 44 pt rule. Across-room testing follows [Designing for tvOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos#Best-practices).
- Keep the credential transient and out of telemetry and spoken values. This is a product data-handling restriction applying [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices), not a security certification.

## Worked before/after

Suppose the intended code is `004219`, but the person enters `009219`.

**Before:** They can only swipe, cannot see the current target, receive “Invalid”, lose all six digits, and have no stated retry or new-code path.

**After:** They navigate using directional presses and Select. Slots show six asterisks and the active position. Pair submits `009219` once. Rejection preserves the masked draft and says “This code wasn’t accepted. Check the code and change any incorrect digits, or get a new code.” They navigate to slot 3, press Select, navigate to key 4 and select it. Only slot 3 changes: the sequence is now `004219`. No full re-entry or automatic submission occurs. They deliberately select Pair; only a confirmed service response opens Apple TV Paired. Alternatively, Get a New Code opens instructions; Back to Entry preserves the draft, while Enter New Code deliberately resets it. This is a worked specification walkthrough, not an executed test.

## Acceptance audit

| Check | Result and evidence |
| --- | --- |
| Required in-place patch | Passed: reread interface.md; it contains the revised concrete specification. |
| Original blockers addressed | Passed by text inspection: press-based alternative, visible focus, single-slot correction, retained rejected input, explanatory errors, retry/new-code/exit routes are specified. |
| Sequence and lifecycle contract | Passed by text inspection: exact six digits, leading zeroes, incomplete-entry prevention, deliberate submission, duplicate guard, cancellation and late-response handling are specified. |
| Recovery walkthrough | Passed as a document walkthrough: `009219` → edit slot 3 → `004219`; expiry and connectivity have separate messages and actions. |
| Installed guidance route | Passed: explicitly read root SKILL.md, searched topic-index.md, read each selected family and topic procedure before its reference. |
| Existing original specification | Failed design review: its four stated behaviors block accessible entry and recovery. These failures are repaired in the written contract; no running product was inspected. |
| Remote navigation, deletion, retry, new-code paths, success and cancellation | Not executed. Implement and exercise the acceptance scenarios in interface.md on tvOS. |
| VoiceOver, Switch Control, actual focus order, text enlargement, contrast, focus clearance and TV legibility | Not executed or measured. Require supported Apple-device inspection and actual rendering. |
| SDK/API availability, native component fit, build, backend pairing/security behavior | Not executed or verified. Require implementation and service evidence. |

## Evidence limits and route record

Only the original interface.md and installed local guidance were used. No web browsing occurred; official links identify source articles from local snapshots, not live verification. The installed references identify a 2026-10-25 snapshot/retrieval date. Local existence does not establish independent source review or current SDK support.

Read `/tmp/hig-eval-qlg5leos/.agents/skills/apple-hig/SKILL.md` explicitly, then searched its `references/topic-index.md` for tvOS, numeric entry, focus, remotes, and accessibility. Under that installed package, read these family → topic → reference routes:

- `apple-hig-getting-started` → `designing-for-tvos`.
- `apple-hig-selection-and-input` → `digit-entry-views`.
- `apple-hig-inputs` → `focus-and-selection`, `remotes`.
- `apple-hig-foundations` → `accessibility`, `privacy`.
- `apple-hig-menus-and-actions` → `buttons`.

Each family was read at `subskills/<family>/SKILL.md`; each topic at `subskills/<family>/.topics/apple-hig-<topic>/SKILL.md`, before its `subskills/<family>/references/<topic>.md` source guide. Each read used a separate cat command; the index search used rg. No device, SDK, GUI, accessibility, authentication, or hardware execution is claimed. There was no supplied implementation, service schema, layout, screenshot, or issuer flow to verify. Native component customization feasibility and the real code-issuance destination remain implementation dependencies.
