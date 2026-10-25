# Loading

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/loading)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Load content without interrupting useful interaction, ideally before waiting becomes noticeable.

<a id="Best-practices"></a>
## Best practices

Show useful scaffolding, graphics, or placeholders promptly and replace them as real content arrives. Continue loading in the background while people use other features. For unavoidable waits, offer relevant tips or engaging content matched to the likely duration without repetitive loops. Schedule large assets with background-download mechanisms after install, during updates, or other nondisruptive periods to improve installation and startup.

<a id="Showing-progress"></a>
## Showing progress

If loading lasts more than a moment or two, show that work continues and give an estimate where possible. Use determinate progress for measurable work and indeterminate for unknown duration. Games can use a thematic custom loading view where standard progress styling would feel out of place.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, iPadOS, macOS, tvOS, or visionOS rules are specified.

<a id="watchOS"></a>
### watchOS

Prefer immediate content and avoid wait indicators when possible. For a brief unavoidable second or two, an indicator is preferable to a blank display. Application advice: longer waits should not encourage prolonged wrist watching.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Launching](https://developer.apple.com/design/human-interface-guidelines/launching)
[Progress indicators](https://developer.apple.com/design/human-interface-guidelines/progress-indicators)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/BackgroundAssets>

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2025/325>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 9, 2025, June 10, 2024.
