# Contextual-action repair

Patched `interface.md` in place from a one-paragraph problem statement into an implementable action contract for macOS and iPadOS. Rename and Delete now have explicit targets, availability, alternate routes, outcomes and recovery.

## Decisions

- Replace the all-command right-click menu with relevant Rename… and Delete actions. Empty-space invocation offers no file actions.
- Preserve multi-selection when invoking on a selected entry; invoking on an unselected entry selects that entry alone. Commands capture identities and revalidate before execution.
- Make Rename discoverable through the Mac File menu and an iPad in-app Actions menu. Delete also has a Mac Edit-menu route.
- Resolve the availability ambiguity by surface: hide unavailable contextual actions; retain dimmed ordinary-menu commands. Preserve the documented Mac Cut/Copy/Paste exception if those commands are introduced.
- Delete the whole eligible selection atomically, with one Undo unit. Mixed eligibility disables the entire batch. Specify recovery before enabling deletion.

Source-backed recommendations and official article links are recorded in `interface.md`. Product choices include exact selection transitions, single-item-only Rename, count labels, atomic deletion and session history boundaries. The supplied text does not establish archive-engine capabilities.

## Worked before/after

Given writable entries `A.txt`, `B.txt`, and `C.txt`, select A and B, then secondary-click B.

Before: all app commands appear, including unrelated commands; Rename is only in that hidden menu. Choosing Delete affects B alone because it was last clicked. Unavailable choices disappear without a stated rule.

After: A and B stay selected. The contextual menu has scope “2 Selected Items” and offers Delete 2 Items. Rename is absent because this repair supports only single-entry rename. Delete removes A and B in one atomic operation; C remains. Edit > Undo Delete restores A and B and reveals the restored selection. File > Rename… remains visible but dimmed for the two-item selection. Selecting A alone enables Rename… there without any contextual-menu gesture. A read-only archive hides both contextual actions while keeping their ordinary-menu alternatives dimmed.

## Acceptance checks

Static specification inspection — passed:

- The patch addresses each supplied defect and retains both stated platforms.
- Menu tree, empty/single/multiple selection, mixed eligibility, read-only and pending states have deterministic rules.
- Every specified contextual action has a Mac main-menu route and an iPad in-app route.
- Batch scope, stale targets, cancellation, failure, undo/redo and focus after deletion are specified.
- Unavailable ordinary and contextual commands have distinct rules; no unsupported blanket rule to hide or dim every menu type is asserted.

Runtime acceptance — not executed; implementers must verify:

1. Run the A/B/C example, Undo, Redo, then Undo and a new edit; confirm the redo branch clears and restored content and metadata match.
2. Invoke on an unselected C, selected B and empty space; verify singleton, preserved batch and no file-action menu respectively. Change archive revision while a menu is open; verify no stale operation executes.
3. Test zero, one and many selections, mixed protected/writable entries, unsupported formats and pending edits. Ordinary menus retain dimmed commands; contextual menus omit unavailable actions and never show an empty separator/menu.
4. Cancel Rename, submit a collision and invalid name, then complete a valid rename. Confirm no changes on cancellation/error and identity/selection preservation on success.
5. Inject a batch write failure; confirm no partial deletion. Verify recovery data, directory overlap normalization, save/history boundaries and no deletion of external source files.
6. Compare equivalent entries and menu placement near upper/lower window edges. Check native menu size, scanning order, count labels, localization and keyboard navigation. With no archive and with multiple windows, verify active-window targeting and disabled commands.
7. On iPad, exercise touch-and-hold, pointer invocation, selection mode and Actions access without a keyboard or visible menu bar. On Mac, exercise Control-click, secondary-click and main-menu operation with context menus unused.
8. Verify focus after deletion and visible offscreen restoration; test assistive-technology names, scope and command reachability in an actual implementation.

Failed checks: none observed in the static revised specification. Runtime checks have no pass/fail evidence.

## Evidence and limits

Read the installed apple-hig root SKILL.md explicitly, searched its complete topic index, then read the Menus and actions family and the Context menus, Menus and The menu bar procedures before their source guides. For deletion recovery, read the Patterns family, Undo and redo procedure, then its guide. Each read used a separate single-file command. All paths resolved within `.agents/skills/apple-hig`; no web browsing was used.

The only supplied product evidence was the original `interface.md` paragraph. This work changes a specification, not executable application code. No device, SDK build, GUI, keyboard, archive-engine or accessibility execution occurred. Local source guides identify a 2026-10-25 snapshot; their presence does not establish independent review or current API availability. Official URLs are attribution from those local files, not pages fetched during this task.
