# Pairing specification repair

Patched `interface.md` in place, replacing the original single sentence with an implementable tvOS entry, focus, correction, submission, and recovery contract.

## Decisions and changes

The supplied specification confirmed four barriers: swipe-only entry, invisible active digit, total input loss after a mistake, and an unexplained “Invalid” dead end. The revision uses fullscreen numeric entry with a native keyboard, directional navigation and deliberate Select activation, distinct active-position and keyboard-focus feedback, single-position editing/deletion, and explicit Pair submission. Leading zeroes survive unchanged.

Codes are treated as sensitive household authorization secrets and masked. Rejection preserves the sequence and offers editing, resubmission, and new-code help. Expiration, connectivity failure, retry restriction, pending requests, cancellation, stale responses, and success now have distinct outcomes. Get New Code gives an exact issuing-screen route instead of claiming the TV can issue a code. That external screen/service remains a dependency requiring implementation verification.

The revision also defines action labels and availability, Back behavior, accessibility semantics without spoken secrets, text enlargement, and across-room layout requirements. Official article links and the distinction between source guidance and product decisions are embedded in `interface.md`. The local accessibility reference’s tvOS-specific 66 × 66 pt default is used over the buttons reference’s general 44 × 44 pt region; neither was measured on a rendered interface.

## Worked before / after

Scenario: the intended code is `004281`; the person accidentally enters `004291`.

Before: swipes provide no focused-digit indication. One mistake discards the entire code and shows “Invalid,” with no retry or new-code route.

After: six masked positions remain after “That code wasn’t recognized. Check it and edit the code, or get a new code.” The person activates Edit Code, selects position 5 using Left/Right and Select, then selects 8 on the numeric keyboard. Only position 5 changes; the internal sequence becomes `004281`, preserving both leading zeroes. Pair submits it explicitly. Only service acceptance produces “Apple TV paired.” If the code has expired instead, Get New Code explains where to obtain a replacement; Enter New Code explicitly clears the old sequence. This is a worked specification trace, not an executed device test.

## Acceptance checks and status

Passed — static specification inspection:

- `interface.md` was actually replaced with the concrete contract; six-digit identity, leading zeroes, unsupported characters, overflow, correction, explicit commit, and cancellation are defined.
- Entry, rejection, expiration, network failure, retry restriction, pending, success, and late-response states each specify feedback and recovery.
- Focus routes cover the keyboard, position editing, submission, help, and cancellation. Swiping is optional; error handling preserves useful input.
- Secret masking and transient lifetime are stated; success is tied to service acceptance rather than visual completion.

Failed checks: none identified in the static contract review. This does not imply runtime checks passed.

Not executed — implementation acceptance scenarios:

1. On supported Apple TV hardware, enter `004281` with directional presses and Select without swiping; verify exact request data and no automatic submission. Repeat using supported physical keyboard input. Reject letters/seventh digits without losing entered digits.
2. Deliberately enter `004291`, reject it, edit only position 5, and verify `004281` is submitted. Exercise deletion at first/empty/filled positions and Back in every substate.
3. Traverse every available action in both directions. Verify focus, active digit, pressed and unavailable states remain distinct and enlargement clips nothing. Pending requests retain a visible target and reachable Cancel.
4. Exercise all service results, timeout, repeated activation, cancellation during a request, and stale responses. Verify no duplicate submission or stale session mutation; reconcile cancellation/server-acceptance races.
5. Open new-code help, return without losing digits, then choose Enter New Code and verify clearing. Confirm the issuing screen actually provides Get New Code and the service accepts the replacement.
6. Inspect native rendering from across the room, including around 8 feet or farther. Measure text/control geometry, contrast, enlarged text at 200%, and light/dark/Increase Contrast presentation. Verify reflow retains every action.
7. With supported tvOS accessibility tools and assistive input, complete entry, correction, recovery, and exit. Verify meaningful names/states, status feedback, and no exposure of digits. Inspect logs and request handling for secret leaks.

## Evidence and limits

Only the supplied one-sentence `interface.md` and installed local skill instructions/references were used. No web requests were made. No app code, service contract, issuing screen, SDK, simulator, GUI, device, rendered layout, or accessibility execution was supplied or run. API availability, native control feasibility for the exact route, focus-engine behavior, security, service semantics, contrast, physical comfort, and assistive behavior remain unverified. The specification is a repair artifact, not a functioning pairing implementation or security certification.

Auditable route: explicitly read the installed `apple-hig/SKILL.md`, searched `references/topic-index.md`, then read each selected family and topic procedure before its reference. Families/topics: getting-started → designing-for-tvos; selection-and-input → digit-entry-views and virtual-keyboards; inputs → focus-and-selection and remotes; menus-and-actions → buttons; foundations → accessibility and privacy. All reads used one file per shell command. References are dated local application guidance derived from Apple HIG, not live Apple documentation or independently verified SDK references. No screenshot or animation was supplied, so no media-specific route was needed.
