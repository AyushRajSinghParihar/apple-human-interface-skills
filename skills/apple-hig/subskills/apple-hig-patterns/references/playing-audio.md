# Playing audio

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/playing-audio)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Respect the person's selected output, volume, and silence state. Silent mode suppresses incidental feedback/game soundtracks but permits deliberately initiated media, alarms, and messages. System volume governs output, with separate iPhone ringer settings. Connecting headphones should reroute smoothly; disconnecting them should pause playback for privacy.

<a id="Best-practices"></a>
## Best practices

Adjust relative mix levels without changing global volume. Permit output rerouting and use the system volume view with its output chooser. Select an audio-session category that fits the importance of sound and coexistence with other audio:

| Category | Silent switch | Mixing | Background |
| --- | --- | --- | --- |
| Solo ambient | Respected | No | No |
| Ambient | Respected | Yes | No |
| Playback | Ignored for essential audio | Configurable | Playback supported |
| Record | Ignored | No | Recording supported |
| Play and record | Ignored | Configurable | Both supported |

Solo ambient suits nonessential exclusive sound; ambient lets external music coexist; playback suits media/learning; recording apps may switch to playback to review; play-and-record suits calls or messaging. Respond to external playback controls only while playing or in an appropriate audio/output context, without stealing another app's audio. Never repurpose unsupported controls. Custom players should solve needs beyond standard commands, such as unusual skip intervals or related content. When a temporary interruption ends, deactivate with notification so other apps can resume.

<a id="Handling-interruptions"></a>
## Handling interruptions

Choose interruption policy deliberately for recording/calls. For recording or other audio work that should continue, the app can ask the system to leave current audio uninterrupted by an incoming call unless the person accepts that call. For example, a closed iPad Smart Folio mutes the microphone and interrupts a VoIP session; end the call rather than automatically unmuting on reopen. Distinguish resumable interruptions such as calls from nonresumable choices such as a newly started playlist. A media player should resume automatically only when appropriate and signaled; a game's incidental sound can follow its gameplay resumption without the same explicit-playback check.

<a id="Platform-considerations"></a>
## Platform considerations

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Use system sound services for short sounds and vibrations.

<a id="macOS"></a>
### macOS

Notification audio mixes with other sound by default.

<a id="tvOS"></a>
### tvOS

Audio is initiated by interaction or device calibration, rather than automatic sounds for alerts or notifications.

<a id="visionOS"></a>
### visionOS

Use meaningful sound to help navigation and spatial understanding, while always providing an alternative for essential information. Native controls already provide sounds; custom objects need appropriate feedback too. Spatial Audio can combine environmental ambience and localized moving or stationary sources, following a moved window. Avoid repetitive fatigue with subtle pitch/level variation, which can be randomized from one asset. Tracked sound normally reinforces an object's changing position/distance; wearer-fixed sound can suit an enveloping experience. Now Playing audio pauses when its window closes; other audio may duck when attention moves to another app.

<a id="watchOS"></a>
### watchOS

System-managed short clips can play in the foreground; longer audio can continue after wrist lowering or app switching. Encode audio as 64 kbps HE-AAC for quality at low data size. A system Now Playing view controls current/recent audio, including another watch/iPhone source, and automatically selects the relevant source.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Playing video](https://developer.apple.com/design/human-interface-guidelines/playing-video)
[Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/AVFoundation/configuring-your-app-for-media-playback> — AVFoundation
<https://developer.apple.com/documentation/AVFAudio/AVAudioSession> — AVFAudio
<https://developer.apple.com/documentation/MusicKit> — MusicKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2026/254>
  <https://developer.apple.com/videos/play/wwdc2023/10271>
  <https://developer.apple.com/videos/play/wwdc2021/10265>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 21, 2023.
