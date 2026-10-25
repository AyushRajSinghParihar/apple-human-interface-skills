# Menu bar repair

Patched interface.md in place, replacing the original defect description with a concrete macOS menu tree, shortcut map, eligibility and target rules, draft history model, Publish lifecycle, and acceptance scenarios.

## Decisions

- Replace hamburger-only command access with the system menu bar. Restore standard App, File, Edit, View, Window, and Help roles; place Publish… in Database between View and Window. Additional existing commands must be inventoried during implementation.
- Restore Undo/Redo at the top of Edit with ⌘Z/⇧⌘Z; keep Save at ⌘S in every state. Publish has no default shortcut.
- Resolve commands using the active window, document ownership, and focused editor. Revalidate at invocation; capture document identity for asynchronous work. Never use a hidden document as fallback.
- Define Save as local draft persistence and Publish as reviewed external application. These are explicit product assumptions because the brief supplies no persistence model. Publish success starts a fresh local history baseline; Undo does not promise server reversal.
- Keep unavailable ordinary menu commands dimmed and visible. Specify keyboard routes, cancellation, and failure handling. Exact publish review and concurrency policies are product decisions, not HIG mandates.

Official article links and source-backed recommendations appear in interface.md. The local menu-bar guide's conflicting general/specialized ordering wording is acknowledged; the custom menu has an explicit task-based placement.

## Worked before/after

Before: all commands live in a custom in-window hamburger, Publish replaces Undo, Save's shortcut changes, and window commands target a hidden document. The brief does not identify actual old key bindings or backend consequences.

After: A is hidden and B is active. Editing a cell in B enables Edit > Undo Edit Cell (⌘Z). File > Save (⌘S) persists B's draft without publishing. Undo restores B's prior cell value and marks B dirty; Redo restores the edit. After saving again, Database > Publish… reviews B's identity, saved revision, and destination. Cancel makes no external change. Window > Minimize minimizes B. Selecting A in Window activates A; subsequent document commands then target A. This is a specification trace, not an executed application trace.

## Acceptance audit

| Check | Status | Evidence |
| --- | --- | --- |
| Required artifact changes | Passed | interface.md revised and result.md created; both read back |
| Four reported defects addressed | Passed, static specification audit | System menu tree, restored Undo/Redo, stable Save binding, active-window targeting |
| Edge cases specified | Passed, static specification audit | No document, empty selection, clipboard mismatch, read-only draft, multiple documents, key panel, standalone settings, asynchronous identity |
| Recovery specified | Passed, static specification audit | Undo/redo branch and offscreen reveal, save cancellation/failure, publish cancellation/failure/unknown outcome, close cancellation |
| Runtime dispatch, persistence, clipboard, and publishing | Not executed | No app implementation or backend supplied |
| Native rendering, keyboard access, Full Keyboard Access, VoiceOver, localization, and window behavior | Not executed | Requires macOS application execution; concrete scenarios are in interface.md |
| SDK compilation and automated application tests | Not executed | No application source or SDK evaluated |

No executed runtime checks failed because none were run. The original brief fails the four stated design expectations; the revision passes only static specification inspection.

## Evidence limits and instruction route

Explicitly read the installed apple-hig root SKILL.md, searched its complete topic index, and read the menus-and-actions family and menu-bar/menus procedures before their source guides. Also read the inputs family and Keyboards procedure, patterns family and Undo and redo procedure, presentation family and Windows procedure, and Edit menus procedure before their respective source guides. Each file read used a separate cat command against the installed package under .agents/skills/apple-hig; the topic-index search used rg.

Only supplied local files and installed instructions were used. No web browsing, device interaction, GUI, accessibility execution, SDK compilation, or backend verification occurred. Official links are citations from the local snapshot, not fresh online verification. The brief provides no app name, framework, full command inventory, implementation, or accessibility tree. Unknown hamburger capabilities have not been claimed as migrated. The revised document is the requested specification artifact; runtime implementation remains outside the available evidence.
