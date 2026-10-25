# Login and invitation repair

Patched `interface.md` in place, replacing its single paragraph of defective behavior with a field contract, validation and recovery states, keyboard actions, accessibility requirements, and source links.

## Decisions

- Email uses appropriate keyboard/content semantics with correction and automatic capitalization disabled; entered characters retain their meaning.
- Password starts secure and stays secure. Paste and system credential filling remain available; app defaults must not prepopulate it.
- Persistent labels remain visible after entry. Inline errors attach to the affected field; ambiguous credential errors attach to the credential group, and connection errors remain form-level.
- Invalid invitations preserve all input for correction. Local validation, service rejection, and network failure have distinct recovery behavior.
- Next advances focus; Go and the primary action share submission logic. Required-data gating has visible explanation; submission prevents duplicate requests.
- Clear, long-value editing, keyboard clearance, text enlargement, and alternative input are explicitly specified.

The original gives no invitation schema, framework, service rules, or screen structure. The patch explicitly assumes a separate invitation-code form, supplies email/link alternatives if that assumption is wrong, and leaves token format and authority with the existing service. Error copy, detailed validation timing, retention scope, and state transitions are design decisions rather than verbatim Apple requirements. This is a specification repair, not an account-system redesign.

## Worked before/after

Example fixture: Email `alex+family@example.com`, Password `Family example 7!`, invitation `00Ab-7x` (illustrative, not a real credential or prescribed token format).

**Before, from the supplied description:** Email is subject to autocorrection; password is visible; entering values removes their only labels. Return does nothing. When the service rejects an invitation, every value disappears and no error is associated with a field. The original does not supply a reproducible runtime trace or the exact address mutation.

**After, required by the revised specification:** Email remains exactly `alex+family@example.com`; its Email label remains visible. Next moves to Password, whose characters are obscured. Go validates and submits once. On the assumed Join family screen, pasting `00Ab-7x` preserves its leading zeros and case. If rejected, the value remains and the invitation field exposes “This invitation can’t be used. Check the code or ask your family organizer for a new invitation.” The person edits only the code and retries. A transport failure instead offers connection recovery without labeling the token invalid. These are specified outcomes, not executed observations.

## Acceptance checks and status

**Passed — static document inspection:** The revised document covers each of the six supplied defects, defines field labels/types/validation/focus, preserves values on rejection, and provides explicit submit and recovery transitions. It keeps service-dependent token constraints qualified and includes official article/section links.

**Failed — supplied baseline specification:** Its stated behaviors fail the desired checks for unmodified email entry, secure password entry, persistent field purpose, recoverable invitation errors, functional Return, and associated error feedback. These are findings about the supplied description, not measured implementation failures.

**Not executed — implementation acceptance:**

| Check | Required result |
| --- | --- |
| Empty and partial values | Missing requirements are explained; no request is sent; partial typing is preserved. Empty final Return identifies the first missing field. |
| Email correction and validity | Typing/pasting plus-addressed, subdomain, long, and service-supported international addresses does not autocorrect, capitalize, or silently rewrite them; malformed committed input gets an Email error. Repeat with different input languages/locales. |
| Secure entry | Password is obscured from first render, paste/system filling works, and spaces remain significant. No app-default password is inserted. |
| Return and duplicate activation | Next advances; Go and button submit the same validated snapshot once; rapid repeated activation cannot duplicate a request. |
| Invalid invitation | Invalid/expired token retains every value and exposes the relevant error. Correcting the token permits retry without unrelated re-entry. Include leading-zero and punctuation fixtures. |
| Network and success | Connection failure retains input and permits retry; success navigates only on confirmation and clears login password on exit. |
| Clear and long values | Clear erases only its named field; long values remain inspectable/editable; labels and errors do not truncate. |
| Keyboard/layout | On iPhone, keyboard appearance/movement and orientation changes leave active input, error, and completion action reachable. |
| Accessibility and enlargement | At least 200% text enlargement retains content/actions. VoiceOver exposes labels, secure semantics, required state and errors; Tab/Shift-Tab, Full Keyboard Access, and Switch Control can complete and retry without a focus trap. |
| Appearance and geometry | Measure light/dark and Increase Contrast behavior, control separation, and the specified 44 × 44 pt default activation areas. Error meaning remains available without color. |

## Evidence and routing limits

Read the installed root `.agents/skills/apple-hig/SKILL.md` explicitly, then the Selection and input family and its Text fields/Virtual keyboards procedures; Foundations and its Accessibility procedure; Patterns and its Entering data procedure. Each selected procedure was read before its supporting guide, using separate single-file commands. Searched the installed topic index for task concepts and final topic matches. All guidance came from the supplied local package; no web browsing occurred.

Material guidance is linked in the revised specification: [Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields#Best-practices), [Virtual keyboards](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#iOS-iPadOS), [Entering data](https://developer.apple.com/design/human-interface-guidelines/entering-data#Best-practices), and [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility). These links identify the official sources represented by the local snapshot, not pages fetched during this task. The package is independent guidance, not an SDK reference or proof of current runtime behavior.

Only the prose interface description and installed instructions were available for this work. No device, simulator, SDK build, GUI, service integration, contrast measurement, or accessibility execution was performed. Native rendering, credential filling, spoken error delivery, focus traversal, physical comfort, and implementation compliance remain unverified.
