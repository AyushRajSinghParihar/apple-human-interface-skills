# Remotes

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/remotes) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

The Siri Remote combines physical buttons and a touch-sensitive clickpad for tvOS navigation, selection, and playback across the room.

<a id="Best-practices"></a>
## Best practices
Preserve standard gestures and focus direction outside specialized gameplay. Provide clear feedback connecting gesture to content. Presses indicate deliberate activation; resting/moving/passing the remote can cause accidental taps, so avoid acting on taps during live playback. Positional up/down/left/right taps can help only when intuitive and discoverable.

Back normally opens the hierarchy’s parent, which is not always the previously visited screen; at the root it returns Home. During play, Back can open a pause menu to avoid accidental exits; Back from that menu resumes, while another deliberate action can return to the game menu. Holding Back reaches Home. Play/Pause must play, pause, or resume active media.

<a id="Gestures"></a>
## Gestures
Swipe scrolls with momentum based on swipe strength; vertical swipes along an edge accelerate through many items. Press activates or selects, and pressing before swiping enters scrubbing.

<a id="Buttons"></a>
## Buttons
Touch-surface swipe navigates/changes focus in apps and acts like a D-pad in games. Surface press activates/deepens navigation or acts as the game primary button. Back handles parent/exit or pause/resume according to context. Play/Pause controls media, while games may use it as a secondary action or to skip an intro.

<a id="Compatible-remotes"></a>
## Compatible remotes
For an app with an electronic program guide, guide/browse buttons open it; page-up/down navigate within it, also supported by upper/lower surface taps. Without an EPG, the system sends those requests to the default guide app. While content is playing, page-up/down should change channels rather than page through the guide.

<a id="Platform-considerations"></a>
## Platform considerations
This source is tvOS-specific and marks the other five platforms unsupported.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/remotes) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.
