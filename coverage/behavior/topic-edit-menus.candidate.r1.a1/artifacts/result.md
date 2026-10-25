# Repair outcome

Patched interface.md in place, replacing the original single-paragraph brief with an implementable command, selection, failure, and recovery specification for the custom iPad annotation view.

## Decisions and changes

- Replace the bespoke long-press menu with the system edit menu, preserving horizontal touch and vertical keyboard/pointer presentations and system placement/shape behavior.
- Remove Rename Account and hidden Delete All from the selection menu. Their broader tasks remain outside this repair. Delete now explicitly means selected text only.
- Preserve selection independently of menu focus and validate annotation identity, revision, and range before committing changes.
- Specify Copy, Cut, Paste, Delete, and Select All eligibility for selected, empty, and read-only states. Paste accepts usable nonempty plain text; unsupported data cannot enable it.
- Make Cut copy successfully before removal, preserve text on failures, and distinguish Delete's lack of pasteboard writes. Make successful mutations atomic undo units with exact text/selection restoration and visible recovery.

The format policy, transaction rules, stale-target handling, and history lifetime are product decisions. HIG supports the interaction principles; it does not establish an SDK implementation or prescribe these exact transaction mechanics.

## Worked before/after

Start with editable annotation `Review blue notes`, selecting `blue`, and a pasteboard containing only an image.

Before (from the supplied brief): opening the bespoke menu loses selection, offers Rename Account and hidden Delete All, and shows Paste despite unsupported data. Cut removes selection before copying succeeds and is irreversible. This is the specified failure model, not a reproduced device trace.

After (required behavior): opening the system menu preserves `blue` as the command target. Copy, Cut, Delete, and Select All are eligible; Paste is omitted because an image alone is unsupported. No account or bulk-delete command appears. If Cut's pasteboard write fails, text remains `Review blue notes`, `blue` remains selected, and history is unchanged. If it succeeds, the pasteboard contains `blue`, the annotation becomes `Review  notes`, and the caret sits where `blue` began. Undo restores `Review blue notes` with `blue` selected; Redo removes it again. Neither history action changes the pasteboard. With compatible text `green`, Paste replacing `blue` instead yields `Review green notes`; one Undo restores `blue` and its selection.

## Acceptance checks

Static specification checks — passed by inspection of the revised artifact:

- All supplied defects have explicit replacement rules: unrelated commands, selection loss, unsupported Paste, and destructive Cut ordering.
- Command table covers empty selection, read-only content, exact target scope, and Cut versus Delete pasteboard effects.
- Failed operations preserve content and create no history entry; stale asynchronous targets cannot mutate a new range.
- Undo/Redo units, restored selection, reveal behavior, redo invalidation, and save/close boundaries are defined.

Runtime acceptance — not executed; expected results for implementation validation:

| Scenario | Required result |
| --- | --- |
| Open, navigate, dismiss, and reopen menu on multiline selection | Same range and annotation remain selected; no edit or history entry. |
| Empty selection and empty annotation | Copy/Cut/Delete absent; Select All absent for empty text; compatible Paste available only at a valid editable caret. |
| Read-only prose or identifier | Selection and Copy work, including across lines; no mutation commands. |
| Empty, image-only, unreadable, mixed rich/plain, and valid text pasteboard | Only usable nonempty plain text qualifies; replacement/insertion occurs exactly once. |
| Clipboard changes after menu opens | Eligibility is revalidated; failed decoding leaves text and selection intact. |
| Inject Copy/Cut transfer failure or removal failure | No text loss or history entry; after successful copy followed by failed removal, copied clipboard text may remain. |
| Delete selected text with known clipboard sentinel | Only selected text disappears; clipboard sentinel remains unchanged. |
| Change selection/revision or remove annotation during pending transfer | No stale mutation or guessed new target. |
| Cut, Paste replacement, Delete; Undo/Redo each | Exact before/after text and selection/caret restored; clipboard unchanged by history actions. |
| Undo, then new edit; save; close/reopen | Redo branch cleared by new edit; save retains history; reopened session starts fresh. |
| Undo an offscreen deletion | Restored text becomes visible without unnecessary context loss. |
| Touch and keyboard/pointer menu activation | Native horizontal/vertical presentations, system pointer shape, essential content unobscured, and focus returns to the text range. |
| Standard iPadOS undo/redo gestures | Same history units as commands; annotation gestures do not intercept them. |

Failed checks: none recorded against the revised specification. The original brief describes failures; no runtime checks were attempted. Passing the static checks does not establish the runtime outcomes above.

## Local evidence and limits

Read the installed root `.agents/skills/apple-hig/SKILL.md` explicitly, searched `references/topic-index.md`, then read each owning family and exact topic procedure before its article. All reads used individual-file commands. Routes consumed:

| Family | Topic procedure | Supporting article |
| --- | --- | --- |
| apple-hig-menus-and-actions | .topics/apple-hig-edit-menus/SKILL.md | references/edit-menus.md |
| apple-hig-inputs | .topics/apple-hig-focus-and-selection/SKILL.md | references/focus-and-selection.md |
| apple-hig-content | .topics/apple-hig-text-views/SKILL.md | references/text-views.md |
| apple-hig-patterns | .topics/apple-hig-undo-and-redo/SKILL.md | references/undo-and-redo.md |

These paths resolve under `.agents/skills/apple-hig/subskills/<family>/`. The supplied interface.md and installed local snapshot are the only substantive evidence. No web browsing occurred. Official links below identify the local guidance's source; they were not fetched:

- [Edit menus — Best practices and iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/edit-menus): system menu, relevant actions, Cut/Delete semantics, and platform presentations.
- [Focus and selection — Best practices](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices): selected state and focus are distinct.
- [Text views — Best practices](https://developer.apple.com/design/human-interface-guidelines/text-views#Best-practices): useful text should support selection/copy.
- [Undo and redo — Best practices](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#Best-practices): predictable recovery, meaningful history, operation descriptions, and visible restoration.

No application source, SDK version, device, simulator, GUI, or accessibility execution was supplied or run. Native pasteboard permissions, menu geometry, focus return, gesture integration, assistive-technology behavior, and SDK availability remain unverified. This work repairs the specification; it does not demonstrate implementation compliance.
