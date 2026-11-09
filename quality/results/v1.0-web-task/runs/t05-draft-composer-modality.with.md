Use one titled composer with internal navigation, persistent drafts, and a single owner for temporary presentations.

**Before → after**

| Before | Revised behavior |
|---|---|
| Browse → composer sheet → attachment modal → settings modal | Browse → one composer sheet; Attachments and Draft Options are internal pages |
| Untitled composer | Title: **New Draft** |
| Swipe is the only exit | Visible **Close** and **Done**, plus supported swipe/keyboard dismissal |
| Swipe or Done deletes writing | Close preserves unfinished work; Done saves before closing |
| Upload error opens two alerts | Inline upload recovery; at most one decision overlay |
| Attachment flow has no Back | Back returns one step and preserves writing and confirmed attachments |

This applies Apple’s guidance on clear task titles, discoverable exits, protected work, internal back navigation, and avoiding stacked presentations. [Modality](https://developer.apple.com/design/human-interface-guidelines/modality), [Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets)

**Revised state specification**

Assumption: **Done saves a draft**. Publishing or sending is a separate, explicitly named action.

State model:

```text
Browse ↔ Composer(Editor ↔ Attachments ↔ AttachmentDetail)
                    ↕
                DraftOptions

Decision overlay: none | exitResolution | criticalError
Persistence: saved | saving | failed
```

- Present one composer sheet over Browse; Browse is unavailable until it closes.
- Editor shows **New Draft**, leading **Close**, and trailing **Done**.
- Attachment pages show **Back**. Selecting **Add** commits selected attachments to the draft and returns to Editor. Back abandons only unconfirmed selection; it never deletes draft content.
- Draft-specific settings become **Draft Options**, reached from Editor with Back navigation. Changes belong to that draft.
- App-wide Settings belongs outside composition. Preserve and close the composer before navigating there; offer **Resume Draft** afterward.

| Event | Transition and data outcome |
|---|---|
| New Draft / Resume Draft | Open Editor with a new draft identity or the retained draft |
| Edit text, attachments, or options | Persist locally as changes occur; retain attachment files and upload status |
| Back | Return one internal step; preserve committed draft changes |
| Done | Finish saving the latest revision, then close to Browse; never delete or publish |
| Close, downward dismissal, supported Escape, or outside dismissal | Use the same exit handler from every internal page |
| Exit with no changes | Close; leave any existing draft intact |
| Exit with changed content | Hold dismissal and offer **Save Draft**, **Discard Changes**, **Cancel** |
| Save Draft | Persist successfully, then close to Browse |
| Discard Changes | Destructively restore the entry version; delete a newly created draft; then close |
| Cancel | Return to the exact page and editing context |
| Save failure | Keep composer and content open; show recovery and Retry; do not report success |
| Interruption / relaunch | Recover the latest durably saved content and attachments; reopen at Editor without stale overlays |

Exit-choice copy: **“Save changes to this draft?”** Message: “Discard Changes removes changes made since you opened it.” Use destructive styling for Discard Changes; no destructive keyboard default. Cancellation, including dismissing the choice, keeps editing.

**Presentation and error rules**

- One sheet and at most one decision overlay. Dismiss an overlay completely before presenting another.
- Ordinary upload failure stays beside its attachment: **“Upload failed”**, **Retry**, **Remove**. Writing remains editable and the local attachment remains available.
- Repeated taps and duplicate callbacks cannot create extra overlays or duplicate retries. Ignore obsolete callbacks after removal or discard.
- If a critical error needs an alert, deduplicate it and defer other decisions until dismissal. Revalidate deferred events before displaying them.
- Removing an attachment requires an explicit action; upload failure never removes it automatically.

Apple recommends contextual feedback for routine status and reserving alerts for consequential interruptions. [Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts)

**iPhone and iPad**

On iPhone, use a large composer sheet so writing and the keyboard have room. On iPad, prefer a centered sheet with standard sizing; adapt to narrow windows without resetting the draft or navigation. Keep the same exit and preservation policy for touch, keyboard, pointer, and resizing. [Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets)

**Acceptance checks**

1. Type text, add an attachment, change options, and navigate Back repeatedly: committed content survives.
2. From every internal page, test Close, swipe, supported Escape, and outside dismissal: changed content reaches the same save/discard/cancel decision.
3. Cancel that decision: the same page, text, selection, and focus return.
4. Save Draft or Done, then reopen: the latest revision and attachments appear exactly once.
5. Simulate save failure: dismissal stops, writing remains available, and Retry succeeds.
6. Discard Changes: an existing draft returns to its entry version; a new draft is removed.
7. Rapidly tap an upload error and deliver duplicate failures: no stacked alerts or duplicate upload attempts.
8. Trigger an error during exit resolution: one overlay remains visible; no stale alert appears afterward.
9. Background, relaunch, rotate, and resize an iPad window: durably saved writing survives.
10. Test on both devices with large text, VoiceOver, touch, and attached keyboard: title, Back, exit, completion, and recovery controls remain reachable; focus returns to the invoking control.

The supplied specification fails preservation, exit, navigation, and presentation checks. The revised contract addresses those defects; runtime acceptance checks remain **not executed**.