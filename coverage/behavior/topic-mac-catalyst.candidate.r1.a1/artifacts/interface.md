# Recipe editor — Mac Catalyst specification

## Scope and baseline

Keep the existing iPad recipe editor and recipe data model, adapting its Catalyst presentation for macOS. The supplied baseline assumes fullscreen touch, puts app commands behind long press, uses a floating software keyboard, breaks at narrow widths, and needs multiple recipes open. No native build is supplied. The behaviors below are implementation requirements, not verified runtime results. Existing recipe fields and operations remain available; field names in examples are illustrative because no schema or command inventory was supplied.

## Platform and sizing decision

Use the Mac idiom for the Catalyst target, with semantic text styles and reviewed Mac image assets. Review every fixed metric rather than multiplying the existing layout. The local Catalyst guide describes default iPad idiom scaling at 77% and Mac idiom at 100%; choosing Mac idiom does not establish that the existing layout works unchanged. Confirm SDK support before implementation. Recipe text editing has no demonstrated dependency on unavailable iPad hardware; audit actual dependencies before declaring the port feasible.

Use normal system window frames, title bars, movement, resize, minimize, zoom, close, and optional full screen. Never require full screen. Title each editor with its recipe name; distinguish unnamed recipes with a stable temporary number.

Proposed product dimensions, in Mac-idiom layout points, pending Mac validation:

- Initial content area: 1000 × 720; minimum: 560 × 400. Permit enlargement without an arbitrary maximum.
- At content width 900 or greater, arrange the existing editor's related sections in two columns, with preparation content beside recipe details where present. Maintain logical reading order.
- Below 900, stack those same sections in one vertical scrolling editor. At either width, stack rows further when text or translated labels need more room. No horizontal scrolling for ordinary text editing.
- Keep the top toolbar and content clear of system window controls. Wrap labels, grow editable content, and scroll focused fields into view. Preserve recipe ID, draft, selection/insertion range, undo history, and a scroll anchor through reflow; retain the focused field even when its coordinates change.
- Essential actions live in the top/menu area, never solely at the bottom. A short window scrolls content rather than clipping completion controls.

## Window and persistence contract

One editor window owns one recipe ID and its draft. File > Open Recipe… invokes the existing recipe selection flow adapted to mouse and keyboard. Selecting a different recipe opens its own window without replacing the current editor; selecting an already-open recipe raises its existing window. Canceling selection changes nothing. File > New Recipe creates a distinct untitled recipe/window. Avoid duplicate editable windows for the same ID.

Windows retain independent focus, insertion range, scroll position and undo stacks. Commands resolve against the active editor, not the last recipe selected globally. Standard text commands resolve to the focused text responder. Switching apps or windows does not save over another recipe or discard work; preserve standard active/inactive cues.

Save explicitly and autosave drafts after edits using the existing persistence system. A draft is allowed to be incomplete. Track clean, dirty, saving, and save-failed states per recipe; mark clean only when the current revision is persisted. If edits arrive during a save, keep the later revision dirty and save it next. On failure, retain the draft and show an inline message with Retry through File > Save. Closing or quitting must finish persistence before dismissing dirty windows; a failure keeps the affected editor open and focused, with its draft intact. Closing one editor leaves others open. Reopening restores persisted draft content; relaunch restores previously open recipe IDs and saved window context where supported. Do not promise crash recovery for edits that were never persisted.

## Discoverable commands

All existing commands currently available through long press must receive a visible menu-bar route before release. Audit their actual labels, scopes and availability; the brief does not enumerate them. Long press may remain an accelerator on iPad but is never required on Mac. Contextual secondary-click actions may duplicate the same commands; they must not become their sole route.

| Menu | Required command and shortcut | Scope / availability |
| --- | --- | --- |
| App | Retain supported standard About, Services, Hide/Show and Quit (⌘Q) behavior | App-wide; Quit follows persistence contract |
| File | New Recipe (⌘N) | Creates recipe/window; available without an editor |
| File | Open Recipe… (⌘O) | Requests recipe selection; available without an editor |
| File | Close Window (⌘W), Save (⌘S) | Active editor; Save enabled for unsaved work or retry, disabled while the same revision is saving |
| Edit | Undo (⌘Z), Redo (⇧⌘Z), Cut/Copy/Paste, Select All | Standard responder semantics; dim unavailable actions; name undo targets when known |
| View | Show/Hide Toolbar; Enter/Exit Full Screen | Active window; labels describe next action |
| Window | Minimize (⌘M), Zoom, Bring All to Front, named open windows | System window behavior; Zoom differs from Full Screen |
| Help | Recipe Editor Help | Explain opening, saving, recovery and keyboard workflow |

Preserve system menu ordering and shortcuts. Add Settings only if actual app settings exist; omit Format unless existing rich-text capabilities warrant it. Place other audited recipe commands by scope under File/Edit or a Recipe menu between View and Window. Leave infrequent commands without shortcuts rather than inventing conflicts. Keep unavailable commands visible and dimmed.

Top toolbar: leading New Recipe and Open Recipe; center recipe title; trailing Save. Every toolbar action invokes the same command and enablement as its menu equivalent. At narrow width, overflow New/Open before Save, using system overflow only. When hidden, menu routes remain sufficient. Do not add a second More menu. Titles may visually truncate while the full recipe name remains available for identification.

## Keyboard and pointer behavior

Remove the app-drawn floating software keyboard and any reserved blank keyboard area from the Mac target. Use standard Catalyst text input with physical keyboard, system input methods and ordinary selection/copy/paste. Do not suppress user-enabled system accessibility input. The virtual-keyboard HIG component is not defined for macOS; this is not a claim that macOS lacks assistive onscreen input.

Keyboard-only path: invoke Open Recipe…, navigate and activate a recipe in the selection flow, then traverse existing editable fields in reading order with Tab/Shift-Tab. Multiline editors retain ordinary newline and text-navigation semantics; provide the platform focus-navigation route to leave them. With Full Keyboard Access enabled, every interactive control must be reachable and activatable, including the selection flow and save retry. Maintain a visible system focus indicator separate from recipe selection. Escape cancels the open-selection flow and returns focus to its invoking editor without changing its draft. Do not use Escape to silently discard edits.

Primary click selects or inserts text; secondary click respects the user's configuration and offers relevant existing contextual actions. Use standard text and arrow cursor roles through supported Catalyst behavior. Hover may show tooltips but must not reveal the only actionable control. Preserve system trackpad gestures and shortcuts; do not simulate iPad pointer magnetism or depend on touch-and-hold. Switching between pointer and keyboard preserves selection and editing state.

## Guidance basis

These links identify the official articles underlying the installed local snapshot; no online verification was performed.

- [Mac Catalyst — Choose an idiom; Integrate the Mac experience](https://developer.apple.com/design/human-interface-guidelines/mac-catalyst): idiom review, menus, desktop input and layout.
- [Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos) and [Windows — macOS](https://developer.apple.com/design/human-interface-guidelines/windows#macOS): independent work, system windows and activation.
- [Layout — Adaptability](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability): reflow while preserving functionality. The dimensions above are product proposals, not Apple minimums.
- [The menu bar](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar) and [Toolbars — macOS](https://developer.apple.com/design/human-interface-guidelines/toolbars#macOS): standard command structure and menu parity.
- [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards), [Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection), and [Pointing devices — macOS](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#macOS): familiar input and separate focus/selection.
- [Virtual keyboards — Platform considerations](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#Platform-considerations): component scope; do not carry the iPad software-keyboard model into the Mac layout.
