# Review result

Use intent, consequence, and recoverability to decide confirmation and Return behavior. Do not apply one rule to every destructive button.

This is a specification review of `interface.md`, not an implementation or runtime test. Evidence is limited to that brief and the installed local apple-hig package. No web, device, SDK, GUI, or accessibility execution was performed. Official links below identify the sources represented by the local snapshot; they were not fetched.

## Concrete decisions

| Flow | Supplied evidence and effect | Decision |
|---|---|---|
| A — Remove one photo | Routine removal has working Undo but always interrupts with an alert. Repeated unnecessary interruption slows the ordinary task. | Remove the routine confirmation. Remove only the selected photo immediately and preserve working Undo. Do not introduce a new Return-to-delete binding. |
| B — Empty Archive | The person explicitly chooses irreversible Empty Archive, then sees `Empty Archive?`, Cancel, and a normal default Empty Archive activated by Return. | Keep the confirmation and retain normal default Empty Archive. This is the deliberate-destruction exception; neither red destructive styling nor removing the Return default is automatically required. Add explicit irreversible-consequence text. |
| C — Inspector | Opening a harmless inspector unexpectedly presents default Delete All; Return destroys unrelated data. The action and scope contradict the initiating task. | Remove the destructive default and decouple inspector opening from deletion. Opening the inspector and pressing Return must never delete unrelated data. If a legitimate Delete All command remains, require a separate deliberate invocation with clear scope before any confirmation. |

A follows the guidance that common undoable deletions generally need no confirmation; B warrants an important irreversible confirmation. [Alerts — Best practices](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices), [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices).

The general button advice favors a likely nondestructive primary action, but the alert-specific guidance explicitly permits a normal default for deliberately chosen destruction such as Empty Trash. B fits that exception; C does not. For unexpected destructive consequences, use destructive styling, offer Cancel, and consider no default to encourage deliberate reading. Do not make Cancel the default. Color alone does not establish the actual key behavior. [Buttons — Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role), [Alerts — Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons).

## Before/after interaction contracts

These are proposed product specifications derived from the guidance, not claims about unseen handlers.

### A

Selected photo → explicit Remove Photo command → photo removed without an alert → Undo restores that same photo and reveals it. Keep selection/navigation context useful after removal and restoration. Offer `Undo Remove Photo` and `Redo Remove Photo` at the top of Edit, using Command-Z and Shift-Command-Z. Removal is one meaningful history operation. The brief establishes working Undo, but does not establish its menu labels, visibility, history boundaries, or shortcuts. [Undo and redo — Best practices and macOS](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo).

There is no confirmation default after this correction. Return retains its existing appropriate content behavior; its precise mapping is unknown and must be inspected rather than invented.

### B

Explicit Empty Archive command → confirmation → either cancellation with no mutation, or one irreversible emptying of the named archive.

Proposed copy:

- Title: `Empty Archive?`
- Message: `All items in the archive will be permanently deleted. This action cannot be undone.`
- Buttons in a horizontal row: Cancel leading; Empty Archive trailing.
- Empty Archive: normal default action; Return confirms.
- Cancel: cancellation action, not default; Cancel, Escape, and Command-Period dismiss without deleting.

The copy assumes the command affects all items in the archive; verify that scope before shipping. No extra caution symbol is needed merely because this is an intentional empty-trash-like operation. Do not offer a false Undo for the irreversible result. [Alerts — Content, Buttons, and macOS](https://developer.apple.com/design/human-interface-guidelines/alerts).

### C

Open Inspector → inspector for the intended task, with no deletion confirmation and no deletion from Return. There is no evidence of an appropriate inspector completion button, so do not invent one or rename it Cancel.

If Delete All serves a real product task, place it behind a distinct explicit command and disclose the actual target set. If an unexpected destructive consequence must still be presented for a legitimate reason, use a destructive `Delete All` action, leading Cancel and trailing Delete All in a horizontal row, and **no default** as the chosen conservative correction. Bare Return on initial presentation must not commit loss; deliberate focus/activation must remain distinguishable from default activation. Cancel, Escape, and Command-Period leave data unchanged. Exact warning copy cannot be finalized until scope and reversibility are known. Do not treat a warning as sufficient justification for deleting unrelated data from inspector entry. [Alerts — Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons), [Keyboards — Standard keyboard shortcuts](https://developer.apple.com/design/human-interface-guidelines/keyboards#Standard-keyboard-shortcuts).

If a future, separate flow explicitly requests and clearly explains destruction, reassess it on that evidence; the current inspector entry provides no such intent.

## Acceptance checks and current status

**Passed in the supplied specification:** A reports working Undo. B has an explicit destructive initiating command, confirmation, Cancel, and a normal Return default consistent with the deliberate-destruction exception. These are brief-level findings only.

**Failed in the supplied specification:** A always interrupts routine undoable removal. C assigns unexpected unrelated destruction to the default Return action. B's supplied title and labels do not explicitly disclose that deletion cannot be undone; the proposed message closes that communication gap.

**Not executed — acceptance checks for the corrected flows:**

| Check | Required observable result |
|---|---|
| A ordinary removal | One selected photo is removed without an alert; other photos remain intact. |
| A recovery | Command-Z restores the same photo visibly; Shift-Command-Z repeats the removal. Labels identify the action; a new edit after Undo updates Redo appropriately. Inspect save/open history policy and a meaningful sequence of edits. |
| A Return | No new default or global Return handler deletes a photo outside an explicit removal action. |
| B confirmation | Appears only after Empty Archive is deliberately invoked; clearly states target scope and irreversibility. |
| B Return | On initial confirmation, Return activates Empty Archive once and affects only the disclosed archive. |
| B cancellation | Cancel, Escape, and Command-Period close the confirmation without mutation and return to the initiating context. |
| C inspector | Opening the inspector, pressing Return immediately, and editing inspector fields never invoke Delete All or affect unrelated data. |
| C retained warning, if any | Unexpected-loss warning has destructive styling, explicit scope, Cancel, and no default. Initial bare Return causes no deletion; deliberate activation and each cancellation path have the specified outcomes. |
| Repeated activation | Repeated commands do not stack alerts or execute duplicate deletion; no initiating key event unintentionally commits a newly opened confirmation. |
| Native presentation and keyboard access | Labels remain legible with enlarged text; native button roles, Return, cancellation, and Full Keyboard Access match the contract. Focus returns to useful context after dismissal. |

Keyboard and native rendering checks require a Mac runtime. Full Keyboard Access needs actual execution; the local keyboard guide calls for supporting and testing it. [Keyboards — Best practices](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices).

## Evidence still missing

No code, runnable build, screenshots, event traces, or data fixtures were supplied. Obtain the framework/OS targets, button role/default/key-equivalent declarations, deletion and cancellation handlers, and focus/event routing. In particular, determine whether Return activation comes from a native default, focused-control activation, or a global handler.

Verify A's actual Undo contents, history boundaries, restoration visibility, and menu access; B's archive boundaries and true irreversibility; and C's deletion scope, reversibility, and reason for exposing Delete All in the inspector. C's current Cancel availability is unknown, not an established additional defect. No evidence establishes actual red styling, button geometry, accessible names, VoiceOver behavior, or focus order. Those remain unverified; this review does not certify accessibility or SDK correctness.

## Local instruction/source audit

Read the installed root `/tmp/hig-eval-amimcjkd/.agents/skills/apple-hig/SKILL.md` explicitly, then searched its `references/topic-index.md` for alerts, buttons, keyboards, deletion, confirmation, and Undo concepts. Each file read used a separate command.

From that installed package, read these family routes before their topic procedures, and each procedure before its source guide:

- `subskills/apple-hig-presentation/SKILL.md` → `.topics/apple-hig-alerts/SKILL.md` → `references/alerts.md`.
- `subskills/apple-hig-menus-and-actions/SKILL.md` → `.topics/apple-hig-buttons/SKILL.md` → `references/buttons.md`.
- `subskills/apple-hig-inputs/SKILL.md` → `.topics/apple-hig-keyboards/SKILL.md` → `references/keyboards.md`.
- `subskills/apple-hig-patterns/SKILL.md` → `.topics/apple-hig-undo-and-redo/SKILL.md` → `references/undo-and-redo.md`.
- Presentation's interruption route also led through the Patterns family to `.topics/apple-hig-modality/SKILL.md` → `references/modality.md`.

Topic and reference paths in each route are relative to its family directory. The local articles identify a 2026-10-25 snapshot/retrieval date; no independent source review or current SDK verification is inferred.
