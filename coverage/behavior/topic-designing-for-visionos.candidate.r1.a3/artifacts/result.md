# Revised museum archive interaction specification

This first visionOS experience preserves the tablet catalog’s search, list, detail, and rotatable sculpture. Visitors can complete the entire flow seated. This is a framework-agnostic design contract, not an implemented or device-tested interface.

## Decisions: presentation and input are independent

| Activity | Presentation decision | Comfortable input decision |
| --- | --- | --- |
| Search, browse, read detail | One movable, resizable standard window in Shared Space. Search, results, and detail remain ordinary contained UI. Preserve system glass, movement, resizing, and close controls. | System eye targeting with indirect tap/hold/drag usable with hands in lap or at sides. Search uses system text entry; keyboard entry is an alternative. Scrolling also has visible Previous/Next results controls. |
| Inspect sculpture | Explicit **Inspect sculpture** action opens one bounded volume in Shared Space, retaining the catalog window and its context. Depth supports examining the sculpture; replacing the room adds no demonstrated value. | Indirect drag rotates the selected sculpture only. Visible rotation, view, size, and reset actions provide a complete alternative. Brief direct manipulation may be supported when comfortably reachable, but is optional. |

No Full Space at launch or during this first inspection flow. A future reconstructed exhibition would need a separate task justification, deliberate entry, stable references, explicit return, and immersive-experience guidance before specification. Presentation does not imply custom hand tracking or mandatory two-handed input.

These choices apply the least-immersive-per-activity and resting-hand recommendations in [Designing for visionOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos#Best-practices), and the window/volume distinction in [Windows — visionOS](https://developer.apple.com/design/human-interface-guidelines/windows#visionOS). Specific labels, increments, and restoration rules below are product decisions.

## Browsing contract

1. Launch into the catalog window at system-chosen placement; allow the visitor to move and resize it. Never rigidly attach search or other content to the head. Keep search and navigation in the window, with no critical controls behind the visitor.
2. At wide sizes, show results beside selected-item detail; at narrow sizes, show results then detail with a labeled Back to results action. Preserve query, results order, selected item, and scroll anchor across resize and Back.
3. Search activation opens text entry. Submit commits the query; looking or hovering never submits or selects an item. Keep the last completed results visible while loading, labeled “Updating results.” Empty results retain search and offer Clear search. Failure retains the query and offers Retry.
4. Result activation selects the item and displays detail. Selection has a persistent label/indicator distinct from transient system hover. A row’s image and title form one target. Focus alone never opens inspection.
5. Detail includes the archive’s existing metadata and an explicit Inspect sculpture action. If no usable model exists, show “3D inspection unavailable” and retain text/images. Do not substitute a broken spatial surface for the record.
6. Indirect scrolling is the default. Previous/Next results move by one visible group and announce the new range; disabled boundaries are exposed. No repeated reach or raised-arm scrolling is required.

## Sculpture inspection contract

**Entry:** Save browsing state and initiating control. Show model-loading status in detail, with Cancel. On success, open one volume with the selected sculpture, its title, and usable controls in comfortable forward view. Let system placement and visitor movement controls govern placement; avoid prescribing a fixed viewing distance. Sustained reading should normally be at least 1 m away, following [Eyes — Best practices](https://developer.apple.com/design/human-interface-guidelines/eyes#Best-practices); device testing must reconcile actual placement and readability.

**Stable scene:** Keep the room, catalog, lighting reference, and model base stationary. Rotate the sculpture around its own center, never the camera, volume, or environment. No automatic spin, orbiting camera, or inertial continuation. Stop rotation on release or interruption. Fit the model inside its bounds; keep labels outside its silhouette. Do not imply physical scale unless trustworthy archive dimensions exist. The default is labeled “Fit view”; optional enlargement is viewing magnification, not a claim of actual size.

**Controls:** Provide Rotate left/right (15° yaw per activation), Tilt up/down (15° pitch, clamped at ±60°), Front/Back/Left/Right views, Smaller/Larger (bounded viewing magnification), Reset view, and Done. Reset restores default orientation and fit size without changing the record. Indirect drag offers continuous bounded orientation changes with immediate feedback; release stops. Named views make every side available without walking around the volume. Direct manipulation, if provided, invokes the same transform operations and is never required.

**Exit:** Done closes the volume and returns focus to Inspect sculpture with query, selection, results anchor, and detail intact. System volume-close performs the same return. Cancel/loading failure leaves the catalog unchanged and gives Retry on failure. Opening another record replaces the existing inspection only after explicit inspection activation; do not accumulate volumes. Closing the catalog also closes its dependent inspection. Preserve browsing state for reopening; restore inspection only after another explicit Inspect action. System interruptions stop manipulation and retain the last stable pose; resumption never starts motion automatically.

## Input, semantics, and layout requirements

Use standard interaction behavior where the eventual stack supports it; no Apple SDK is assumed here. Reserve system gestures and hand/wrist overlay space. Do not collect gaze or implement gaze-triggered navigation: the system supplies hover outside the app; activation changes application state. These distinctions follow [Eyes](https://developer.apple.com/design/human-interface-guidelines/eyes#Custom-hover-effects) and [Gestures — visionOS](https://developer.apple.com/design/human-interface-guidelines/gestures#visionOS).

Expose each control’s name, role, enabled/selected state, and value. Expose sculpture identity, archive description, current named view/orientation, and magnification as text. Describe meaningful visual features using available archive content; do not invent missing descriptions. Reading metadata remains possible without manipulating the model. Logical traversal follows search → results → detail → Inspect; inspection follows identity/description → transform controls → Reset → Done. Return focus on dismissal. Support system assistive activation, hand/head Pointer Control, Zoom, and connected-keyboard focus/activation; speech and two-hand gestures are optional.

Start with visionOS default 60 × 60 pt control targets rather than the smaller permitted minimum. For eye-targeted items, apply at least a 16 pt margin around bounds or 60 pt between centers; verify actual activation geometry, not icon size. Keep horizontal control groups compact rather than a tall stack; reflow without hiding actions. Support 200% text enlargement and visual indications in addition to color. Reduce Motion removes animated orientation transitions and depth changes while preserving the chosen final view; no world motion exists in either mode. These requirements derive from [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#visionOS), its Vision/Mobility guidance, and [Eyes — Making items easy to see](https://developer.apple.com/design/human-interface-guidelines/eyes#Making-items-easy-to-see).

## Framework-agnostic state sketch

```text
CatalogState = {query, results, selectedID, scrollAnchor, route, returnFocus}
InspectionState = closed | loading(id) | ready(id, orientation, magnification)

activateInspect(id): save CatalogState; InspectionState = loading(id)
modelReady(id): if still requested, open volume; state = ready(id, front, fit)
cancelOrFail(): stop pending open; retain CatalogState; expose retry on failure
rotate(delta): change sculpture orientation only; clamp pitch; stop on release
setNamedView(view): set sculpture orientation; preserve room and catalog transforms
reset(): orientation = front; magnification = fit
doneOrSystemVolumeClose(): close volume; restore CatalogState and returnFocus
interrupt(): stop manipulation; retain stable state
closeCatalog(): stop loading/manipulation; close dependent volume; save browsing state
```

## Worked before/after

Given a seated visitor searching “bronze” and selecting record S-17 (illustrative ID):

| Step | Supplied proposal | Revised behavior |
| --- | --- | --- |
| Launch/search | Full Space starts; search follows the head. | Shared Space catalog window; search stays within the movable window. |
| Browse | Every scroll requires raised arms. | Resting-hand indirect scroll or Next results; select S-17 explicitly. |
| Inspect rear | Inspection spins the environment. | Inspect opens the sculpture volume; Back view turns only S-17 to its rear. Surroundings remain stable. |
| Return | Close is behind the viewer. | Forward-visible Done or system close returns to S-17 detail, preserving “bronze,” list position, and selection. |

## Acceptance checks and current status

**Passed — specification review only:** Each supplied problem has an explicit replacement; browsing and inspection have separate presentation/input decisions; seated completion, loading/error exits, context restoration, and transform ownership are specified. No runtime behavior is established by these passes.

**Failed — supplied proposal against this contract:** Launch immersion is unnecessary for catalog work; head-locked search obstructs comfortable interaction; compulsory raised-arm scrolling prevents resting input; rear close requires turning; environment rotation removes a stable reference. These are findings from `interface.md`, not observed device behavior.

**Not executed — required implementation/device acceptance:**

- Search → select → inspect → rotate → Done returns the exact query, selection, results anchor, and focus; repeat through system close, cancel, failure, interruption, resize, and catalog reopening.
- With hands resting and either hand, complete browsing and inspection seated; no essential action requires reach, turning, walking, two hands, or speech. Repeat at different heights/postures on a worn headset.
- Observe rotation: only sculpture transform changes; no camera/world motion or motion after release. Named views and Reset work without drag. Reduce Motion preserves final views without animated transitions.
- On a worn headset, verify targeting, depth/refocus comfort, readable placement, control reachability, multiple viewpoints, and close/move controls. Confirm the volume does not obscure required catalog actions.
- Verify keyboard and supported assistive routes for the full task, semantic order, focus restoration, hand/head Pointer Control, and Zoom. At 200% text, all actions and content remain reachable; measure target spacing and contrast in actual rendering.

## Evidence limits and instruction audit

Only `interface.md` and installed local instructions/references informed this specification; no web access was used. Official links identify the local guides’ source articles and were not opened. No native build, Apple SDK, GUI, headset, accessibility execution, geometry measurement, or comfort test was available or performed.

The installed root `apple-hig/SKILL.md` was explicitly read first. Family routes read: getting-started, inputs, presentation, foundations. The visionOS and accessibility topic procedures were read before their source guides. The installed routes and topic index point to Eyes, Gestures, Windows, and Spatial layout topic procedures that are absent at those exact paths; reads failed, and a hidden-file search found no alternate installed copies for them. Available Eyes, Gestures, and Windows references were used directly as a documented fallback after the missing-procedure attempts. Spatial-layout detail is deferred rather than claiming that procedure was followed. No Full Space styling or detailed spatial geometry is specified. All instruction/reference reads used one file per shell command.

The local guides describe a dated HIG snapshot, not SDK availability or independently verified device behavior. No material conflict was found in the passages read. Missing procedures limit routing completeness; this artifact is a concrete design proposal pending implementation and the acceptance checks above.
