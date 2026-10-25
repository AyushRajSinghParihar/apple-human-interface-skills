# Attachment-action repair

Patched [interface.md](interface.md) in place with an implementable iPadOS presentation, action table, empty-selection rules, scoped data mutations, and questionnaire exit contract.

## Decisions

- Keep a deliberate post-action decision, anchored to the attachment-row button in wide windows, with compact adaptation. A generic menu request would instead require a menu. The supplied trigger intent was unspecified; the patch makes it explicit.
- Replace Yes with Use Selected Attachment and Other with Enter Supporting Details. The former links only the captured attachment to the captured claim; the latter opens a separate six-field sheet after the choices dismiss.
- Remove Delete Everything and its handler from attachment scope. A destructive color or extra confirmation would not repair unrelated claim deletion.
- Disable attachment use when selection is empty or already linked; keep the details route available and explain why attachment use is unavailable.
- Make cancellation harmless. Outside dismissal cancels the wide choice popover; compact presentation has Cancel. All edited questionnaire exit requests resolve discard versus keep editing, with draft retention during presentation replacement.
- Revalidate captured IDs and prevent duplicate commits. This is product safety policy, not an observed backend guarantee.

The original brief does not define Yes or the six field names. The revised specification explicitly assumes Yes links an attachment and the questionnaire supplies alternative evidence. Field content and validation remain existing product contracts; this work does not invent them.

## Worked before/after

Claim C42 has receipt R7 selected; unrelated claim C99 also exists.

Before: the row opens a distant centered action sheet with Yes, Other, Cancel, and Delete Everything. Yes has no specified outcome. Other starts six fields within an unspecified presentation. Delete Everything can remove C99.

After: Use Attachment opens a short popover at that row. Use Selected Attachment links R7 only to C42. If selection later changes to R8, the captured R7 remains the target and is revalidated; R8 is never silently substituted. Enter Supporting Details closes the choices and opens the C42 editor. After typing, Cancel offers Discard Changes or Keep Editing; the latter restores all six values. C99 remains untouched through every route. With no selection, attachment use is unavailable with an explanation, while details entry still works.

## Acceptance checks and status

Passed by static specification inspection:

| Check | Evidence in revised interface.md |
| --- | --- |
| Source relationship is explicit | Button-bounds anchor, visible filename, resize and missing-source rules |
| Every choice predicts its outcome | Labels, roles, availability and consequences table |
| No unrelated destruction | Delete Everything and handler removed; mutations restricted to captured IDs |
| Empty selection is safe | Disabled attachment command, explanatory row text, available details route |
| Questionnaire is a separate task | Dismiss-before-present sequence; centered form sheet; Cancel/Done contract |
| Edited exits preserve work | Shared Cancel/swipe/Escape/navigation policy; explicit discard; retained draft |
| Repeat and stale-target behavior defined | Single presentation, ID revalidation and idempotent linking |

Failed: none found in the revised specification during static review. This is not a runtime pass.

Not executed — implementation acceptance checks:

1. On iPad, invoke from rows near each screen edge, rotate and resize into compact width. Confirm native anchoring, readable choices without scrolling, and safe outside/Cancel dismissal.
2. Exercise valid, empty, already-linked and stale selection; change selection while choices are open. Verify only the captured eligible claim/attachment pair changes and unrelated claims remain identical.
3. Open details, complete valid/invalid input, and exercise clean and edited Cancel, swipe, Escape where supported, interruption, discard-decision dismissal and Keep Editing. Verify exact draft retention/discard and no stacked presentations.
4. Repeat invocation and linking during delay/failure. Verify one presentation, no duplicate association, and recoverable errors.
5. Check larger text, keyboard visibility, 44 × 44 pt button hit regions, pointer/keyboard activation, focus restoration, and VoiceOver names/order on the implemented interface.

## Evidence and limits

Read the installed root apple-hig SKILL.md explicitly, then presentation family → action-sheets, popovers and sheets procedures → their local references; menus-and-actions family → buttons procedure → reference; menus and pull-down-buttons procedures → references to distinguish menu-reveal alternatives; patterns family → modality procedure → reference to resolve edited exits. Each file read used its own cat command, with paths resolved inside the installed package.

Material recommendations are supported by the supplied local snapshots of [Action sheets](https://developer.apple.com/design/human-interface-guidelines/action-sheets), [Popovers](https://developer.apple.com/design/human-interface-guidelines/popovers), [Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets), [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons), and [Modality](https://developer.apple.com/design/human-interface-guidelines/modality). [Menus](https://developer.apple.com/design/human-interface-guidelines/menus) and [Pull-down buttons](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons) informed the rejected generic-menu interpretation. These are source links, not online verification. General popover anchoring guidance is applied to this action-sheet design; local guidance does not establish a particular SDK API or its default Cancel rendering.

Only the brief and local instructions were used. No web browsing, device, SDK build, GUI, accessibility execution, backend test, or hit-region measurement occurred. No implementation was supplied. Native presentation details, platform availability, assistive behavior, and actual data safety require implementation and execution; file edits establish only the revised specification.
