# Maps

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/maps) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

MapKit-style maps offer familiar pan, zoom, rotation, annotations, overlays, and routing in graphical, satellite, or hybrid views.

<a id="Best-practices"></a>
## Best practices
Keep maps interactive and avoid blocking expected gestures. Use saturated default emphasis for ordinary/native-aligned maps and muted emphasis for rich custom overlays. Add search/category filters, clearly distinguish selected features, and cluster nearby points that separate as zoom increases. Keep the Apple logo/legal link visible, stable relative to the map, with suggested 7 pt side padding and 10 pt vertical padding. Place them 10 pt above the lowest resting position of a movable bottom card. They are omitted on maps smaller than 200 × 100 px.

<a id="Custom-information"></a>
## Custom information
Style annotations coherently with the app; default markers are red/white pins, with configurable tint/image or short 2–3-character Unicode strings. Independently selectable system map features can offer custom information alongside app annotations. Above-roads overlays sit below buildings/trees; above-labels overlays obscure all map detail beneath. Ensure custom controls contrast against changing geography with restrained strokes/shadows or map blending.

<a id="Place-cards"></a>
## Place cards
Cards provide current structured hours, contacts, addresses, and place details.

<a id="Displaying-place-cards-in-a-map"></a>
### Displaying place cards in a map
Attach cards to selected app places or system points/territories/physical features. Automatic chooses by map size; callout can be full or compact; caption links to Apple Maps; sheet presents details in a sheet. Full callout is a popover on iPad/Mac and a sheet on iPhone. Choose enough detail without hiding the broader map or duplicating information already shown. Test devices/window sizes, use a suitable minimum width when needed, and offset the card so the selected location stays visible. A web embed can default to one specified place’s card.

<a id="Adding-place-cards-outside-of-a-map"></a>
### Adding place cards outside of a map
Lists/search/store locators can open cards without a map view, but the card itself must then include a map. Signal the action through place names, addresses, details controls, or a pin-plus-name.

<a id="Indoor-maps"></a>
## Indoor maps
Show major rooms/buildings at all scales and disclose stores/restrooms/detail progressively on zoom. Distinguish areas/services with color plus icons. Provide a concise floor-number picker for multilevel venues. Include nearby streets/transit for context, dimming noninteractive surroundings, and offer routing to stations/parking or a handoff to Apple Maps. Bound panning according to zoom so part of the venue remains visible. Make custom indoor styling consistent with the app rather than imitating Apple Maps.

<a id="Platform-considerations"></a>
## Platform considerations
No extra iOS/iPadOS/macOS/tvOS/visionOS rules.

<a id="watchOS"></a>
### watchOS
Watch maps are static snapshots that open Maps when tapped. Supply the region at runtime and at most five annotations. Fit the whole map element onscreen without scrolling and use the smallest region encompassing all important points.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/maps) for linked Apple design assets and implementation resources.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Videos"></a>
#### Videos
Apple’s linked design sessions provide demonstrations and additional implementation context; no video review is implied here.

<a id="Change-log"></a>
## Change log
Source revision dates: December 18, 2024, September 12, 2023, September 23, 2022.
