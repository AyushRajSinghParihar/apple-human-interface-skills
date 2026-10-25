# Recipe planner: adaptive iPhone Duo specification

Platform: source-described iPhone Duo. This is a design contract based on installed local guidance; hardware and implementation SDK remain unverified. No framework is prescribed.

## Task and hierarchy

Browse recipes, read a selected recipe, and add it to a chosen meal day. Use one recipe-list → recipe-detail hierarchy. Detail contains ingredients, instructions, and a meal-day draft. Add to Plan commits that draft once; configuration changes never commit it. With no selection, compact shows the list; expanded detail says “Choose a recipe.”

Prefer an adaptable standard split container: regular width exposes list and selected detail together; compact width collapses to the active route. Do not stretch the compact screen. An arrangement is unnecessary for this parent/detail relationship. If later used to reposition supporting content inside detail, keep navigation split/tab structures outside it; arrangements do not navigate. [Duo: Split views and Arrangement views](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Split-views), [Split views](https://developer.apple.com/design/human-interface-guidelines/split-views#iOS).

## Layout and transitions

Choose presentation using available size classes, safe areas, margins, and reserved regions. Pose names below identify scenarios, not breakpoints. Do not invent panel dimensions, hinge angles, or camera insets. Retain ordinary iPhone conventions. [Duo: Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Best-practices), [Layout: Size classes](https://developer.apple.com/design/human-interface-guidelines/layout#Size-classes).

| Environment | Layout | Transition outcome |
| --- | --- | --- |
| Closed outer display, compact width | List or selected detail, with Back to Recipes on detail; system vertical bars. | Closing preserves active detail and reading position. Back restores list position with selection retained. |
| Open inner display, regular width | Coordinated recipe list and detail columns, readable margins. | Opening reveals the list beside the same recipe; no selection or draft reset. |
| Inner portrait | Same hierarchy with ordinary system horizontal bars; available space determines pane exposure. | Rotation changes presentation only. |
| Partial fold: book-like, surface-supported, or edge-standing | Standard split adaptation around center reserved space; collapse to active pane if available width becomes compact. | Make modest continuous adjustments; no pose-specific screens or abrupt action relocation. |
| Intermediate/narrow Split View or reduced usable area | Apply the same expanded/collapsed contract; provide Back when list is hidden. | Preserve state in both resize directions. |

Separate full-width background decoration from inset scrolling content. Required recipe text and actionable regions must clear the permanent outer camera region, its growth for Live Activities, the inner camera region while active, and the center folding region. Recompute when these change. Prefer standard adaptable containers; custom content must consume reserved-region information as well as safe areas. Screen bounds alone do not describe usable content space. [Duo: Reserved regions](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Reserved-regions), [Layout: Guides and safe areas](https://developer.apple.com/design/human-interface-guidelines/layout#Guides-and-safe-areas).

## State ownership

Keep state outside pane instances: selected recipe ID, active list/detail route, list scroll anchor, recipe-specific detail section/scroll anchor, meal-day draft, and in-progress draft values. Use stable recipe identity. Opening, closing, rotation, resizing, and camera changes only alter presentation. Restore logical reading anchors after reflow rather than raw pixel offsets.

Changing recipe intentionally updates detail; retain previous recipe drafts keyed by recipe ID. Add to Plan requires a selected recipe and valid day, prevents repeated activation during commit, and confirms the recipe and day after success. Failure preserves the draft for retry. Back navigates to the list without discarding drafts. These are product decisions implementing the source’s state-preservation requirement. [Duo: Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Best-practices).

## Controls and compression

The planner is navigation-led. Preserve access to the recipe hierarchy while secondary tools overflow. Do not add tabs merely to fill space; if an implementation already has top-level destinations, keep them available during compression.

| Group, highest retention first | Scope | Compression and placement |
| --- | --- | --- |
| Navigation: Back to Recipes | Return from collapsed detail; unnecessary while list is visible. | Preserve route; Back is first toward the top in vertical bars. |
| Primary: Add to Plan | Commit current recipe/day. | Highest action priority, after navigation in vertical order; retain before secondary tools. |
| Local: Meal day | Edit current recipe draft beside its planning summary. | Stay near affected detail pane and reachable through scrolling, not at a distant global edge. |
| Secondary: Share Recipe | Share selected recipe. | Lowest action priority; moves into system overflow first. |

Use system toolbar groups and spacing; keep navigation, primary, and secondary groups distinct. Supply meaningful titles and symbols for Add to Plan and Share Recipe so expansion and overflow remain understandable. Use standard Back semantics. Reserve ellipsis for the single system overflow; no duplicate custom More menu. Every available action needs a reachable labeled route even at extreme compression.

Preserve system vertical bars on the outer display and landscape inner display; inner portrait uses horizontal bars. Keep relative action placement stable. Respect asymmetric safe areas in multitasking on either side: each app uses its outer edge. Hardware-side controls stay on their physical side in RTL; reading-order Back and content alignment adapt through system directionality. Preserve recipe photographs and internal digit order. [Duo: Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls), [Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars#Actions), [Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left#Controls).

## Acceptance scenarios

1. With a selected recipe, scrolled instructions, and uncommitted meal day, exercise closed → open → partial fold → closed, then rotation in both directions. Require identical recipe ID, active route, logical reading anchor, and draft; zero plan writes from transitions. Repeat with no selection and after explicitly returning to the list.
2. Exercise smallest, largest, and intermediate usable areas, outer camera expansion, inner camera activation/deactivation, and multitasking on either side in LTR and RTL. Required content and hit regions must clear reserved space. Verify Back, Add to Plan, Meal day, and Share remain operable, including overflow, with specified priority and no duplicate overflow.
3. Commit once and simulate failure/retry: success names the correct recipe/day; failure retains draft. Back restores prior list position and selected appearance.
4. Confirm physical reachability, native bar placement, and reserved-region adaptation with supported previews/device execution. These checks remain unexecuted until actual evidence exists; this document alone does not establish runtime or accessibility behavior.
