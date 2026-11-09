# Command organization repair

Patched interface.md in place, replacing the one-sentence faulty behavior with a concrete macOS command tree, shortcut map, eligibility contract, pending-state transitions, and irreversible-action flow.

## Decisions

- Fixed positions and scope-based grouping replace movement after use. Open… belongs in File; proposed database operations live in Database, with Drop Table… separated from Refresh.
- Text-only proposed groups replace mandatory icons. Only meaningful imagery should be added, consistently within its group.
- ⌘O and ⌘W retain familiar meanings; Refresh and Drop Table… have no assigned shortcut. Every command need not have a shortcut.
- Unavailable commands remain visible and dimmed, and their parent remains openable. One validation/dispatch contract blocks execution through every route, including stale keyboard events.
- Drop Table… receives explicit target-specific confirmation and no default button, with safe cancellation. Completed external destruction is never advertised as undoable.

The official article/section links supporting these decisions are included in interface.md. They were taken from local references; no web content was fetched. The menu-bar reference notes conflicting general/specialized ordering wording: the specification uses concrete task scope (File, then Database between View and Window), rather than asserting an absolute custom-menu hierarchy rule.

## Worked before/after

Illustrative fixture: a window displays the read-only database `Analytics`, with table `events` selected. The proposed Drop Table command represents the brief's otherwise unnamed destructive actions.

Before, as described by the supplied brief: using Open changes command positions; every command has an icon and shortcut; unrelated destruction is adjacent to Open; unavailable actions disappear yet their keyboard equivalents still execute.

After: File > Open… remains in the same position after repeated uses. Database > Refresh remains above a separator and Drop Table…. Drop Table… is visible but dimmed because Analytics is read-only. A stale shortcut event or alternate invocation cannot drop events. When the connection becomes writable and all other predicates pass, Drop Table… becomes enabled in the same position. Choosing it names Analytics and events in confirmation; Escape cancels without mutation. Confirmation revalidates the captured identity rather than dropping whichever table is selected later.

## Acceptance checks and status

Passed — static specification inspection:

- interface.md contains fixed menu placement, separators, labels, shortcuts, scope, eligibility, and outcomes for every proposed command.
- No proposed item requires an icon; shortcuts are selective and ordinary unavailable items stay discoverable.
- All routes share validation, including invocation-time checks and per-window targeting.
- Destruction defines confirmation copy, roles, Return behavior, cancellation, pending, success, failure, uncertain outcome, and recovery limits.

Failed — supplied starting specification only: command position stability, selective icons/bindings, related grouping, visible unavailable commands, and disabled-command execution parity are explicitly contradicted by its text. No runtime failure was observed.

Not executed — implementation acceptance scenarios:

1. Repeat Open/Refresh and compare menu positions; cancel Open and verify unchanged work. Open Database with every child disabled.
2. Exercise no window, empty/multiple selection, read-only, disconnected, permission denied, busy, and unresolved-edit states. Attempt every available invocation route; assert zero side effects when disabled.
3. Change eligibility while a menu is open, then invoke. Repeat with two windows and different selections; assert correct target and no stale dispatch.
4. Run Refresh twice rapidly; assert one operation, correct pending enablement, stable selection on success, and useful failure feedback.
5. Cancel Drop Table using its button, Escape, and ⌘Period; test Return alone, then explicit confirmation. Change/remove the captured target before confirmation; assert no retargeting. Exercise backend failure and uncertain outcome without automatic retry.
6. On the Mac, verify native menu keyboard navigation and Full Keyboard Access can complete opening, refresh, and cancellation without a pointer. Check localized long names, international keyboard layouts, and assistive navigation. No submenus or toggles are introduced; all-disabled-parent behavior remains applicable.

## Evidence limits

Inputs were the supplied interface.md and installed skill instructions/references only. The installed root SKILL.md was explicitly read, followed by the Menus and actions family, Menus and The menu bar topic procedures, and their guides; the topic index was searched before finalizing routing. Keyboards was read through Inputs; Alerts through Presentation; Undo and redo through Patterns, each family and topic before its source guide.

No source code, full command inventory, engine, window model, or existing recovery implementation was supplied. Open-as-local-file, Refresh, and Drop Table are explicit proposed assumptions, requiring mapping to actual supported capabilities during implementation. No device, SDK compilation, GUI, keyboard, accessibility, backend, or native rendering execution occurred. Static review establishes a revised design contract, not working application behavior or current external-source verification.
