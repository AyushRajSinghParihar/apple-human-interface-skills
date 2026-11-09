# iPhone audio editor — revised interaction specification

Platform: iOS, iPhone. Preserve audio editing and the requirement that every action can be completed one-handed. This is a design contract, not an implemented or device-validated interface. No framework or minimum OS version is specified.

## Screen and visible actions

Keep the standard hierarchical Back control at the top, with the project name. Put editing controls in a persistent bottom safe-area region above the Home indicator, separate from navigation. Keep the waveform and selected clip visible above it. Never require simultaneous touches, a long reach while holding another control, or a speed threshold.

Use three compact groups: a selected-clip row with Previous Clip, clip name/selection state, Next Clip; a position row with Earlier, current time, Later; and an edit toolbar with Split, Delete, Undo, Redo. Provide a bottom Back to Projects button as a one-handed equivalent of the standard top Back. Both navigate to the same parent project list. Bottom controls remain available during editing and do not auto-hide.

Use standard buttons and system press/disabled states. Split and Delete use visible text; Undo and Redo use standard curved-arrow symbols with visible captions and action names. Delete has a destructive role, with its word label conveying the consequence as well as color. No destructive action is primary/default. All targets are at least 44 × 44 pt, with at least 8 pt between nonoverlapping hit regions (spacing is a product choice). Prefer system text styling; at enlarged text sizes reflow groups into labeled rows in a vertically scrollable bottom controls region rather than clipping, shrinking targets, or hiding actions behind a gesture. Keep Back to Projects pinned outside that region. Reserve at least one visible waveform/clip summary row; the selected clip and position must remain identifiable. All controls must remain reachable by ordinary scrolling at 200% text size and in landscape.

## Action and state contract

| Action/input | Outcome and availability | Feedback/recovery |
|---|---|---|
| Tap clip; Previous Clip / Next Clip | Select one clip; previous/next follow timeline order and move the playhead to that clip's start. Boundary buttons disable. When no clip is selected, Next selects the first and Previous the last. | Outline plus clip name and “Selected”; reveal selection in viewport. Empty timeline reads “No clips”. |
| Tap waveform position or one-finger horizontal drag inside waveform | Set/scrub playhead, clamped to project bounds, at every drag speed. Does not delete, split, or change clip selection. | Playhead and elapsed-time readout track the finger immediately. A canceled drag restores its starting position. |
| Earlier / Later | Move playhead by 0.1 seconds per tap, clamped to project bounds. Disable at respective bound; both disable in an empty project. | Update position in seconds to tenths; no drag or repeat-hold required. This increment is a product choice for a usable tap-only path. |
| Split | Enabled only with a selected editable clip and playhead strictly inside it at a valid audio frame. Snap position to the nearest valid frame; disable if that is an endpoint. | One activation replaces the selected clip with two contiguous clips retaining source audio and settings; select the right segment, retain playhead, and show “Clip split”. One undo unit. |
| Delete | Enabled only with a selected editable clip. Delete that clip from the arrangement, retaining original source media. Leave a gap; do not ripple later clips. | Clear selection, retain playhead, and show “Clip deleted — Undo available”. One undo unit. Undo remains available beyond any status message. |
| Undo / Redo | Always visible; disabled when the corresponding stack is empty. Accessible action name includes next operation, e.g. “Undo Delete Clip”. | Reverse/reapply exactly one edit, reveal affected clips, restore recorded selection and playhead, and show outcome text. |
| Standard top Back, edge Back, bottom Back to Projects | Return to project list with committed edits and editor context retained in the current session. An interactive Back canceled by the user leaves editor state intact. | Reopening the project restores selection, position and session history. No editing recognizer intercepts navigation edges. |

Disabled edit controls have adjacent contextual guidance: “Select a clip” or “Move the playhead inside the selected clip to split”. Locked clips read “Clip is locked”; editing controls disable. Editing is atomic: source media and history remain unchanged if an edit fails; show a persistent inline failure message with a Retry button that retries the same command against unchanged state. Prevent duplicate commits while an operation is pending and retain navigation. Committed edits must survive leaving the screen; do not silently discard them.

## Gesture and system conflict map

- Remove the three-finger circle recognizer entirely. Split is a labeled tap action; it has no replacement custom gesture.
- Remove swipe-to-delete and all velocity-based action switching. One-finger horizontal movement inside the waveform always scrubs, regardless of speed or direction. Clip selection and time-step buttons provide a drag-free path.
- Leave system navigation edges, Home, Control Center, notification and accessibility gestures to iOS. Use normal navigation behavior rather than drawing over or capturing the edge. A scrub that starts within the waveform stays a scrub until release; an edge-origin Back stays navigation.
- Preserve standard iOS three-finger undo/redo and supported iPhone shake behavior as optional equivalents using the same history. They are never required for one-handed use. For system-provided shake titles, supply only operation wording such as “Delete Clip”, avoiding duplicated “Undo”.

## Recovery and history

Split and Delete are nondestructive arrangement edits. Routine deletion therefore commits without a confirmation alert; this decision depends on complete restoration and retaining source media. Irreversible source-file deletion is outside this command's scope.

Store each edit's clip identities, source ranges, positions, settings, selection and playhead before/after. Undo Split restores the exact original clip; Undo Delete restores the original clip in its original gap. Redo reapplies the recorded result. Selecting, scrubbing and stepping create no history entries and do not clear redo; a new committed edit after undo clears redo. Preserve the meaningful edit sequence for the open project session without an arbitrary shallow cap. Autosave and navigation away/back do not clear it. Closing the project session or restarting the app starts a new history; saved arrangement and source media persist. Show restored offscreen clips without making people hunt for the result.

## Alternative access and one-handed use

The complete sequence can use sequential single taps: choose clip with Previous/Next, move position with Earlier/Later, Split or Delete, Undo/Redo, then Back to Projects. Support either hand without prescribed finger posture or timed activation. Reach and repeated-tap comfort still require physical testing.

Expose controls with their visible names, button roles, enabled states and the selected clip/position values. Make clip selection and position operable through standard focusable controls; do not make waveform manipulation a prerequisite. Support activation with VoiceOver, Switch Control, Voice Control, AssistiveTouch and Full Keyboard Access. Preserve system accessibility shortcuts. Give edit outcomes visible text as well as accessible status feedback; sound or haptics alone never communicate success. Maintain essential labels and action access with at least 200% text enlargement. Implementation must verify focus access and actual assistive behavior.

## Design basis

Local installed HIG guidance supports supplementary gestures and preserved system navigation ([Gestures, Custom gestures and iOS](https://developer.apple.com/design/human-interface-guidelines/gestures#Custom-gestures)); clear roles, labels and target separation ([Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices)); essential action prioritization ([Toolbars, iOS](https://developer.apple.com/design/human-interface-guidelines/toolbars#iOS)); simple alternatives and iOS control sizing ([Accessibility, Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility)); predictable visible restoration ([Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#Best-practices)); and recovery instead of routine undoable-deletion alerts ([Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices)). Bottom grouping, 8 pt spacing, 0.1-second stepping, non-ripple deletion and session boundaries are product decisions applying that guidance, not universal HIG rules.
