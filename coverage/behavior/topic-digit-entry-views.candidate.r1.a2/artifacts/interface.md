# Apple TV household pairing-code entry

## Purpose and presentation

Platform: tvOS. Pair this Apple TV with the household that issued a six-digit code. Use a fullscreen digit-entry presentation with the system numeric keyboard, rather than gesture-only digit cycling. Prefer native controls; framework and SDK availability must be verified during implementation.

Title: **Pair This Apple TV**.
Prompt: “Enter the six-digit code from your household’s pairing screen to connect this Apple TV.”
Help beneath entry: “Need a new code? Open the household’s pairing screen and choose Get New Code.”

The issuing screen is an external product dependency, not a supplied implementation. It must provide that named action and a fresh code; the TV must not pretend to generate a code accepted by the service. The TV’s **Get New Code** action opens a persistent help state repeating those instructions, with **Enter New Code** and **Cancel**. Enter New Code deliberately clears the old sequence and returns to entry. Back from help preserves the old sequence.

## Value, entry, and correction

- Store a sequence of exactly six ASCII digits, never a number; `004281` must remain `004281`. No sign, decimal point, spacing, or automatic correction. Reject unsupported characters without deleting existing digits; ignore additional digits once full, with “Six digits entered. Choose Pair or edit the code.”
- Treat the code as an authorization secret. Mask entered positions with asterisks from entry onward; empty positions remain visibly distinct. Do not echo the code in errors, help, success, analytics, or logs. Keep it only in transient entry/request state; clear on successful pairing, cancellation, new-code entry, or leaving the flow. Transfer only to the existing pairing service for validation. This specification does not define a new authentication protocol.
- Initially the first empty position is active. Show its outline and position label, for example “Digit 1 of 6”; the active position remains visible even when empty or masked. Keyboard focus is a separate system highlight on the key/action that Select will activate.
- Selecting a digit key fills the active position and advances to the next empty position. After the sixth digit, retain the last position and show **Pair** as available; do not submit automatically.
- **Edit Code** enters position selection: Left/Right moves among six positions, Select chooses that position and returns to the keyboard. The next digit replaces only that position, then advances. **Delete Digit** clears the active filled position; if active is empty, it clears the preceding filled position and makes that position active. At the first empty position with nothing entered, it does nothing. No validation failure clears other digits.
- **Pair** is unavailable until all six positions are filled. Show “Enter all six digits to pair.” while incomplete. **Cancel** always exits to the parent household setup screen without pairing.

## Remote and focus contract

Swipes and directional presses navigate visible keys/actions; Select deliberately activates the highlighted item. No swipe is required to enter, correct, retry, obtain new-code instructions, or cancel. Preserve system keyboard behavior and system accessibility shortcuts. Physical keyboard digit entry, when supported, uses the same value and correction rules; it must not bypass validation. Voice or companion hardware is optional.

Focus routes: numeric keyboard → Edit Code → Delete Digit → Pair (when available) → Get New Code → Cancel. Arrange actions in that vertical order below the keyboard; Up/Down connects adjacent available rows, Up from Edit Code returns to the keyboard’s last focused key, and Down from Cancel stays there. Within the native keyboard retain its directional routes. Position selection is a single horizontal group with a visible **Done Editing** action below it returning to the keyboard; Back also returns to the keyboard without changing digits. Every action has a visible system focus treatment and pressed feedback; allow space for enlargement without clipping digits, prompts, or neighbors. Moving focus never submits or replaces a digit.

Back from ordinary entry cancels to the parent; Back from help returns to entry; Back from position selection ends position selection. Holding Back retains system behavior. Play/Pause is not repurposed to submit.

## Validation and recovery states

| State / trigger | Visible response and available actions | Retained state |
| --- | --- | --- |
| Complete → Pair | “Checking code…”; prevent duplicate submissions and edits while waiting; keep Cancel available and focused action stable | Six masked digits |
| Service accepts | Clear secret; show “Apple TV paired.” and **Continue** to household home | Confirmed household association only |
| Service rejects code | “That code wasn’t recognized. Check it and edit the code, or get a new code.” Keep Edit Code, Pair, Get New Code, Cancel available | All six digits; no guessing which digit is wrong |
| Service reports expiration | “That code has expired. Get a new code from your household’s pairing screen.” Pair unavailable; Get New Code and Cancel available, plus Edit Code for replacement | Masked sequence until explicit replacement or exit |
| Network failure / request timeout | “Couldn’t check the code. Check your connection and try again.” **Try Again** retries the unchanged complete sequence; Edit Code, Get New Code, Cancel remain available | All digits |
| Service reports retry restriction | “Too many attempts. Try again when the service allows it, or get a new code.” Disable submission until service permits; show any service-provided wait duration accurately; Get New Code and Cancel remain available | All digits; no invented client retry limit |
| Cancel while waiting | Exit to parent and clear local secret; ignore late UI callbacks | No local entry state |

Errors persist until editing, a new request, help, or exit; they never disappear on a timer. Keep focus where the person left it when a response arrives; announce the changed status through platform accessibility mechanisms. If the focused submit action becomes unavailable, retain its visible pending/status location and provide a directional route to Cancel rather than leaving an invisible target. A service response must be tied to the current request/session; stale responses cannot pair a later session. Cancellation may race server completion: reconcile actual association on the next setup visit rather than promising that Cancel revokes a server acceptance.

## Accessibility and viewing contract

Use system text and focus styling suitable for across-room viewing. Start with the local guidance’s tvOS default text size of 29 pt and default control area of 66 × 66 pt, with separation and room for enlarged focus. These are design starting points, not measured output. Preserve all prompts/actions at 200% text enlargement through reflow or scrolling with reachable controls. Pair errors and active-position state with text/shape, not color or sound alone. Expose meaningful control names, enabled/busy states, masked position values, and status text to assistive input without exposing code digits. Verify the complete task with supported tvOS assistive input; this document establishes requirements, not execution evidence.

## Guidance basis

The following official links identify material guidance read from the installed local snapshot; no live lookup was performed:

- [Digit entry views](https://developer.apple.com/design/human-interface-guidelines/digit-entry-views#Best-practices): fullscreen numeric entry, title/prompt, masking sensitive codes.
- [Virtual keyboards — tvOS](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#tvOS): numeric keyboard for digit-entry views; preserve native input variants.
- [Designing for tvOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos#Best-practices), [Focus and selection — tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS), and [Remotes](https://developer.apple.com/design/human-interface-guidelines/remotes#Buttons): distant readability, visible focus, directional reachability, deliberate activation and Back.
- [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Style), [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility), and [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Protecting-data): clear system actions, alternative access, platform sizing, and secret protection. The accessibility reference gives a tvOS-specific 66 × 66 pt default versus the button guide’s general 44 × 44 pt region; use the platform-specific default here.

Editing semantics, explicit submission, error copy, retry states, and issuing-screen contract are product decisions applying this guidance, not Apple-defined pairing or security policies.
