# SharePlay

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/shareplay) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

SharePlay synchronizes a real-time activity across participants’ devices alongside FaceTime or Messages. Start can come from app UI, FaceTime, or a link; the system guides app installation and content/subscription access. Each participant normally needs their own entitlement to purchased/subscribed content.

<a id="Best-practices"></a>
## Best practices
Use it for simultaneous participation; add saved state or sharing links for later asynchronous collaboration. Match the activity: synchronized identical views for watching/browsing, personal roles/views for games where useful. Adapt across platforms and communication contexts. Provide a recognizable SharePlay control or system share entry point. Bring joiners directly to shared content, using dismissible prerequisites and postponing profiles/nonessential onboarding; provisional access or Family Sharing can lower purchase friction. Invitations need concise descriptions, titles, and appropriate art. Explain who caused shared changes; system playback synchronization can pause for everyone. Use SharePlay as noun or action verb without adjectives such as spatial/virtual and without altered suffixes.

<a id="Platform-considerations"></a>
## Platform considerations
No extra tvOS rules; watchOS is unsupported.

<a id="iOS-iPadOS-macOS"></a>
### iOS, iPadOS, macOS
Support shared video continuing in Picture in Picture on phone/tablet and a usable continuing playback window on Mac while other work proceeds.

<a id="visionOS"></a>
### visionOS
Standard windows share by screen mirroring through the window-bar Share button; adopt SharePlay for volumes and immersive content.

<a id="Designing-shared-activities"></a>
#### Designing shared activities
Keep shared objects, windows, sounds, and interactions in a consistent relative location through shared context. Prefer a window start, because immersive-only entry needs custom sharing UI. Resolve simultaneous use naturally with predictable rules rather than UI that steals another person’s tool. Keep views/immersion coordinated except when a distinct perspective is meaningful; represent a participant in a separate immersive context with a contact image and retain FaceTime Audio. Ask before an immersion change interrupts someone’s other task. Volume/subtitle/accessibility preferences remain per-person. Offer a clear way to leave/rejoin, with a windowed continuation when possible.

<a id="Personas"></a>
#### Personas
Remote Vision Pro participants may appear as spatial Personas, or contact photos if no Persona exists. Other devices use 2D video windows. Nearby Vision Pro participants see one another through passthrough with content aligned in the same physical place. Offer UI alternatives for activities relying on gestures/facial expression so people without spatial Personas participate fully.

<a id="Spatial-templates"></a>
#### Spatial templates
Side-by-side places people on a curve facing shared media; surround seats a group around central 3D/tabletop content; conversational seats a group around a center with content at the edge, favoring social interaction/background tasks over everyone manipulating the same view. Split complex activities into stages with appropriate system/custom templates. Tie changes to explicit actions, avoid frequent or large moves, fade seat changes, and give reorientation cues.

<a id="Custom-templates"></a>
#### Custom templates
Custom seats apply to spatial Personas, while others can participate without seats. Nearby real people cannot be virtually moved; use position markers when real arrangement matters. Choose seat direction rather than blindly accepting the content-center default. Plan all supported seats up front, normally five for the maximum five spatial Personas, leaving seats stable when someone leaves and adding spectators where a game limit permits. Space seats at least 1 m apart; too-close Personas become contact photos. Choose a balanced fill order for partial attendance. Keep player/spectator/team roles independent of seats except where one role truly requires a location, such as a host.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/shareplay) for linked Apple design assets and implementation resources.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Videos"></a>
#### Videos
Apple’s linked design sessions provide demonstrations and additional implementation context; no video review is implied here.

<a id="Change-log"></a>
## Change log
Source revision dates: September 9, 2026, December 5, 2023, June 21, 2023, December 19, 2022.
