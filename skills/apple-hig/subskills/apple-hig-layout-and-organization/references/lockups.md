# Lockups

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/lockups)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A tvOS lockup combines content, a header above it, and a footer below it into one focusable unit; all parts grow and shrink together as focus changes. Available forms include cards, caption buttons, monograms, and posters.

<a id="Best-practices"></a>
## Best practices

Reserve enough spacing for the focused unit to expand without displacing or overlapping neighbors. Keep dimensions consistent within a row or logical group.

<a id="Cards"></a>
## Cards

Use a card's combined header, content, and footer to present media ratings or reviews.

<a id="Caption-buttons"></a>
## Caption buttons

A caption button presents image or text content with a title and optional subtitle below. Match focus tilt to the navigation arrangement: vertical movement for vertical stacks, horizontal movement for rows, and both axes for grids.

<a id="Monograms"></a>
## Monograms

Identify people with a circular portrait and name; use initials as a fallback when no portrait exists. Prefer a real image when available because it creates a stronger connection to the person.

<a id="Posters"></a>
## Posters

A poster presents an image; optional title and subtitle appear upon focus. Size the poster for its actual content rather than assuming a universal aspect or dimension.

<a id="Platform-considerations"></a>
## Platform considerations

Lockups are specific to tvOS and unsupported in iOS, iPadOS, macOS, visionOS, and watchOS.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Designing for tvOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos)
[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/TVUIKit/TVLockupView> — TVUIKit
<https://developer.apple.com/documentation/TVUIKit/TVLockupHeaderFooterView> — TVUIKit
