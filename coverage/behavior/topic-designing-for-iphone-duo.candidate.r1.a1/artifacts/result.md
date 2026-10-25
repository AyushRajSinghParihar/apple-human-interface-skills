# Recipe planner adaptation result

Patched `interface.md` in place. Replaced the stretch-only proposal with list/detail transitions, persistent recipe and draft ownership, reserved-region handling, system bar placement, action priorities, and acceptance scenarios. This is a revised specification, not running application code.

## Decisions

- Expand the existing recipe hierarchy at regular width and collapse to the active route at compact width. Use a split container rather than an arrangement for navigation. [Duo: Best practices and split views](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Best-practices).
- Use environmental sizing and reserved regions, covering outer camera expansion, active inner camera, center fold, and asymmetric multitasking. Pose names are scenarios, not fixed breakpoints. [Duo: Reserved regions](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Reserved-regions), [Layout](https://developer.apple.com/design/human-interface-guidelines/layout#Size-classes).
- Preserve system bar placement and physical hardware alignment in RTL. Prioritize navigation and Add to Plan, keep Meal day local, and overflow Share first. [Duo: Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls), [Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars#Item-groupings).

Recipe-specific draft keys, logical reading anchors, the command inventory, and commit/retry behavior are concrete product decisions applying this guidance. The original brief did not specify these details. No hardware measurements or SDK availability claims are introduced.

## Worked before/after

Fixture: Lentil Soup selected, instructions at step 4, Friday an uncommitted meal-day draft.

Before: the supplied proposal stretches the compact screen, loses the recipe on configuration changes, and leaves essential controls outside reach. No executable reproduction was supplied.

After, as specified: closed shows Lentil Soup at step 4. Opening reveals the list with Lentil Soup selected beside the same detail and Friday draft. Partial folding reflows around reserved space without changing selection or writing a plan entry. Closing returns to the same logical reading anchor. Back restores list position. Intentional Add to Plan commits Lentil Soup to Friday once. This is a worked design outcome, not observed runtime evidence.

## Acceptance audit

| Check | Status and evidence |
| --- | --- |
| Required in-place patch and result file | Passed: both files written and inspected locally. |
| Closed/open/partial/portrait/intermediate transition contracts | Passed at specification level: explicit layout and state outcomes. |
| Navigation versus arrangement, camera/fold avoidance, control priorities, RTL hardware exception | Passed at specification level: explicit decisions and source links. |
| Original proposal meets adaptation needs | Failed at supplied-description level: original explicitly reports stretched layout, lost selection, and unreachable controls; no independent device observation. |
| State restoration, plan writes, overflow access, camera/fold geometry | Not executed: no application, test harness, SDK, or supported preview supplied. Execute the scenarios in `interface.md` when available. |
| Physical reachability, native rendering, accessibility, actual pose transitions | Not executed: no GUI, device, or assistive-technology execution performed. |

## Evidence limits and routing

Only supplied local files and installed instructions were used; no web access occurred. Official links identify articles/sections named in local snapshots and were not visited. The local Duo guide reports retrieval 2026-10-25 and source revision September 9, 2026. This is source-described behavior, not independent confirmation of a product, shipping platform, API, or SDK.

Auditable route: installed apple-hig root SKILL.md → supplied interface.md → Getting started family → topic-index searches → Duo topic procedure → Duo source guide. Additional routes read Foundations, Layout and organization, and Menus and actions families, then Layout, Split views, and Toolbars procedures before their respective source guides. Right to left procedure was read before its guide to resolve hardware alignment versus reading direction. All installed paths were resolved under `.agents/skills/apple-hig/`; each read command consumed one file. No media demonstration was needed or reviewed. No conflicting passages were identified in the guidance read.
