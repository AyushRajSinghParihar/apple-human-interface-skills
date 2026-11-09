The revised flow uses one composer presentation on both iPhone and iPad. Attachments and composer settings are destinations inside it. Leaving the composer preserves unfinished writing; deleting a draft requires an explicit action and confirmation.

### Before and after

| Before | After |
|---|---|
| Browse → composer sheet → attachment modal → settings modal | Browse → one composer sheet, with navigation to Attachments or Settings |
| Composer has no title | Root title: **New Message** or the appropriate content name; child screens: **Attachments** and **Settings** |
| Downward swipe is the only exit | A labeled **Close** button plus system dismissal gestures |
| Swipe or Done silently deletes the draft | Close, swipe, and Done preserve the draft; **Discard Draft** confirms before deletion |
| Upload errors can show two alerts | One presentation coordinator allows at most one alert |
| Attachment flow has no Back action | Every attachment screen has Back; returning preserves composer and attachment progress |

### Revised state specification

**State model**

```text
Browse
└─ Composer session — one sheet
   ├─ Compose(draftID)
   ├─ Attachments(draftID)
   │  └─ Attachment detail / upload status
   └─ Settings(draftID)
```

Attachments and Settings are navigation destinations, not additional sheets. Opening Settings from Attachments pushes it onto the same navigation stack; Back returns to Attachments.

Track these independently:

- **Draft:** content, attachment references and status, and draft-specific settings.
- **Navigation:** current composer destination and its back stack.
- **Transient alert:** none, upload error, or discard confirmation. Only one may be active.

**Draft lifetime and exits**

- Opening the composer creates a draft or resumes the selected existing draft.
- Persist edits continuously and when the app backgrounds. Restore the latest successfully persisted state after relaunch.
- **Close**, a downward swipe, and any supported outside-tap dismissal return to Browse and retain the draft for resumption.
- **Done** on the composer saves the draft and closes it. Done inside an editing destination commits that destination’s changes and returns to its parent.
- Sending or publishing uses a separate, explicit action. Remove the draft only after successful submission.
- **Discard Draft** shows: “Discard this draft?” with **Keep Draft** and destructive **Discard** actions. Keep Draft returns to the unchanged editing state.
- If persistence fails, retain the working copy, show a recoverable error, and prevent dismissal that would lose it. Never report the draft as saved.

**Attachments and errors**

- Back returns one level without clearing writing, selected attachments, or upload status.
- Upload failure keeps the attachment available for Retry or Remove; it never deletes the draft.
- Route error taps through one alert coordinator. Repeated taps on the same error do not create additional alerts.
- Distinct errors remain visible in attachment status and can be inspected after the current alert closes.
- System file or photo pickers may temporarily present from the active destination. Dismiss the picker before navigating or presenting an alert.

**iPhone and iPad**

Use the same state transitions and draft policy on both devices. Adapt sheet sizing to the available space. Always provide visible Close and Back controls; gestures, keyboard dismissal, and outside taps must not be required to complete the flow.

### Acceptance checks

1. **Safe exit:** Enter text and add an attachment. Test Close, Done, swipe dismissal, and supported iPad outside-tap dismissal. Reopening restores the draft.
2. **Recovery:** Background and relaunch the app after edits have persisted. Text, settings, and attachment status restore.
3. **Save failure:** Simulate persistence failure. The composer retains its content, shows recovery options, and prevents a lossy dismissal.
4. **Explicit discard:** Cancel discard confirmation and verify the draft is unchanged. Confirm Discard and verify only that draft is deleted.
5. **Single presentation:** Navigate Compose → Attachments → Settings. Verify there is one composer sheet and a working Back path through every destination.
6. **Attachment continuity:** Go Back during an upload or after failure. Verify writing and attachment status remain intact.
7. **Alert exclusivity:** Rapidly tap one or several upload errors. Verify at most one alert is visible and all failures remain accessible.
8. **Picker coordination:** Trigger an upload failure while a system picker is open. Verify no alert is stacked over it; the error remains accessible after dismissal.
9. **Submission:** Failed submission preserves the draft. Successful submission removes it only after success is confirmed.
10. **Device and accessibility coverage:** Repeat the flow on iPhone and iPad, including rotation, VoiceOver, and keyboard navigation. Titles, Close, Back, and destructive actions remain discoverable and usable.