# Designing for visionOS

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Apple Vision Pro presents a spatial canvas containing windows, volumes, and 3D objects. Apps normally start in the Shared Space beside other apps; a person can choose a Full Space in which one app provides mixed, portal-based, or fully surrounding content.

Passthrough is live camera imagery of the actual surroundings. The Digital Crown adjusts how much of that context remains visible. Spatial Audio models the room acoustically; with permission to understand surroundings an app can refine its audio experience. Eyes typically target content and an indirect hand gesture activates it; direct gestures can touch virtual content.

Accessibility includes VoiceOver, Switch Control, Dwell Control, Guided Access, and Head Pointer. Standard components provide an accessible starting point; enhance custom content with the platform frameworks.

Device safety matters: the source specifies use by people age 13 or older, and excludes use while operating vehicles or heavy machinery or moving around hazards such as streets, stairs, and balconies. Consult Apple’s current device user guide for operational restrictions.

<a id="Best-practices"></a>
## Best practices
- Use space, audio, immersion, passthrough, and eye/hand inputs deliberately. Select the least immersive presentation that delivers each moment rather than making every task fully immersive.
- Prefer standard windows for contained UI and ordinary tasks. People can position windows and dynamic scaling preserves readability at different distances.
- Preserve visual comfort: cameras mediate both real and virtual vision. Position content relative to the head inside a comfortable field of view regardless of posture or height.
- Avoid requiring head turns, body repositioning, or excessive movement during full immersion. Bring useful content to a resting person.
- Avoid rapid, overwhelming, abrupt motion or motion without a stable visual reference.
- Make indirect gestures work with hands resting at the sides or in the lap. Keep direct interaction within reach and brief enough to prevent fatigue.
- Use SharePlay and spatial Personas when shared activities benefit from a sense of presence.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos) for linked Apple design assets and implementation resources.

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
Source revision dates: February 2, 2024, September 12, 2023, June 21, 2023.
