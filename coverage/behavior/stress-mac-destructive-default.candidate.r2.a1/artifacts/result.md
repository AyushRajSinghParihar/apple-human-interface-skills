# macOS deletion review

Remove A’s routine confirmation, retain B’s intentional destructive confirmation and normal Return default, and remove C’s unexpected destructive default and side effect. Consequence, reversibility, and prior intent determine the behavior; button color alone does not.

This is a specification review of `interface.md`, not a runtime audit. The brief supplies all observed behavior. No implementation, screenshots, runtime, or SDK evidence was supplied. Only local files and installed skill instructions were used; official links below identify the supplied snapshot’s sources and were not fetched.

## Concrete decisions

| Flow | Finding and effect | Correction and activation contract |
| --- | --- | --- |
| A — remove one photo | Routine removal already has working Undo, yet always interrupts. This adds an unnecessary decision to common reversible work. | Remove the alert. Explicitly choosing Remove Photo removes only the selected photo and records one reversible operation. There is no confirmation Return action; do not introduce a destructive Return default in the surrounding view. Preserve that view’s existing appropriate Return behavior, which is unspecified. |
| B — Empty Archive | The person deliberately requested irreversible deletion. Confirmation is appropriate. Empty Archive as a normal default Return action is permitted by the alert-specific exception; it is not a defect merely because it destroys data. | Keep the confirmation and normal default Empty Archive. Use title **Empty Archive?** and proposed message **All items in the archive will be permanently deleted. This cannot be undone.** Use **Cancel** leading and **Empty Archive** trailing. Return confirms the requested operation; Cancel, Escape, and Command-Period dismiss without deletion. Do not make Cancel the default. Retain normal default styling rather than imposing red styling solely because this deliberately requested operation is destructive. |
| C — harmless inspector | Opening the inspector unexpectedly exposes default Delete All, and Return destroys unrelated data. This is a critical mismatch between intent and consequence. | Opening the inspector must only inspect; remove Delete All’s default/Return binding and unrelated deletion handler from this path. Return must never delete unrelated data. The inspector’s appropriate nondestructive Return action remains to be established from its actual controls. If deletion is genuinely needed, expose it as a separate explicit command with a clearly named scope. Any retained alert for an unexpected destructive consequence must explain the affected data, use destructive styling for that action, provide Cancel, and have **no default** so Return cannot accept loss. Do not substitute a default Cancel. |

A’s proposed recovery contract: expose **Undo Remove Photo** and **Redo Remove Photo** at the top of Edit, using Command-Z and Shift-Command-Z. Undo restores the same photo and its prior placement; reveal the restored result so recovery is visible. These restoration details are proposed acceptance criteria, not independently verified properties of the reported working Undo.

For B, confirmation precedes any mutation. Accepting deletes only archive contents; cancellation preserves them and returns to the initiating context. For C, closing or cancelling the inspector preserves all data. Restore useful focus to the initiating control after a temporary presentation closes. Do not stack repeated confirmations. These are proposed transition contracts, not runtime findings.

## Source support and qualifications

- [Alerts — Best practices](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices): common undoable deletion generally needs no confirmation; irreversible destruction warrants confirmation. This supports removing A’s interruption and retaining B’s.
- [Alerts — Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons): explicitly requested destruction can retain a normal default so Return confirms intent. Unexpected destructive consequences use destructive styling; destructive actions have Cancel alongside them, Cancel is not the default, and no default can be considered to require deliberate reading. This supports B’s exception and C’s no-default fallback.
- [Buttons — Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role): primary is generally a likely nondestructive action. Read with the more specific alert exception above; it does not establish a universal ban on destructive defaults.
- [Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo): precise action labels, visible restoration, and standard Mac Edit-menu shortcuts support A’s recovery contract.
- [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices): interrupt only for a clear decision benefit, provide an exit, and avoid stacked alerts.

Exact copy, focus restoration, photo-placement restoration, and separating deletion from C’s inspector are application decisions derived from the stated tasks. No claim is made that HIG dictates these exact words or implementation APIs. The installed snapshot is dated 2026-10-25; no newer guidance was checked.

## Acceptance checks and current status

**Passed in document review:** A’s stated working Undo supports recovery instead of routine confirmation. B’s deliberate initiation, confirmation, Cancel option, and normal default fit the documented exception. Labels Cancel and Empty Archive name their outcomes.

**Failed in the supplied description:** A always interrupts routine reversible deletion. C makes unrelated destruction the default outcome of a harmless task. These are brief-level findings, not reproduced failures. B’s description does not establish a Return-default defect. Its missing irreversibility message is an evidence gap; the proposed message makes the consequence explicit.

**Not executed — required implementation/runtime checks:**

| Flow | Acceptance check |
| --- | --- |
| A | Removing one selected photo shows no alert and affects no other photo. Undo restores the correct photo and placement visibly; Redo removes it again. Menu labels and shortcuts work. A meaningful edit sequence and a new edit after Undo preserve coherent history; inspect save/open history policy. Return in the containing view does not acquire a deletion binding. |
| B | Opening confirmation changes no data. Return activates Empty Archive once and affects only the archive. Cancel, Escape, and Command-Period preserve contents and dismiss. Verify consequence text, button order, normal default appearance, and focus return. Repeated invocation does not stack alerts or duplicate deletion. |
| C | Open inspector, press Return, then dismiss: unrelated data remains unchanged throughout. No Delete All default or inherited Return handler survives. If a separate destructive alert is retained, it accurately names scope, has destructive styling and Cancel, and initial Return performs no deletion because there is no default. Explicit cancellation preserves data; explicit deletion affects only its named scope. |
| All | On the Mac, inspect keyboard focus, accessible names and VoiceOver reading/activation order, native alert rendering, and enlarged/localized text for clipping. Verify default-key behavior separately from deliberately focused button activation. |

## Evidence still missing

The implementation framework and deployment target; actual action handlers, key equivalents and default bindings; screenshots and full alert copy; affected-data boundaries, including what Empty Archive contains and what C deletes; B’s cancellation behavior; C’s underlying reversibility; A’s undo history, restoration and save/open behavior; and supported focus/dismissal paths. No build, SDK compilation, GUI, device, keyboard, or accessibility execution occurred. The corrected contracts above require implementation evidence and Mac execution before they can be reported as passing behavior.

## Local instruction audit

Each file was read individually by `cat`, resolving paths within `.agents/skills/apple-hig/`: root `SKILL.md`; Presentation family → Alerts procedure → alerts guide; Menus and actions family → Buttons procedure → buttons guide; Patterns family → Undo and redo and Modality procedures → their guides. Every family and topic procedure was read before its corresponding source guide. `interface.md` was read before making findings.
