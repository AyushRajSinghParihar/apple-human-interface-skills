# Sign-in keyboard repair

Patched `interface.md` in place, replacing the defect-only brief with a concrete tvOS entry, focus, validation, and recovery contract.

## Decisions

- Replace tiny custom keys with system entry, allowing tvOS to adapt linear/grid layouts. This removes the need to invent key dimensions without a supplied design or runtime.
- Keep the active editor stable after characters; separate navigation, activation, completion, and submission. Define directional routes and Back restoration.
- Preserve passwords exactly and obscure them. Preserve code strings, including leading zeroes; use numeric digit entry only when the service confirms that format.
- Allow system-supported paste and alternate entry without requiring a second device. Availability remains conditional on the actual deployment and secure-field behavior.
- Retain session drafts across focus changes and in-flow navigation; clear on explicit cancellation or success. Define partial input, submission gating, pending, rejection, and retry behavior.

The guidance links in `interface.md` identify the official articles corresponding to the local sources. Focus stability, system input, secure entry, and useful alternatives are source-backed recommendations. The exact session lifecycle, action labels, explicit-submit rule, and retry transitions are design decisions for this repair, not universal HIG mandates.

## Worked before/after

Illustrative values, not known production credentials or code formats:

| Step | Before, from the supplied brief | After, specified behavior |
|---|---|---|
| Enter password `aB9!` | Silent uppercasing changes its meaning; focus is lost after characters. | Secure draft retains exactly `aB9!`; editor stays active after every character. |
| Enter partial code `00`, dismiss editor, move to another control, return | Moving away clears the partial code. | Session draft remains `00`; returning and selecting the field resumes correction/entry. |
| Complete an illustrative numeric code `0042` | Alternate entry is blocked; code format was not supplied. | If the service confirms this numeric format, preserve `0042`, including zeroes; use numeric entry. Otherwise retain general text entry. Supported paste uses the same draft. |
| Activate Continue and receive a rejection | Not described in the brief. | Keep the draft, show a nonsecret error, and allow correction, retry, or cancellation. |

## Acceptance checks

Static specification review **passed**: each of the five reported defects has an explicit replacement rule; field semantics, navigation, submission, cancellation, and error recovery are specified. This establishes document coverage only.

**Failed checks:** none observed during document review. The original brief reports broken behavior; no runtime was available to reproduce it or establish a runtime pass.

The following execution checks are **not executed** and remain implementation acceptance criteria:

1. With Siri Remote, reach every field, enabled action, and Cancel; enter and exit each editor. Verify visible focus, unclipped enlargement, and across-room legibility. No control or keyboard region traps focus.
2. Enter several characters, delete, move the caret, and replace text. The keyboard remains active without an app-driven focus reset after each edit. Done and Back restore the originating field; Back does not submit.
3. Enter `aB9!`, spaces, punctuation, and a long valid password. Inspect the value passed at the authentication boundary: exact input is preserved and display stays obscured. No automatic casing, trimming, correction, or truncation occurs.
4. Enter partial code `00`; dismiss, change focus, visit an in-flow parent/help screen, and return. Draft remains `00`. Cancel and successful completion clear session drafts. Process-restart restoration is outside this contract.
5. For confirmed numeric codes, verify leading zeroes, required length, deletion, rejection, and cancellation in digit entry. For alphanumeric codes, verify letters and punctuation required by the service remain enterable. Do not assume a code format from these examples.
6. Test empty, partial, invalid, and valid values plus full-value paste where supported. Requirements explain gating; invalid values remain correctable; typed and pasted values follow the same validation. Locale/input changes do not alter sequence identity.
7. Exercise supported hardware and companion entry, including linear/grid adaptation. Record OS, devices, and secure-field capabilities. Where paste is unavailable, verify Remote entry still completes the task; do not count unavailable system features as demonstrated support.
8. Submit explicitly; verify pending feedback and no duplicate request. Simulate rejection, expiry, and network failure: drafts remain, error text excludes secrets, and correction/retry/Cancel are reachable. Merely reaching code length never submits.

## Evidence limits and route audit

Read the installed root `.agents/skills/apple-hig/SKILL.md` explicitly and searched its topic index. Read the Getting started, Selection and input, Inputs, and Patterns family instructions. Read the routed procedures before their source guides: Designing for tvOS; Virtual keyboards; Text fields; Digit entry views; Focus and selection; Remotes; Entering data. Each source was consumed by a separate single-file command from this installed package.

Evidence consists of the one-line original `interface.md` and those local instructions/guides. No web browsing occurred. Official links are attribution, not evidence of visiting those pages. The package is a dated, derived HIG snapshot, not an SDK reference. No implementation, deployment target, service schema, screenshots, device, SDK build, GUI, remote, keyboard, companion-device, or accessibility execution was supplied or performed. Native focus, secure-field capability, actual rendering, assistive behavior, and authentication success therefore remain unverified. Confirm service code format and deployed API support during implementation.
