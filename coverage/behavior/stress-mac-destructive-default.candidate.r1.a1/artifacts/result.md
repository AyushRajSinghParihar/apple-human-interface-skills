# Review result

The correction depends on reversibility and prior intent, not button color: remove A’s routine confirmation, retain B’s deliberate-destruction default, and remove C’s unexpected destructive default and trigger.

Evidence is limited to `interface.md`, a prose description of three macOS flows. These are specification findings, not observations from running an app. No implementation or runtime was supplied. All guidance below comes from the installed local HIG snapshot; official links identify its sources and were not browsed.

## Decisions and concrete contracts

### A — Routine removal of one photo

**Finding:** The brief says Undo works, yet every removal interrupts with an alert. This adds unnecessary modality to a common reversible action. HIG says common undoable deletions generally need no confirmation and modality should have a clear decision benefit. [Alerts — Best practices](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices), [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices).

**Correction:** Explicitly choosing Remove Photo removes only the selected photo immediately, without an alert. Retain working Undo. Proposed command labels are Undo Remove Photo and Redo Remove Photo; place Undo/Redo at the top of Edit with Command-Z and Shift-Command-Z. Undo restores the same photo and makes the restoration visible. These labels and restoration details are product decisions applying the guidance. [Undo and redo — Best practices and macOS](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo).

**Return contract:** There is no confirmation default because there is no confirmation. Do not introduce a global Return-to-delete binding; Return remains governed by the focused control and normal surrounding task. The current parent-view Return mapping is unknown.

### B — Deliberately chosen Empty Archive

**Finding:** The person explicitly requests irreversible destruction. Confirmation is appropriate. Empty Archive as the normal default Return action is permitted, not a defect: the alerts guidance expressly allows this for deliberately requested destruction, such as Empty Trash. The general preference for nondestructive primary buttons must retain this exception. [Alerts — Best practices and Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts), [Buttons — Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role).

**Decision:** Keep the confirmation and its normal default Empty Archive button. Do not automatically recolor it red, disable Return, or make Cancel the default merely because the outcome is irreversible. Keep Cancel available alongside it.

**Proposed exact confirmation:**

- Title: “Empty Archive?”
- Message: “All items in the archive will be permanently deleted. This action cannot be undone.”
- Leading button: Cancel, cancellation role, not default.
- Trailing button: Empty Archive, normal/default action; Return confirms.

The message is proposed copy, not text evidenced in the brief. It assumes the command affects all archive items; verify actual scope before shipping. Confirmation deletes only the stated archive contents. Cancel, Escape, and Command-Period dismiss without deletion and return to the originating context. Use the ordinary Mac app icon; a caution symbol is not warranted solely for this routine explicit emptying task. [Alerts — Content, Buttons, and macOS](https://developer.apple.com/design/human-interface-guidelines/alerts).

### C — Harmless inspector unexpectedly offers Delete All

**Finding:** Opening an inspector unexpectedly exposes Delete All as default, and Return destroys unrelated data. This is the highest-priority defect: the triggering task provides no destructive intent, and default activation causes concealed loss. HIG’s deliberate-destruction exception does not apply. Destructive styling alone would not repair the trigger or Return behavior. [Alerts — Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons), [Buttons — Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role).

**Correction:** Opening the inspector must only inspect. Remove Delete All as its default and remove any deletion handler reached by opening it or pressing Return in the ordinary inspection task. Do not add a deletion confirmation merely to preserve this unrelated interruption. Keep unrelated data intact on opening, Return, closing, and reopening.

If bulk deletion is a real product requirement, provide a separately and deliberately invoked command in a relevant context with an explicit scope. Its exact label and copy cannot be finalized without knowing the affected data and recovery policy. If an alert must explain an unexpected destructive consequence, name that loss, style the destructive action accordingly, include Cancel, and choose **no default** so Return cannot silently accept it. Cancel remains nondefault; HIG says to consider no default when deliberate reading is necessary. This is the chosen conservative application here, not a universal prohibition on destructive defaults. [Alerts — Content and Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts).

## Acceptance checks and status

**Passed — document review only:** Classified all three flows using the supplied reversibility and prior-intent evidence. B’s explicitly requested destruction supports the documented default exception. Read the installed root skill, Presentation → Alerts, Menus and actions → Buttons, and Patterns → Undo and redo / Modality procedures before their supporting guides.

**Failed — supplied specification:** A unnecessarily interrupts every routine undoable removal. C exposes unrelated destruction through an unexpected default and Return. These failures are described by the brief, not independently reproduced. B’s Return default passes the design review; its full copy, cancellation behavior, and actual deletion scope remain unverified.

**Not executed — required acceptance checks:**

| Flow | Check | Expected result |
| --- | --- | --- |
| A | Remove one selected photo repeatedly | No confirmation; only the selected photo is removed per command. |
| A | Undo, Redo, then Undo followed by a new edit | Correct photo restored visibly; Redo reapplies that removal; new edit invalidates the obsolete redo branch. |
| A | Inspect Edit menu and exercise shortcuts | Specific Undo/Redo labels; Command-Z and Shift-Command-Z reach the correct history actions. |
| A | Press Return in normal parent-view focus states | No newly introduced implicit photo deletion or confirmation. |
| B | Explicitly choose Empty Archive, inspect alert, then press Return | Clear irreversible scope; Empty Archive is normal/default and empties only the archive. |
| B | Reopen and choose Cancel, Escape, or Command-Period separately | No deletion; alert dismisses and focus returns appropriately. |
| C | Open inspector, press Return, close, and reopen | No unrelated loss or destructive default on any path. |
| C | If a separate deletion flow is retained, inspect trigger and scope | Deliberate relevant command; accurate consequences and safe cancellation; any unexpected-loss alert has destructive styling and no default. |
| All | Repeated triggers, focus transfer/restoration, keyboard navigation | No stacked alerts, accidental repeated commit, or loss of task context. |
| All | Native Mac rendering, enlarged text, VoiceOver names/order and control activation | Labels remain readable and distinct; accessible names and activation match the specified outcomes. |

## Evidence still missing

No source code, framework/SDK/version details, screenshots, actual handlers, key equivalents, focus configuration, menu wiring, or data/history implementation were supplied. Need these to establish whether roles, styling, default activation, cancellation, and command scope match this contract. In particular, verify B’s archive boundary and displayed irreversibility warning, A’s undo/history behavior beyond the brief’s assertion, and C’s actual affected data and recovery possibilities.

A runnable Mac build and controlled test data are needed to execute the acceptance checks, including native Return/Escape/Command-Period behavior, focus restoration, VoiceOver, enlarged text, and rendering. No device, GUI, SDK compilation, accessibility, or runtime execution is claimed. This review delivers decisions and proposed acceptance criteria; it does not establish that the app has been corrected.
