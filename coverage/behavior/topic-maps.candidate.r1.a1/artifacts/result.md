# Venue finder repair

Patched [interface.md](interface.md) in place, replacing the one-line defect report with an implementable iPhone interaction specification. The existing custom map stack and supplied list/search are retained.

## Decisions and effects

| Supplied defect | Revised specification | Basis |
|---|---|---|
| Attribution omitted | Restore provider attribution and legal links on every map; preserve Apple marks when using Apple data; reserve readable space | Local Maps guide, Best practices |
| All pins are unlabeled dots | Named pins, non-color selection outline, shared venue IDs, count clusters, and a co-located-venue list | Maps, Custom information; Accessibility |
| Selection recenters far away | Retain camera when the pin is visible; otherwise minimally pan to the stored venue coordinate, accounting for details; never substitute user location | Maps, selected-place context; exact camera policy is a product decision |
| Location denial blanks map | Festival region, pins, list, search, and details work without permission; personal location is an optional explicit one-shot action | Privacy, contextual/minimal permission; fallback behavior is a product decision |

The patch also defines missing-coordinate handling, query scope and clearing, exact-result identity, recovery from map failure versus location failure, accessible labels and targets, and large-text behavior. Source links and qualifications are included in interface.md. The 24 pt clearance, 10-second timeout, search algorithm, and session-only user-location retention are application choices, not quoted Apple requirements. The Maps guide's attribution spacing is suggested guidance; this specification adopts it. Its tiny-map omission exception is recorded without using it to hide attribution.

## Worked before/after

Illustrative fixture, not supplied festival data: venue A is “River Stage” and venue B is “Garden Hall,” each with a valid stored coordinate. They are near enough to fit the festival overview.

**Before:** The person denies location and sees a blank map. Where pins render, both are identical dots; selecting River Stage moves the camera far away. Attribution is absent. The brief does not establish actual search or assistive-technology behavior.

**After:** Entry renders the festival overview without requesting location. River Stage and Garden Hall have identifiable markers, or a “2 venues” cluster when targets overlap. The person opens Show Venues, types “river,” and sees River Stage regardless of location status. Activating its row opens the matching venue detail with a map. Show on Map selects venue A by ID. If its marker is already visible, the camera stays put; otherwise it pans to A's coordinate at the current zoom. Inline details leave A visible, and attribution remains readable. Closing details leaves that camera intact. Back to the list restores the query and scroll position. An attempted location action that is denied leaves all of these finding paths available.

## Acceptance checks

These are implementation acceptance criteria, not claims of executed app tests.

| Check | Pass condition | Execution status |
|---|---|---|
| Fresh entry in each authorization state | Festival data renders without a prompt; no blank map caused by denial | Not executed |
| Pin identity and crowded/co-located fixtures | Names/selection remain distinguishable without color; count clusters expand or expose exact member list; All Venues restores full scope | Not executed |
| Selection from pin, list, search | All select the same stable ID; visible pins preserve camera; offscreen pins use stored coordinates; details do not obscure selection | Not executed |
| Attribution | Correct provider marks/legal links readable and operable in main/detail maps, with keyboard and small/large layouts; suggested padding applied | Not executed |
| Search lifecycle | Case-insensitive name query, empty query, zero results, Clear Search, Cancel, Back, and exact-result selection obey the specified state contract | Not executed |
| Location lifecycle | Prompt only on invocation; granted/approximate/denied/restricted/disabled/failure/timeout paths preserve finding; duplicate attempts suppressed; no background collection | Not executed |
| Data/service failures | Missing coordinates stay in search; missing dataset has a message; tile failure offers retry/list without blaming permission | Not executed |
| Access to complete task | On a supported Apple environment, verify meaningful names/selected states and entry-to-detail activation with VoiceOver, Switch Control, and Full Keyboard Access; list avoids precision pin targeting | Not executed |
| Geometry and reading | Measure nonoverlapping 44 × 44 pt app targets; at 200% and largest supported text sizes/Bold Text, names and actions remain available; measure contrast in light/dark and Increase Contrast | Not executed |

## Evidence and audit limits

**Passed — static document review:** inspected the supplied interface.md; explicitly read the installed root SKILL.md; searched relevant topic-index rows; read each selected family and topic procedure before its source guide. Confirmed the revised document covers all four supplied defects and carries concrete state transitions and source links. Confirmed both requested files exist after writing and checked the patch for whitespace errors.

Routes used, relative to `/tmp/hig-eval-jdjholid/.agents/skills/apple-hig/`:

- `SKILL.md` → `references/topic-index.md` searches for map/location/search/accessibility/button/privacy concepts.
- `subskills/apple-hig-technologies/SKILL.md` → `.topics/apple-hig-maps/SKILL.md` → `references/maps.md` within that family.
- `subskills/apple-hig-foundations/SKILL.md` → Privacy, Accessibility, and Typography topic procedures → their corresponding family references.
- `subskills/apple-hig-navigation-and-search/SKILL.md` → Search fields procedure → its reference.
- `subskills/apple-hig-layout-and-organization/SKILL.md` → Lists and tables procedure → its reference.
- `subskills/apple-hig-menus-and-actions/SKILL.md` → Buttons procedure → its reference.
- `subskills/apple-hig-patterns/SKILL.md` → Searching procedure → its reference, following the search-field handoff.

Each read used a separate command naming one local file. Relevant typography prose was available in the returned output; its long numerical tables were truncated and no unobserved table values were used. No web browsing or visual-media review was performed. Official links are attribution to the installed snapshot, not evidence of a fresh online check.

**Failed:** no revised-specification defect found in static review. The original four defects are supplied observations, not failures reproduced on a device.

**Not executed:** app build, SDK/API availability, GUI/device interaction, permission prompts, map service behavior, accessibility execution, contrast measurement, hit-region measurement, native rendering, or physical comfort tests. Only a short prose brief was supplied: no app source, screenshots, real coordinates, provider license details, or minimum iOS version were established. Provider legal requirements, one-time-button integration, accurate venue data, actual privacy flows, and runtime behavior remain implementation verification work. This repair delivers the requested specification, not runtime certification.
