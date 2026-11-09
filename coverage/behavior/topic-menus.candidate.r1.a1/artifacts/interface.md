# Mac database utility: command specification

Platform: macOS. This specification replaces usage-based command movement, mandatory icons/shortcuts, destructive actions beside Open, and disappearing unavailable commands whose keyboard equivalents still execute.

## Scope and command organization

Use the macOS menu bar as the discoverable command catalog. Preserve the system Apple menu and standard app, File, Edit, View, Window, Help ordering. Place the custom Database menu between View and Window. Keep supported existing standard commands in their conventional groups and order; do not add unsupported capabilities simply to fill menus.

The original brief supplies no command inventory or database engine. The following is the concrete proposed minimum command set: Open opens a local database file; Refresh reloads the active database's object list; Drop Table permanently removes one selected table. These are design assumptions, not observations of existing functionality. Map any additional existing commands by scope before implementation, preserving all capabilities.

| Menu / ordered group | Command | Shortcut | Scope and eligibility | Outcome |
| --- | --- | --- | --- | --- |
| File / opening | Open… | ⌘O | App; enabled unless another modal operation blocks opening | Request a file, then open its database in a window. Cancel preserves all current work. |
| File / closing, separated from opening | Close | ⌘W | Active database window exists and can close | Close that window using the existing unsaved-work policy. Never repurpose this shortcut for destruction. |
| Database / ordinary operations | Refresh | None | Active database is connected and idle | Reload object metadata without modifying stored data; retain selection by object identity when it still exists. |
| Database / destructive operations, after a separator | Drop Table… | None | Exactly one table selected in the active window; connected, writable, permission to drop, idle, no unresolved local edits | Request confirmation for the captured table, then permanently drop only that table. |

App-wide Settings… stays in the app menu with ⌘Comma if supported; editing commands remain in Edit with their standard meanings. Undo/Redo, where supported, stay at the top of Edit with ⌘Z/⇧⌘Z and target-specific labels. Window retains supported Minimize and Zoom behavior; Help stays last. No Format menu is needed without rich-text formatting. Do not claim Undo can restore a committed Drop Table.

## Stable presentation

- Keep menu titles, command positions, groups, and separators fixed across use, selection, window changes, and eligibility changes. Do not reorder by frequency or recency. This specification introduces no recent-items list.
- Keep unavailable ordinary menu commands visible and dimmed. Keep Database openable even when all its commands are disabled. Opening the menu must never execute a command.
- Use short predictive labels. Open… requires a file choice and Drop Table… requires confirmation; Refresh acts immediately. Use real, shallow submenus only if the inventory later warrants them.
- Use text-only items for the proposed command groups. Remove decorative icons; no icon is required per item. If a future group gains meaningful icons, use them consistently throughout that logical group. Retain system-provided standard imagery where applicable.
- Assign shortcuts selectively to frequent actions, preserving standard meanings. Do not manufacture a shortcut for every item or derive Drop Table from an Open shortcut with extra modifiers. Any later custom shortcut requires conflict and international-layout review and appears beside its menu item.

## Shared availability and dispatch

Each command has one identity and one eligibility predicate shared by menu validation, keyboard dispatch, and any existing alternate surfaces. Resolve the active window and selection at invocation; never use another window's stale selection. Recheck eligibility immediately before side effects. A disabled command invoked through any route performs no mutation and launches no operation; retain focus and report the current reason in the window's status area if explicitly invoked. Menu inspection alone needs no interruption.

Transitions: connected/idle → Refresh pending disables Refresh and Drop Table in that window → success refreshes metadata and restores eligibility; failure preserves data, reports the failure in context, and restores eligibility according to the current connection state. Pending actions cannot be duplicated by repeated activation. Other eligible windows retain their own command state.

No window, empty selection, multiple selection, disconnected, read-only, insufficient permission, pending operation, or unresolved local edits each disable Drop Table. A table selection change updates validation without changing menu order. A keyboard equivalent must never bypass any predicate, including one changed while a menu was open.

## Irreversible action contract

Drop Table… captures database identity, table identity, and displayed names before showing one confirmation. Title: `Drop Table “{table}”?` Message: `This permanently removes “{table}” and all its rows from “{database}”. This cannot be undone.` Buttons: Cancel (leading), Drop Table (trailing, explicit destructive outcome). Use no default button so Return alone does not commit; Escape and ⌘Period cancel. This deliberate-reading choice is a product decision, not a universal rule requiring all destructive confirmations to lack a default.

Cancel changes no data and restores focus to the initiating selection. Confirm revalidates the captured target, connection, permissions, edits, and busy state; never silently retarget after selection or window changes. If validation fails, dismiss without execution and explain why in the originating window. While executing, block duplicate submissions. On success, remove the table from the object list and clear its selection; on failure, retain the displayed object until a refresh establishes server state and report the error. An uncertain server outcome must be described as uncertain and reconciled before retry. No cosmetic UI restoration is presented as database Undo.

## Design basis

These choices apply the installed local HIG snapshot: stable scope-based menu organization and visible disabled items ([The menu bar](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Best-practices)); related groups, meaningful icons, and predictive labels ([Menus](https://developer.apple.com/design/human-interface-guidelines/menus#Organization), [Icons](https://developer.apple.com/design/human-interface-guidelines/menus#Icons), [Labels](https://developer.apple.com/design/human-interface-guidelines/menus#Labels)); selective familiar bindings ([Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards#Custom-keyboard-shortcuts)); consequential confirmation and cancellation ([Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons)); honest recovery ([Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#Platform-considerations)). Shared dispatch validation and the exact database commands/state predicates are concrete engineering/design decisions derived from the supplied failure, not quoted Apple API requirements.
