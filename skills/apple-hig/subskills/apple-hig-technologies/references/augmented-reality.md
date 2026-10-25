# Augmented reality

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/augmented-reality) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

AR blends virtual objects with live physical surroundings. Require capable devices for an AR-first app; hide optional unsupported features rather than showing capability errors. Most guidance here addresses iOS/iPadOS; visionOS uses its own ARKit spatial model.

<a id="Best-practices"></a>
## Best practices
Use most of the display for the scene with minimal controls/text. Realistic art needs plausible scale, detected-surface placement, environmental light/grain, diffuse shadows, and continuously updated perspective, targeting 60 scene updates per second. Prefer small/coarse reflective areas because camera-based reflections are approximate. Add suitable spatial audio/haptics for contact. Persistent indirect controls should be reachable, stationary in screen space, and translucent where appropriate. Explain environmental needs and adapt to small spaces or missing surfaces. Reduce fatigue with comfortable object distance, short play intervals/rest, gradual movement introduction, and no sudden expansive actions that endanger people.

<a id="Providing-coaching"></a>
## Providing coaching
Prefer the system coaching overlay for initialization/surface discovery and relocalization, hiding unrelated UI while it appears. Configure needed plane detection; if custom coaching is essential, use standard behavior as reference.

<a id="Helping-people-place-objects"></a>
## Helping people place objects
Signal a detected placement surface with an indicator aligned to it. Place immediately using current estimates, then gently refine/nudge as detection improves. Guide toward offscreen objects visually or audibly. Do not rely on exact detected edges; classification can restrict furniture to floors or games to tables.

<a id="Designing-object-interactions"></a>
## Designing object interactions
Prefer direct familiar manipulation, with indirect controls where movement makes touching hard. Consider one-finger dragging to move an object and two-finger rotation to spin it. Keep manipulation simple because touchscreen gestures are two-dimensional while the AR scene has depth. Enlarge reasonable hit proximity for small/thin/distant objects. Allow scaling only when it serves the scenario; product visualization may need fixed real size. Scaling a distant object does not make it nearer. Test pinch/rotation conflicts. Keep moving objects visible and attached to plausible surfaces, avoiding jumps/disappearance. Motion/proximity can also produce meaningful responses.

<a id="Offering-a-multiuser-experience"></a>
## Offering a multiuser experience
ARKit can merge each person’s independently mapped environment. Support people occlusion for convincing depth where applicable and late joining through implicit map merging unless simultaneous start is necessary.

<a id="Reacting-to-real-world-objects"></a>
## Reacting to real-world objects
Use 2D/3D reference assets for recognized physical content. When an image disappears, delay removal of attached virtual content up to about 1 second to avoid flicker. Keep active image sets at 100 or fewer for performance, swapping contextually when necessary. Track precise image position only when it may move or attached content is small relative to the image.

<a id="Communicating-with-people"></a>
## Communicating with people
Use plain descriptions of surfaces, lighting, and slower phone movement, not planes/tracking/features jargon. Prefer contextual 3D hints before text overlays. Put critical labels/instructions in screen space; 3D labels should face the viewer at stable apparent text size regardless of object distance. Offer an unobtrusive way to request more information.

<a id="Handling-interruptions"></a>
## Handling interruptions
After app switches/calls, use coaching to restore prior device pose and relocalize. Consider hiding old objects until placement is stable. Embed non-AR subtasks inside the AR flow to avoid needless interruption. Offer cancel/reset because relocalization can otherwise run indefinitely. Indicate lost face tracking after roughly 0.5 seconds, with minimal guidance text.

<a id="Suggesting-problem-resolutions"></a>
## Suggesting problem resolutions
Provide a restart. Explain likely remedies: insufficient detail/light calls for more lighting, movement, or a textured target surface; excessive motion calls for slower movement. Do not make people wait indefinitely for conditions to improve.

<a id="Icons-and-badges"></a>
## Icons and badges
Use the supplied AR glyph only to launch ARKit experiences, changing size/color only, with clear space at least 10% of its height. Use unmodified AR badges exclusively to distinguish AR-capable objects in mixed collections; badge-only glyphs fit constrained spaces. Omit redundant badges when every item supports AR. Keep badges in a consistent visible corner without covering key imagery and with 10%-height clear space.

<a id="Platform-considerations"></a>
## Platform considerations
No extra iOS/iPadOS rules; macOS/tvOS/watchOS are unsupported.

<a id="visionOS"></a>
### visionOS
With permission, ARKit can provide detected surfaces, hands/fingers for custom gestures, and nearby-object information for immersive interactions. Consult the Full Space/privacy guidance for access requirements.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/augmented-reality) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Videos"></a>
#### Videos
Apple’s linked design sessions provide demonstrations and additional implementation context; no video review is implied here.
