# Account flow repair

Updated [interface.md](interface.md) in place from its original one-line description into a concrete macOS interaction and data-state specification.

## Decisions and changes

- Local-only budgeting works without service login; signed-out account caches remain protected. Sign-in is requested for account sync/shared access. This applies [Managing accounts — Best practices](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Best-practices).
- Replace silent merging with immutable workspace ownership and atomic transitions across windows. Preserve unsynced edits before switching or sign-out; failure leaves the source active. Isolation, persistence and response scoping are product engineering decisions informed by [Privacy — Protecting data](https://developer.apple.com/design/human-interface-guidelines/privacy#Protecting-data), not storage guarantees supplied by HIG.
- Replace the unlabeled trash glyph with Account… and a separate Delete Account… section. Specify availability and outcomes for every account control, using [Buttons — macOS](https://developer.apple.com/design/human-interface-guidelines/buttons#macOS).
- Make deletion an authenticated, reviewed service operation with explicit owned/shared data consequences, export, actual retention/timing disclosure, idempotency and honest completion. Sign-out and deletion have distinct data policies. Discoverability, real deletion and conditional billing/provider requirements follow [Managing accounts — Deleting accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Deleting-accounts).
- Use a final consequential alert with Cancel, Delete Account and no default; Escape cancels. This is a deliberate-reading product choice. [Alerts — Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons) also permits a normal default for explicitly requested destruction; it does not universally prohibit destructive defaults. Ordinary successful switching does not interrupt with an alert. [Modality](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices) supports narrow interruptions and protected exits.
- Specify keyboard access, meaningful labels, persistent textual status and enlargement checks using [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility). Preserve the local guidance's sizing discrepancy: general buttons say 44 × 44 pt; the macOS accessibility table gives 28 × 28 pt default / 20 × 20 pt minimum. Use Mac defaults as the baseline and measure the implementation; no measured target claim is made here.

## Worked before/after

Illustrative scenario, not an executed test: Alex has three unsynced expenses in a private account budget; Sam has a separate account on the same Mac app.

| Step | Original supplied behavior | Revised contract |
| --- | --- | --- |
| Open local budgets | Login required | Local-only workspace opens without service login; Alex's signed-out cache does not become guest data. |
| Switch Alex → Sam | Private data silently merges | Save Alex's three edits locally, authenticate Sam, then activate only Sam's store. Cancel or failed save/authentication leaves Alex active. A late Alex response cannot appear in Sam's workspace. |
| Return to Alex, then sign out | Unsynced changes are deleted | Reauthentication restores the three edits. Sign-out locks them under Alex and returns to the separate local workspace. |
| Delete Alex | Unlabeled trash glyph beside avatar; confirmation/outcome unspecified | Delete Account… shows Alex's identity, affected budgets/member counts and three unsynced changes. Export is optional. Cancel preserves everything. Confirm sends the reviewed operation; only confirmed service completion produces Account deleted and local cleanup. Sam and local-only budgets survive. |

## Acceptance checks

These are implementation acceptance cases. Static pass means the written specification covers the case; it does not mean the app passed execution.

| Check | Specification inspection | Execution |
| --- | --- | --- |
| Local access without login; locked signed-out account caches; offline launch | Passed: access rules explicit | Not executed |
| Switch with dirty edits; failure/cancel preserves source; no cross-account merge/upload/render | Passed: ownership and transition rules explicit | Not executed |
| Sign-out offline/online; returning account restores unsynced work | Passed: preservation, lock and credential rules explicit | Not executed |
| Multiple windows, late responses, duplicate activation, quit/restart | Passed: atomic transition and recovery specified | Not executed |
| Delete review identifies correct account, owned shared budgets, other-owned budgets and unsynced edits | Passed: scope and plan defined | Not executed |
| Cancel, Escape, Command-Period, Return, outside click; focus restoration | Passed: alert exits and no-default contract explicit | Not executed |
| Export cancellation/failure; offline plan; rejection; timeout; accepted request after restart; cleanup failure | Passed: distinct data outcomes specified | Not executed |
| Service deletion completes, sessions/tokens revoked, actual retention/timing disclosed, notification delivered | Passed as requirements only | Not executed; backend evidence absent |
| Billing management and supported authentication/provider integration | Conditional requirements explicit | Not executed; capabilities unknown |
| Full Keyboard Access, assistive names/states, 200% text, contrast, hit geometry | Passed as acceptance requirements only | Not executed; requires Mac runtime and measurement |

Failed checks: none detected in the revised document's static scenario trace. No runtime check was run or passed. The supplied original description fails the four intended design outcomes; unspecified original confirmation, keyboard and backend behavior was not treated as an observed defect.

## Audit and evidence limits

Read the installed root `.agents/skills/apple-hig/SKILL.md` explicitly, then searched its `references/topic-index.md` for account/deletion/control/input concepts. Read the Patterns, Presentation, Menus and actions, and Foundations family SKILL.md files. Read each selected topic procedure before its supporting reference: Managing accounts, Modality, Alerts, Buttons, Privacy and Accessibility. All paths were resolved within this installed package; each reading command consumed one file. No web access was used. Official links above identify the articles represented by the local snapshot, not live verification.

Evidence consists of the original interface.md, installed local guidance and the revised text. No app implementation, backend contract, authentication configuration, subscription inventory, legal retention policy, SDK build, device, GUI, Accessibility Inspector or assistive-technology execution was available. The scenario trace validates specification coverage only. Backend deletion scope and storage/session isolation require engineering verification; retention and timing require actual service/legal facts. Do not ship invented completion estimates, unsupported authentication claims or an Account deleted message based only on request submission.
