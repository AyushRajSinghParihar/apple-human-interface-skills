# Revised visionOS museum archive interaction specification

This first release preserves the tablet catalog’s search → list → detail → sculpture workflow. It supports seated use throughout. It launches in Shared Space, uses a movable window for browsing, and opens a bounded sculpture volume only after an explicit Inspect in 3D action. No activity in this release requires Full Space.

## Evidence and decisions

The supplied `interface.md` is a description of a proposal, not evidence of a running application. It explicitly proposes Full Space at launch, head-pinned search, raised arms for every scroll, Close behind the viewer, and rotation of the entire environment. These are confirmed properties of the written proposal; their physical effects have not been measured.

| Activity | Presentation decision | Comfortable input decision | Why |
|---|---|---|---|
| Search, browse results, read details | One user-positionable Shared Space window. Search belongs to the window. Use list and detail side by side when readable; otherwise use a detail route with Back. | Eye targeting and indirect activation with hands resting in lap or at sides. Indirect scrolling; visible Previous/Next page actions provide a discrete alternative. Activate Search before text entry through the platform’s available text-entry methods. | Contained reading and selection need no replacement surroundings. Presentation and input are independent choices: a window must still support resting input. |
| Inspect a sculpture | A bounded 3D volume in Shared Space, associated with the selected catalog record; metadata and controls remain in the window. One active sculpture at a time. | Resting-hand indirect rotation, plus labeled Rotate left/right, Tilt up/down, Front, Back, and Reset view actions. Optional brief direct manipulation when nearby; never required. | Depth helps inspect form. A volume supplies that value without a surrounding museum scene. Sustained inspection must not depend on reaching or walking around it. |

These choices apply Apple’s advice to select the least immersive useful presentation, prefer standard windows for ordinary tasks, and support indirect interaction with resting hands. Full Space is deferred because no supplied task needs an app-controlled surrounding setting. This is a product scope decision, not a claim that Full Space is universally inappropriate. Passthrough and system immersion control remain under system/person control; do not intercept the Digital Crown. No room mapping, spatial audio, or collaboration feature is assumed. [Designing for visionOS, Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos#Best-practices).

## Placement and controls

- On first opening, put useful content in front of the person within comfortable view. Let them position the window and sculpture using platform placement affordances. Do not continuously follow head pose. Do not automatically move content after the person positions it.
- Treat window and volume as associated, separately positionable surfaces. Default placement must keep the sculpture and its controls near one another without obscuring search, text, or dismissal. Avoid a tall stack of controls or essential actions behind the viewer. Exact depth, separation, and angular extent remain device-test decisions; no fixed physical viewing distance is specified.
- Keep Back, End inspection, and Reset view visible in the control window while inspecting. Provide the usual surface-close route through the eventual platform adapter. Closing the volume has the same state effect as End inspection. Closing the catalog ends inspection and saves resumable catalog state.
- Retain a stationary visual reference around the sculpture, such as an unobtrusive base. Rotation changes only the sculpture’s local transform. Never rotate the camera, room, window, base, or surrounding environment. Disable automatic spinning and inertial continuation in this first release.
- Use platform-scaled text and controls. Start ordinary text at the local guide’s visionOS default of 17 pt and action targets at 60 × 60 pt; these are logical platform units, not CSS pixels or physical dimensions. Preserve content/actions at 200% text enlargement through reflow and scrolling. Do not use the smaller listed minima as density targets. Actual target geometry, separation, and contrast await implementation measurement.

Comfortable view, avoiding head locking, hand/head Pointer Control and Zoom, repeated-gesture alternatives, and motion accommodation are supported by [Accessibility, visionOS](https://developer.apple.com/design/human-interface-guidelines/accessibility#visionOS), [Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility), and [Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). The base, one-object limit, button increments, and state policy below are project decisions rather than quoted Apple requirements.

## Interaction and state contract

Framework-agnostic state:

```text
catalog = { query, resultIds, listAnchor, selectedId, detailScroll, route }
inspection = { phase: closed | loading | ready | error,
               objectId, localOrientation, requestToken }
savedViews[objectId] = localOrientation
```

1. **Launch/resume:** Restore query, selected record, list anchor, detail route, and detail scroll where records still exist. Open only the catalog window; do not reopen a 3D presentation unexpectedly. If a record disappeared, retain query and results context and explain that the record is unavailable.
2. **Browse:** Looking at a row may show targeting feedback; looking alone neither selects a record nor opens an object. Explicit activation selects a record and displays detail. Persist selection separately from transient target/focus. Back restores the list anchor and focus to that row. A new submitted query resets the list anchor; no results exposes Clear search. Search errors retain the query and offer Retry.
3. **Open inspection:** Inspect in 3D snapshots catalog context and starts loading the selected object. Show a persistent loading status with Cancel. Keep catalog reading and Back usable. Open the volume when ready, using the saved orientation for this record or its documented front view. Supply a visible title and a textual object description; do not invent curatorial descriptions from an unavailable model.
4. **Manipulate:** After activation begins an indirect drag, horizontal movement rotates the object about its own vertical axis; vertical movement tilts it. Release ends manipulation immediately. Rotation buttons change yaw by 15 degrees per activation; tilt buttons change pitch by 15 degrees, clamped to ±60 degrees. Front/Back choose named orientations. Reset restores the original front orientation. These increments are initial tuning choices. Neither looking away nor incidental hand movement initiates rotation.
5. **Alternatives:** Expose the same manipulation actions as labeled, focusable commands usable through keyboard and supported assistive activation. Example semantic action: `Rotate left; role=button; enabled=ready`; sculpture: `role=3D object; name=record title; value=current named view or orientation`. Task order is catalog navigation → selected detail → Inspect → object description → rotation/view commands → Reset → End inspection. Keep dismissal reachable during loading/error. Do not require speech, a two-handed gesture, a timed response, or precise surface grabbing.
6. **End/interrupt:** End inspection, volume-close, or Back from detail cancels pending loads, saves a ready object’s orientation, removes the volume, and restores catalog context/focus to Inspect (or the selected row when returning to the list). A late load completion cannot reopen a closed volume. App interruption stops active manipulation and saves state; resumption never resumes motion automatically.
7. **Failure/change of record:** A model load failure leaves the record detail available with Retry and End inspection; use any existing archive image as a fallback. Selecting another record ends the previous inspection. Opening its model requires Inspect again. Never show a late asset for the previous record.

```text
on inspect(id):
  cancelPreviousRequest()
  token = newToken()
  inspection = loading(id, token)
  load(id).then(asset =>
    if inspection matches loading(id, token):
      showVolume(asset, savedViews[id] or FRONT)
      inspection.phase = ready
  )

on rotate(delta):
  if inspection.phase == ready:
    sculpture.localOrientation = boundedUpdate(delta)
    // world, camera, base, and catalog transforms remain unchanged

on endInspection():
  invalidateRequestToken()
  saveReadyOrientation()
  removeVolume()
  inspection.phase = closed
  restoreCatalogContextAndFocus()
```

Respect Reduce Motion: no fly-in, automatic spin, bounce, orbiting camera, or animated depth relocation. Use immediate updates for discrete view commands and a simple appearance/disappearance treatment; retain all view choices. Provide visible status text for load/error changes rather than conveying them only by sound or color. Assistive semantics and preference behavior are requirements for a future implementation, not verified platform support. [Accessibility, Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive).

## Worked before/after

Illustrative record “Sculpture A” is a placeholder, not supplied archive data. A seated visitor searches for it, reads its record, inspects its reverse, then resumes browsing.

**Before, per proposal:** Launch enters Full Space. Search remains pinned to the head. Each results scroll requires raised arms. Sculpture rotation spins the entire environment. Close is behind the visitor, requiring a turn to exit.

**After:** Launch opens the movable catalog window. The visitor activates its Search field, submits the query, scrolls indirectly with hands in the lap (or uses Next page), and selects Sculpture A. Inspect in 3D opens its volume without replacing the surroundings. Back view or resting-hand rotation reveals the reverse while the base and catalog stay still. End inspection in the forward control window removes the volume. The query, list anchor, selected record, and detail reading position remain; Back returns to the same result row. Reinspection restores the object orientation, with Reset available. The visitor never needs to stand, reach repeatedly, or turn to locate an essential exit.

## Acceptance checks and current status

**Passed — document/static review only:** The revised specification explicitly separates presentation and input for both tasks; preserves the tablet’s core workflow; defines deliberate inspection entry, every specified exit, state restoration, stale-load handling, stable surroundings, resting input, and discrete alternatives. These checks establish completeness of the written contract, not implementation behavior.

**Failed — supplied proposal against this contract:** Full Space launch for ordinary catalog work; head-locked search; mandatory raised-arm scrolling; behind-viewer Close; world rotation during object inspection. No implemented version was tested or repaired.

**Not executed — implementation/device acceptance:**

| Scenario | Required observable outcome |
|---|---|
| Launch, search, select, inspect, end, Back | Shared Space throughout; query, anchors, selection and reading state match the contract. |
| Cancel loading, switch records, close/reopen surfaces, interrupt app | No stale object appears, no motion resumes, and catalog state survives. Error permits Retry and exit. |
| Inspect from seated postures and varied heights | Search, view controls, Reset and exit stay comfortably usable without repeated reach, head turns, or standing. Placement remains adjustable. |
| Resting hands; brief optional direct manipulation | Entire task works indirectly from lap/sides. Direct manipulation is optional and release stops rotation. Validate tracking and accidental activation on hardware. |
| Rotate/tilt/reset repeatedly | Only local sculpture orientation changes; stationary base, window and surroundings supply stable references. |
| Keyboard and supported VoiceOver, Switch Control, Dwell Control, hand/head Pointer Control, Zoom | Complete browse-to-inspect-to-return path; meaningful names/values, logical focus restoration, no gaze-only selection, no gesture-only action. Verify actual adapter capabilities. |
| 200% text, light/dark, Increase Contrast, Reduce Motion | No lost text/actions; measure contrast and activation areas; motion accommodation retains inspection meaning. |

## Source audit and evidence limits

Read the installed root `.agents/skills/apple-hig/SKILL.md` explicitly, then the Getting started family, its `apple-hig-designing-for-visionos` topic procedure, and its supporting `designing-for-visionos.md` guide. Also read Inputs, Presentation, and Foundations family procedures. Read the available Accessibility topic procedure before `foundations/references/accessibility.md`. Each file read used a separate command.

The installed family routes and topic index point to Eyes, Windows, and Spatial layout topic procedures, but those three `SKILL.md` paths are absent. Direct reads failed; a hidden-file search located their reference articles but no matching topic procedures. Those articles were not used to bypass the required procedure-first route. Detailed eye-target geometry, window lifecycle conventions, and spatial-layout prescriptions therefore remain limited to the available visionOS and accessibility guidance; revisit the missing procedures before implementation.

Official links above identify the source articles; they were not fetched. Only supplied local files and installed instructions were used. The available guides identify a snapshot retrieved 2026-10-25 and are package-authored guidance based on Apple sources, not SDK documentation. No independent source/media review is inferred. No native build, SDK, headset, GUI, model assets, measured layout, or assistive execution was available or performed. Physical comfort, eye/hand responsiveness, rendering, accessibility behavior, API availability, and compilation remain unverified. This document is an implementable interaction contract, not executable Apple code or a claim of conformance.
