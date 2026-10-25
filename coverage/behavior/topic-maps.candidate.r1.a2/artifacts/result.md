# Venue finder repair

Patched `interface.md` in place, replacing the defect-only brief with an implementable iPhone interaction specification. The existing custom map stack and supplied venue/list/search data remain the basis.

## Decisions and changes

- Restore provider attribution with explicit visibility and placement rules. Apple-specific branding is conditional on Apple-backed content; the actual provider is unknown.
- Replace anonymous dots with named pins, redundant selected-state cues, and count clusters with a list escape for coincident coordinates.
- Share stable venue identity across map/list/search. Preserve context on selection; pan only when needed to reveal the chosen venue, and keep text details usable without coordinates.
- Make festival browsing independent of personal location. Denial, restriction, unavailable fixes, and unavailable map tiles have separate recovery states.
- Specify query scope, clear/cancel/result transitions and state restoration. Add accessible labels, text reflow, activation targets, and a reduced-motion camera alternative.

The camera algorithm, local search matching/order, inline detail placement, exact recovery copy, and no-new-location-storage contract are project design decisions. Their purpose is to make the HIG principles actionable; they are not quoted Apple requirements. Source links and qualifications are included in `interface.md`.

## Worked before/after

Illustrative fixture only: venues A and B have valid nearby coordinates; “River Stage” is B's fictional display name.

**Before:** After denying location, the brief says the map becomes blank. If browsing is possible, identical dots do not identify River Stage, and selecting a venue recenters far away.

**After:** Denial leaves the festival extent and named venue list visible. Entering “River” finds B from the existing search data without requesting permission. Selecting B sets its stable ID and shows River Stage's detail. If B is already visible, center and zoom stay unchanged; otherwise the map pans just enough to reveal B. Its selected outline/symbol and name distinguish it. Attribution stays visible. Returning from detail retains the query and viewport. With invalid coordinates, B still opens text details and the camera stays put.

## Acceptance checks

These are implementation acceptance scenarios, not reported runtime passes.

| Check | Pass condition |
|---|---|
| Attribution | Provider logo/legal links remain visible, stable and activatable with detail open, keyboard shown, and at small supported iPhone sizes; Apple-backed content meets adopted spacing targets. |
| Marker identity | Each venue can be identified and selected by name; selected appearance remains understandable without tint. Dense/coincident pins resolve through clusters or a named list. |
| Selection camera | Selecting visible B preserves viewport; offscreen B becomes visible with context. Repeat after sorting/filtering to catch index/ID mismatches. Invalid coordinates cause no jump. |
| Denied/restricted location | On fresh launch and after a settings change, festival browsing/search/detail still work; no repeated permission prompt or blank map occurs. |
| Permission timing | Entry/search request nothing. Explicit location activation invokes the supported system flow; success, approximate position and unavailable fix follow the specified states. |
| Search | Case/whitespace matching, no results, clear, cancel and result selection match the contract; leaving/returning preserves useful state. |
| Failure distinction | Simulated tile failure retains list/search and Retry; a failed location fix does not erase venue data. |
| Interaction | Pan/zoom/rotation remain usable and do not activate obstructing controls; detail never conceals the selected marker. |
| Accessibility | At 200% text size, names/actions remain available. Measure target geometry and actual light/dark/Increase Contrast combinations. Exercise the complete list/search/detail path with VoiceOver, Switch Control and Full Keyboard Access, and selection with Reduce Motion. |

## Evidence and limits

**Passed — static specification inspection:** Read the original one-line brief; explicitly read the installed root `apple-hig/SKILL.md`, searched its topic index, then read Technologies → Maps, Foundations → Privacy and Accessibility, and Navigation and search → Search fields. Each selected family/topic procedure was read before its supporting source guide, using one file per command. The patched specification covers all four supplied defects with concrete states and transitions. Both requested Markdown artifacts were written locally.

**Failed — supplied baseline:** The brief explicitly reports missing attribution, identical unlabeled dots, a distant recenter on selection, and a blank map after denial. These are reported baseline defects, not independently reproduced failures.

**Not executed:** No app code, actual map provider, screenshots, venue dataset, supported iOS version, build project, or device evidence was supplied. No SDK compilation, device/simulator, GUI, permission prompt, accessibility execution, contrast measurement, hit-target measurement, coordinate validation, routing test, provider legal verification, or network/privacy audit was performed. Acceptance scenarios remain pending implementation. System location-button availability requires SDK/deployment verification.

Only supplied local files and installed instructions were used. Official links identify the sources represented by the local snapshot; no web pages were fetched. The package describes itself as independent, dated guidance rather than an SDK reference or compliance certification.
