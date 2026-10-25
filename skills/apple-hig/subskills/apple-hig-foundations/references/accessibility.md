# Accessibility

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/accessibility) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Build an interface people can understand, perceive through different senses, and adapt to their preferred methods. Treat accessibility as a design input and audit with Accessibility Inspector. Evaluate actual support before describing Accessibility Nutrition Labels on the App Store.

<a id="Vision"></a>
## Vision
Support text enlargement of at least 200%; the source gives 140% for watchOS. Dynamic Type or equivalent custom resizing must preserve usability. Follow platform defaults/minima when choosing custom styles, and enlarge thin-weight custom fonts further when needed.

|Platform|Default text|Minimum text|
|---|---:|---:|
|iOS, iPadOS|17 pt|11 pt|
|macOS|13 pt|10 pt|
|tvOS|29 pt|23 pt|
|visionOS|17 pt|12 pt|
|watchOS|16 pt|12 pt|

Measure contrast using established calculators such as WCAG or APCA. Apple’s Accessibility Inspector table uses these WCAG-AA guidance values: text up to 17 pt, all weights, 4.5:1; 18 pt at all weights, 3:1; bold text at any size, 3:1. Preserve the table’s stated scope rather than assuming it replaces a separate conformance evaluation. If default colors fall short, Increase Contrast must supply a higher-contrast scheme. Test both light and dark.

Prefer semantic system colors that adapt to accessibility preferences. Pair color with shape, icons, or text; red/green and blue/orange distinctions can be difficult. Let people customize chart or character colors where useful. Give VoiceOver meaningful descriptions of interface and content.

<a id="Hearing"></a>
## Hearing
Make dialogue and important information available without sound. Captions describe audible information in synchrony with media, subtitles present dialogue in a chosen language, audio descriptions narrate otherwise visual events in audio pauses, and transcripts provide a complete text account of audible and visual information. Let people adjust text presentation. Pair sound feedback with matching haptics and visual direction cues, especially for offscreen game or spatial events. Music Haptics and audio graphs on iOS/iPadOS can offer tactile representations of music and data.

<a id="Mobility"></a>
## Mobility
Use comfortable controls and sufficient separation, not just adequate visible size.

|Platform|Default control|Minimum control|
|---|---:|---:|
|iOS, iPadOS|44 × 44 pt|28 × 28 pt|
|macOS|28 × 28 pt|20 × 20 pt|
|tvOS|66 × 66 pt|56 × 56 pt|
|visionOS|60 × 60 pt|28 × 28 pt|
|watchOS|44 × 44 pt|28 × 28 pt|

The source suggests around 12 pt padding for bezelled elements and 24 pt outside visible edges for elements without a bezel. Use simple gestures for repeated tasks and offer an onscreen alternative for essential gestures, such as a dismiss button alongside swipe-to-dismiss. Avoid requiring complex multiple-finger or multiple-hand actions. Label controls so Voice Control can target them. Siri/Shortcuts can expose repeated tasks through voice, Action buttons, Home Screen, and Control Center. Test VoiceOver, AssistiveTouch, Full Keyboard Access, Pointer Control, and Switch Control rather than assuming support.

<a id="Speech"></a>
## Speech
Support complete keyboard navigation and Full Keyboard Access; preserve system accessibility shortcuts. Support Switch Control navigation and activation through hardware, controller, and sound inputs such as a click or pop, so speech is never a necessary input method.

<a id="Cognitive"></a>
## Cognitive
Use familiar, simple, consistent navigation and gestures. Prefer explicit dismissal over timed disappearance, allowing time for processing and assistive navigation. Games can offer difficulty, reaction-time, success-criteria, and control-assistance accommodations. Give clear playback controls and consider a global autoplay preference. Respect Dim Flashing Lights during media playback.

Honor Reduce Motion by reducing automatic and repeated movement, scaling, zooming, and peripheral effects. Reduce spring bounce; tie appropriate motion directly to gestures; avoid animated depth changes and blur transitions; replace spatial translations with fades. Fast or blinking motion can distract, cause dizziness, or trigger seizures.

For Assistive Access on iOS/iPadOS, focus on core tasks, remove nonessential workflows, and split multistep tasks into one interaction per screen. The source requires two confirmations for actions that are difficult to reverse, such as deletion, in this mode.

<a id="Platform-considerations"></a>
## Platform considerations
The source adds no separate rules for iOS, iPadOS, macOS, tvOS, or watchOS beyond the guidance above.

<a id="visionOS"></a>
### visionOS
Support hand/head Pointer Control and Zoom. Keep controls inside a comfortable field of view; horizontal arrangements usually strain the neck less than tall ones. Avoid rapid shifts of attention among distant locations. Reduce peripheral animation speed and intensity, use gentle camera/video motion, and avoid making the surrounding world move without the person’s control. Do not lock content to the head, which can feel confining and interfere with Pointer Control. Minimize large or repeated gestures and consider the physical surroundings.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/accessibility) for linked Apple design assets and implementation resources.

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
Source revision dates: June 9, 2025, March 7, 2025, June 10, 2024, December 5, 2023, June 21, 2023.
