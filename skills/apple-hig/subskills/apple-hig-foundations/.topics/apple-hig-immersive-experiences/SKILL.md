---
name: apple-hig-immersive-experiences
description: Use when choosing or reviewing visionOS immersion styles, passthrough, entry/exit transitions, movement boundaries, virtual hands, or environmental comfort.
---

# Choose immersion for a specific moment

Read [Immersive experiences](../../references/immersive-experiences.md). Inspect the activity, useful spatial content, expected movement, entry/exit behavior, and custom environment. Establish design, review, or adaptation mode. This model is visionOS-specific; retain the existing stack and distinguish a scene proposal from actual worn-device observations.

Choose the least immersive mode that serves the moment. Shared Space or mixed immersion keeps ordinary work grounded. Mixed Full Space suits unbounded content integrated with surroundings; progressive lets the person vary an environment's coverage; full replaces passthrough. If people may move beyond the guide's approximately 1.5 m progressive/full boundary, use or return to mixed rather than requiring movement inside a constraining scene. If mixed content would obscure most surroundings, reconsider stronger immersion explicitly instead of defeating passthrough.

Specify deliberate enter and exit controls. Explain whether Exit returns to less immersion or ends the app; preserve task state, and provide pause/save before an exit that quits. Preserve Digital Crown control and boundary/system awareness behavior. Sensitive room/scene/hand data needs appropriate permission; it is not implied by drawing 3D content.

Design stationary interaction, central important content, and a stable visual reference. Keep peripheral motion/detail restrained. An environment needs a ground plane even with a panorama, coherent scale/lighting, and nonrepetitive spatial audio that yields to other activity. If replacing real hands, match familiar poses and fade virtual hands out to reveal real hands when tracking becomes invalid.

**Worked transformation:** Before, an exhibit hides the room immediately, asks people to walk to the next sculpture, and exits by quitting without preserving selection. Decision: stronger immersion is optional and should support a resting viewer. After, browsing begins grounded; entering an exhibit is explicit, sculptures come to the viewer, and “Return to catalog” restores the selected work. Tracking loss reveals real hands if virtual hands were active.

Deliver a style/transition/state storyboard or implementation. Fail if ordinary work requires unnecessary immersion, exit loses work, the scene demands unsupported movement, or tracking failure leaves misleading hands. Geometry/source checks cannot establish boundary response, physical comfort, or passthrough appearance without device testing.

Use [Spatial layout](../apple-hig-spatial-layout/SKILL.md) for anchors/scale, [Motion](../apple-hig-motion/SKILL.md) for world movement, and [Privacy](../apple-hig-privacy/SKILL.md) for permission-gated sensing.
