# Recipient-entry repair

Patched [interface.md](interface.md) in place with an implementable macOS recipient-token contract. The original supplied artifact described five defects; no application implementation or screenshots were supplied.

## Decisions and patch summary

- Replace the uneditable image with individual text tokens backed by ordered address identities.
- Commit using comma, legacy semicolon or Return; preserve unfinished and invalid input for correction, including paste and legacy import. Composition is not interrupted.
- Validate before inviting and block the entire submission on an error. Suppress duplicates using domain-normalized keys while preserving local-part case and aliases. This conservative identity policy does not promise that differently cased local parts reach different mailboxes.
- Scope deletion to text or selected tokens, with a selection step before deleting the preceding token. Define editing, undo, range selection, reorder, clipboard and safe cross-field transfer.
- Define a complete keyboard task path, explicit recipient actions and individually accessible text/state instead of image-only information.

The [Token fields guide](https://developer.apple.com/design/human-interface-guidelines/token-fields#Best-practices) supports macOS recipient tokens and comma conversion. [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices), [Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices), and [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) support familiar editing, reachable actions, distinct selection and focus, and accessible content. Exact parsing, duplicate policy, two-step Backspace, extra delimiters and submission blocking are proposed product decisions, not quoted Apple mandates. ASCII-only mailbox support is an explicit release limitation; unsupported formats receive an error rather than silent rejection.

## Worked before/after

Input: `ana@example.com;bad@;ana@EXAMPLE.COM;bo@example.com`, then Return.

Before, according to the supplied brief: one uneditable image; invalid `bad@` accepted silently; Ana can be invited twice. Backspace removes all recipients, and there is no keyboard selection behavior.

After, as specified: tokens are `ana@example.com`, error token `bad@`, and `bo@example.com`. The repeated Ana address is suppressed with “Already added: ana@EXAMPLE.COM.” Invite sends nothing while `bad@` remains invalid. Select that token and press Return, change it to `bea@example.com`, then Return to recommit. The ordered recipients are Ana, Bea, Bo. With the caret at the empty end, Backspace selects Bo; another Backspace removes only Bo. Command-Z restores Bo. Invite then submits exactly the three unique addresses. These are expected transitions, not executed application results.

## Acceptance checks

| Check to run against implementation | Expected outcome |
|---|---|
| Enter comma/semicolon/Return-separated addresses; import semicolon text | Same ordered tokens and validation; Return never sends. |
| Paste worked example; activate Invite | Three tokens including one explicit error; duplicate suppressed; zero sends. Correct error and retry: three unique recipients. |
| Enter bare `Alex`; paste two different addresses with the same display name | Bare name remains unresolved; full addresses distinguish the two valid identities; no first-match substitution. |
| Paste quoted display name containing a comma; paste an unclosed quote; enter unsupported mailbox format | First parses as one mailbox; malformed/unsupported text remains correctable with explanation. |
| Type unfinished address, Tab away, return; test input-method composition | No lost text or focus trap; errors persist; composition is not prematurely committed. |
| Edit a token into an existing address; undo | Duplicate collapses to existing recipient; undo restores prior recipient state without deleting the original. |
| Backspace with text, empty caret, one selected token and selected range | Normal text deletion; select-before-delete at boundary; only selection removed; undo restores it. |
| Arrow and Shift-arrow navigation; Command-A/C/X/V/Z and redo | Predictable selection and standard editing within the field; addresses survive copying and paste. |
| Reorder via pointer and Move actions; transfer to compatible field | Identity/order preserved; rejected move retains source; copy retains source; duplicate destination is handled without repeated invite. |
| Keyboard-only entry → edit → remove → Invite; reverse navigation | Task completes without pointer; no activation merely from focus or selection; Full Keyboard Access reaches actions. |
| Inspect assistive semantics and navigate task using VoiceOver/Switch Control | Individual address values, selection, errors and action states are available in task order; status does not steal focus. |
| Enlarge text to 200%; inspect light/dark and Increase Contrast | Addresses, errors and actions remain usable; meaning survives without color. Measure actual contrast and geometry. |

## Audit and evidence limits

Passed — static specification inspection: interface.md was replaced and reread; each of the five supplied defects has a concrete correction. The document defines commit, identity, correction, deletion, selection, reorder, transfer and submission transitions. result.md records decisions, the worked transformation and checks.

Failed — the original specification explicitly reports all five defects. No runtime failure was independently reproduced. No revised implementation check has been executed or passed.

Not executed — SDK/API verification, compilation, native token rendering, parser or invitation tests, pasteboard/drag behavior, international keyboard input, input-method composition, Full Keyboard Access, VoiceOver, Switch Control, Accessibility Inspector, contrast/geometry measurement and 200% rendering. Only local text files and installed guidance were inspected on a headless Linux server; no device, GUI or accessibility execution is claimed.

Routing audit: explicitly read the installed root `.agents/skills/apple-hig/SKILL.md`, inspected interface.md, and searched `references/topic-index.md` for token, text-field, keyboard and accessibility concepts. Read the Navigation and search, Inputs, and Foundations family SKILL.md files; then the Token fields, Keyboards, Focus and selection, and Accessibility topic SKILL.md files; then each matching local source guide. Every instruction/source read used a separate single-file command resolved from this installed package. This is a repair to an existing macOS control, not a platform feasibility/adaptation exercise. No web browsing occurred. Official links above are attribution from the local dated snapshot, not evidence of live-source or SDK verification.
