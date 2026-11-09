Use one composer presentation with internal navigation, a visible exit, and a shared policy that protects drafts on every dismissal path.

**Before → after**

| Before | Revised behavior |
|---|---|
| Composer → attachment modal → settings modal | One composer sheet; Attachments and draft-specific Options are internal navigation destinations. App-wide Settings stays in Browse. |
| Untitled composer | Title: **New Draft**; use **Edit Draft** when reopening. |
| Downward swipe is the only exit | Root toolbar has **Cancel** leading and **Done** trailing. Swipe and supported keyboard dismissal use the same exit policy. |
| Swipe or Done deletes writing | **Done saves the draft**. Cancel or swipe resolves unfinished changes before dismissal. |
| Upload error opens two alerts | Show upload failures inline with **Retry** and **Remove**. A single presentation coordinator prevents simultaneous alerts. |
| No attachment Back action | **Back** returns one step and preserves text, attachment choices, and upload state. |

This follows Apple’s guidance on [titled tasks, discoverable exits, and avoiding modal stacks](https://developer.apple.com/design/human-interface-guidelines/modality), [sheet navigation and dismissal](https://developer.apple.com/design/human-interface-guidelines/sheets), and [reserving alerts for necessary interruptions](https://developer.apple.com/design/human-interface-guidelines/alerts).

**Revised state specification**

Assumption: Done means saving a draft; publishing or sending is a separate action.

| State | Actions and transitions | Data contract |
|---|---|---|
| **Browse** | New Draft → Composer; select saved draft → Composer | Restore durable content, attachment references, and draft options. |
| **Composer** | Attachments → Attachments; Options → Draft Options; Done → Saving; Cancel/swipe → exit policy | Browse is blocked while the sheet is open. Keep a recoverable local working copy as edits occur. |
| **Attachments** | Back → previous composer step; select/remove/retry attachments in place | Back never discards writing or dismisses the composer. Failed uploads retain their local files and selections. |
| **Draft Options** | Back → previous step | Changes belong to the same draft transaction. App-wide settings are outside this flow. |
| **Resolve Exit** | **Save Draft** → Saving; **Discard Changes** → Browse; **Cancel** → originating step | Show “Save changes to this draft?” Discard is destructive. For a new draft it removes the working copy; for an existing draft it restores the last explicitly saved version. |
| **Saving** | Success → Browse; failure → originating step with an actionable error | Close only after durable save succeeds. Preserve working content on failure. Prevent duplicate saves. |

The **exit policy** applies from every internal step:

- No changes: dismiss to Browse.
- Changed content: cancel the attempted dismissal and show the exit choices.
- Cancelling the choices, including keyboard cancellation, returns to the same step with all content intact.
- Done saves; it never triggers discard. Pending or failed uploads remain recorded in the saved draft and can resume or retry later.

Recovery copies survive interruption or relaunch. Only successful save or deliberate discard clears the relevant recovery state. Reopening returns to the composer root, without resurrecting stale alerts or nested screens.

**Presentation contract**

- **iPhone:** Use a large composer sheet to give writing room.
- **iPad:** Prefer a standard centered page/form sheet with appropriate sizing.
- Both use the same states and data policy. Navigation changes screens inside the existing sheet.
- Only one decision overlay may be active. Deduplicate repeated error events; keep other failures inline until the current decision finishes. Never present an alert over an alert or exit confirmation.
- Return focus to the invoking control after internal navigation, and to the initiating Browse control after dismissal.

**Acceptance checks — specified, not executed**

1. Enter text, add an attachment, then try Cancel, swipe, and supported keyboard dismissal. Each offers the same save/discard resolution; cancelling preserves the exact work and current step.
2. Tap Done. The draft appears in Browse and reopens intact. Simulate save failure: the composer stays open with recoverable content.
3. Exit an unchanged composer. It closes without a warning.
4. Choose Discard Changes. A new draft is removed; an existing draft reopens at its last saved version.
5. Navigate through Attachments and Options, then use Back repeatedly. Each action returns one step without losing edits.
6. Rapidly tap an upload error and trigger multiple failures. No simultaneous alerts, duplicate dialogs, or lost attachment files occur.
7. Background and terminate the app after editing; relaunch. Recover the working draft without stale presentations.
8. On iPhone and iPad, verify sizing, rotation, keyboard access, large text, VoiceOver labels, and focus restoration. All exits and actions remain reachable.