# Repair decisions and evidence

Patched `interface.md` in place, replacing the four problematic behaviors with a concrete macOS specification. The patch defines local access, ownership boundaries, labeled account controls, durable-save and session transitions, deletion copy and keyboard behavior, asynchronous recovery, and implementation acceptance criteria. It specifies product behavior; no application code was supplied or changed.

## Decisions and source support

| Supplied behavior | Revised decision | Basis |
| --- | --- | --- |
| Login required to view local budgets | Open On This Mac without online login; authenticate for account-dependent work | [Managing accounts — Best practices](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Best-practices) supports useful unregistered access when accounts are not essential. Local budgeting is treated as independent functionality. |
| Switching silently merges private data | Separate stable owner namespaces, authenticate before commit, fence stale sync, clear all private windows | [Privacy — Best practices and Protecting data](https://developer.apple.com/design/human-interface-guidelines/privacy#Protecting-data) supports clear use and protected data. Namespace, migration quarantine, and atomic transition details are proposed engineering safeguards, not quoted Apple requirements. |
| Sign Out deletes unsynced changes | Save locally first, keep drafts private to their owner, resume on return; abort transition if saving fails | [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices) supports protecting unfinished content across exits. Offline sign-out and durable-save semantics are product decisions. |
| Unlabeled trash beside avatar deletes account | Remove shortcut; Account… exposes a separate labeled Delete Account… route, with exact scope and confirmation | [Buttons — Content and macOS](https://developer.apple.com/design/human-interface-guidelines/buttons#Content) supports clear action labels and continuation ellipses; [Managing accounts — Deleting accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Deleting-accounts) supports discoverable real deletion, timing, retention disclosure, completion notification, and separate billing management. |
| Deletion consequences unspecified | Confirm identity, budgets, unsynced loss, collaborator impact, retention and timing; distinguish pending, rejected, unknown, complete | [Alerts — Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons) supports meaningful outcomes and cancellation. No default is an intentional product choice; the guide permits a default for deliberately requested destruction. |
| Input/accessibility behavior unspecified | Native controls, visible names, keyboard paths, focus restoration, persistent text status, enlargement checks | [Accessibility — Vision, Mobility, Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). These are specified checks, not observed accessibility results. |

The local button guide states a general 44 × 44 pt target, while the accessibility guide gives macOS default/minimum controls as 28 × 28 / 20 × 20 pt. These are not treated as interchangeable universal minima. The patch retains native Mac controls and requires actual target/separation measurement; custom targets should conservatively use the larger general guidance where practical. No geometry was supplied to measure.

## Worked before/after

Illustrative fixture, not observed app data: Alex has an account-owned “Family” budget with three unsynced edits; Sam has a separate account; “Household Draft” is an On This Mac budget.

Before: launch blocks Household Draft behind login. Switching Alex → Sam silently merges private budgets. Signing out loses the three edits. The trash glyph offers no visible account or consequence label.

After: launch offline opens Household Draft without login. Alex’s switch first saves the three edits under Alex’s owner ID. Canceling Sam’s authentication returns to Alex unchanged. Successful authentication opens only Sam’s workspace; a late Alex sync response cannot modify it. Alex’s edits remain protected locally and return when Alex signs in again. Sign Out offline preserves them while hiding Alex’s workspace.

If Alex later chooses Delete Account…, the summary identifies Alex, one owned budget and three unsynced changes, with the verified timing/retention policy. Cancel, Escape, and Command-Period preserve everything. Return alone does not delete. Explicit confirmation submits one request; loss of connectivity shows an unresolved status. Only confirmed completion removes Alex’s account data. Sam’s budgets and Household Draft remain; collaborators lose access to Alex’s owned Family budget as disclosed.

## Acceptance checks

| Check | Required result | Evidence status |
| --- | --- | --- |
| Offline launch without authentication | Local budgets available; private account cache hidden | Passed specification trace; runtime not executed |
| Dirty switch and canceled/failed target authentication | Durable owner-scoped edits; old account retained on cancellation/failure | Passed specification trace; runtime not executed |
| Offline sign-out and disk-save failure | Offline work retained; failed save prevents transition | Passed specification trace; runtime not executed |
| Late sync, relaunch, multiple windows, legacy unowned data | No cross-owner content, writes, history, or automatic assignment | Passed specification trace; storage/security tests not executed |
| Cancel deletion, Return, Escape, Command-Period | Safe cancellation and focus return; Return alone does not commit | Passed specification trace; native input not executed |
| Deletion retries, unknown outcome, confirmed completion | One request identity; no premature success or data removal; only target removed | Passed specification trace; backend not executed |
| Shared budgets, retention, timing, billing and notification | Accurate summary and enforced policy; billing separately managed if present | Contract specified; actual policies/capabilities unverified |
| Keyboard, VoiceOver, Full Keyboard Access, enlarged text, contrast, target sizes | Whole flow operable; names/status readable; no clipped essential content | Not executed; no UI available |

Passed: static document coverage of all four supplied defects and the specified alternate exits. Failed: no unresolved contradiction found in the revised document during static review; this is not a runtime pass. Not executed: application, device, SDK compilation, native GUI, accessibility tools, backend deletion, credential/token revocation, storage isolation, network fault injection, or legal-policy verification.

## Evidence limits and routing audit

Only the original one-line `interface.md` and installed guidance were used. No screenshots, implementation, service contracts, authentication methods, billing details, retention requirements, SDK, or Mac runtime were supplied. The family-budget label does not establish existing family permissions. The ownership/deletion policy and notification prerequisites in the patch are proposed requirements requiring implementation validation. No claim of security certification, legal compliance, or functioning deletion is made.

Explicitly read installed `/tmp/hig-eval-zewidmun/.agents/skills/apple-hig/SKILL.md`, then searched its `references/topic-index.md` for accounts, deletion, alerts, menus, and undo. Read the owning family SKILL.md files for patterns, presentation, menus-and-actions, and foundations. Before reading supporting articles, read the installed `.topics/apple-hig-<topic>/SKILL.md` procedures for managing-accounts, modality, alerts, buttons, privacy, and accessibility; then read each corresponding family `references/<topic>.md`. Each read/search used a separate cat/rg command against one file. No web browsing occurred. Official links above identify the local guides’ source articles; they were not fetched or independently verified.
