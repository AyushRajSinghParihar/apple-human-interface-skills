# Navigation repair result

Patched interface.md in place with a concrete iPhone destination, command and restoration contract.

## Decisions and patch summary

| Supplied behavior | Revised specification |
|---|---|
| Share/Delete are tabs | Collections and Visit are destinations; Share is a contextual toolbar action and Delete Collection is a detail button |
| Tabs disappear while loading | Tabs stay visible and enabled; loading, empty and failure states live inside destinations |
| Usage changes order | Fixed logical order: Collections, Visit |
| Selection uses only color | Label, icon, non-color selection shape and semantic selected state |
| Returning resets Collections | Independent navigation paths, selected IDs and scroll anchors/offsets |

Stable destinations and restoration follow [Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars#Best-practices); command separation and hierarchy follow [Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars). Action roles/targets follow [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons); redundant selection cues follow [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility).

Visit, its contents, user-created collection ownership and irreversible deletion are explicit design assumptions because the brief supplies no complete destination inventory or data model. They are not observed app features or Apple requirements. The patch also specifies stale-data fallback, late responses, modal return and deletion pending/failure behavior. Its no-default confirmation is a product choice: [Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts) permits explicitly requested destructive confirmations to have a normal default. The iPad five-default-tab advice was not treated as an iPhone limit.

## Worked before/after

Before: A visitor scrolls Collections and opens an object. During loading, tabs disappear. After navigating elsewhere, usage changes their order; returning to Collections resets scroll/selection. Share and Delete occupy destination positions, and only color shows selection.

After: The visitor opens an object from a saved list anchor, switches to Visit while its information loads, then taps Collections in its unchanged first position. The object detail and list context return. Share acts on that object; cancelling sharing leaves the same detail visible. Back returns to the saved list anchor. A selection shape identifies Collections in grayscale. This is a specified walkthrough, not an executed app demonstration.

## Acceptance checks and status

Passed — static inspection of the revised document:

- All five supplied defects have explicit replacements.
- Both destinations have content, retained-state and unavailable-content contracts.
- Commands are separate from tabs; narrow-width access, modal return and destructive cancellation are defined.
- Acceptance cases cover round trips, tab reselection, loading/empty/error/offline, late responses, stale IDs, deletion, localization and non-color selection.

Failed — no unresolved specification check found in this static review. This does not establish that an implementation passes.

Not executed — every runtime acceptance case in interface.md: asynchronous restoration, native presentation, modal focus return, keyboard/default handling, measured target geometry/contrast, 200% text layout, localization, VoiceOver and other assistive input. No app source, device, simulator, GUI or SDK execution evidence was supplied or produced. These remain implementation acceptance work.

## Evidence and limits

Explicitly read the installed `.agents/skills/apple-hig/SKILL.md`, inspected interface.md and searched the installed topic index. Followed these package-relative routes, reading each procedure before its supporting guide:

- Navigation and search family → Tab bars procedure → tab-bars.md.
- Menus and actions family → Toolbars and Buttons procedures → toolbars.md and buttons.md.
- Foundations family → Accessibility procedure → accessibility.md.
- Presentation family → Alerts procedure → alerts.md.

Only supplied local files and installed instructions/references were used. Official URLs above are attribution links from local references, not visited pages. The references are independent guidance derived from a dated English HIG snapshot (2026-10-25); their presence does not establish independent review or current SDK availability. No screenshots, rendered color/geometry measurements or deployment target were available. This deliverable repairs the specification; it does not claim an implemented app or accessibility conformance.
