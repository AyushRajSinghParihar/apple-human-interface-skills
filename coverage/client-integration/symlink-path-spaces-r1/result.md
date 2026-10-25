# iPad editor button review

Scope: review of the supplied behavioral brief, not an implementation inspection. No code, screenshot, hit-region measurements, or deletion semantics were supplied. This contract is framework independent. No browsing, builds, runtime tests, or Apple-device execution were performed.

## Installed guidance route

The project's `.agents/skills/apple-hig` installation link resolves to `/tmp/hig client install drpxs020/portable source with spaces/apple-hig`. Paths below are relative to that installed package, resolved from its routing links rather than the working directory:

1. `SKILL.md`
2. `subskills/apple-hig-menus-and-actions/SKILL.md`
3. `subskills/apple-hig-menus-and-actions/.topics/apple-hig-buttons/SKILL.md`
4. `subskills/apple-hig-menus-and-actions/references/buttons.md`

Searched relevant rows in `references/topic-index.md` before finalizing the route. The destructive-default decision also required the Presentation family → Alerts procedure → `references/alerts.md`. Each full-file read used its own `cat` command. Guidance is the installed 2026-10-25 snapshot; official links below are attribution, not claims of live verification.

## Findings

| Supplied evidence | Effect and source-backed assessment | Correction |
| --- | --- | --- |
| Delete is the default. | Accidental default activation can cause loss. Generally, primary/default should be the likely nondestructive action. | Remove Delete's editor-level default status; give it destructive semantics. Confirm its scope and reversibility before specifying recovery. [Buttons: Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role) |
| Publish and Preview have equal prominence. | This can obscure priority if publishing is the editor's main task, but equal prominence alone is not a violation: guidance permits one or two prominent likely actions. | Proposed product hierarchy: Publish primary, Preview secondary, using style rather than unequal sizes. Validate that publishing is the intended primary task. [Buttons: Style](https://developer.apple.com/design/human-interface-guidelines/buttons#Style) |
| Repeated Publish activation starts duplicate uploads. | The action lacks a reliable pending contract. The procedure requires duplicate-activation handling; iPadOS guidance calls for activity indication within the initiating button. | Admit one publish operation per document revision, indicate pending state in Publish, and reject duplicate activation in the command handler. The deduplication mechanism below is an engineering proposal, not a prescribed HIG API. [Buttons: iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS) |

## Corrected action contract

Retain the existing editor action surface; its exact placement is unknown. These are immediate commands, not persistent selection controls. Prefer system button styles when available in the existing stack; custom controls need perceivable press feedback. Give every action a distinct, nonoverlapping selectable region of at least **44 × 44 pt** with surrounding separation; visual glyph size alone does not establish target size. Use readable short labels and accessible names identifying the same outcomes. [Buttons: Best practices, Content, Style](https://developer.apple.com/design/human-interface-guidelines/buttons)

| Control | Outcome and affected object | Role, default and availability | State contract |
| --- | --- | --- | --- |
| Publish | Submit a captured revision of the current document for publication. Exact destination and public visibility must be established before implementation. | Primary and most prominent, assuming publishing is the likely task; eligible editor default only when valid and ready. Never install an unscoped Return handler that steals text-entry Return. No new keyboard shortcut is prescribed. | Ready → Publishing → Published or Failed/Uncertain, as below. Explain unavailable prerequisites if context does not make them clear. |
| Preview | Open a preview of the current draft without uploading, publishing, or deleting it. | Normal role, secondary style; no editor default. Available when a valid preview can be generated. | Returning from preview preserves draft content and editing context. During publishing, it may remain available only if it cannot mutate or resubmit the captured revision. |
| Delete | Delete the current document; affected object, local/remote scope and reversibility remain unknown. | Destructive role, lower emphasis, never the editor default. Disable while publication is unresolved under this proposed contract, with the reason available. | Do not commit deletion until its consequence/recovery policy is resolved. If uncommon and irreversible, use the confirmation contract below. |

Publish behavior (proposed implementation-neutral reliability design):

1. Atomically change Ready to Publishing and capture document ID/revision **before** starting asynchronous work. All activation routes share this gate, including touch, pointer, keyboard, and accessibility actions.
2. Show an activity indicator inside Publish, replacing its image if present; optionally label it “Publishing.” Keep the operation's context visible. Make additional activations unavailable and ignore any that still reach the handler. UI disabling alone is insufficient for races. [Buttons: iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS)
3. Associate the logical publication with a stable operation identifier. Where the service supports it, deduplicate retries server-side using that identifier. If editing remains available, later edits belong to a different revision and cannot silently enter this operation.
4. Mark Published only after authoritative completion, not on press feedback or request dispatch. Report which revision was published and prevent another activation from republishing the same completed revision unintentionally.
5. On a confirmed failure, preserve the draft, explain the problem in context, and permit an explicit retry. On a timeout with uncertain outcome, reconcile operation status before starting another publication; reuse the logical operation identity for retries. Never claim failure proves nothing was published.

Deletion decision: inspect reversibility first. Common undoable deletion generally needs no confirmation; uncommon irreversible destruction does. For the latter, propose title “Delete This Document?”, a message naming the document and verified scope of permanent loss, and “Delete Document” plus “Cancel.” Use no default to require deliberate choice; Cancel performs no mutation and restores editor context. Do not make Cancel the default. This is a conservative product choice: the guide expressly permits a normal destructive default in a confirmation of explicitly requested destruction, so “destructive actions can never be default” would be inaccurate. [Alerts: Best practices, Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts)

## Proposed checks and evidence status

**Passed — document review only:** installed root → family → buttons procedure → guide route read; topic index searched; alert handoff read; all three supplied controls mapped to button contracts; framework independence preserved.

**Failed — supplied behavior, not independently reproduced:** Delete is the editor default despite the likely nondestructive task; repeated Publish starts duplicate uploads. Equal Publish/Preview prominence remains a hierarchy decision to validate, not a proven HIG failure.

**Not executed — acceptance checks:**

| Check | Expected evidence/result |
| --- | --- |
| Publish once, then rapidly repeat activation through every supported input route | Exactly one logical publication and one captured revision; pending indication appears immediately. Include concurrent handler calls, not just sequential taps. |
| Delay response, retry after timeout, and deliver late success | Reconciliation/deduplication prevents duplicate publication; UI reflects the authoritative result. |
| Confirmed failure, then explicit retry | Draft survives; error is understandable; retry completes without creating duplicate effects. |
| Edit while publishing, then complete | Published revision is identified correctly; later edits remain intact and unpublished. |
| Activate Preview and return | No upload/delete occurs; draft and editing context survive. |
| Activate editor default or Return while editing text | Delete never runs; text input keeps its expected Return behavior; only a valid scoped primary command publishes. |
| Exercise Delete after defining scope/reversibility | Outcome matches the label; irreversible confirmation names real loss; Cancel and supported Escape/Command-Period paths leave data intact. Verify any recovery mechanism if chosen. |
| Inspect layout and enlarged/localized labels | Targets measure at least 44 × 44 pt, do not overlap, and labels do not clip; Publish's priority uses style rather than unequal peer sizes. |
| Inspect control states and names; exercise on iPad with assistive technology | Correct labels/names, focus, disabled reasons and press feedback; pending/completion are perceivable. Native rendering, VoiceOver behavior, physical targeting comfort and keyboard behavior require actual execution. |

No runtime or device check above is claimed as passed. Deletion scope/reversibility, publication semantics, exact placement, target geometry, and actual accessibility behavior remain unverified.
