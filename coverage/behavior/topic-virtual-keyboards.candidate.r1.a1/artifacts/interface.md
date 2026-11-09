# Apple TV sign-in: revised interaction specification

Platform: tvOS. Scope: repair entry and navigation in the existing sign-in flow; retain its authentication service and framework. This is a specification, not an executed implementation.

## Entry controls and values

Replace the tiny custom keyboard with standard tvOS text-entry controls and the system virtual keyboard. Let the system adapt between Siri Remote linear entry and grid entry for other input devices; do not force either layout. Use system focus treatment with space for enlargement. Labels, prompts, and errors must remain legible across the room, including while editing.

| Field | Value and presentation | Entry and completion |
|---|---|---|
| Password | Persistent “Password” label; secure, obscured entry. Preserve the exact entered character sequence, including case, punctuation, and spaces. Never uppercase, trim, autocorrect, or otherwise normalize it. Do not prepopulate it. | Use supported password semantics and disable automatic capitalization/correction where configurable. Completion returns to the form; authentication requires deliberate “Sign In” activation. |
| Sign-in code | Persistent “Sign-in code” label and prompt explaining where to obtain it. Treat as a string, preserving case and leading zeroes. Obscure an authentication secret. | Until the service contract confirms numeric-only entry, use a text field capable of all required characters. If confirmed numeric-only, use the fullscreen tvOS digit-entry presentation with title and prompt. Show the service-defined length/character requirements; do not invent a six-digit rule. Completion returns to the form; “Continue” submits. |

Only show the fields required by the existing authentication step; do not add password and code entry to every step. Keep the active field, its purpose, correction feedback, and completion route available in the system presentation. Long values remain editable through system scrolling/caret behavior without exposing secure contents.

## Focus and remote contract

- On first entry, focus the first required field. Arrange fields in a vertical stack followed by the primary action and “Cancel sign-in”. Up/Down traverses that order and reverses it; skip unavailable actions. With one field, the route is field ↔ primary action ↔ Cancel. Boundary movement does not wrap unexpectedly.
- Moving focus highlights a target; only Select activates it. Select on a field opens its system editor. Within the keyboard, system directional navigation, character selection, deletion, and correction apply.
- After each character, update the draft without replacing the focused control, rebuilding the editor, or requesting form focus. Preserve the editing session and let the system retain the keyboard target. Do not reset to the first key or jump to the submit action.
- Explicit Done/completion dismisses the editor and restores focus to its originating field. Back dismisses the editor first, retaining the current draft and returning to that field; it does not submit. From the form, Back returns to its parent. Preserve system hold-Back behavior.
- Editing, moving focus, dismissing the editor, or returning from an in-flow help/parent screen never clears a partially entered code. Retain drafts in the current sign-in session, independently of focus and view reconstruction. Explicit Cancel ends that session and clears its drafts; successful sign-in also clears them. No persistence across process termination is promised.
- Distinguish focused, pressed, and unavailable states using native feedback. An inactive primary action must not trap focus: field and Cancel remain reachable, with a visible explanation of missing input.

## Alternate entry, validation, and recovery

Do not intercept or suppress system paste or supported hardware/companion entry. Where available for the deployed tvOS version, field type, and connected device, allow those routes to edit the same draft and use the same validation. Do not add a nonfunctional Paste button or promise dictation/paste in secure fields where the system does not offer it. Siri Remote entry remains sufficient without another device.

Permit intermediate input without per-character errors or resets. Enable the primary action when required values meet the known local format; explain unmet requirements beside the field. If service constraints are unknown, require nonempty input and let service validation resolve validity. Validate full pasted values identically to typed values; report invalid length/characters without silently truncating or coercing input. Deletion and replacement remain possible.

Submit only on explicit primary-action activation, never on reaching a code length or moving focus. Prevent duplicate submission while pending and show a visible pending status. On service rejection or network failure, retain drafts, show a nonsecret explanation, and keep correction, retry, and Cancel reachable. An expired code stays present until edited/replaced; explain that a new code is needed. No retry policy or authentication protocol is changed here.

## Guidance basis

These are product interaction decisions informed by the installed local HIG snapshot; they are not claims of API availability. System entry and input adaptation: [Virtual keyboards — tvOS](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#tvOS). Focus stability and reachability: [Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection). Remote activation and Back: [Remotes](https://developer.apple.com/design/human-interface-guidelines/remotes). Secure fields and labels: [Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields). Conditional numeric presentation: [Digit entry views](https://developer.apple.com/design/human-interface-guidelines/digit-entry-views). Paste, validation, and reduced effort: [Entering data](https://developer.apple.com/design/human-interface-guidelines/entering-data). Across-room design: [Designing for tvOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos).
