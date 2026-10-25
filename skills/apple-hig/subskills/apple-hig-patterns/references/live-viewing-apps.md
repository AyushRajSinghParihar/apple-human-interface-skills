# Live-viewing apps

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/live-viewing-apps)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Prioritize live content and clearly distinguish it from video on demand throughout the experience.

<a id="Best-practices"></a>
## Best practices

Put live viewing first and minimize launch-to-play delay, ideally with zero or one activation of a prominent Watch action. Remove that affordance once playback begins. Label other live channels with a consistent live cue and consider progress through the current program. Playback remains primary; keep supported alternatives such as restart, record, download, or favorite in a consistent order, and show future airings where relevant.

A channel-browsing footer can preserve playback. Separate it visually from moving content, identify the current program, match its categories to the guide, and make invocation/dismissal predictably opposite gestures. Show instant channel-change feedback while a stream loads. Audio should follow currently playing live content during in-context browsing, but stop when navigation leaves the live tab.

<a id="EPG-experience"></a>
## EPG experience

The electronic guide should make current time, program, and channel obvious and let people return immediately to playback. Support efficient paging, scrolling, or jumping, with favorites/My Channels for common choices. Use familiar categories consistently with any footer. Continue playback through PiP or background presentation while browsing.

<a id="Cloud-DVR"></a>
## Cloud DVR

Start/stop current recording through the info panel. Future-program details should offer recording that program or future episodes. Let people refine scope, such as new episodes or games involving particular teams. Recorded-content detail views should support play, delete, and relevant recording settings. Offer storage management, ideally automatically replacing oldest/already-viewed recordings when configured, before space runs out.

<a id="Platform-considerations"></a>
## Platform considerations

The source adds no separate rules for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Remotes](https://developer.apple.com/design/human-interface-guidelines/remotes)
[Playing video](https://developer.apple.com/design/human-interface-guidelines/playing-video)
