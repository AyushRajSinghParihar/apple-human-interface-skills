# Settings

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/settings)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Use sensible defaults and respect system preferences. App-wide configuration, task-local controls, and system Settings belong in different places according to how often and where people need them.

<a id="Best-practices"></a>
## Best practices

Optimize defaults for most people and automatically detect capabilities such as connected controllers or appearance. Keep the settings set small. Support expected access, including Command-Comma and game Escape. Do not duplicate systemwide accessibility, scrolling, or authentication settings in a way that suggests they have different scope.

<a id="General-settings"></a>
## General settings

Put infrequently changed experience-wide choices, such as window configuration, saving behavior, key mappings, or account preferences, in the app's settings area.

<a id="Task-specific-options"></a>
## Task-specific options

Expose frequent view/task changes where their effects are visible: filtering, reordering, and showing/hiding content. In games, approach to a current challenge normally belongs to gameplay rather than a settings trip.

<a id="System-settings"></a>
## System settings

Reserve system-app entries for the rarest changes and, where useful, link directly from the app.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, iPadOS, tvOS, or visionOS rules are specified.

<a id="macOS"></a>
### macOS

Place Settings in the app menu, not the main toolbar; document-level configuration belongs in File. A settings window can use a stable noncustomizable always-visible pane toolbar with active selection. Dim minimize/zoom because reopening is easy and size follows the pane. Use the current pane as title, or App Name Settings for one pane, and restore the previously visited pane.

<a id="watchOS"></a>
### watchOS

Apps do not add custom entries to system Settings. Offer only essential options, perhaps at the main view's bottom or through More for object configuration.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/Settings> — SwiftUI
<https://developer.apple.com/documentation/Foundation/UserDefaults> — Foundation
<https://developer.apple.com/documentation/PreferencePanes>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 10, 2024.
