# Focus and selection

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Focus visually identifies an interaction target for component-based navigation with keyboards, remotes, and controllers. Focus can select an item automatically, except where selection would shift context; tvOS normally requires separate activation. Rings/highlights on tablet/Mac and depth/parallax on TV reflect their platform focus models.

<a id="Best-practices"></a>
## Best practices
Use system focus effects unless customization is essential. Do not move focus without input. If a focused item disappears during discrete directional navigation, move to a nearby one-step item; with other input, hide the indicator rather than guessing the next target. Follow platform reachability conventions: keyboard content focus on iPad/Mac coexists with Full Keyboard Access for all controls, whereas tvOS requires directional access to every interactive item. Use rings for text/search and usually full-row highlights for lists/collections. Standard focused/unfocused selection colors preserve active context.

<a id="Platform-considerations"></a>
## Platform considerations
The source marks focus unsupported on iOS/watchOS in this topic’s sense.

<a id="iPadOS"></a>
### iPadOS
Since iPadOS 15, Tab moves between focus groups and arrows move inside a group. Group custom views to produce expected reading order, normally leading-to-trailing then top-to-bottom; a vertical stack may need one focus-group container. Set priority so a likely primary item receives focus when a group is entered. Halo effects outline an item and can be refined for shape, clipping, or badge overlap. A content-configured cell’s highlighted accent appearance is separate from a focus effect.

<a id="tvOS"></a>
### tvOS
In full-screen content, gestures should act on the content rather than invisible focus. Use component focus for menus instead of a tiny free pointer; a gameplay-specific pointer must be conspicuous and integrated. Allow room and high-resolution art for enlarged focus states. Represent unfocused (receded), focused (raised/lit/moving), pressed (immediate feedback), selected (persistent choice such as filled favorite), and unavailable (inactive and unreachable) states distinctly.

<a id="visionOS"></a>
### visionOS
Connected keyboards/controllers use the same focus system family. Looking at content uses hover feedback instead; do not treat gaze hover as keyboard/controller focus.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Videos"></a>
#### Videos
Apple’s linked design sessions provide demonstrations and additional implementation context; no video review is implied here.

<a id="Change-log"></a>
## Change log
Source revision dates: October 24, 2023, June 21, 2023.
