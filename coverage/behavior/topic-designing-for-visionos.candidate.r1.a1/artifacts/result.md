# Revised museum archive interaction specification

Scope: first visionOS adaptation of the tablet search → list → detail → rotatable sculpture flow in `interface.md`. This is a framework-agnostic design contract, not an SDK implementation. Seated, stationary use is a first-class requirement. Assume one visitor and one inspected sculpture at a time; collaboration and a surrounding exhibition are outside this first version.

## Decisions: presentation and input are separate choices

| Activity | Presentation decision | Comfortable input decision |
|---|---|---|
| Search and browse | Launch a movable, resizable standard window in Shared Space. Keep search, results and detail in this window. Use a list/detail arrangement when space permits; use a detail route with Back when narrow. | System-mediated eye targeting plus indirect tap/drag with hands resting in lap or at sides. Search activates ordinary text entry; support connected keyboard input. Scrolling also has labeled Previous page / Next page actions. |
| Inspect sculpture | Explicit “Inspect in 3D” opens one bounded volume in Shared Space. Keep catalog context in the window; put inspection actions together in a compact, forward-facing control area. A volume supplies depth and multiple views without replacing the surroundings. | Indirect manipulation rotates only the sculpture. Labeled Rotate left/right, Tilt up/down, Zoom in/out and Reset view provide discrete alternatives. Brief direct manipulation may supplement these controls when reachable; it is never required. |

Full Space is not selected: neither catalog work nor examining one 3D object needs an app-controlled surrounding environment. Do not enter it on launch or request custom hand tracking to reproduce ordinary interactions. Preserve passthrough and system immersion/recentering controls. These choices follow the local [visionOS best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos#Best-practices), [window and volume guidance](https://developer.apple.com/design/human-interface-guidelines/windows#visionOS), and [visionOS gestures guidance](https://developer.apple.com/design/human-interface-guidelines/gestures#visionOS). Links identify sources; no web retrieval was performed.

## Spatial and control contract

- Search belongs to the catalog window, anchored to the surrounding space, never rigidly head-locked. Let the system place initial surfaces and the visitor move them. Do not repeatedly reposition them as the head moves. Offer system recentering rather than inventing a competing gesture.
- Keep title, object, essential actions and return path in comfortable forward view. Do not require walking around the sculpture: rotation reveals the rear while seated. Controls must remain available when the object rotates. Retain system close/move controls and add a plainly labeled “Back to catalog” action in the inspection control area; no essential control lives behind the visitor.
- Start with a fitted inspection model and an explicit “Inspection scale” label. Zoom changes the object scale, not the camera or room. Do not claim life-size accuracy without verified asset dimensions. Keep the object within volume bounds; cap scale to avoid clipping. If dimensions are unavailable, omit any actual-size action.
- Use stable surroundings and a stable object pivot/base reference. No automatic spin, camera orbit, environment rotation, parallax flourish or inertia after release. Reset affects the model orientation and inspection scale only; it does not move the visitor's surfaces.
- Prefer standard control behavior, glass window background and dynamic scaling for the UI. Avoid rapidly alternating reading depths. Sustained text should normally be at least 1 m away; allow visitor positioning rather than enforcing a fixed viewing distance. Start with 17 pt body text, 60 × 60 pt control activation areas, at least 16 pt gaps between regular buttons and at least 60 pt between centers. These are visionOS design targets, not pixel measurements or measured results. Reflow controls into rows without overlapping targets.

Placement and sizing are grounded in local [spatial layout](https://developer.apple.com/design/human-interface-guidelines/spatial-layout#Best-practices), [eyes](https://developer.apple.com/design/human-interface-guidelines/eyes#Best-practices), and [accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility) references. Physical placement remains subject to worn-device validation; field of view varies and is not exposed as a fixed system dimension.

## Interaction and state contract

Maintain `catalog = {query, filters, resultOrder, scrollAnchor, selectedId, route, returnFocus}` and `inspection = {objectId, orientation, scale, loadStatus}`. Filters are retained if present in the eventual catalog; the supplied brief does not establish their existence.

1. Launch restores the catalog state in Shared Space; no inspection or immersion is forced. First launch shows search and results.
2. Looking at a row may produce system hover feedback. Looking alone never selects, opens, rotates or changes archive state. Activation selects the row and opens detail. A row's image and label share one target. Keyboard focus and persistent selection are distinct from hover. Do not request raw gaze or execute gaze-dependent application behavior.
3. Search submission updates results and announces the result count through semantic status. Loading preserves the submitted query. Empty results offer Clear search. Errors offer Retry without discarding context.
4. “Inspect in 3D” saves catalog return state, creates or reuses the single volume, and loads the selected asset. Show persistent loading status and Back to catalog. Do not show interactive rotation controls until ready. On load failure, keep text/image detail available and offer Retry or Back.
5. Once ready, indirect drag on the object changes its orientation about its own pivot. For a first prototype, horizontal drag controls yaw and vertical drag controls tilt; clamp tilt to ±60° to avoid disorientation. Discrete buttons change yaw/tilt by 15° and zoom by 10%, bounded by fit constraints. These increments and limits are product proposals, not Apple requirements; tune them after testing. Stop immediately on release or input loss.
6. Reset restores the asset's documented front orientation and fitted scale. No autoplay follows. Opening a different sculpture begins at its own default view; do not transfer the prior object's rotation.
7. Back to catalog or system volume close ends inspection, preserves catalog query, selection and scroll anchor, and restores focus to “Inspect in 3D” for that record. Loading completion after close must not reopen a volume. Closing the catalog ends its associated inspection; persist catalog state for relaunch. System interruption cancels an active drag without further movement; resume without forced immersion or an animated camera transition.

Abstract event rules:

```text
on HOVER(target): system renders declared feedback; archive state unchanged
on ACTIVATE_INSPECT(id): save return state; begin cancellable load(id)
on LOAD_READY(id, token): show only if token still belongs to active inspection
on ROTATE(delta): if ready, update model.orientation only
on ZOOM(delta): if ready, update model.scale within fitted bounds only
on RESET: restore model default; preserve catalog and surface placement
on EXIT_INSPECTION: cancel load/drag; close volume; restore catalog and return focus
invariant: environmentTransform and viewerCameraTransform are never changed by inspection
```

## Equivalent access and feedback

Every essential action has a visible labeled control and an equivalent semantic activation route. Define names, roles, enabled states and values: for example “Rotate left, button,” “Inspection scale, 110%,” and “Inspect in 3D, unavailable: model not available.” Include the archive's textual sculpture description and provenance alongside the 3D asset; do not invent missing curatorial descriptions.

Proposed navigation order is search → results → selected detail → Inspect in 3D; inspection order is title/description → Back to catalog → orientation/scale actions → Reset. On return, restore the originating control. Support platform assistive targeting and activation, including hand/head Pointer Control and Zoom, without requiring gaze, speech, two hands, held poses or direct reach. Keyboard navigation must reach all essential actions with visible focus. Pagination and discrete rotation remove essential drag requirements.

At 200% text, reflow rather than truncate titles, metadata or action labels. Selection and errors need words or symbols in addition to color; sound is supplementary. Honor Reduce Motion with immediate model steps or minimal fades and no animated depth transitions; retain all views and actions. Actual semantics, contrast and assistive behavior must be verified in an implementation. Source: [accessibility visionOS guidance](https://developer.apple.com/design/human-interface-guidelines/accessibility#visionOS), [eyes interaction guidance](https://developer.apple.com/design/human-interface-guidelines/eyes#Custom-hover-effects).

## Worked before / after

Scenario: a seated visitor searches for a sculpture, reads its detail, inspects its rear, then returns to the results.

| Step | Supplied proposal | Revised behavior |
|---|---|---|
| Launch/search | Full Space begins immediately; search is pinned to the head. | Shared Space catalog window; search stays with the movable window. Visitor activates search and enters a query. |
| Browse | Every scroll requires raised arms. | Resting-hand indirect scroll or Next page. Select a result and preserve its list position. |
| Inspect rear | Sculpture manipulation spins the entire environment. | Activate Inspect in 3D. In a volume, six Rotate right activations produce 90° object yaw; twelve produce the rear at 180°. The room, camera and catalog remain stable. |
| Return | Close is behind the viewer. | Activate forward-facing Back to catalog, or system volume close. Restore query, selected record, list anchor and focus without turning or standing. |

The supplied proposal fails the task-level design checks for unnecessary immersion, head locking, repeated reach, hidden exit and world motion. The revised contract addresses each; that is a specification review, not proof of runtime comfort.

## Acceptance checks and observed status

| Check | Pass condition | Status / evidence |
|---|---|---|
| Adaptation completeness | Search, list, detail, 3D inspection and context-preserving return are specified. | **Passed — document review only.** |
| Presentation/input separation | Each activity has both a presentation choice and a resting input path. | **Passed — document review only.** |
| Original proposal | Ordinary work avoids forced immersion, head locking, repeated reach, rear-only exit and room rotation. | **Failed — explicitly contradicted by interface.md.** |
| State walkthrough | Query/selection/anchor survive inspect, reset, close, load failure and interruption; late loads cannot reopen inspection. | **Passed — contract walkthrough only; implementation not executed.** |
| Stationary physical task | Seated visitors of differing heights browse, inspect every side and exit with resting hands, no required turn/reach; controls remain comfortably visible. | **Not executed — worn headset required.** |
| Manipulation | Drag and button alternatives affect only the object; release stops motion, fit prevents clipping, reset restores default. | **Not executed — no prototype/runtime.** |
| Targeting | Hover never activates; adjacent targets are distinguishable; indirect targeting works without repeated refocusing. | **Not executed — worn-device input testing required.** |
| Accessibility | Complete task via supported assistive input and keyboard; meaningful names/order; Pointer Control/Zoom; 200% text; Reduce Motion retains content. | **Not executed — no Apple accessibility execution.** |
| Layout and visuals | Activation geometry and spacing meet specified targets; text reflows; measured contrast works across appearances/backgrounds and Increase Contrast. | **Not executed — no rendered interface or measurements.** |
| SDK/device integration | System close/move/recenter behavior, volume lifecycle and input compatibility work on target OS. | **Not executed — no native build, SDK or headset available.** |

## Evidence limits and installed-source audit

Only `interface.md` and installed instructions/references were used. No web browsing, device session, GUI interaction, simulator, SDK compilation or accessibility test occurred. Official links are attribution from local snapshots, not verification of current online guidance. Asset dimensions, model quality, performance, target OS version, actual layouts and curatorial content are unknown. Resolve those before implementation; do not advertise accessibility or physical comfort as validated.

Successful local `cat` reads consumed the installed package root `SKILL.md`, then family routes for getting-started, inputs, presentation and foundations. Available routed procedures read before their source guides were:

- `subskills/apple-hig-getting-started/.topics/apple-hig-designing-for-visionos/SKILL.md`
- `subskills/apple-hig-foundations/.topics/apple-hig-accessibility/SKILL.md`

All paths are relative to `.agents/skills/apple-hig/`. Successful source reads then covered `subskills/apple-hig-getting-started/references/designing-for-visionos.md`, `subskills/apple-hig-inputs/references/{eyes,gestures}.md`, `subskills/apple-hig-presentation/references/windows.md`, and `subskills/apple-hig-foundations/references/{spatial-layout,accessibility}.md`.

**Routing audit limitation:** the installed family links for inputs `.topics/apple-hig-eyes/SKILL.md`, `.topics/apple-hig-gestures/SKILL.md`, presentation `.topics/apple-hig-windows/SKILL.md`, and foundations `.topics/apple-hig-spatial-layout/SKILL.md` resolve to missing files. Reads were attempted and failed; hidden-file discovery confirmed no matching installed procedures. Their available source guides were used as a documented fallback. This means full procedure consumption for those routes could not pass; no replacement instructions were fabricated. No Full Space is selected, so detailed immersive-style procedure routing was unnecessary. Local guidance is derived from dated Apple sources and is not an SDK reference or evidence of independent source review.
