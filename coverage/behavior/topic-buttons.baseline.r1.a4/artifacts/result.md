# iPad field-report export controls: correction plan

Review basis: `interface.md`, a supplied textual description, not an executed interface. All four functions remain: Publish, Preview, Save Draft, Delete. Rankings below reflect potential harm and task obstruction, not measured incident rates.

## Ranked verified findings

| Rank | Verified observation and effect | Correction and source basis |
| --- | --- | --- |
| 1 — High | During an eight-second Publish upload nothing changes; repeated taps create duplicate uploads. People cannot tell whether activation worked and can publish repeatedly. | Immediately show an activity indicator inside Publish, replacing any image, with “Publishing…”; reject repeated activation while pending. The iPadOS-specific [Buttons guidance](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS) calls for in-button activity feedback for delayed completion. Duplicate prevention is an engineering decision supporting that feedback, not an explicit HIG protocol. |
| 2 — High | Every hit region is 20 × 20 pt with 2 pt gaps. Small, crowded targets increase missed and adjacent activations, particularly near Delete. | Use nonoverlapping hit regions at least 44 × 44 pt, with clear separation; choose 12 pt clear gaps as an initial layout specification, then validate usability. [Buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices) gives general 44 × 44 pt hit regions and sufficient surrounding space. [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility) lists iPadOS 44 × 44 pt default controls and 28 × 28 pt minimum controls. These are different specifications: do not recast 28 as a 44 pt universal minimum. The supplied 20 pt fails both; use the conservative 44 pt hit-region target here. The exact gap is a product choice, not an Apple minimum. |
| 3 — High | Delete is the editor’s primary/default action. Accidental default activation risks data loss; reversibility is unknown. | Remove its primary/default role; give it a destructive role, explicit “Delete” label and separation from Publish. Choose Publish as the expected action for this export-focused footer, pending validation of actual task frequency. [Buttons — Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role) generally assigns primary to a likely nondestructive action. |
| 4 — High | Glyph-only Preview has no accessible name. Assistive users cannot reliably identify its purpose. | Show “Preview” and expose the accessible name “Preview”, button semantics, enabled state and focusability. A familiar supplementary icon is optional. [Accessibility — Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision) supports meaningful VoiceOver descriptions and labels for Voice Control. |
| 5 — Medium | All four buttons have equal filled prominence. The footer gives no useful priority and makes destruction compete with export. | One prominent Publish button; secondary Preview and Save Draft; visually separate destructive Delete without primary fill. Keep comparable sizing, distinguishing priority through style. [Buttons — Style](https://developer.apple.com/design/human-interface-guidelines/buttons#Style) advises one or two prominent actions per view. This is guidance, not an absolute maximum. |

## Decisions and corrected behavior

Use framework-neutral button semantics and explicit roles; use equivalent built-in components if the eventual framework supplies them. This specification requires no Apple SDK. Each control receives visible press feedback and keyboard/accessibility activation equivalent to touch, following [Buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices).

The resting footer concept is:

`[Delete: destructive]   [Save Draft: secondary] [Preview: secondary] [Publish: prominent]`

This is logical grouping, not a pixel-perfect rendering. Keep all four discoverable; reflow into rows when width or enlarged text requires it. Never shrink hit regions or truncate action meanings to preserve a single row. Provide sufficient separation and non-color cues for Delete; support text enlargement of at least 200%, following [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). Contrast and final layout require measurement later.

Delete remains an explicit action, but its protection depends on actual data semantics. For common undoable deletion, provide reliable Undo rather than routine confirmation. If deletion is uncommon and irreversible, confirm with “Delete Report?”, a truthful consequence message, Delete and Cancel, and no default so activation is deliberate. The editor’s destructive default is distinct from the deliberate-destruction confirmation exception: [Alerts — Best practices and Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons) permits a normal default for explicitly requested destruction, requires Cancel alongside destructive actions, and says not to make Cancel the default. Do not infer a missing confirmation defect from the supplied description. If Assistive Access is supported, separately address its two-confirmation guidance for difficult-to-reverse actions in [Accessibility — Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive).

During publishing, keep the button’s position and size stable. Expose “Publishing…” and busy/unavailable state to assistive technology; announce start and terminal status without moving focus or announcing every progress tick. Use an indeterminate in-button indicator when duration is unknown. If end-to-end progress is measurable, add honest progress in a stable adjacent status region; do not invent a percentage from elapsed time or treat transferred bytes as completed publication. Explain extended stalls with a useful recovery path. These choices apply [Progress indicators — Best practices](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices).

Publish an immutable report revision. Preview and Save Draft remain available during upload; edits and draft saving affect the current draft, not the in-flight revision. Temporarily disable Delete with an explanation while the report is publishing to avoid a delete/publish race. Do not block the entire editor. These concurrency choices are product decisions requiring backend support.

Offer Cancel Upload only if the service can safely cancel or reconcile an already committed publish; otherwise explain that publication is still being checked. Never present cancellation as successful before acknowledgement. HIG advises allowing cancellation where safe and explaining consequential cancellation; safe cancellation is not established by the supplied evidence.

## Framework-agnostic state specification

```text
states = idle | publishing | checkingOutcome | failed | published

activatePublish():
  atomically:
    if state in {publishing, checkingOutcome}: return
    if currentRevision already published: show its published status; return
    operation = persistedOperation(reportID, immutableRevision, stableUniqueKey)
    state = publishing                 // before starting asynchronous work
  render busy Publish + "Publishing…"; announce start
  send operation using stableUniqueKey

receiveOutcome(operationID, outcome):
  ignore stale responses for a different operation
  if confirmed committed:
    persist published revision + result identifier
    state = published; remove indicator; show "Published"; announce completion
  else if confirmed not committed:
    state = failed; remove indicator
    show actionable failure + Retry; preserve report and draft; announce failure
  else:                               // timeout / connection loss is ambiguous
    state = checkingOutcome
    keep duplicate guard; show "Checking publication…"
    reconcile stableUniqueKey with service; offer Check Status

retry():
  only after confirmed failure, retry the same logical operation/key
  transition synchronously to publishing; preserve the same duplicate guard

on edit after success:
  mark new revision unpublished; restore Publish for that revision
```

The server must persistently deduplicate the stable operation key and return the same outcome for retransmissions. Persist and reconcile pending operations after reload/reconnect. A UI lock alone cannot guarantee exactly one published report. If no service deduplication/status contract exists, that is an implementation dependency to resolve, not a verified existing capability. Success for an older revision must identify that revision and leave newer edits marked unpublished. A successful unchanged revision retains an accessible Published status and cannot accidentally republish.

## Worked before/after: slow upload

**Before (supplied):** At t=0 a person taps Publish. The footer remains unchanged for eight seconds. At t=2 and t=5 they tap again; the supplied behavior creates duplicate uploads. Delete remains the primary/default action, and Preview is unnamed.

**After (specified):** At t=0 the handler atomically guards the operation, captures revision R7 and renders `[indicator Publishing…]` before awaiting the network. The footer still offers Preview and Save Draft; Delete is temporarily unavailable with “Available after publication finishes.” At t=2 and t=5 further Publish activations do nothing and create no requests. At t=8, only a confirmed server commit changes the control to Published, removes the indicator, and announces “Report published.” If R8 was edited meanwhile, the status says “Revision R7 published; newer changes are unpublished,” and Publish becomes available for R8. If the connection instead drops at t=8, show Checking publication and reconcile the original operation rather than starting another publish. This is an illustrative target sequence, not a measured execution.

## Acceptance checks (to execute when an implementation exists)

- Inspect all four functions in normal and constrained-width layouts at 200% text: labels remain meaningful, all hit regions are at least 44 × 44 pt and do not overlap, and the chosen spacing separates adjacent actions. Verify touch near boundaries, including Delete.
- Verify only Publish is prominent/default in the resting export footer; Delete has destructive semantics and never responds as the editor’s default. Check deliberate activation, undo or conditional confirmation, and keyboard cancellation where applicable.
- Inspect the accessibility tree: Preview is named Preview; all buttons expose roles, names and availability. Manually verify touch, attached-keyboard focus/activation, VoiceOver, Voice Control, Switch Control and pointer behavior. Busy, success and failure status must be perceivable without relying on color or animation alone.
- Simulate an eight-second upload: start feedback appears on the next render without waiting for the request; repeated touch, keyboard and assistive activations create one logical operation. Preview and draft saving work; Delete cannot race the publish.
- Exercise confirmed success, confirmed failure, timeout after server commit, reconnect, reload and delayed stale responses. Retry/reconciliation preserves the operation key; server records show one publication per operation. No false success, stuck busy state, lost draft or silent publication of newer edits is acceptable.
- Verify honest progress across upload and finalization. Unknown duration has no invented percentage; extended stalls offer meaningful status/recovery. If cancellation is supported, test both precommit cancellation and commit/cancel races before claiming success.
- Measure final contrast and inspect enlarged-text/light/dark layouts. Treat these as follow-up checks, not verified defects in the textual interface.

## Evidence limits and instruction trail

The only product evidence is `interface.md`. Findings are verified against that description; no rendered app, implementation, backend contract, screenshot, target geometry measurement or runtime was supplied. No device, SDK, GUI, accessibility tool, upload or acceptance-check execution occurred. No web browsing was used. Official links above identify the source sections cited by the installed local snapshot; they were not fetched or independently verified as current.

Read the installed package root `apple-hig/SKILL.md` first, then these selected family procedures before their source guides: `subskills/apple-hig-menus-and-actions/SKILL.md` → `references/buttons.md`; `subskills/apple-hig-status/SKILL.md` → `references/progress-indicators.md`; `subskills/apple-hig-foundations/SKILL.md` → `references/accessibility.md`; `subskills/apple-hig-presentation/SKILL.md` → `references/alerts.md`. The root topic index was searched for exact component routes. All paths resolve within `.agents/skills/apple-hig`; each instruction/source read used a separate single-file command. These families route directly to the articles; no additional topic procedure was specified by those routes. The installed guides are dated 2026-10-25 and describe themselves as derived local guidance; their presence does not establish independent review.
