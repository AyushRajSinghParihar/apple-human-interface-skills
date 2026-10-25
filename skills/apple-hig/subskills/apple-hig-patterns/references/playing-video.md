# Playing video

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/playing-video)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Prefer system players for familiar playback, aspect modes, PiP, and accessible controls. Native players exist in iOS, iPadOS, macOS, tvOS, and visionOS, with TV-app integration for supported content.

The source defines aspect-fill as the default for wide 2:1–2.40:1 video, potentially cropping edges, and aspect-fit for 4:3, 16:9, up to 2:1, and beyond 2.40:1, preserving the full image with bars as needed. Its exact 2:1 endpoint overlaps both statements; use system player behavior instead of inferring an exclusive boundary. TV and visionOS add transport actions and informational content tabs; spatial transport controls appear in an ornament.

<a id="Best-practices"></a>
## Best practices

Use standard player behavior even when a genuine need requires customization. Preserve the original aspect ratio without baking in letterboxing/pillarboxing, which breaks scaling and PiP. Add only useful metadata that does not obscure playback. Honor ordinary controls, including Space to play/pause with a keyboard and expected remote gestures. Keep extra actions to a step or two; use transport controls for playback-related actions and tabs for supplemental information/recommendations. Handle secondary-audio hints so switching video/PiP and another app does not create unwanted audio mixing.

<a id="Integrating-with-the-TV-app"></a>
## Integrating with the TV app

Match the TV app's black transition and begin/resume content directly, avoiding splash/detail screens or intro barriers. Rare required interstitials should allow Select to advance and Play to skip to content. Resume long videos at their prior stop time without asking. Honor a supplied viewer profile automatically; if absent, ask once to establish it for later. Keep Space play/pause available.

<a id="Loading-content"></a>
### Loading content

Avoid a loading screen for quick starts. Beyond about 2 seconds, a black screen with a centered spinner and minimal other content can communicate waiting. Begin once sufficient content is ready and stream the rest in the background; any branding should remain minimal against black.

<a id="Exiting-playback"></a>
### Exiting playback

Playback exits into the app, not back to TV. Show related details with resume, or a containing menu/main menu when details are unavailable. Prepare this exit context immediately after receiving the playback request so even a rapid exit is coherent.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, iPadOS, or macOS rules are specified.

<a id="tvOS"></a>
### tvOS

Keep noninteractive overlays small and brief; translucent SDR graphics reduce distraction and image-retention risk compared with bright opaque graphics. For interactive overlays, use a minimum 0.5-second delay before pausing media and presenting the overlay, and clearly offer dismissal/resumption afterward.

<a id="visionOS"></a>
### visionOS

Let the person start playback, begin in a modest resizable window, and keep surroundings visible for comfort. Do not automatically launch fully immersive video. In immersion, preserve the system's predictable player placement and keep virtual objects away from its controls. For scrub previews, provide 160-pixel-wide thumbnails. Inline video is 2D and should leave window content around it rather than filling the window and implying an immersive player; its controls share the plane. RealityKit video suits splash/transitional effects that need no standard playback integration and supports correct 2D/3D aspect and captions.

<a id="watchOS"></a>
### watchOS

System playback supports short foreground clips, inline or in a separate interface. Prefer clips no longer than 30 seconds to limit storage and wrist fatigue. Avoid scaling assets. Recommended encoding is H.264 High Profile, 160 kbps up to 30 fps; 208×260 px fullscreen portrait or 320×180 px 16:9 landscape; audio 64 kbps HE-AAC. A poster should represent actual content and invite playback without imitating an unrelated system control.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Playing audio](https://developer.apple.com/design/human-interface-guidelines/playing-audio)
[Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/AVFoundation/configuring-your-app-for-media-playback> — AVFoundation
<https://developer.apple.com/documentation/AVKit>
[HTTP Live Streaming](https://developer.apple.com/streaming/)

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2022/10147>
  <https://developer.apple.com/videos/play/wwdc2025/304>
  <https://developer.apple.com/videos/play/wwdc2021/10191>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: September 12, 2023, June 21, 2023.
