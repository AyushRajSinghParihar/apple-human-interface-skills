# Permission repair result

Replaced `interface.md` in place with an implementable iPhone permission specification. Manual check-in now works without permissions; Add Photo selects one item without broad library access; optional current-location attachment uses a task-time system control. The specification removes automatic denial loops and defines cancellation, restricted access, approximate location, failures, Settings return, draft preservation, and submission boundaries.

## Decisions and support

- Request access at the relevant action and explain its use with a complete sentence, replacing “Needed.” No custom pre-alert is needed because the editor provides context. This applies [Privacy: Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission).
- Minimize collection and transfer: import one selected image, remove embedded location metadata, and upload only visible attachments on submission. The single-item picker and deferred upload are product decisions applying [Privacy: Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices), not verified SDK prescriptions.
- Prefer the [system location button](https://developer.apple.com/design/human-interface-guidelines/privacy#Location-button) for this individual task. Preserve existing authorization semantics; accept approximate location and keep manual entry available. The 15-second timeout is an app decision.
- Use explicit action labels, system styles, iPhone hit regions, and submission activity feedback based on [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons). Settings is a voluntary recovery route, never a check-in prerequisite.

## Worked before/after

Before: A volunteer launches the app to record a shift manually. Launch is blocked until all permissions are granted. Location is explained as “Needed.” Denial repeats the request. Selecting a single attachment uploads the full photo library.

After: The volunteer opens the tracker immediately and enters the site manually. Add Photo opens single-image system selection; choosing one image creates a local preview without uploading it. Current Location invokes system-managed task-time access. If declined, the editor retains the entered site and selected photo and says “Location wasn’t added. You can enter the site manually.” Submit Check-In sends the entered data and that one photo, without a location attachment. Cancelling photo selection instead would leave the draft unchanged and allow submission without a photo.

## Acceptance checks and status

Passed — specification inspection only:

- `interface.md` was changed from the supplied one-paragraph behavior to a concrete replacement contract.
- Every data category has a purpose, minimum scope, and transfer boundary.
- Launch/manual submission no longer depend on photo or location authorization.
- Photo cancellation, failed import, replacement, and removal preserve unrelated draft data.
- Location denial, restriction, approximate access, timeout, revocation, and Settings return have explicit transitions without automatic requests.
- Submission does not silently omit a selected attachment or upload unselected photos.

Failed — the supplied original specification fails the above permission timing, minimization, purpose-copy, and denial-recovery requirements. No executable implementation was supplied or evaluated, so this is a specification finding only.

Not executed — implementation acceptance scenarios:

1. Fresh install: launch, enter a manual site, and submit successfully with no permission prompts.
2. Select one photo from a library containing several items; inspect app access and network traffic to verify only the selected image is imported and only submitted on confirmation. Verify location metadata is absent. Repeat with prior denied, limited, and full Photos authorization.
3. Cancel selection, cancel replacement, simulate image loading failure, remove the attachment, and retry submission; verify draft preservation and explicit attachment outcomes.
4. Exercise location first-use, existing While Using, denial, cancellation, restriction, services off, approximate access, timeout, and revocation. Verify no launch/re-entry prompt loop, no precision escalation, and no background acquisition.
5. Visit Settings and return without changing permission, then with a changed permission. Verify no automatic acquisition and preserved manual fields; acquire only after another explicit action.
6. Inspect outgoing check-in data after removing each attachment. Simulate upload failure and duplicate taps; verify retained draft, no silent data loss, and no duplicate check-in.
7. On iPhone, inspect actual button targets and native system control rendering, long localized labels, accessibility text sizes, and VoiceOver names/order. None of these are established by this document.

## Source route and evidence limits

Read the installed root `.agents/skills/apple-hig/SKILL.md` explicitly, then Foundations → Privacy procedure → privacy reference. Searched the complete topic index for permission, privacy, photo, location, buttons, and picker concepts. Also read Menus and actions → Buttons procedure → buttons reference before applying control guidance. Each source file was consumed with a separate single-file command. The index's generic Pickers topic concerns ordered/date/value choices, and Photo editing concerns Photos extensions; neither establishes a photo-library selection API contract.

Only the supplied `interface.md` and installed local guidance informed this revision; no web browsing occurred. Official links above are attribution from those local references, not evidence of live verification. The local references are dated 2026-10-25 and are guidance snapshots, not SDK references or independent security review.

No device, simulator, SDK compilation, GUI, network tracing, accessibility, or runtime permission tests were executed. Picker and location-control availability and exact APIs remain SDK verification work; the specification preserves manual entry when unsupported. Server retention/deletion details and App Store privacy disclosures need implementation-specific verification before release. This deliverable repairs the specification and does not claim to repair or certify executable app behavior.
