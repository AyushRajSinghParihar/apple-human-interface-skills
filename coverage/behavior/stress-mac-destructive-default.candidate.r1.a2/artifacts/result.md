# macOS deletion-flow review

Based on `interface.md` and the installed HIG snapshot only. The supplied descriptions establish the review findings below; no implementation or runtime was provided. These are corrections to the interaction contract, not implemented application changes.

## Concrete result and decisions

| Flow | Finding and effect | Decision |
| --- | --- | --- |
| A: remove one photo | An alert interrupts every routine removal despite working Undo. This adds friction to a recoverable task. | Remove the routine confirmation. An explicit Remove Photo command removes only the selected photo immediately and offers recovery through Undo. Do not introduce a global Return-to-delete binding. |
| B: Empty Archive | The person deliberately requests irreversible deletion, then receives a confirmation with Cancel and Empty Archive. A normal default Empty Archive activated by Return is consistent with the deliberate-destruction exception. | Keep the confirmation and normal default Empty Archive; do not automatically change it to red, remove its default, or make Cancel default solely because data is deleted. Explain the irreversible scope. |
| C: open inspector | A harmless action unexpectedly makes Delete All the default; Return destroys unrelated data. This conceals a destructive consequence and risks accidental loss. Highest-priority correction. | Opening the inspector must only open the inspector. Remove the deletion prompt/default from that entry path. If bulk deletion is needed, expose it through a separate, explicitly chosen command with accurate scope and confirmation. |

The controlling distinction is prior intent, consequence, and recovery, rather than button color. [Alerts — Best practices and Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons) says common undoable deletions generally need no confirmation, permits a normal default for explicitly chosen destruction, requires Cancel alongside destructive alert actions, and says not to make Cancel the default. For deliberate reading, it suggests considering no default. [Buttons — Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role) generally favors a likely nondestructive primary action; the alert-specific exception qualifies that general advice.

### A: direct removal with recovery

Proposed contract: selection → explicit Remove Photo → selected photo removed, context retained → Edit > Undo Remove Photo restores the same photo and reveals the restoration. Edit > Redo Remove Photo reapplies that removal. Use Command-Z and Shift-Command-Z, with Undo/Redo at the top of Edit. These names and the exact selection-restoration policy are product recommendations; standard menu/shortcut placement and visible recovery follow [Undo and redo — Best practices and macOS](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#macOS).

There is no confirmation default after this correction. Return retains the meaning of its current context; it must not become a new app-wide removal shortcut. The brief does not establish A's current Return binding, so no existing binding defect is asserted.

### B: intentional irreversible emptying

Keep title `Empty Archive?`, with proposed supporting text: `All items in the archive will be permanently deleted. This action cannot be undone.` Use that wording only if “all items in the archive” is the actual deletion boundary; otherwise substitute the precise scope.

For a horizontal button row, place Cancel leading and the normal default Empty Archive trailing. Return confirms Empty Archive once. Cancel, Escape, and Command-Period dismiss without deletion and return to the archive context. There is no Undo promise. Do not add a routine caution symbol merely because this resembles emptying Trash. These decisions follow [Alerts — Content, Buttons, and macOS](https://developer.apple.com/design/human-interface-guidelines/alerts#macOS). The supplied title and labels are not themselves a demonstrated defect; the body text and ordering are unspecified and remain inspection items.

### C: separate inspection from destruction

Proposed contract: Open Inspector → inspector appears with data unchanged. Return in this initial state cannot invoke Delete All. The inspector's actual content is unknown, so a specific harmless default cannot be selected from the evidence; leave deletion without a default binding on entry rather than assigning Cancel as a blanket fix.

If a separate bulk-delete command is retained, label it with its true target (for example, Delete All Photos only if that is accurate). Confirm the actual affected data and recovery limits before prescribing final copy. If a necessary alert still presents an unexpected destructive consequence, explain it, provide Cancel, use destructive styling for the destructive action, and consider no default to require deliberate reading. Return must not accept unexplained loss. Red styling alone would not fix the misleading trigger or handler. See [Alerts — Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons).

If a redesigned bulk-delete flow is explicitly requested by the person, reassess it under B's intentional-destruction exception; C's present unsafe context does not establish that every future Delete All confirmation must lack a default.

## Acceptance checks and current status

**Passed — document review only:** macOS and the three distinct intent/reversibility contexts are explicit. A is reported to have working Undo. B is reported to have Cancel, an outcome-specific confirmation action, and a normal Return default following deliberate Empty Archive intent. These are supplied facts, not independently executed checks.

**Failed — supplied interaction contract:** A unnecessarily interrupts a routine undoable deletion. C couples harmless inspection to unexpected unrelated destruction and makes that destruction the Return default. B's described default is not a failure.

**Not executed — required implementation acceptance:**

| Check | Expected result |
| --- | --- |
| A: remove one selected photo | Only that photo is removed, with no routine confirmation. |
| A: Undo/Redo through Edit and standard shortcuts | Same object and relevant state restore visibly; Redo reapplies the removal. A sequence of edits and a new edit after Undo produce coherent history. Verify documented save/open history boundaries. |
| A: Return in each relevant content context | No new implicit or global deletion activation. |
| B: enter via Empty Archive, then Return | Confirmation names actual scope and irreversibility; normal default commits precisely that scope once. |
| B: Cancel, Escape, Command-Period | Dismiss with data unchanged and return to the initiating context. |
| C: open inspector, then Return, including repeated entry | Inspector opens with no deletion; Return cannot invoke Delete All or a stale destructive default. Unrelated data remains unchanged. |
| C: separately request bulk deletion, if supported | Label, scope, recovery statement, roles, and default match the actual task; cancellation never deletes. Unexpected loss cannot be accepted by default. |
| Keyboard and presentation | Complete relevant paths without a pointer; verify Full Keyboard Access, actual focus/default activation, focus return, native button order/styling, readable enlarged/localized text, and no stacked confirmations or duplicate destructive execution. |

Cancellation and keyboard checks follow [Keyboards — Best practices and Standard keyboard shortcuts](https://developer.apple.com/design/human-interface-guidelines/keyboards#Standard-keyboard-shortcuts). Avoiding unnecessary blocking and stacked alerts follows [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices).

## Evidence still missing

- Application code, framework, supported macOS versions, actual control roles, key equivalents, responder/default handling, and deletion handlers. No SDK/API correctness or compilation claim is possible.
- Screenshots or layout evidence for body copy, styling, ordering, target geometry, focus indicators, and enlarged/localized text. The brief does not establish that any button is actually red.
- Exact archive and Delete All data boundaries, whether other documents/accounts/devices are affected, recovery limits for C, and failure/partial-completion behavior. Do not invent these details in final confirmation copy.
- Independent evidence for A's restoration fidelity and history boundaries. “Working Undo” is accepted from the brief, not measured.
- Mac runtime recordings or tests for Return, cancellation, repeated activation, focus restoration, and Full Keyboard Access. Native rendering and assistive-technology behavior, including VoiceOver, have not been executed or established.

## Local guidance audit

Explicitly read the installed root `apple-hig/SKILL.md`, then searched its `references/topic-index.md` for alerts, buttons, keyboard, deletion, confirmation, and Undo concepts. Read each owning family before its topic procedures, and each procedure before its source guide:

- Presentation → Alerts → `references/alerts.md`.
- Menus and actions → Buttons → `references/buttons.md`.
- Inputs → Keyboards → `references/keyboards.md`.
- Patterns → Undo and redo and Modality → their respective reference guides.

All paths resolved under `/tmp/hig-eval-v0ux0u52/.agents/skills/apple-hig/`; each instruction/source file was read with a separate `cat` command. Official links above identify the source sections represented by the installed snapshot; they were not fetched. No web, device, GUI, SDK, or accessibility execution was performed.
