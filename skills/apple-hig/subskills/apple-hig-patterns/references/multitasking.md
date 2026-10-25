# Multitasking

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/multitasking)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Support switching and simultaneous work wherever the platform allows it; exceptions include some games and a visionOS Full Space. Be ready to preserve context whenever focus changes.

<a id="Best-practices"></a>
## Best practices

Pause attention-dependent gameplay/media when leaving the experience, with seamless resumption. Distinguish audio interruption types: sustained primary audio such as music/podcasts requires an indefinite pause, while brief directions may duck or pause temporarily and then restore. Finish input-free user-initiated tasks in the background before suspension. Notify only for important/time-sensitive completion that prompts another step; routine background work can report status on return.

<a id="Platform-considerations"></a>
## Platform considerations

This multitasking mode is unsupported in watchOS.

<a id="iOS"></a>
### iOS

Picture in Picture allows video/FaceTime beside another app.

<a id="iPadOS"></a>
### iPadOS

Support several apps' windows and multiple windows of one app. Fullscreen windows switch through the app switcher; windowed mode allows resize, placement, tiling, fullscreen, minimize, and close. Frontmost colored controls/shadows communicate state. PiP can overlay either mode. Apps neither control nor receive the person's multitasking configuration, so adapt to size rather than assuming one layout.

<a id="macOS"></a>
### macOS

Multiple apps/windows are the normal environment. Preserve system layering and main/key/inactive appearance cues.

<a id="tvOS"></a>
### tvOS

Supported experiences can browse/play while another movie/show remains in PiP.

<a id="visionOS"></a>
### visionOS

Shared Space hosts multiple windows/volumes with one active window. Looking elsewhere activates that window and lets the prior window recede/translucently dim. Preserve system feathered-edge feedback instead of changing edges. Closing a window backgrounds rather than quits the app; closing a Now Playing window pauses audio, which can resume in Control Center. Video started in one window should continue when the person merely looks at another, qualifying the general attention-pause rule. Non-Now-Playing audio can duck when attention shifts.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
[Windows](https://developer.apple.com/design/human-interface-guidelines/windows)
[Playing video](https://developer.apple.com/design/human-interface-guidelines/playing-video)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/UIKit/responding-to-the-launch-of-your-app> — UIKit
<https://developer.apple.com/documentation/UIKit/multitasking-on-ipad-mac-and-apple-vision-pro> — UIKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2025/208>
  <https://developer.apple.com/videos/play/wwdc2025/282>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 9, 2025, December 5, 2023, June 21, 2023.
