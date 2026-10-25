# Collaboration and sharing

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/collaboration-and-sharing)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

System sharing and Messages integrations can start collaboration and support communication, permissions, and ongoing event updates. CloudKit, iCloud Drive, and custom infrastructure can participate; custom implementations also need universal links. SharePlay separately supports synchronous shared activities.

<a id="Best-practices"></a>
## Best practices

Put Share somewhere convenient, typically the toolbar, and use the system share sheet/popover or ShareLink. Collaboration method and permission choices appear in the iOS 16 share sheet and in the iPadOS 16 and macOS 13 sharing popover. Support send-a-copy alongside collaboration: CloudKit supplies file plus collaboration object, iCloud Drive already supports it, and custom infrastructure includes a file or plain-text representation in its object. Summarize access/edit permissions briefly and offer a small logically grouped set of choices, including who can access, edit, or add participants.

Show Collaboration prominently when sharing starts, preferably next to Share. Its popover has participants/communication at top, optional custom actions in the middle, and management at bottom. Add only essential custom content, such as recent changes. Customize Manage Shared File wording where useful; CloudKit supplies management UI, while other implementations create it. Messages event notifications can report changes, mentions, joins, or departures with a universal link to the relevant app view.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, iPadOS, or macOS rules are specified. This collaboration integration is unavailable in tvOS.

<a id="visionOS"></a>
### visionOS

Shared Space screen sharing streams the current window. Entering Full Space pauses the stream for others until the app returns to Shared Space.

<a id="watchOS"></a>
### watchOS

SwiftUI ShareLink presents the system sharing interface.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Activity views](https://developer.apple.com/design/human-interface-guidelines/activity-views)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SharedWithYou>
<https://developer.apple.com/documentation/SwiftUI/ShareLink> — SwiftUI

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2022/10015>
  <https://developer.apple.com/videos/play/wwdc2022/10095>
  <https://developer.apple.com/videos/play/wwdc2022/10093>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: December 5, 2023, June 21, 2023, September 14, 2022.
