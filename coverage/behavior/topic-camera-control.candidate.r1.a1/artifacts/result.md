# Revised document-scanner interaction specification

## Scope and decisions

This is a framework-agnostic design contract for the scanner described in `interface.md`. The supplied brief states that Camera Control switches accounts, opens a crowded nested settings list during capture, and provides no selected-exposure feedback. It also requires older-iPhone support. No implementation or screenshots were supplied.

1. **Camera Control adjusts capture only.** Remove account switching and general settings from its functions. Keep account selection outside the active capture flow: Scan home → Account → select account → return to Scan home. An active scan retains its destination account; changing accounts applies to a new scan. Settings are available from Scan home. This is a product decision applying the capture-focused overlay model and iOS hierarchy guidance, rather than a quoted Apple prohibition on accounts. [Camera Control — Anatomy and Best practices](https://developer.apple.com/design/human-interface-guidelines/camera-control#Anatomy), [Designing for iOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices).
2. **Use a small, fixed inventory:** Zoom, Exposure, in that order throughout the capture session. Both are frequent scan adjustments; with two entries neither can uniquely occupy the middle. Do not add low-value controls just to create a middle position. If a future inventory grows, place frequent functions centrally and rare ones at the ends. Disable unavailable functions in place; never insert or remove entries on a mode change. Respect the system's remembered function. [Camera Control — Best practices](https://developer.apple.com/design/human-interface-guidelines/camera-control#Best-practices).
3. **Use system Zoom and Exposure controls when the eventual integration supports them.** Otherwise adapt the same value contracts below without inventing SDK calls or custom hardware gestures. Camera Control is an enhancement; every scan action remains available by touch on older phones. The local source names iPhone 16 and 16 Pro and excludes non-iOS platforms; it does not establish support for every later iPhone. Integration must use actual capability checks, not a model-name inference. [Camera Control — Anatomy and Platform considerations](https://developer.apple.com/design/human-interface-guidelines/camera-control#Platform-considerations).

## Function and value contract

Ranges below are product targets, not HIG-mandated limits. Intersect them with actual camera capabilities before registering the fixed inventory; retain the inventory identities afterward. Use actual applied values as the single source for both touch and hardware presentations.

| Function | Kind and initial value | Range and prominent values | Name and symbol |
| --- | --- | --- | --- |
| Zoom | Slider; 1× if supported, otherwise nearest supported value | Target 1×–3×, bounded by supported scan-camera range; prominent 1×, 2×, 3× where supported | “Zoom”; use system Zoom identity; custom-adapter candidate `plus.magnifyingglass` |
| Exposure | Slider for exposure compensation; 0 EV if supported | Target −2 to +2 EV, intersected with supported bounds; prominent whole EV values and endpoints; preserve finer supported adjustments | “Exposure”; use system Exposure identity; custom-adapter candidate `plusminus.circle` |

Exposure readout example: **Exposure +0.7 EV**; neutral: **Exposure 0 EV**. Zoom example: **Zoom 1.5×**. Localize number formatting, names, and value strings. Show units on every selected value. Report applied camera values, including quantization or clamping, rather than a requested value the camera rejected. Markers help settling without forcing whole-EV steps. If an adjustment fails, retain the last applied value and show “Adjustment unavailable.” Disable the control with an explanation if its range cannot vary.

For custom-adapter candidates, verify the exact SF Symbol against the deployment environment before release; these names are proposals, not availability evidence. Use a verified library alternative for the same function if necessary, never custom artwork in this overlay. Match neighboring text weight, use a static monochrome function symbol, and do not change its identity with slider value. A system-provided control supplies its own identity. These contracts apply the source's short-label, value/unit, prominent-value, and library-symbol guidance. [Camera Control — Best practices](https://developer.apple.com/design/human-interface-guidelines/camera-control#Best-practices), [SF Symbols — Weights and scales](https://developer.apple.com/design/human-interface-guidelines/sf-symbols#Weights-and-scales).

No discrete setting is needed in this minimal inventory. If a future capture function offers enumerated choices, use a picker rather than a continuous slider; it still requires a fixed inventory revision outside the active session.

## Interaction and state model

`phase = home | live | capturing | review | suspended`; `overlay = closed | adjusting | choosing`. Maintain `pages`, `scanAccount`, `appliedValues`, and platform-managed remembered function independently of overlay visibility.

| Event and precondition | Required result |
| --- | --- |
| Open scanner | Enter live preview after camera readiness; show touch Capture, Zoom and Exposure controls, page count and destination account. Capture is disabled until ready. |
| Light press in live preview | Request the system's adjustment overlay for its remembered function. Show its name, current value and units immediately. Do not reset the remembered function each time. |
| Light double press | Reveal the flat fixed function selector; no nested app settings or account menu. |
| Select a function, then slide | Use system selection/adjustment behavior; change only the selected enabled function. Apply and display the accepted value in the live preview. Selecting a disabled function cannot change values; show the unavailable reason. |
| Dismiss overlay through system behavior | Restore duplicate touch controls with the same values; retain selected function and scan state. Do not invent a dismissal timeout or repurpose a reserved gesture. |
| Touch Zoom or Exposure | Open a single-level equivalent adjustment surface bound to the same values. Touch Capture remains available. |
| Capture action while live and ready | Capture one page through the existing scanner capture path; reject duplicate in-flight requests; retain account and prior pages. On success increment count and return to live preview. On failure keep existing pages and show a retryable status. |
| Review pages | Close overlay; disable capture adjustments in place for review mode; show captured pages. Returning to live restores values, function identity and enabled state. |
| Background/interruption | Close overlay, suspend capture requests, preserve pages, account and values. On return reestablish camera readiness, reconcile values to supported bounds, and display applied values before enabling capture. |

A physical full press may invoke the same capture action if the verified platform integration offers that event. This is a proposed mapping requiring implementation/device verification; the supplied local article explicitly documents light press, light double press and sliding, but does not specify full-press capture dispatch. Never emulate hardware press thresholds or override system launch/gesture meanings. If full-press dispatch is unavailable, touch Capture still completes scanning.

Pseudocode describes application events, not Apple APIs:

```text
onAdjustment(function, requested):
    require phase == live and cameraReady and enabled[function]
    accepted = cameraAdapter.apply(function, bound(requested))
    if accepted.success:
        appliedValues[function] = accepted.actualValue
    else:
        showStatus("Adjustment unavailable")
    refreshHardwareAndTouchValues(appliedValues)

onCaptureRequested():
    if phase != live or not cameraReady: return
    phase = capturing  // serialize auto, touch, and supported hardware triggers
    capturePageIntoCurrentScan(scanAccount)
    // success: append once; failure: retain pages and offer retry
    phase = live when cameraReady
```

The source recommends a locked camera capture extension. Include it as a separate integration requirement for supported system entrypoints; it is not supplied by this specification. Its destination should be a fresh scanner capture session, not accounts or settings. Authentication, saved-document access and handoff need a separate defined contract before shipping locked capture. No lock-screen launch is claimed here. [Camera Control — Best practices](https://developer.apple.com/design/human-interface-guidelines/camera-control#Best-practices).

## Overlay and fallback layout

In portrait and landscape, reserve room along the physical Camera Control edge for the system overlay and enlarged name/value labels. Maximize the preview beneath that overlay; keep page count, capture status and destination account outside its label footprint. Place document framing guidance in the remaining clear preview area; reflow guidance when the overlay opens. Do not place an essential action in that reserved edge area.

While the hardware overlay is visible, hide only the duplicate touch Zoom and Exposure controls. Keep Capture, page count and review access available. Restore duplicate controls on dismissal. On older phones, always show those touch controls; do not leave an empty hardware-overlay strip or display hardware-only instructions.

Use available bounds and safe regions to position controls, rather than hard-coded device coordinates. At enlarged text sizes, wrap names/values and stack app controls as needed; keep the selected value readable without covering Capture or page status. Preserve selected values and pages across rotation. Exact overlay extents require real integration measurements; this document does not invent pixel bounds. [Camera Control — Best practices](https://developer.apple.com/design/human-interface-guidelines/camera-control#Best-practices), [Layout — Adaptability and Guides and safe areas](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability).

## Worked before/after

**Before (supplied):** During a document scan, Camera Control changes accounts and opens nested settings; the selected exposure has no feedback. The brief does not establish the exact gesture sequence or slider range.

**After (illustrative trace):** A user starts a scan for Work. In live preview, light press opens remembered Exposure with “Exposure 0 EV.” Sliding requests +0.7 EV; assuming the camera accepts it, the preview and label update to “Exposure +0.7 EV.” Duplicate touch exposure/zoom controls recede, while Capture and page count remain visible. The user captures using touch Capture (or verified full-press integration), adding page 1 to Work. Dismissing and reopening the overlay retains Exposure and +0.7 EV. Light double press reveals only Zoom and Exposure. Account selection remains on Scan home and cannot silently redirect this scan. On an older iPhone the user performs the same exposure adjustment with the touch control and captures into Work.

## Acceptance checks and evidence status

**Passed — document inspection only:** Read the installed root, Inputs and Getting started families, iOS and Camera Control procedures, then their source guides; followed Camera Control's routed Foundations family, Layout and SF Symbols procedures and guides. The revised contract contains a fixed inventory, value feedback, explicit mode availability, remembered selection, orientation behavior and older-phone fallback. These are specification checks, not executed behavior.

**Failed — supplied proposal against the revised contract:** Account switching occupies the capture input; a crowded nested settings list replaces a flat capture selector; exposure lacks selected-value feedback. Evidence is the text of `interface.md`, not an observed app run.

**Not executed — acceptance scenarios for implementation:**

- On a supported device, light press opens the remembered function, light double press exposes the fixed selector, and sliding changes only the selected adjustment. Verify physical comfort and system behavior separately from event simulations.
- Apply +0.7 EV, dismiss/reopen, rotate, and interrupt/resume: the applied value remains accurate and visible with units. Camera clamping and errors never leave a stale requested value on screen.
- Enter capturing/review/suspended states: unavailable functions remain registered in the same order, cannot mutate values, and return enabled when live and ready. A remembered disabled function never disappears.
- Trigger simultaneous capture sources: exactly one page is appended per accepted capture, with existing pages and destination preserved on failure.
- Inspect portrait, landscape, smallest supported usable bounds, and largest supported text settings: labels remain readable, no essential content/action overlaps the overlay, and duplicate controls return on dismissal. Record actual bounds/settings when performed.
- On an older phone or unavailable Camera Control capability, complete adjustment, capture and review through touch; no hardware-only step blocks scanning.
- Verify exact symbol availability, applied range/units, platform event support and any locked-capture launch/handoff against the eventual deployment target. No unavailable/custom overlay glyph is shipped.

## Evidence limits

Only supplied local text and installed guidance were used; no web browsing occurred. Official links above identify the cited articles, not pages fetched in this task. The local Camera Control guide is retrieved 2026-10-25 and records source revision September 9, 2024; it is a dated, independently packaged interpretation of HIG, not an SDK reference. Its iPhone 16/16 Pro description cannot certify newer hardware, exact APIs, press dispatch or symbol availability.

No device, Apple SDK, build, GUI, physical gesture, accessibility, safe-area rendering, haptic or locked-capture execution was performed. No measured layout or runtime accessibility result is asserted. Product assumptions introduced here are the two-function inventory, target ranges, account ownership rule and capture-state behavior; validate those with the existing capture stack before implementation.
