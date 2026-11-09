Use one titled composer with internal navigation, a shared exit guard, and durable draft recovery. Attachment and composer settings become steps within that task.

**Before → after**

| Before | Revised behavior |
|---|---|
| Browse → composer sheet → attachment modal → settings modal | Browse → one composer sheet containing Editor, Attachments, and Attachment Settings |
| Untitled composer | “New Draft”; child steps titled “Attachments” and “Attachment Settings” |
| Swipe is the only exit | Visible Cancel and Done on Editor; Back on child steps |
| Swipe or Done deletes writing | Done saves; Cancel and dismissal gestures resolve unfinished changes |
| Upload error opens two alerts | Inline upload recovery; one coordinated decision presentation at a time |
| Attachment flow has no Back | Settings → Attachments → Editor, retaining work |

**Revised state specification**

Assumption: Done saves a draft; it does not publish or send. Settings here apply to the attachment. App-wide settings belong outside this task.

Model these independently:

- `route`: Browse, Editor, Attachments, Attachment Settings.
- `draft`: stable ID, text, attachment references, settings, revision, and saved revision.
- `persistence`: saving, saved, or failed.
- `decision`: none, exit choices, or one critical alert.

Create recovery storage when editing begins. Persist edits and attachment references as they change. Recovery storage protects interrupted writing; Done explicitly saves the draft to the product’s draft list.

| Event | Transition and data outcome |
|---|---|
| Compose | Browse → Editor. Present one composer sheet; block interaction with Browse. |
| Add attachment | Editor → Attachments inside the existing sheet. Retain text and selection. |
| Attachment settings | Attachments → Attachment Settings in the same navigation stack. |
| Back | Pop exactly one step. Preserve edits, attachment choices, and upload state. Never dismiss the composer. |
| Done on Editor | Persist the current revision and attachment state. After success, close to Browse and show the saved draft. On failure, remain in Editor with recovery actions. |
| Cancel, downward dismissal, or supported keyboard dismissal | Enter the shared exit handler from any step. Never delete directly. |
| Exit with no changes since the last explicit save | Close to Browse without a prompt. Keep any existing saved draft. |
| Exit with unfinished changes | Cancel dismissal and show the exit choices below. Preserve the originating route. |
| Backgrounding or system interruption | Preserve recovery data without requiring a decision. Reopening offers the recovered draft at Editor. |
| Upload failure | Keep text and the local attachment reference. Show inline failure with Retry and Remove; saving the draft remains possible. |

Exit choices use a native confirmation dialog:

**“Save this draft?”**  
“Save your writing and attachment choices before closing.”

- **Save Draft:** persist successfully, then close to Browse.
- **Discard Changes** — destructive: revert to the last explicitly saved version, or delete a never-saved draft; then close.
- **Cancel:** dismiss only the dialog and return to the originating step.

Dismissing the dialog without choosing an action has the same safe outcome as Cancel. A failed save leaves the composer open. No destructive action is the keyboard default.

**Presentation and device contract**

Use a large composer sheet on iPhone and a standard centered page/form sheet on iPad. Adapt to compact iPad windows without changing the state model. Resizing and rotation retain the draft, route, selection, and upload state.

Editor shows leading Cancel and trailing Done. Child steps show Back; Back applies their changes to the working draft and returns one level. Do not show Cancel, Back, and Done together.

A single coordinator owns confirmation dialogs and critical alerts. Repeated taps are deduplicated; concurrent failures update inline status. Resolve an active decision before considering another, and discard obsolete requests. A necessary alert may appear over the composer, but alerts never stack. Restore focus to the initiating control after a decision and to Compose after closing.

These choices follow Apple’s guidance on [sheets](https://developer.apple.com/design/human-interface-guidelines/sheets), [modality and unfinished work](https://developer.apple.com/design/human-interface-guidelines/modality), [save/discard choices](https://developer.apple.com/design/human-interface-guidelines/action-sheets), and [alerts](https://developer.apple.com/design/human-interface-guidelines/alerts). The recovery policy and exact copy are proposed product decisions.

**Acceptance checks**

1. Open Compose: “New Draft,” Cancel, and Done are visible; Browse cannot receive interaction.
2. Enter text, add an attachment, change its settings, and navigate Back twice: all changes survive; only one composer sheet exists.
3. On a changed draft, invoke Cancel, swipe dismissal, and supported keyboard dismissal separately from each step: each reaches the same exit choices without losing content.
4. Cancel or dismiss the exit dialog: return to the same step with writing and focus preserved.
5. Choose Save Draft or Done: close only after persistence succeeds; reopening shows the saved revision.
6. Force a save failure: remain in the composer, retain all content, and offer Retry. Do not report successful saving.
7. Choose Discard Changes: only the identified draft’s unsaved changes are removed; an earlier saved version survives.
8. Repeatedly tap an upload error while multiple uploads fail: no stacked alerts or duplicate dialogs appear. Retry preserves writing.
9. Background and terminate after recovery persistence, then relaunch: recover text, attachment references, and settings without silently restarting uploads twice.
10. Rotate iPhone and resize iPad across compact and regular widths: preserve route and draft; verify actions remain reachable with the keyboard and enlarged text.
11. With VoiceOver, touch, pointer, and attached keyboard: verify visible exits, logical focus, safe cancellation, and focus restoration.

Specification review passed against the supplied defects. Runtime, persistence-failure, and device accessibility checks remain unexecuted.