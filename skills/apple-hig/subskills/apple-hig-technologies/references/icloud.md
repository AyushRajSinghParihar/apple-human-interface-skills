# iCloud

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/icloud) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Make cloud-backed content feel continuously available without requiring people to manage synchronization or storage location.

<a id="Best-practices"></a>
## Best practices
Use iCloud automatically when enabled. If a choice is needed, offer one clear all-data-or-none option on first use rather than per-document storage decisions. Keep content current while respecting bandwidth/storage; very large documents may need user-controlled downloads, a newer-version indicator, and subtle progress after several seconds. Store meaningful user-created content, not regenerable resources. Remember Documents-folder content enters iCloud backups even without explicit iCloud support.

Handle disabled/offline iCloud unobtrusively instead of alarming people; indicate that changes will synchronize later if useful. Synchronize continuation state such as reading position and only settings that should travel among devices. Before deleting, explain deletion across iCloud and every device and obtain confirmation. Resolve conflicts automatically if possible; otherwise promptly show clearly differentiated versions with an easy choice. Include cloud content in search. Games can use GameSave for cross-device saves and built-in or custom offline/conflict resolution UI.

<a id="Platform-considerations"></a>
## Platform considerations
No separate platform rules are supplied.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/icloud) for linked Apple design assets and implementation resources.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Change-log"></a>
## Change log
Source revision dates: June 9, 2025.
