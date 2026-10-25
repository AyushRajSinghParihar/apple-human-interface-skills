# Launching

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/launching)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Launch ends when the first usable screen is ready, including any initial download. Onboarding follows launch rather than replacing it.

<a id="Best-practices"></a>
## Best practices

Aim for immediate interaction, generally within a few seconds. Provide a system launch screen on iOS, iPadOS, and tvOS; Mac, visionOS, and watchOS do not require one. Put any necessary branded splash in onboarding or after launch. Restore detailed previous state, including scroll position and window configuration, so reopening continues prior work.

<a id="Launch-screens"></a>
## Launch screens

The launch screen exists only to make startup appear fast. Match the first screen closely, including current orientation and appearance, to avoid flashes; if startup transitions from a plain color, use that color. Avoid text because this static content is not localized, and avoid advertising or an About-style presentation. Logos and other branding belong on the launch screen only when they are fixed elements of the first app screen. This section does not apply to macOS, visionOS, or watchOS.

<a id="Platform-considerations"></a>
## Platform considerations

Launch screens apply to iOS, iPadOS, and tvOS; other platforms use their own launch behavior.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Launch in current orientation when supporting both portrait and landscape. For a single supported orientation, use it consistently and handle either direction of rotation into landscape correctly.

<a id="tvOS"></a>
### tvOS

Launch imagery is static rather than layered. Live-viewing apps can begin relevant live playback after a few seconds of inactivity where appropriate.

<a id="visionOS"></a>
### visionOS

Consider starting in Shared Space even for an immersive app. An initial window can supply context and loading time while letting the person explicitly choose the transition to Full Space alongside their other apps.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding)
[Loading](https://developer.apple.com/design/human-interface-guidelines/loading)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/Xcode/specifying-your-apps-launch-screen> — Xcode
<https://developer.apple.com/documentation/UIKit/responding-to-the-launch-of-your-app> — UIKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2019/423>
  <https://developer.apple.com/videos/play/wwdc2017/816>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 10, 2024, June 21, 2023.
