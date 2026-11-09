The revised flow uses one composer presentation on both iPhone and iPad. Attachment and settings screens sit inside its navigation stack. Unfinished writing survives every dismissal.

### Revised specification

**States and navigation**

```text
Browse
  └─ Composer sheet: “New Draft”
       ├─ Attachments → Attachment details
       └─ Draft Settings
```

- Present one adaptive sheet, sized appropriately for iPhone and iPad.
- Push attachment and settings screens within that sheet; do not present additional sheets or modals.
- Give each screen a visible title. Use “Edit Draft” when reopening saved work.
- Attachment details return to Attachments with **Back**. Attachments and Draft Settings return to the composer with **Back**, retaining all changes.
- Keep **Close** available throughout the flow.

**Draft preservation and exit**

- Create a recoverable draft when the user first enters content or selects an attachment. Save changes continuously.
- **Done** saves the draft and returns to Browse. It does not publish or delete.
- **Close**, downward swipe, and any system dismissal permitted by the presentation save the draft and return to Browse.
- If persistence fails, keep the composer open, retain the content in memory, and show a retryable error. Interactive dismissal must not bypass this protection.
- Delete unfinished work only through an explicit **Discard Draft** action followed by confirmation. Canceling confirmation preserves the draft and current screen.
- Reopening a draft restores its text, attachment selections, and settings. Failed uploads remain visible and retryable.
- An empty, untouched composer can close without creating a draft.

**Errors and transient UI**

- Show upload failures inline beside the affected attachment, with **Retry** and **Remove** actions.
- Route any necessary alerts through one presentation coordinator. Allow at most one alert or confirmation at a time; coalesce repeated taps for the same error.
- Never present an alert over another alert or confirmation. Reevaluate queued errors before displaying them so resolved errors do not reappear.

### Before and after

| Before | After |
|---|---|
| Composer → attachment modal → settings modal | One composer sheet with internal navigation |
| Untitled composer | “New Draft” or “Edit Draft” |
| Downward swipe is the only exit | Visible Close and Done; supported system dismissal |
| Swipe or Done silently deletes writing | Every ordinary exit preserves the draft |
| Error taps can open two alerts | Inline recovery; centrally serialized alerts |
| Attachment flow has no back action | Back at every nested level, preserving changes |

### Acceptance checks

Run these on both iPhone and iPad:

- Open Attachments, attachment details, and Draft Settings. Only one sheet is presented; Back returns one level without losing edits.
- Enter text, select attachments, and change settings. Exit separately using Done, Close, swipe, and any supported outside-tap dismissal. Reopen and verify all changes remain.
- Background and terminate the app after a save completes. Relaunch and verify the draft is recoverable.
- Force a save failure, then attempt each exit. The composer remains open, content remains intact, and retry succeeds.
- Trigger an upload failure and tap it repeatedly. No overlapping alerts appear; Retry and Remove work.
- Trigger two errors while a discard confirmation is visible. No second presentation appears; resolved errors are not shown later.
- Choose Discard Draft, then cancel. Everything remains. Confirm discard and verify only that draft is deleted.
- Open and close an untouched composer. No empty draft is added.
- Verify titles, Back, Close, Done, and error actions remain accessible with VoiceOver, large text, rotation, and iPad window resizing.