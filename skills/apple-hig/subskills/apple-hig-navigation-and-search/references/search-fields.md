# Search fields

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/search-fields)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A search field combines editable query text with a Search glyph, clearing, and a scope-explaining placeholder. Scope bars and tokens can refine the query; entry placement depends on the platform and search's role.

<a id="Best-practices"></a>
## Best practices

Explain searchable content in the placeholder. Prefer updating results during typing where possible. Offer recent or predictive queries to reduce effort, prioritize relevant results, and group results when it improves navigation. Add filtering where it helps people narrow the result set.

<a id="Scope-bars-and-tokens"></a>
## Scope bars and tokens

A scope bar switches among clearly defined categories or breadths. Start broad to show the available result context and let people narrow deliberately. A token encapsulates a meaningful term or attribute as a selectable, editable unit, such as one contact or a photo filter. Pair available tokens with suggestions to teach these less-visible options.

<a id="Platform-considerations"></a>
## Platform considerations

visionOS has no additional rules in this source.

<a id="iOS"></a>
### iOS

Search can be a tab, a toolbar item, or inline with content. Choose its placement from the scope, navigation structure, and priority.

<a id="Search-as-a-tab"></a>
#### Search as a tab

A standard search tab opens a landing page with a field above useful categories, suggestions, or discovery content. A separate button-style search tab immediately focuses the field and opens the keyboard; leaving that transient search returns to the prior tab. Choose the former for browsing rich content and the latter for fast directed lookup.

<a id="Search-in-a-toolbar"></a>
#### Search in a toolbar

Bottom toolbars can contain an expanded field or a search button according to available width. Activation moves the field above the keyboard. Top/navigation toolbars use a button that opens a field above the keyboard, or at the top when bottom space is insufficient. Favor reachable bottom placement when space permits, even as the toolbar's only control. Use top placement when bottom content serves an important immediate purpose or there is no bottom toolbar.

<a id="Search-as-an-inline-field"></a>
#### Search as an inline field

Place a field beside its content when location should communicate local rather than global scope, especially when the app has multiple searches. At the top of a list, put it above that list and consider pinning it to the top toolbar during scrolling.

<a id="iPadOS-macOS"></a>
### iPadOS, macOS

Keep counterpart apps' search patterns consistent. Trailing toolbar search suits searching across split-view columns and preserving a result selection beside its detail, or filtering content in the detail area. Search at the top of a sidebar suits filtering navigation or finding nested settings while leaving a rich detail view distinct. A sidebar or tab-bar item can instead open a dedicated discovery area with space for suggestions and categories.

In a dedicated search area, immediate focus can speed entry and reveal the field. On iPad with only a virtual keyboard, leave it unfocused so the keyboard does not unexpectedly cover discovery content. Account for fluid resizing: a compact iPad layout may need search above the relevant content-list column instead of in the full-width toolbar.

<a id="tvOS"></a>
### tvOS

The search screen combines a keyboard with customizable results below it. Reduce remote typing through popular, contextual, and recent suggestions.

<a id="watchOS"></a>
### watchOS

Activating search opens a fullscreen text-entry control. The app returns to the search field after Search or Cancel.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Searching](https://developer.apple.com/design/human-interface-guidelines/searching)
[Token fields](https://developer.apple.com/design/human-interface-guidelines/token-fields)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/Adding-a-search-interface-to-your-app> — SwiftUI
<https://developer.apple.com/documentation/SwiftUI/View/searchable(text:placement:prompt:)> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UISearchBar> — UIKit
<https://developer.apple.com/documentation/UIKit/UISearchTextField> — UIKit
<https://developer.apple.com/documentation/AppKit/NSSearchField> — AppKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2026/292>
  <https://developer.apple.com/videos/play/wwdc2025/356>
  <https://developer.apple.com/videos/play/wwdc2021/10126>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 8, 2026, June 9, 2025, September 12, 2023, June 5, 2023.
