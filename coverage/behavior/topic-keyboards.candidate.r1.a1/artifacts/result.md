# Keyboard workflow decisions

Patched interface.md in place, replacing the five-failure brief with an implementable command inventory, input dispatch rules, focus groups, search states, cancellation precedence, and compact/wide toolbar behavior. The baseline toolbar and title/body model are explicit design choices because the supplied file provides no screens, command names, framework, or code.

The central decisions are:

- Restore familiar editing meanings, particularly Command-C; let composition and system shortcuts retain priority. Command-F and Command-N supply direct routes to search and creation. Frequent existing toolbar commands still need an actual inventory. Source: [Keyboards — standard and custom shortcuts](https://developer.apple.com/design/human-interface-guidelines/keyboards#Standard-keyboard-shortcuts).
- Tab visits meaningful content groups and arrows navigate results without activation. Selected note and focused result remain different states. Full Keyboard Access separately covers all controls; ordinary content focus cannot prove that coverage. Sources: [Focus and selection — iPadOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#iPadOS), [Keyboards — best practices](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices).
- Escape and Command-Period cancel transient work and never delete notes. Search submission uses one handler for hardware Return and both visible/software Search actions. Explicit submission is a product choice: the guide prefers live updates where feasible, but the supplied evidence establishes no latency or search implementation. Sources: [Keyboards — standard shortcuts](https://developer.apple.com/design/human-interface-guidelines/keyboards#Standard-keyboard-shortcuts), [Search fields — best practices](https://developer.apple.com/design/human-interface-guidelines/search-fields#Best-practices).
- Label app-wide search scope, preserve query/result identity across detail and resizing, and retain essential routes as toolbar width shrinks. Sources: [Search fields — iPadOS and macOS](https://developer.apple.com/design/human-interface-guidelines/search-fields#iPadOS-macOS), [Searching — best practices](https://developer.apple.com/design/human-interface-guidelines/searching#Best-practices), [Toolbars — item groupings](https://developer.apple.com/design/human-interface-guidelines/toolbars#Item-groupings).

These links identify official sources cited by the installed local guidance; no linked pages were fetched. App-specific choices such as exact group order, submission focus, query restoration, and the proposed toolbar inventory are requirements of this revision, not claimed universal Apple mandates.

## Worked before/after

Task: find “Planning”, copy a decision into that meeting's note, and return to results.

Before, as reported by the supplied brief: the hardware keyboard cannot submit search; Tab cycles through decoration; the editor consumes Command-C; toolbar commands offer no shortcuts; Escape deletes the current note. The workflow requires another input method and risks note loss.

After, as specified (not executed): select text in the current note and press Command-C. Press Command-F, type “Planning”, and press hardware Return. Tab enters results; Down moves focus without opening another note. Return opens the chosen meeting and restores its caret. Command-V pastes the copied decision; Return adds a paragraph. Tab exits the editor without trapping focus. Escape with no transient UI leaves the note intact. With FKA enabled, navigate to Back to Results and activate it using the configured system activation key; the same query and opened row return. Reopen the note and confirm the edit remains. To abandon search instead, Escape while search is active restores its originating caret without deleting text.

## Acceptance checks and status

Passed — static specification review only:

- All five reported failures have concrete replacements in interface.md.
- Command inventory covers editing, creation, search, activation, and cancellation, with scopes and availability.
- Ordinary content navigation and FKA are specified separately; decorations are excluded.
- Empty, failure, stale response, clear, cancel, resize, and return states are specified.

Failed — supplied baseline behavior (reported in interface.md, not reproduced): copy interception, decorative Tab loop, missing toolbar shortcuts, destructive Escape, software-only search submission.

Not executed — implementation acceptance checks:

| Check | Required observable result |
| --- | --- |
| Copy/cut/paste/select all in title, query, and body | Correct focused-input scope; clipboard survives Copy with no selection; no unrelated app action. |
| Undo/redo and selection arrows | Expected editing results, with history retained through search/return; disabled history commands do nothing. |
| Ordinary Tab and reverse Tab | Search → Results → Note → Search, reverse traversal, empty-group skipping; arrows stay native in editor; no decoration trap. |
| Focus versus selection | Arrow through results without changing open note; Return opens exact focused identity; selected styling persists when focus leaves. |
| Search submission with software keyboard hidden | Hardware Return produces the same results as visible/software Search; empty query shows all notes. |
| Search edges | No-match and error paths keep query editable; retry works; stale responses cannot replace current results; Clear and Cancel follow their distinct contracts. |
| Safe Escape and Command-Period | Composition/menu/rename/search cancellation occurs in precedence order; ordinary editor Escape preserves note and edits. |
| FKA traversal and activation | All named controls, including Rename, Back, Retry, Clear, and overflow, reachable and exitable using system commands; no app interception. |
| Command discovery and availability | Meaningful titles, correct shortcuts, supported hold-Command display, no stale-note action; reconcile all actual toolbar commands. |
| Wide/compact and dynamic changes | Focus/caret and query survive resize; essential actions remain accessible; row removal and overflow restoration follow the contract. |
| International layout and input method | Character entry, composition Return/Escape, system switching, accessibility shortcuts, and app shortcuts coexist. |
| Full task and persistence | Complete the worked task without pointer/software keyboard; reopen note and verify edit; persistence failure retains the draft visibly. |

## Evidence limits

Read the installed root SKILL.md explicitly, then routed families and topic procedures before their source guides. Routes used: Inputs → Keyboards and Focus and selection; Menus and actions → Toolbars; Patterns → Searching; Navigation and search → Search fields. Searched the installed topic index for keyboard, focus, iPad, shortcuts, search, and toolbar concepts. All reads used one file per shell command.

Only the supplied one-line interface brief and installed local instructions/guides support this work. No app implementation, SDK documentation, build, device, GUI, clipboard, focus engine, FKA, VoiceOver, physical keyboard, localization, search corpus, or persistence execution was available or performed. The checklist defines future acceptance; it does not certify runtime behavior, actual shortcut availability, API support, native rendering, assistive-technology order, or physical comfort. Installed guides are a dated derivative snapshot, not proof of independent source review. No web browsing or software installation occurred.
