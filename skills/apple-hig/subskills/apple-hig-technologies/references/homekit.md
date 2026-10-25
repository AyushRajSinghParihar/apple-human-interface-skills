# HomeKit

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/homekit) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

HomeKit enables secure home/accessory control through Siri and Apple Home. An integration can add setup, fine-grained configuration, unique features, automations, and support while preserving the shared home model.

<a id="Terminology-and-layout"></a>
## Terminology and layout
Honor HomeKit’s hierarchy even if the app organizes by accessories. Make room, zone, and home details easy to find near accessory information. Handle multiple homes and defer to Home-app settings instead of asking people to rebuild duplicate configurations.

<a id="Homes"></a>
### Homes
A home is a meaningful physical location, including a house or office; each is a separate hierarchy root.

<a id="Rooms"></a>
### Rooms
A room is a user-meaningful name, without size or physical-location attributes. Room assignment enables natural grouped voice control.

<a id="Accessories-services-and-characteristics"></a>
### Accessories, services, and characteristics
An accessory is a physical device assigned a category, such as fan/light/thermostat; a switch’s category should match what it controls. Services are separately controllable functions within a device, and characteristics are their adjustable attributes. UI should use descriptive names such as fan/light and speed/brightness rather than service/characteristic jargon. People address service names through Siri. Service groups combine functions to control as a unit, even within one room.

<a id="Actions-and-scenes"></a>
### Actions and scenes
An action changes a characteristic; a scene combines actions across services/accessories. Use scene in UI, even though the API calls it an action set.

<a id="Automations"></a>
### Automations
Automations react to location changes, schedules, accessory state, or sensors.

<a id="Zones"></a>
### Zones
An optional zone groups rooms, such as a floor, for collective control.

<a id="Setup"></a>
## Setup
Always start with the system flow for naming, network joining, pairing, room/category assignment, and favorites. Explain why Home data is needed in the permission purpose string. Do not require accounts/personal data or another platform’s setup during HomeKit setup; offer optional cloud accounts and custom accessory features only after basic functionality works. Honor the chosen HomeKit configuration.

<a id="Help-people-choose-useful-names"></a>
### Help people choose useful names
Suggest understandable function names, avoiding brands/model numbers. Names may contain alphanumeric characters, spaces, and apostrophes, must begin/end with a letter/number, and must not contain emoji. On custom rename, validate and explain fixes. Avoid duplicating room/zone in the service name; guide people to assign location structurally instead.

<a id="Siri-interactions"></a>
## Siri interactions
After setup, teach commands using the person’s actual service names; introduce more advanced examples later in appropriate details views. Siri understands services, categories, rooms, zones, groups, scenes, and implied characteristics such as dim/bright or open state. A question about whether someone is in a room can identify the accessory category and its occupancy-detection characteristic. It can infer the current room through HomePod and address an entire named home. Suggest meaningful groups/zones. Offer Shortcuts only for unique features HomeKit cannot perform, such as ordering consumables, explaining the distinction rather than duplicating existing scenes/actions.

<a id="Custom-functionality"></a>
## Custom functionality
Highlight unique accessory features while explaining when Apple Home is needed to include other devices. Respect the authoritative HomeKit database and reflect external changes automatically. If conflict confirmation is necessary, show both alternatives clearly. Obtain permission or explicit intent before writing changes; never overwrite HomeKit settings silently.

<a id="Cameras"></a>
### Cameras
Do not cover the camera image with unrelated content. Show microphone controls only when bidirectional audio is supported.

<a id="Using-HomeKit-icons"></a>
## Using HomeKit icons
Use official HomeKit artwork for setup/instructions; the Apple Home app icon can reference that app or link to its App Store page. Never redraw Apple’s icons.

<a id="Styles"></a>
### Styles
<a id="Black-HomeKit-icon"></a>
#### Black HomeKit icon
Use black on a light background alongside black technology icons.

<a id="White-HomeKit-icon"></a>
#### White HomeKit icon
Use white on a dark background alongside white technology icons.

<a id="Custom-color-HomeKit-icon"></a>
#### Custom color HomeKit icon
Match other technology icons and their containers. Keep HomeKit icon/name noninteractive, not inline word replacement. If peers have names beside/below their icons, use the same arrangement/font. The separate Home-app icon may link to its product page.

<a id="Referring-to-HomeKit"></a>
## Referring to HomeKit
Keep the app’s identity more prominent. Use trademarks exactly, singular/nonpossessive, without translation, implication of Apple endorsement, or inclusion in app name/images. Credit trademarks in legal information. Use actual Apple product names rather than generic category descriptors, with device/OS references in technical/compatibility descriptions.

<a id="Referencing-HomeKit-and-the-Home-app"></a>
### Referencing HomeKit and the Home app
HomeKit is one word with H/K uppercase; Apple Home is two words with A/H uppercase. Uniformly uppercase layouts may adapt case. Describe compatibility/use, not branded product categories or HomeKit as an actor performing an action. Apple HomeKit is acceptable; HomeKit may name setup/configuration/instructions. Refer to the app first as Apple Home or the Apple Home app; later Home app is acceptable, avoiding an ambiguous standalone Home.

<a id="Platform-considerations"></a>
## Platform considerations
The source gives no further platform-specific rules; check actual API availability for the intended integration.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/homekit) for linked Apple design assets and implementation resources.

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
Source revision dates: May 2, 2023.
