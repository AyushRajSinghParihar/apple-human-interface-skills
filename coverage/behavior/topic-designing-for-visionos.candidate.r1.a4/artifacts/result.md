# Revised museum archive interaction specification

Design contract for the first visionOS release, based on `interface.md`. This is framework-agnostic; no Apple SDK is assumed. Assumptions: one visitor, one selected archive item, seated use supported throughout, and a sculpture asset whose availability and physical dimensions must be verified. Search, list, detail, and object rotation remain the core tasks.

## Decisions: presentation and input are separate

| Activity | Presentation decision | Comfortable input decision |
|---|---|---|
| Search, browse, read details | One movable, resizable glass window in Shared Space. Search remains inside the window. Use the system’s initial placement and dynamic scaling; never rigidly head-lock it. | Eye targeting with standard indirect tap/drag from hands resting in lap or at sides. Search activates ordinary text entry. Provide labeled Previous results / Next results actions as alternatives to scrolling. |
| Inspect a sculpture | Explicit “Inspect sculpture” opens one bounded volume in Shared Space; retain archive details in the original window. Deep geometry belongs in the volume rather than protruding through the reading surface. | Resting-hand indirect activation of Rotate left, Rotate right, Tilt up, Tilt down, and Reset view. Optional ordinary indirect drag on the sculpture supplements these controls; nearby direct manipulation is brief and optional. No custom tracked-hand gesture is required. |

These choices apply the least immersive presentation that serves each task ([Designing for visionOS, Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos#Best-practices)). Windows serve familiar contained work; volumes support multi-angle 3D inspection ([Windows, visionOS](https://developer.apple.com/design/human-interface-guidelines/windows#visionOS)). Full Space adds no demonstrated benefit to this first release, so it is not entered at launch or during inspection. A future contextual exhibit would need a separate deliberate entry/return and immersion review.

Indirect interaction from rest is preferred for sustained work; direct interaction remains optional, rather than a repeated raised-arm requirement ([Gestures, visionOS](https://developer.apple.com/design/human-interface-guidelines/gestures#visionOS)). Do not intercept system palm/wrist overlays or replace system recentering.

## Surface, placement, and action contract

- Archive window: search, results, selected-item detail, and Inspect action. At narrow sizes show list or detail with a labeled Back to results action; at wider sizes both may appear. Preserve query, result ordering, selected ID, and list position across resizing and navigation. Retain system move, resize, and close controls. Reuse this window rather than opening one per item.
- Inspection volume: one sculpture, object identity, and stable orientation/depth cues. It is space-anchored and movable; it does not follow every head turn. Start with a dynamically scaled study model, fitted within bounds for every supported rotation. Display “Study scale — not actual size.” Do not imply verified life-size dimensions. No floor placement, walking, crouching, or reaching behind the model is required.
- Essential controls stay together on the archive window’s visible detail surface: orientation actions, Reset view, and “Return to catalog.” Keep that surface near the inspection task without forcing placement or chasing the viewer’s head. Retain system volume close/move controls that face the viewer. If a person moves a surface away, preserve system movement/recentering so it can be recovered.
- Important content starts centrally and remains readable across supported window sizes. Avoid competing peripheral animation and repeated refocusing between widely separated depths. Sustained reading normally belongs at least 1 m away; this is source guidance, not a hard-coded lock on user placement ([Eyes, Best practices](https://developer.apple.com/design/human-interface-guidelines/eyes#Best-practices)). No universal field-of-view angle is specified.
- For regular application buttons specify 60 × 60 pt activation areas and at least 16 pt clear gaps; this exceeds 60 pt center spacing for adjacent equal-sized buttons. Keep targets and hover regions disjoint. These are visionOS points, not physical centimeters or Linux pixels. Reflow controls when space is insufficient ([Spatial layout, Best practices](https://developer.apple.com/design/human-interface-guidelines/spatial-layout#Best-practices); [Accessibility, Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility)).
- A result’s image and title form one stable activation/hover region. Looking produces system feedback only; it neither selects an item nor changes archive state. Explicit activation selects it. No pre-activation gaze logging or gaze-dependent business logic is assumed ([Eyes](https://developer.apple.com/design/human-interface-guidelines/eyes)).

Space anchoring, dynamic versus fixed scale, and stationary use follow [Spatial layout](https://developer.apple.com/design/human-interface-guidelines/spatial-layout). Exact comfortable placement, asset bounds, and viewing alignment remain prototype decisions requiring device validation.

## State and transitions

Logical events below describe behavior, not API names.

```text
ArchiveState = {query, results, selectedID, listPosition, returnTarget}
Inspection = closed | loading(itemID, token) | ready(itemID, orientation) | error(itemID)

launch:
  restore ArchiveState when available; show archive window in Shared Space
  Inspection = closed                     // never launch into immersion

activateResult(id):
  selectedID = id; show its detail          // selection requires activation

activateInspect:
  remember returnTarget = Inspect(selectedID)
  reuse the single inspection surface for selectedID
  cancel/invalidate older load token; Inspection = loading(selectedID, newToken)
  show persistent loading text and Return to catalog

assetArrives(id, token):
  if token matches current load and id == selectedID:
    fit asset into volume; Inspection = ready(id, defaultOrientation)
  else ignore                              // no stale sculpture substitution

assetFails:
  Inspection = error(selectedID)
  retain detail and description; offer Retry and Return to catalog

rotate(direction):
  if ready: adjust sculpture orientation by 15 degrees per activation
  never transform camera, room, passthrough, window, or volume anchor
  update visible orientation value; no automatic spin or inertia

optionalIndirectDrag(delta):
  if ready: update sculpture orientation with immediate proportional feedback
  stop on release/cancel; keep all geometry within bounds

resetView:
  restore sculpture orientation and fit only; do not recenter the user's space

returnToCatalog OR systemCloseVolume:
  invalidate pending load; close inspection; preserve ArchiveState
  restore logical navigation target to Inspect(selectedID) when possible

selectDifferentItemWhileInspecting:
  close old inspection; select new item and show detail
  require explicit Inspect before loading its model

systemCloseArchiveWindow:
  save ArchiveState; close owned inspection and invalidate its loads
  reopening restores query, selection and position with inspection closed
```

The 15-degree step, single-volume policy, and launch restoration are product decisions, not Apple requirements. Preserve state through interruption; no background rotation continues while inactive. Inspection failure never blocks browsing. The close/return action does not depend on a model finishing loading.

## Equivalent operation and content

Every essential action has a labeled control, usable without a drag, speech, two hands, or a prescribed dominant hand. Define accessible names, button roles, enabled/loading states, and orientation values for custom controls. Provide a meaningful sculpture description and catalog metadata even when a 3D model is unavailable; curatorial descriptions must come from verified archive content, not invented geometry claims. Support keyboard and platform assistive navigation/activation, including hand/head Pointer Control and Zoom. These are implementation requirements, not established runtime support ([Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)).

Use platform text defaults as the starting point (visionOS default 17 pt), allow at least 200% text enlargement, and reflow rather than hide actions. Do not encode selection or errors solely with color or sound. No automatic scene movement is specified. All manual orientation controls remain available if animated manipulation cannot be used. Actual rendering, contrast, assistive behavior, and preference handling require later implementation review.

## Worked before/after

Scenario: a seated visitor searches for a sculpture, opens its details, examines its back, then returns to the same result.

| Step | Supplied proposal | Revised contract |
|---|---|---|
| Launch/search | Full Space starts immediately; search is head-pinned. | Shared Space archive window opens. Visitor positions it; search stays attached to the window. |
| Browse results | Every scroll requires raised arms. | Visitor scrolls indirectly with resting hands, or activates Next results. Selection and list position are retained. |
| Inspect back | Sculpture inspection spins the entire environment. | Inspect opens a volume. Twelve Rotate right activations turn only the sculpture 180 degrees; room, camera, and controls remain stable. Drag is optional. |
| Leave inspection | Close control is behind the viewer. | Visible Return to catalog or system volume close ends inspection. The same query, selected item, and list position remain; logical navigation returns to Inspect. |

The supplied behaviors are specification-level barriers: unnecessary immersion, head locking, repeated raised-arm work, environmental rotation, and a behind-viewer exit. Their presence in `interface.md` is established; their runtime effects have not been observed.

## Acceptance checks and current status

**Passed — static specification review only:** both activities have independent presentation/input decisions; all five supplied proposal problems have explicit replacements; complete search → detail → inspect → return transitions are specified; stale-load, failure, repeated-open, close, resize, and restoration behavior is defined. These passes establish document coverage only.

**Failed — supplied proposal against this revised contract:** Full Space at launch, head-locked search, mandatory raised-arm scrolling, environment rotation, and behind-viewer Close. These are textual findings, not headset test results.

**Not executed — implementation acceptance scenarios:**

1. Launch and complete the worked scenario entirely seated with hands resting; confirm no mandatory reach, turn, walking, or two-hand action. Repeat with different heights/postures on a worn Vision Pro.
2. Open inspection repeatedly: exactly one volume exists and it shows the selected ID. Switch item during loading; late completion cannot show the old model. Simulate missing/failed assets; browsing and Return remain available.
3. Rotate through all supported orientations, including 180 degrees; verify only model orientation changes, no clipping, no automatic continuation, stable controls, and Reset affects only the model.
4. Exit using Return, system volume close, interruption, and archive close/reopen. Verify query, ordering, selection, and position restoration, pending-load cancellation, and appropriate logical navigation target.
5. Resize to supported extremes and enlarge text to 200%. Verify all content/actions remain reachable, targets remain disjoint, and specified visionOS geometry is preserved. Measure actual contrast in rendered appearances and Increase Contrast settings.
6. Perform the complete route with keyboard and supported assistive inputs, without drag or speech. Verify names/roles/values, navigation, activation, loading/error announcements, Pointer Control, and Zoom on an Apple environment.
7. On a worn device, verify gaze/indirect responsiveness, target separation, depth/readability, stable anchoring, system recentering, system overlays, and comfortable access to Return after user repositioning. Confirm looking alone never selects or persists archive state.

## Evidence limits and local route

Only `interface.md` and the installed guidance were used. No web pages were fetched; official links above identify the source articles named by local references. The local articles are derivative HIG snapshots dated 2026-10-25, not SDK documentation or proof of independent source review. No native build, SDK compilation, simulator, GUI, headset, accessibility tool, or physical-comfort test was run. Asset validity, measured geometry, contrast, runtime state restoration, and assistive execution remain unverified. No specific Apple API availability is claimed.

Auditable route, resolved beneath `.agents/skills/apple-hig/`: root `SKILL.md` → getting-started family → designing-for-visionos topic → its reference. Topic-index searches identified windows, eyes, gestures, spatial layout, and accessibility. Each owning family and each corresponding `.topics/apple-hig-*/SKILL.md` was read before its `references/*.md` guide. Each read used a separate `cat` command. Immersive-experiences details were not specified because this design does not enter Full Space; any future immersive exhibit must follow that route before design approval.
