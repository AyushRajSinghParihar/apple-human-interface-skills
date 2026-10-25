# Toggles

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/toggles)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A toggle controls opposing states, commonly on/off. The system offers styles such as switches and checkboxes, while buttons can also retain toggle state through appearance changes.

<a id="Best-practices"></a>
## Best practices

Use toggles for state, and another component for actions or selection from a list. Identify the affected content through context or an appropriate label. Toggle buttons typically use a meaningful glyph plus a changed background. Make state differences clear through shape, fill, checkmark, or dot; color alone is insufficient.

<a id="Platform-considerations"></a>
## Platform considerations

No extra tvOS, visionOS, or watchOS rules are specified.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Use switch-style toggles in list rows where row content supplies the label. Keep the normal green unless a different accent is necessary, and ensure the on appearance contrasts with off. Outside lists, use a stateful button. A familiar icon and obvious state appearance should explain the visible button without an added explanatory label.

<a id="macOS"></a>
### macOS

Place switches, checkboxes, and radio buttons in the window body rather than the toolbar or status bar.

<a id="Switches"></a>
#### Switches

A switch has stronger visual emphasis than a checkbox; use it for prominent settings or enabling an entire settings group. In grouped forms, a mini switch fits the height of a single row. A regular primary switch plus mini subordinate switches can express hierarchy. Retain established checkboxes rather than replacing them merely for a new appearance.

<a id="Checkboxes"></a>
#### Checkboxes

Checkboxes show empty/off, checkmark/on, or dash/mixed states, usually with a trailing title; editable checklists can omit the title. Leading alignment and indentation make checkboxes useful for hierarchical dependencies. A group label can clarify related choices; align its baseline with the first checkbox. Reflect aggregate mixed state when subordinate choices differ. Use radio buttons when more than two choices must be mutually exclusive.

<a id="Radio-buttons"></a>
#### Radio buttons

Radio groups commonly contain 2–5 labeled circles and allow one choice. A mixed state is possible but rarely useful; a checkbox usually communicates mixed state better. Use checkboxes for multiple independent choices or a lone binary setting. A pair of explicit radio labels can help only when a single checkbox cannot explain the opposing meanings. For more than about 5 options, evaluate a pop-up. When arranged horizontally, allocate consistent space based on the longest label.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/Toggle> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UISwitch> — UIKit
<https://developer.apple.com/documentation/AppKit/NSButton/ButtonType/toggle> — AppKit
<https://developer.apple.com/documentation/AppKit/NSSwitch> — AppKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: March 29, 2024, September 12, 2023.
