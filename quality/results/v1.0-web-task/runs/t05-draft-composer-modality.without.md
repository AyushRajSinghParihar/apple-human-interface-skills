Use one composer sheet with internal navigation, persistent drafts, and one centrally controlled dialog.

**Revised specification**

| State | Presentation and actions | Transition |
|---|---|---|
| Browse | Show **New Draft** and saved drafts. | Open a new or existing draft in the composer sheet. |
| Composer | Title: **New Draft** or **Edit Draft**. Show **Close**, **Done**, Attachments, and Settings. | Attachments and Settings push pages inside the same sheet. |
| Attachments | Title: **Attachments**. Show **Back**; deeper attachment steps also provide Back. | Back returns one level, preserving text, selections, and upload status. |
| Settings | Title: **Draft Settings**. Show **Back**. Changes apply to this draft and persist. | Back returns to the originating page. |

Settings opened from Attachments returns to Attachments. Neither destination presents another app sheet. This follows Apple’s guidance to show one sheet and provide a clear path through modal subviews. [Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets), [Modality](https://developer.apple.com/design/human-interface-guidelines/modality)

**Draft and dismissal rules**

- Autosave text, draft settings, attachment references, and upload status locally as they change. Saving a draft does not require successful upload or network access.
- **Done** saves and dismisses. It never publishes or deletes.
- **Close**, a completed downward dismissal gesture, and any supported outside-tap or keyboard dismissal save and dismiss the entire composer flow. A gesture that only changes sheet height does not exit.
- Dismiss only after the latest changes are durably saved. If saving fails, keep the composer open with the writing intact and offer Retry.
- Reopening a saved draft restores its content and attachment status. Backgrounding and relaunch restore the last durable version.
- Deletion requires **Discard Draft**, followed by a destructive confirmation: **Discard Draft** / **Keep Editing**. Canceling preserves the current page and content. Never discard because of a swipe, Done, Back, upload failure, or canceled confirmation.

**Errors and presentation ownership**

Use one presentation coordinator with a single optional dialog state, rather than separate alert flags. Repeated taps on the same upload error open one dialog with **Retry** and **Close**. Retry dismisses the dialog before starting one retry. Other errors remain inline until selected; asynchronous failures never stack alerts. Ignore callbacks for drafts or uploads that are no longer active.

**iPhone and iPad**

Keep the same states, actions, save rules, and navigation on both. Adapt the sheet’s size to available space: a compact-width presentation on iPhone and an appropriately sized sheet on iPad. Resizing, rotation, and iPad multitasking must preserve the active draft and navigation position. Visible buttons provide every essential action without requiring gestures.

**Before → after**

| Before | After |
|---|---|
| Composer → attachment modal → settings modal | One sheet containing navigable pages |
| Untitled composer | New Draft / Edit Draft |
| Swipe-only exit | Close and Done, plus supported system dismissal |
| Swipe or Done silently deletes writing | Save before dismissal; explicit confirmed discard |
| One error can open two alerts | One dialog owner; duplicate events coalesced |
| Attachment flow has no return path | Back at every nested step |

**Acceptance checks**

Run these on iPhone and iPad, including iPad multitasking:

1. Open Attachments, then Settings. Exactly one app sheet exists; Back returns Settings → Attachments → Composer.
2. Enter text and add an attachment. Back navigation preserves both.
3. Exit separately using Done, Close, and each supported system dismissal. Reopen: all saved content remains; nothing was published.
4. Force a save failure during exit. The composer stays open with its text intact; Retry saves and then permits dismissal.
5. Cancel Discard Draft: everything remains. Confirm it: only the selected draft is deleted.
6. Rapidly tap an upload error and deliver simultaneous failures. At most one dialog appears; Retry starts one operation.
7. Fail an upload offline. Save and reopen the draft: text and attachment status remain available for retry.
8. Background and relaunch after a completed autosave. Restore the saved draft. Rotate or resize during editing without losing content or navigation.
9. Complete navigation, saving, dismissal, and discard using VoiceOver and visible controls without swiping.