# Token fields

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/token-fields)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A macOS token field turns entered terms into manipulable units. Tokens can be selected, reordered, or moved to another field, as with email recipients. Suggested completions can become tokens, and each token can expose contextual information and editing commands. Search tokens are a related but separately scoped use.

<a id="Best-practices"></a>
## Best practices

Offer a context menu when a token has useful details or actions. Comma converts entered text into a token by default; add other useful triggers such as Return where appropriate. Suggestions normally appear immediately, but tune the delay if instant suggestions distract from typing.

<a id="Platform-considerations"></a>
## Platform considerations

Token fields are unsupported in iOS, iPadOS, tvOS, visionOS, and watchOS.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields)
[Search fields](https://developer.apple.com/design/human-interface-guidelines/search-fields)
[Context menus](https://developer.apple.com/design/human-interface-guidelines/context-menus)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/AppKit/NSTokenField> — AppKit
