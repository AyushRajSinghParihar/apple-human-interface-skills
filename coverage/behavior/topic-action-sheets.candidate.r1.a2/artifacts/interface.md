# iPad claims form: attachment decision

## Scope and assumptions

Platform: iPadOS, including narrow multitasking windows. Replace the detached, centered attachment choice with the contract below. The original meaning of Yes is unspecified: this revision assumes it means using the selected attachment for the current claim. Other becomes manual entry of attachment details through the existing six-field questionnaire. Preserve those six fields and their domain validation; their names were not supplied.

## Trigger and context

Each attachment row has a text button, **Use Attachment**. Activating it captures the current claim ID and that row's attachment ID. Show the filename in the row and decision context. Explicit row context suffices even when global selection is empty.

For a selection-dependent entry point with neither row context nor a valid selected attachment, disable Use Attachment and show **Select an attachment to continue.** Do not open a choice or silently pick the first attachment. Selecting a valid attachment enables the action.

Every transition and commit must revalidate the captured claim/attachment relationship. A subsequent selection change must never retarget the decision or questionnaire. If the captured attachment disappears or becomes invalid, close the choice, retain any questionnaire draft, make no mutation, and show **This attachment is no longer available. Select another attachment.**

## Short choice

Use a system action sheet for these related alternatives following the deliberate Use Attachment action. This is a decision, not an explicit menu-reveal request.

In wide iPad layouts, present the choice as a popover anchored closely to the initiating row button, with its arrow pointing to that source and the filename/row visible. Do not center it independently of the trigger. Update the anchor on rotation, scrolling, and window resizing; safely dismiss if the source disappears. In compact layouts use the system's adapted modal presentation rather than forcing a floating popover.

Title: **Use this attachment?** Context: the captured filename.

| Label | Role | Outcome |
| --- | --- | --- |
| Use Attachment | Normal, nondestructive | Associate the captured attachment with the captured claim, then close on success. Repeated activation must not duplicate the association. |
| Enter Details Manually | Normal, nondestructive | Close the choice before opening Attachment Details for the captured IDs. No association or claim change is committed yet. |
| Cancel | Cancel | Close without changing attachments, claims, or questionnaire drafts. |

Keep the action list short, without questionnaire fields or scrolling at ordinary text sizes. Accommodate enlarged text without clipping or accidental activation. Use native cancellation behavior: the wide iPad popover may omit a visible Cancel row when outside dismissal supplies cancellation; retain the cancellation action in the model and expose Cancel when required by the adapted presentation. Outside tap, supported keyboard cancellation, and system dismissal cause no mutation. Do not assign an implicit commit default.

**Remove Delete Everything and its handler from this flow.** No attachment-choice action can delete any claim or attachment. Unrelated claim deletion is outside this specification. Do not substitute a newly invented deletion command.

If association requires delayed persistence, prevent duplicate activation and indicate activity. On failure keep the attachment uncommitted, preserve context, and show an inline explanation with a way to retry. Never close as though successful before persistence succeeds.

## Separate six-field task

Present **Attachment Details** as one centered system form/page sheet with standard sizing over a dimmed parent in a wide iPad window. In compact layouts use an expanded modal form with scrolling so all six fields and completion remain reachable with the keyboard visible. Dismiss the short choice first; do not cascade popovers or stack main-interface sheets.

Show the captured filename. Place **Cancel** at the top leading edge and **Done** at the top trailing edge. Done is enabled only when the existing six-field validation passes. Done saves the manual result for the captured IDs and closes on success. Validation failure stays in the form and identifies affected fields. Save failure preserves entered values and shows an inline explanation; retry uses Done. While saving, prevent duplicate saves and indicate activity in Done.

Clean Cancel or vertical dismissal closes without saving. Cancel or a vertical dismissal attempt after edits opens an unsaved-work action sheet with **Discard Changes** (destructive, first) and **Keep Editing** (safe cancellation). Discard Changes drops only this questionnaire's unsaved edits and returns to the claim. Keep Editing, outside dismissal of the decision, and keyboard cancellation restore the form unchanged. No Back control is needed for this single-view task.

On interruption retain the manual draft keyed to the captured claim and attachment. Resume restores it and revalidates the IDs before save. Invalidated drafts remain retained but cannot commit to another attachment implicitly.

## Controls and return context

Prefer native system controls and semantic roles. For iPadOS buttons provide at least 44 × 44 pt selectable regions and separation between adjacent targets. After completion or cancellation restore interaction context to the initiating row, or the attachment list if the row no longer exists. The form sheet can appropriately be centered; the temporary choice remains anchored in wide layouts.

## Acceptance contract

1. Row invocation names and affects the captured row attachment and claim even if global selection changes afterward.
2. Without row context or valid selection, no decision opens or data changes; selection guidance is visible.
3. Wide presentation follows its source; compact resize adapts safely. Enlarged labels remain readable and selectable.
4. Use Attachment associates once. Enter Details Manually opens the separate six-field task without committing. All choice dismissals preserve data.
5. No action in this flow deletes claims or attachments; unrelated claims remain identical through every path.
6. All six fields and Done remain reachable with the keyboard visible. Invalid input cannot save; failed saves retain values; repeated activation cannot duplicate writes.
7. Clean dismissal closes; edited dismissal either explicitly discards or retains work. Interruption preserves drafts. Missing attachments and selection changes cannot redirect commits.
8. Exercise cancellation, repeated invocation, rotation, window resize, target geometry, keyboard activation, and return context in an implemented iPad interface. These checks are required, not claimed executed.

## Guidance basis

The installed local snapshot supports short related alternatives after an intentional action ([Action sheets](https://developer.apple.com/design/human-interface-guidelines/action-sheets#iOS-iPadOS)), close source anchoring and compact adaptation ([Popovers](https://developer.apple.com/design/human-interface-guidelines/popovers#Best-practices)), scoped form tasks and edit-safe dismissal ([Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets#iOS-iPadOS)), and clear labels, roles, and target regions ([Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)). Exact task labels, captured-ID binding, removal of deletion capability, and draft persistence are product decisions applying that guidance.
