# Searching

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/searching)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Support finding content in the app, document, and system. Recents, predictions, completions, corrections, attribute filters, and scopes can reduce effort. Spotlight on iOS/iPadOS/macOS can expose indexed content without first opening the app.

<a id="Best-practices"></a>
## Best practices

Give important search a prominent toolbar or dedicated tab position. Prefer one clear app-wide search, retaining local filtering when distinct sections justify it. Communicate scope with placeholder, title, or scope control. Offer useful suggestions before/during entry. Treat search history as potentially private and let people clear it.

<a id="Systemwide-search"></a>
## Systemwide search

Index app content with descriptive metadata. Custom file formats need metadata import support for Spotlight. Contextual commands can initiate an advanced Spotlight query and show relevant filtered results. Prefer system Open/Save views for their built-in systemwide search, and supply Quick Look generation for custom document previews.

<a id="Platform-considerations"></a>
## Platform considerations

The source adds no separate rules for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS; systemwide Spotlight support described here specifically applies to iOS/iPadOS/macOS.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Search fields](https://developer.apple.com/design/human-interface-guidelines/search-fields)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/CoreSpotlight/adding-your-app-s-content-to-spotlight-indexes> — Core Spotlight

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2026/292>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 8, 2026, June 9, 2025.
