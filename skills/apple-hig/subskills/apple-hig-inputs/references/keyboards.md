# Keyboards

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/keyboards) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

## Contents

- [Best practices](#Best-practices)
- [Standard keyboard shortcuts](#Standard-keyboard-shortcuts)
- [Custom keyboard shortcuts](#Custom-keyboard-shortcuts)
- [Platform considerations](#Platform-considerations)
- [Resources](#Resources)
- [Change log](#Change-log)

Physical keyboards support text, navigation, and games on every platform except watchOS. Shortcuts normally combine a primary key and modifiers; game bindings often use one key.

<a id="Best-practices"></a>
## Best practices
Support and test Full Keyboard Access on iOS/iPadOS/macOS/visionOS. On iPad, use ordinary keyboard focus for content, text fields/views, sidebars, and suitable custom collections; let Full Keyboard Access provide access to buttons, segmented controls, switches, and all other controls. Preserve standard shortcuts; games should keep expected system actions such as quitting while allowing binding customization.

<a id="Standard-keyboard-shortcuts"></a>
## Standard keyboard shortcuts
Do not repurpose familiar combinations for unrelated actions. A standard shortcut may be reused only when its normal meaning has no place in the app, such as Command-I for Info when italics is unavailable. The following retains the source’s complete command mapping, including legacy/system-context entries; actual behavior depends on the OS and current context. ⌘ = Command, ⌥ = Option, ⇧ = Shift, ⌃ = Control.

|Shortcut|Source-assigned result|
|---|---|
|⌘Space|Toggle Spotlight field|
|⇧⌘Space|Context-dependent|
|⌥⌘Space|Spotlight results window|
|⌃⌘Space|Special Characters window|
|⇧Tab|Previous control|
|⌘Tab / ⇧⌘Tab|Next/previous app in recent-use order|
|⌃Tab / ⌃⇧Tab|Next/previous control group, or next table where Tab visits cells|
|Esc / ⌘Period|Cancel current action|
|⌥⌘Esc|Force Quit dialog|
|⌃⌘Eject|Quit apps after saving changes, then restart|
|⌃⌥⌘Eject|Quit apps after saving changes, then shut down|
|⌃F1|Toggle Full Keyboard Access|
|⌃F2 / ⌃F3|Focus menu bar / Dock|
|⌃F4 / ⌃⇧F4|Focus active-or-next / prior active window|
|⌃F5 / ⌘F5|Focus toolbar / toggle VoiceOver|
|⌃F6 / ⌃⇧F6|Focus first-or-next / previous panel|
|⌃F7|Temporarily override keyboard-access mode|
|F8 / F9 / F10|Context-dependent|
|F11 / F12|Show desktop / toggle Dashboard, as listed in source|
|⌘Grave / ⇧⌘Grave|Next/previous window in front app|
|⌥⌘Grave|Focus window drawer|
|⌘Hyphen / ⇧⌘Equal|Decrease/increase selection size|
|⌥⌘Hyphen / ⌥⌘Equal|Zoom screen out/in when enabled|
|⌘Left bracket / ⌘Right bracket / ⌘Pipe|Left/right/center alignment|
|⌘Colon / ⌘Semicolon|Spelling window / next spelling issue|
|⌘Comma|App settings|
|⌃⌥⌘Comma / ⌃⌥⌘Period|Decrease/increase screen contrast|
|⌘Question mark|App Help menu|
|⌥⌘Forward slash|Toggle font smoothing|
|⇧⌘3 / ⌃⇧⌘3|Screen capture to file / clipboard|
|⇧⌘4 / ⌃⇧⌘4|Selection capture to file / clipboard|
|⌥⌘8 / ⌃⌥⌘8|Toggle screen zoom / invert colors|
|⌘A / ⇧⌘A|Select all / deselect all|
|⌘B|Toggle bold on selection|
|⌘C|Copy selection|
|⇧⌘C|Colors window|
|⌥⌘C|Copy text style|
|⌃⌘C|Copy selection formatting settings|
|⌥⌘D|Toggle Dock|
|⌃⌘D|Dictionary definition for selected word|
|⌘E|Use selection for find|
|⌘F / ⌥⌘F / ⌃⌘F|Find window / focus search / enter full screen|
|⌘G / ⇧⌘G|Next/previous match|
|⌘H / ⌥⌘H|Hide this app / other apps|
|⌘I|Toggle italic, or Info window when relevant|
|⌥⌘I|Inspector window|
|⌘J|Scroll to selection|
|⌘M / ⌥⌘M|Minimize active / all app windows|
|⌘N / ⌘O|New document / Open dialog|
|⌘P / ⇧⌘P|Print / Page Setup dialog|
|⌘Q|Quit app|
|⇧⌘Q / ⌥⇧⌘Q|Log out with / without confirmation|
|⌘S|Save new document or version|
|⇧⌘S|Duplicate active document or Save As|
|⌘T / ⌥⌘T|Fonts window / toggle toolbar|
|⌘U|Toggle underline|
|⌘V|Paste at insertion point|
|⇧⌘V|Paste as, for example quotation|
|⌥⌘V|Apply copied object style|
|⌥⇧⌘V|Paste matching surrounding style|
|⌃⌘V|Apply copied formatting|
|⌘W / ⇧⌘W / ⌥⌘W|Close active window / file and its windows / all app windows|
|⌘X|Cut selection to clipboard|
|⌘Z / ⇧⌘Z|Undo / separate Redo|
|⌘Right / ⌘Left|Source table: current Roman / system-script keyboard layout|
|⇧⌘Right / ⇧⌘Left|Extend to next/previous semantic boundary, usually line end/start|
|⇧Right / ⇧Left|Extend one character right/left|
|⌥⇧Right / ⌥⇧Left|Extend to current then next/prior word boundary|
|⌃Arrow|Move focus among values/cells|
|⇧⌘Up / ⇧⌘Down|Extend to semantic boundary, usually document start/end|
|⇧Up / ⇧Down|Extend one line at nearest same-column character boundary|
|⌥⇧Up|Extend to start of current, then neighboring paragraph as source lists|
|⌥⇧Down|Extend to paragraph end then next; include terminator in cut/copy/paste|
|⌃Space|Toggle current/last input source|
|⌃⌥Space|Next input source|
|Additional modifier + ⌘Space|Context-dependent localized input behavior|

<a id="Custom-keyboard-shortcuts"></a>
## Custom keyboard shortcuts
Create shortcuts for frequent app-specific commands, keeping the set learnable. Prefer Command as primary modifier, Shift for a related variant, Option sparingly for advanced/rare actions, and avoid Control because of system reservations. Preserve expected modifier behavior: Command-drag groups items, Shift-resize constrains aspect ratio, held arrows advance by the smallest app-defined increment.

List modifiers in Control–Option–Shift–Command order. Do not separately print Shift merely because an upper key character needs it: use Command-Question mark rather than spelling Shift-Command-Slash. Consider international keyboards where Option produces characters; extra modifiers are safest with alphabetic keys, and Command is usually safest overall. Let system localization and RTL mirroring operate. Do not derive an unrelated action by adding a modifier to a familiar command.

<a id="Platform-considerations"></a>
## Platform considerations
No extra iOS/iPadOS/macOS/tvOS rules are given; watchOS is marked unsupported.

<a id="visionOS"></a>
### visionOS
Holding Command shows available shortcut-bearing commands grouped under familiar File/Edit/View categories. The flattened display omits submenu context, so each discoverability title must explain its action independently. A connected physical keyboard also produces a virtual overlay for completions and other typing controls.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/keyboards) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Change-log"></a>
## Change log
Source revision dates: June 9, 2025, June 10, 2024, June 21, 2023.
