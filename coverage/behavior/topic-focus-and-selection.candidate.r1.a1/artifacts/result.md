# Apple TV project browser audit

## Scope and evidence

Target: tvOS project browsing with directional remote input. The supplied `interface.md` is a one-line behavior report: initial focus is offscreen; focused and selected cards look identical; a carousel boundary is a navigation dead end; return from detail jumps to the first card; a disabled destructive control remains activatable. These are **verified against the supplied brief**, not independently reproduced runtime defects. There is no supplied implementation, screenshot, project dataset, focus graph, or execution trace to establish causes or measure rendering.

Read the installed apple-hig root, searched its topic index, then read the owning families and topic procedures before their references: Getting started → Designing for tvOS; Inputs → Focus and selection, Remotes; Layout and organization → Collections, Lockups; Menus and actions → Buttons. Sources below are the installed local snapshot; official links identify provenance and were not browsed.

## Ranked findings and decisions

Ranking is an audit judgment based on consequence, followed by ability to navigate and retain context.

| Rank | Brief-confirmed finding and effect | Correction and source |
| --- | --- | --- |
| 1 — High | Disabled destructive control still activates. An unavailable action can produce an unintended destructive consequence; actual data loss is unverified. | Make unavailable controls inactive and excluded from directional targets. Guard the command itself against stale/direct activation, not just its appearance. HIG supports inactive, unreachable unavailable states; command-layer validation is an implementation decision. [Focus and selection — tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS), [Buttons — Style and Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Style). |
| 2 — High | Carousel boundary becomes a dead end. People can lose access to other regions or fail to leave the carousel. Exact affected edge and surrounding controls are unspecified. | Provide directional paths to and from every enabled interactive region. An outward move at the content's final edge may remain in place, but reverse movement and a route out must work. Do not require wraparound. [Focus and selection — Best practices](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices). |
| 3 — High | Initial focus starts offscreen. The interaction target is not apparent on entry. | Choose an eligible visible entry target and reveal its entire focused bounds before showing the focus indicator. Do not silently relocate focus during idle browsing. [Designing for tvOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos#Best-practices). |
| 4 — Medium | Focused cards look identical to selected cards. People cannot distinguish their next action target from their persistent project choice. | Give focus a raised/highlighted treatment and selection a persistent labeled check badge. Compose both when one card has both states. Directional browsing changes focus only; deliberate Select commits the project and opens detail. Selection semantics and badge wording are product decisions. [Focus and selection — tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS). |
| 5 — Medium | Back from detail jumps to the first card. Browsing location is lost and navigation must be repeated. | Preserve origin project identity and viewport; restore that project when returning to the parent browser, with explicit fallback if it disappeared. This restoration policy is application advice supporting continuity, not a quoted universal HIG requirement. [Remotes — Best practices](https://developer.apple.com/design/human-interface-guidelines/remotes#Best-practices), [Collections — Best practices](https://developer.apple.com/design/human-interface-guidelines/collections#Best-practices). |

## Corrected contract

Keep independent state:

- `focusedID`: the enabled interaction target in the current view.
- `selectedProjectID`: persistent chosen project, changed only by deliberate project activation or an explicit product operation.
- `returnAnchor`: originating project ID, previous ordered IDs, and browser viewport.
- `availability(action, project)`: authoritative current eligibility, shared by rendering, navigation, and command execution.

Each project tile is one focusable unit containing its title, artwork if present, and selection badge. Candidate component: a titled caption-button-like lockup in a horizontal collection; the brief's word “card” does not establish an actual native card component. Keep the whole unit's focus treatment together and reserve space for expansion without overlap or clipping. Exact dimensions, tilt, assets, and actual component type remain unverified. [Lockups — Best practices and Caption buttons](https://developer.apple.com/design/human-interface-guidelines/lockups#Best-practices).

| State | Observable treatment and behavior |
| --- | --- |
| Unfocused, unselected | Ordinary tile and readable project identity. |
| Focused, unselected | Raised/highlighted full tile; no selected badge. |
| Unfocused, selected | Persistent check badge labeled “Selected project”; ordinary depth. |
| Focused, selected | Focus treatment plus the persistent selection badge. |
| Pressed | Immediate transient press feedback, then activation if still eligible. |
| Unavailable | Distinct inactive appearance; no focus destination and no command effect. |

Prefer the platform's system focus effects when available; this contract requires no Apple SDK. A custom renderer must preserve the distinctions and observable feedback. [Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS), [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices).

### Routes and input

The following is a proposed logical route map, not a claim about unseen screen geometry. Place controls consistently with it, or derive equivalent predictable spatial neighbors from the actual layout.

```text
Browser actions (enabled controls only; destructive action never initial default)
       Down ↕ Up
Project carousel: P1 ↔ P2 ↔ ... ↔ Pn
       Select → detail(Pi)
       Back from detail → browser at Pi
```

Left/right traverses adjacent eligible projects, scrolling to reveal the next one. At either end, movement inward still works; Up reaches enabled browser actions. Down from actions returns to the last eligible carousel project. If no actions are available, the carousel remains reversible and Back still follows hierarchy. No enabled action may exist without a directional path. Back from the browser opens its parent; at root, preserve system Home behavior. Holding Back retains system behavior. Swipe/directional input navigates; Select press activates. Focus movement alone never opens detail or executes a command. [Remotes — Buttons](https://developer.apple.com/design/human-interface-guidelines/remotes#Buttons).

The unnamed destructive control is a button with destructive semantic role; its precise label, affected object, reversibility, placement, and enabled-state recovery are unknown. “Delete Project” is only an illustrative label if that is its actual outcome. This audit specifies its disabled behavior; confirmation/default/undo decisions require actual command semantics and are not inferred here.

### Framework-agnostic pseudocode

```text
enterBrowser(returning):
    if returning:
        target = eligibleProject(returnAnchor.projectID)
        if target is absent:
            target = nearestSurvivingProject(returnAnchor.previousOrder,
                                             returnAnchor.projectID)
        restoreViewport(returnAnchor.viewport)
    else:
        target = firstVisibleEligibleProject()
    target = target ?? firstEligibleProject() ?? enabledEmptyStateAction()
    revealFullFocusedBounds(target)
    focusedID = target                 // null if nothing is interactive

onDirection(direction):
    target = eligibleSpatialNeighbor(focusedID, direction, routeMap)
    if target exists:
        revealFullFocusedBounds(target)
        focusedID = target
    // no project selection or command execution

onSelectPress():
    target = resolveCurrentTarget(focusedID)
    if target is absent or not eligible(target): return
    showPressFeedback(target)
    if target is project:
        returnAnchor = {projectID: target.id, previousOrder: projectIDs,
                        viewport: currentViewport}
        selectedProjectID = target.id
        openDetail(target.id)
    else:
        executeCommand(target.command, explicitObjectID(target))

executeCommand(command, objectID):
    if not availability(command, objectID): return REJECTED
    // Revalidate atomically with committing the effect; no disabled bypass.
    return commitIfStillEligible(command, objectID)

onDetailBack():
    openParentBrowser()
    enterBrowser(returning = true)
```

Fallback policy is a product decision: nearest surviving project uses previous order, preferring the next item then the previous on a tie; otherwise first eligible project, then an enabled empty-state action. Never silently select that fallback. If the selected project is deleted, clear its selection rather than marking an unrelated project selected. For a focused item disappearing during discrete directional navigation, choose a nearby one-step target; for other input, hide the indicator instead of inventing a focus destination. Detail-return restoration is a separate explicit Back transition. [Focus and selection — Best practices](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices).

## Worked before/after

Illustrative fixture, not supplied project data: projects A–F, D selected, E focused, and the destructive action unavailable.

| Step | Before, using reported defects | After, required behavior |
| --- | --- | --- |
| Open browser | Initial focus is offscreen. | Visible A receives focus on a fresh entry; D retains its selected badge. |
| Navigate to E | Focus and selection use identical styling. | E is raised/highlighted; D alone retains the selection badge. No detail opens. |
| Select E | Existing selection-commit semantics are unknown. | E becomes selected, origin/viewport are saved, detail E opens. |
| Back | Focus jumps to A. | Browser restores E in view, focused and selected. |
| Move right to F | Reported boundary can become a dead end. | At F, Left returns to E; Up reaches enabled actions; Back remains available. Right can stay at the true edge. |
| Attempt unavailable destructive action | Control remains activatable. | It is skipped by focus; a stale/direct command invocation is rejected with no effect. |

## Acceptance checks and status

**Passed — document inspection only:** platform and all five findings traced to `interface.md`; installed route/procedure/reference sequence read; proposed model separates focus, selection, press, and availability. No runtime checks passed.

**Failed — according to supplied behavior report:** visible initial target; distinct focus/selection appearance; exit from carousel boundary; origin restoration; disabled-action suppression. These failures have not been independently reproduced.

**Not executed — required implementation acceptance:**

1. Fresh entry, including a scrolled viewport: one eligible target is visible with its full enlarged bounds; no offscreen indicator. Empty/all-unavailable datasets have a defined reachable enabled action or no active target.
2. Traverse each enabled target and every carousel edge in all four directions. Reach and exit every region; reverse movement and Back work. Check one-item and odd-sized collections; no forced wraparound is necessary.
3. With D selected, move focus to E. D retains its badge and E shows focus; selecting E gives press feedback, commits E, and opens E once. Moving focus causes no activation.
4. Back from detail restores the same stable project ID and viewport even after reorder. If removed or unavailable, use the specified eligible fallback; do not select it implicitly. Test deletion of both focused and selected projects.
5. Attempt unavailable destruction through remote activation, stale focus, and direct command dispatch. All produce zero destructive effects. Disable between eligibility check and commit; the atomic commit guard must reject it.
6. Verify long project titles, first/last tiles, focus enlargement, and selected badges do not clip or overlap. Confirm the entire lockup moves together and identity remains readable across the room.
7. On supported Apple TV hardware, verify actual Siri Remote direction/swipe/press/Back behavior, focus restoration, native or custom rendering, and accessibility behavior. Record hardware, software, and observed results separately.

## Evidence limits

Only local document review and specification authoring occurred on the headless Linux server. No Apple SDK, compilation, device, GUI, remote, accessibility, or automated behavioral execution occurred. There is no evidence of actual card geometry, label quality, accessibility names/order, focus tilt, overlap, performance, or destructive data loss, so none is claimed as an additional defect. This specification is the corrected behavior to implement and test, not evidence that the interface has been fixed. Local guidance is a dated derived HIG snapshot, not an SDK reference or independently reviewed Apple text; no current-web verification was performed, as requested.
