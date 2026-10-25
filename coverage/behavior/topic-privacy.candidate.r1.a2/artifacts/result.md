# Permission-flow repair

Patched interface.md in place with a concrete iOS specification. Launch and manual check-in now require no optional permissions. Photo attachment uses single-image system selection with a local preview and explicit submission; whole-library upload is prohibited. Location is requested only for the current-location action, with one-time access preferred, precise/background escalation excluded, and manual entry preserved. Denial, restriction, cancellation, Settings return, and acquisition failure each have explicit recovery behavior.

## Decisions and source basis

Read the installed apple-hig root SKILL.md, searched references/topic-index.md for privacy, permissions, photos, location, and pickers, then read the Foundations family, its Privacy topic procedure, and its supporting privacy.md article in that order. Each file was read by a separate command. The Selection and input family was also inspected; the index describes its Pickers topic as ordered/date/time value selection, so it was not used as evidence for photo-library APIs.

- Contextual requests and a specific purpose sentence replace the launch gate and “Needed”: [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission).
- A system location button suits this individual optional task. The specification preserves the guide’s one-time expiry and existing While Using qualification: [Privacy — Location button](https://developer.apple.com/design/human-interface-guidelines/privacy#Location-button).
- Narrow collection replaces entire-library transfer: [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices).
- No custom pre-alert is needed. The guide’s single-continuation/no-cancel restriction concerns custom pre-permission explanations; it does not remove cancellation or manual entry from the ordinary editor: [Privacy — Pre-alert screens, windows, or views](https://developer.apple.com/design/human-interface-guidelines/privacy#Pre-alert-screens-windows-or-views).

The photo selector, preview-before-upload contract, metadata stripping, and recovery text are product decisions applying that guidance. They are not asserted to be API requirements from the local article. No implementation framework or deployment target was supplied, so the specification explicitly requires SDK verification and preserves manual check-in if an optional system surface is unavailable.

## Worked before/after

Before: A volunteer opens the app to record a shift manually. Launch waits for every permission. Location says “Needed”; denying it repeats the request. Adding one photo uploads the full library.

After: The volunteer opens the editor immediately, enters a venue manually, and can submit. If they tap “Add photo,” they select one image, preview it, and can remove it without uploading. If they tap the location button and decline the system request, the draft remains and says “Location wasn’t added. You can enter it yourself.” No request repeats. They submit the manual check-in and the single selected attachment, with no device coordinates or other library assets in the payload.

## Acceptance checks

These are implementation acceptance cases, not executed runtime results:

| Case | Expected observable result |
| --- | --- |
| Fresh install, launch, manual submission | No permission prompt; manual check-in succeeds. |
| Add photo, cancel | Unchanged draft; no upload or library authorization request. |
| Select one photo, replace, remove | Only successful selection replaces preview; removed image is absent from submission. |
| Photo loading failure or unavailable selector | Clear recovery, preserved draft, check-in available without photo. |
| Existing denied/restricted/limited/full Photos state | No escalation or authorization loop; verify narrow selector behavior on supported iOS versions. |
| Current location, initial grant | System-controlled consent where applicable; one result previewed; updates stop. |
| Location denial, relaunch, repeated navigation | No automatic prompt; manual entry remains usable. |
| Prior denial versus restriction | Optional Settings recovery only for recoverable denial; restriction does not promise a Settings fix. |
| Approximate location, timeout, services off | Approximate accepted; failures end acquisition and preserve manual path. |
| Settings return, leave editor, cancel draft | No automatic collection; authorization refreshed; acquisition stops and unsaved data discarded. |
| Capture network payloads during selection and submission | No pre-submit attachment transfer; submission contains only chosen image and intended check-in fields; no embedded photo coordinates, unselected assets, or incidental analytics data. |
| Supported device/OS and accessibility settings | Verify real system controls, full localized/accessibility-size location text, and operable recovery controls. |

## Evidence status and limits

Passed — static specification inspection: all four supplied defects have explicit replacement rules in interface.md; the document includes the data-purpose/access matrix, permission sequence, copy, denial recovery, and acceptance obligations. Required local root → family → topic → source routing was followed for Privacy. Both requested project files were written.

Failed — the original supplied specification fails the Privacy procedure’s criteria for gating unrelated work, unclear purpose copy, and excessive collection. This is a finding about the supplied description, not observed app execution.

Not executed — app builds, SDK/API checks, native permission prompts, device/simulator behavior, network inspection, GUI interaction, accessibility execution, localization rendering, and server retention/deletion verification. No app source, deployment target, screenshots, or runtime evidence was supplied. The installed guidance is a dated local snapshot, not an SDK reference or security/legal certification. No web browsing occurred; official links above are attribution from the installed guidance, not newly verified pages.
