# Immersive experiences

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

visionOS can run an app beside others in Shared Space or alone in Full Space. A Full Space can contain ordinary windows/volumes and unbounded 3D content. Choose and transition immersion intentionally.

<a id="Immersion-and-passthrough"></a>
## Immersion and passthrough
Passthrough is live video of real surroundings. People retain system control: holding the Digital Crown recenters content and double-clicking briefly hides content for an unobstructed view. The system may fade content near physical obstacles or an immersive boundary to preserve awareness.

<a id="Immersion-styles"></a>
### Immersion styles
- Dimming/tinting passthrough can focus content in either Shared or Full Space without always hiding other apps. Default tint is black; custom tints are possible.
- `mixed` Full Space blends unbounded 3D content with the surroundings. It has no defined movement boundary. With permission, ARKit can supply room/object information; nearby content dims when a person approaches physical objects.
- `progressive` Full Space partially replaces surroundings with a custom environment. The Digital Crown changes immersion, normally over 120–360 degrees or an app-defined range; portrait and landscape content are supported.
- `full` replaces passthrough with a 360-degree environment.

Progressive/full modes define a boundary about 1.5 m from the initial head position. As a person approaches it, content fades and passthrough returns. Beyond it, the app icon replaces immersive visuals until the person returns or recenters.

<a id="Best-practices"></a>
## Best practices
Offer multiple ways to use the app and support assistive technologies. Prefer starting in Shared Space or mixed immersion, letting people explicitly choose stronger immersion for valuable moments. Keep ordinary browsing/tasks grounded when possible. Start with subtle dimming, tint, scale, motion, or Spatial Audio cues and strengthen only when justified. In visionOS 2+, subtle passthrough tint can harmonize surroundings and hands; dramatic bright tint can distract.

<a id="Promoting-comfort"></a>
## Promoting comfort
Keep key content in view and motion comfortable. Choose an immersion style consistent with expected movement: use or return to mixed if someone might move beyond 1.5 m. In progressive/full, enable stationary interaction, such as bringing an object closer rather than making someone walk. In mixed, avoid obscuring most passthrough; use stronger immersion if content must substantially block the room. Request permission before using sensitive ARKit room, scene, or hand information.

<a id="Transitioning-between-immersive-styles"></a>
## Transitioning between immersive styles
Use smooth, predictable visual transitions so people can track changes. Offer clear enter and exit controls rather than requiring system controls. Explain whether Exit returns to a less immersive context or ends the app. If exit quits, provide a way to pause, save, or return to a save point first.

<a id="Displaying-virtual-hands"></a>
## Displaying virtual hands
A Full Space app can request permission to hide real hands and render virtual ones. Match familiar positions and gestures. Oversized hands can obscure content, feel clumsy, or appear uncomfortably close. If tracking stops, fade virtual hands out and reveal the real hands; fade them back when valid tracking returns.

<a id="Creating-an-environment"></a>
## Creating an environment
Keep supporting movement and high-contrast detail restrained so primary tasks lead. Direct attention with higher-quality assets in important areas and dimmer/simpler peripheral areas. Proximity suggests interactivity: nearby objects invite manipulation. Favor gentle motion away from the field-of-view edges. Make the environment feel expansive rather than confining.

Use spatial sound with enough variation to avoid obvious repetition; duck or stop ambience under another audio activity. Prefer lit 3D meshes and subtle shaders to a flat 360-degree picture, which lacks convincing scale. Always provide a ground-plane mesh to avoid a floating sensation, including when a panorama is unavoidable. Avoid obvious repeated assets.

<a id="Platform-considerations"></a>
## Platform considerations
This experience model is visionOS-specific; the source marks it unsupported on the other five platforms.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences) for linked Apple design assets and implementation resources.

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
Source revision dates: June 9, 2025, November 19, 2024, June 10, 2024, May 7, 2024, February 2, 2024, October 24, 2023, June 21, 2023.
