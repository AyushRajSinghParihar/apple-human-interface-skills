# Revised document-scanning interaction specification

## Scope and decisions

The primary task is to frame and capture document pages. `interface.md` supplies only a short behavior proposal: Camera Control switches accounts, opens a crowded nested settings list during capture, and provides no selected-exposure feedback. It also requires older-iPhone support. No implementation, screenshots, capture modes, or device capability inventory were supplied.

Replace account switching and settings navigation on Camera Control with direct capture adjustments. Keep account selection in the ordinary account area outside capture; leave the active document's account unchanged throughout a scanning session. General settings remain outside the capture adjustment overlay. These are product decisions to keep the scanning task focused, supported by [iOS best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices).

Use a fixed, shallow overlay inventory rather than nested settings. The local [Camera Control guidance](https://developer.apple.com/design/human-interface-guidelines/camera-control#Best-practices) specifies fixed controls, mode-dependent enablement, common controls near the middle, remembered selection, short names, value feedback, and space next to the hardware control. Its anatomy maps ranges to sliders and discrete choices to pickers.

## Fixed inventory and value contracts

Order: **Capture → Exposure → Zoom**. Exposure is central because correcting pale or dark document text is this design's most frequent adjustment; Capture and Zoom flank it. Frequency is an assumption to validate with scanner usage. “Capture” here selects automatic/manual behavior; it is not the shutter action.

| Function | Kind and values | Feedback and enablement |
|---|---|---|
| Capture | Picker: Manual, Auto; initial Manual | Show selected word. Auto captures only after the existing scanner's document/stability checks succeed. If those capabilities are absent, keep Auto disabled with an explanation. |
| Exposure | Slider: target −2 to +2 EV, steps of 1/3 EV; initial 0 EV | Show localized signed value, e.g. “Exposure +0.7 EV”; prominent values −2, −1, 0, +1, +2 EV. Intersect target range with verified camera support before registering the session's inventory. Disable if unavailable. |
| Zoom | Slider: target 1×–3×, steps of 0.1×; initial 1× | Show localized multiplier, e.g. “Zoom 1.5×”; prominent values 1×, 2×, 3× where supported. Use the verified supported intersection; disable if empty. |

Ranges, increments, defaults, order, and auto-capture policy are proposed product contracts, not Apple specifications. Choose bounds before session registration; do not silently change them while someone adjusts. If capabilities change, disable the affected fixed control and explain why. Reconfigure bounds on the next session. Use system exposure/zoom controls where they meet this contract; do not duplicate them with custom controls. [Camera Control anatomy](https://developer.apple.com/design/human-interface-guidelines/camera-control#Anatomy).

Symbols identify functions and never change with their values: candidates `camera`, `plusminus`, and `magnifyingglass`, respectively. Use ordinary monochrome rendering and text-matched weight, without animation or custom symbols. These exact identifiers are candidates pending deployment-catalog validation, not verified assets. Prefer the system-supplied exposure/zoom identities where available. If an eligible symbol cannot be verified, keep the corresponding function available onscreen and defer that overlay function until registration can be validated; never insert homemade artwork. [Camera Control](https://developer.apple.com/design/human-interface-guidelines/camera-control#Best-practices), [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols).

## Event and state contract

States: `Ready`, `Adjusting`, `Capturing`, `Review`, `Interrupted`, `CameraUnavailable`. The overlay is available only during live preview in Ready/Adjusting. A capture session owns the account, page collection, adjustment values, and fixed inventory.

| Event | Required result |
|---|---|
| Light press during Ready | Open the bezel-adjacent adjustment overlay on the system's remembered function. First use requests Exposure if the integration permits; otherwise accept system selection. Never force-reset a remembered choice. |
| Light double press | Reveal the same fixed function inventory. No nested settings, account choices, or navigation routes. |
| Slide on selected enabled function | Adjust that function only; apply preview change and display the effective value. No capture or account change. |
| Select disabled function | Keep its identity and position; show “Unavailable in this mode.” No silent switch to another function or value mutation. |
| Firm capture activation, where supported, or onscreen Capture | Request exactly one page capture through the same guarded command. Full-press behavior is a proposed product mapping pending integration verification; the local source does not specify its API or timing. |
| Dismiss overlay | Return to Ready, retaining applied adjustments; restore duplicate onscreen controls. Dismissal does not undo values. Provide an onscreen Done route. |
| Successful capture | Append one page, show updated page count, return to live preview with values retained. Finish opens Review. |
| Capture failure | Append nothing; show readable error and Retry; retain existing pages and adjustments. |
| Interruption or loss of camera access | Close overlay, stop capture requests, retain pages/account/values. On resume, recheck camera readiness; show a recovery action if unavailable. Never capture automatically on resume. |
| Review or other noncapture screen | No app Camera Control adjustment actions; preserve system behavior. Return to scan restores session values and stable inventory. |

Framework-agnostic arbitration:

```text
requestCapture(origin):
    if state not in {Ready, Adjusting} or not cameraReady or captureInFlight:
        return
    captureInFlight = true
    state = Capturing
    closeOverlayAndRestoreTouchControls()
    captureOnePage(currentEffectiveSettings)

onAutoReady(documentIdentity):
    if captureMode == Auto and not requiresDocumentChange:
        requestCapture(Auto)

onCaptureSuccess(page):
    appendExactlyOnce(page)
    requiresDocumentChange = true
    captureInFlight = false
    state = Ready

onDocumentRemovedOrNewPageDetected:
    requiresDocumentChange = false

onCaptureFailure(error):
    captureInFlight = false
    state = Ready
    showErrorAndRetry(error)
```

Manual activation remains available in Auto. After any successful capture, require a new page/document-change signal before another automatic capture; simultaneous hardware, touch, and automatic requests cannot append duplicates. Detection thresholds and shutter event translation must be specified and verified by the implementation; they are not invented SDK calls here.

## Viewfinder, fallback, and access

In portrait and landscape, allow the system overlay over the viewfinder beside the physical control, reserving adjacent label space. Reposition app page count, status, Capture, Finish, and Done outside that occupied region and inside safe areas. Keep the document framing region usable; do not solve overlap by shrinking essential labels. Hide only duplicate Exposure, Zoom, and Capture-mode app controls while the overlay is visible. Keep unrelated capture/status actions available. On dismissal, restore controls with current values. Reflow controls based on measured space at large text sizes rather than fixed orientation coordinates. [Camera Control best practices](https://developer.apple.com/design/human-interface-guidelines/camera-control#Best-practices), [Layout adaptability and safe areas](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability).

All iPhones get onscreen Capture, Finish, and a single-level Adjustments surface with the same values and capability explanations. Exposure and Zoom also have labeled decrement/increment actions so precise sliding is optional. Hardware support enhances this route; it is never required to finish a scan. On older iPhones, omit hardware instructions and registration, retaining all supported scanner functions. A device that supports Camera Control but lacks a usable integration follows this same fallback.

Use labeled controls with name, role, current value, and enabled state. Do not convey exposure or disabled state through color alone. Provide at least 44 × 44 pt activation targets as the iOS design default. Preserve actions and full values at at least 200% text enlargement; wrap/stack the adjustment surface. Logical task order is status → Capture → Adjustments → page collection → Finish; actual assistive focus behavior needs testing. [Accessibility: Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

Locked capture entry is a separate, unresolved integration item. The local Camera Control article recommends a locked camera capture extension for system launch surfaces. This specification does not claim to supply one or to allow account switching from a locked device. Before adding that entry path, specify its authentication, document access, persistence, and return behavior using the relevant local procedures and verified implementation documentation.

## Worked before/after

**Before, from the brief:** During capture, the physical control can switch accounts or open a crowded nested settings list. Exposure selection has no feedback. The brief gives no exact event sequence or screenshot, so a particular accidental account switch is not an observed incident.

**After, worked scenario:** A person scans an invoice in Manual mode at 0 EV, 1× zoom. A light press opens Exposure (assuming it was last used). Sliding two 1/3-EV steps applies approximately +0.67 EV and displays the localized rounded label “Exposure +0.7 EV.” Duplicate touch adjustments recede; page count and Capture remain available. A light double press reveals Capture, Exposure, Zoom in their fixed order. The person selects Zoom and moves to 1.5×, sees “Zoom 1.5×,” then dismisses with Done. Onscreen values now match. Capture appends one page to the same account's document. Reopening the overlay selects remembered Zoom. On an older iPhone the same person opens Adjustments, uses Exposure + twice and Zoom + five times, then captures the same way onscreen.

## Acceptance checks and reported status

**Passed — document inspection only:** Read the supplied brief; explicitly read installed root → Getting started family → iOS procedure → reference, and Inputs family → Camera Control procedure → reference. Searched the installed topic index. Read Foundations family plus routed Layout, SF Symbols, and Accessibility procedures before their references. The revised contract covers the three supplied problems, fixed inventory, feedback, older-phone fallback, and before/after behavior. No web browsing was used.

**Failed — supplied proposal, by textual inspection:** Account switching does not serve capture adjustment; nested settings obstruct direct adjustment; missing exposure feedback fails the Camera Control procedure's usable-value check. These are findings about the supplied description, not observed runtime failures.

**Not executed — implementation acceptance gates:**

1. On a verified supported iPhone, light press opens adjustments, light double press reveals the fixed inventory, and sliding changes only the selected function. Reopen retains the last selection. Unsupported modes disable entries without removing or moving them.
2. Exercise every exposure/zoom endpoint and prominent value. Displayed localized units match applied effective values; clamping and rounding do not misrepresent the actual value. No symbol changes with live state; catalog availability is verified for each deployment target.
3. Capture via hardware, touch, and Auto concurrently: exactly one page is appended. Auto does not recapture a stationary page. Failure appends nothing and preserves prior pages. Switching to Review prevents app capture actions.
4. In portrait/landscape, smallest supported viewport, largest supported text, at least 200% enlargement, Display Zoom, long translations, and light/dark appearances: no essential labels/actions overlap overlay or hardware regions; duplicates restore correctly; framing stays usable. Measure actual hit targets and contrast. Assess physical reach and sliding precision on hardware.
5. On older iPhones and with hardware integration unavailable, complete capture → adjust → capture → review entirely onscreen. Exercise labeled step actions and supported assistive input; verify focus can reach and activate every essential action and read effective values. No hardware-only dependency.
6. Interrupt while adjusting and while capturing; resume with document/account/values preserved and no spontaneous capture. Revoke camera access and verify recovery and retained pages. Rotate without losing values or selection. Verify swipe-back/system gestures remain available.

## Evidence limits

This is a design artifact, not an implemented scanner. No SDK, device, GUI, simulator, accessibility tool, symbol catalog, or runtime test was executed. Gesture ergonomics, haptics, safe areas, effective camera ranges, auto-detection quality, actual system selection behavior, and full-press integration remain unverified. No tested dimensions or contrast measurements exist.

Only supplied local files and installed instructions informed these decisions. Official URLs above identify the sources named by those local references; they were not fetched. The Camera Control reference was retrieved in the package on 2026-10-25 and records a September 9, 2024 source revision describing iPhone 16/16 Pro and iOS-only scope. That does not establish a complete current hardware list, minimum OS, SDK API availability, or support on other platforms. No source conflict was found in the consulted passages; missing details remain explicit implementation questions.
