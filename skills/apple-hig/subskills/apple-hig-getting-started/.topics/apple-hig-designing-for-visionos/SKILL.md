---
name: apple-hig-designing-for-visionos
description: Use when designing, reviewing, or adapting an experience for Apple Vision Pro, including spatial presentation, Shared Space, Full Space, eye and hand interaction, or comfort.
---

# Choose a useful spatial experience

Read [Designing for visionOS](../../references/designing-for-visionos.md). Use it for platform principles; the task mapping and deliverable structure below are application engineering advice. Do not treat a desktop interface floated in space or full immersion everywhere as the default solution.

## Establish the task and evidence

Inspect the supplied product, screens, spatial storyboard, input model, or implementation. Identify the core activity, what genuinely benefits from depth or immersion, whether collaboration matters, and whether use is seated, standing, or movement-dependent. Distinguish design, review, and adaptation: produce the requested spatial design, evidence-backed findings, or revised artifact rather than a list of platform features. Preserve the existing product's useful content and state when adapting it.

Record what the evidence can establish. A flat mockup cannot establish depth comfort, reach, tracking, or indirect-target responsiveness. Resolve unspecified details with stated assumptions unless they change the purpose or physical requirements of the experience.

## Decide presentation per activity

Map each major task to a presentation and explain why the least immersive option meets or fails its needs:

- Use a standard **window** for contained tasks such as browsing, text entry, settings, and ordinary controls. Allow people to position it; preserve readability through the platform's dynamic scaling rather than baking a fixed viewing distance into the design.
- Use a **volume or spatial object** when inspecting a genuinely three-dimensional subject benefits the task. Identify what stays in a window, how the object is selected/manipulated, and how the person returns to the rest of the work. A 3D object alone does not justify replacing the surroundings.
- Choose **Full Space** for a specific valuable moment that needs an app-controlled spatial setting. Describe whether it retains surroundings, uses a portal, or surrounds the person. Specify deliberate entry and return, a stable visual reference, and how task state survives the transition. Read the immersive-experiences procedure before choosing detailed styles, boundaries, or transitions. Keep ordinary tasks in Shared Space where they work well.

Make system agency explicit: passthrough represents the real surroundings; the Digital Crown gives the person control over immersion. Do not design around preventing that control. If room understanding improves the experience, identify its user benefit and permission boundary rather than assuming access. Use Spatial Audio to convey useful spatial relationships, and consider SharePlay/spatial Personas only when a shared activity benefits from presence.

## Make the interaction physically sustainable

Choose the resting interaction first. Eye targeting plus indirect hand activation must work with hands in the lap or at the sides. Use direct manipulation for nearby, brief interactions; provide another way to complete sustained work instead of requiring raised arms or repeated reach. Standard components offer an accessible starting point; describe equivalent navigation and activation for custom spatial content with the platform's assistive methods.

Place important content within comfortable view for different heights and postures. In full immersion, bring useful content to the resting person rather than requiring turns or body repositioning. Remove abrupt, overwhelming, or unsupported camera movement; provide stable references. Use the spatial-layout and accessibility procedures for detailed placement and accommodation. “Relative to the head” is a placement consideration, not permission to lock content rigidly to it.

If the intended scenario involves vehicles, heavy machinery, hazardous walking routes, or users younger than the source's 13+ device guidance, identify the conflict and revise the scenario. Consult the current Apple device user guide for operational restrictions rather than presenting this overview as a complete safety specification.

## Produce and verify a spatial artifact

Deliver a task-to-presentation map and a concrete revised storyboard, screen/scene specification, or implementation. Include entry/return behavior for immersive moments, resting and alternative input paths, and relevant comfort checks. For reviews, locate each issue in supplied evidence and show its corrected spatial behavior; mark unobserved behavior as needing verification.

Walk the complete task in each chosen presentation. Fail if ordinary work unnecessarily requires immersion, the person cannot return with context intact, essential controls demand repeated reach/turns, or motion lacks a stable reference. Inspect semantics and alternative actions where available. Validate reach, comfort, eye/hand targeting, posture variation, and assistive use in a worn Vision Pro environment before claiming those results. Linux artifact checks and simulator/static review can support narrower claims only; list device checks still pending.

## Worked transformation

**Before:** A pottery catalog proposes a fully surrounding showroom for choosing glaze, reading care notes, and inspecting a vase. Care notes float behind the person; rotating a vase requires sustained raised-hand dragging.

**Decision:** Inspection benefits from depth; reading and catalog selection do not require stronger immersion. Repeated direct manipulation would fatigue the person.

**After:** A movable Shared Space window holds catalog, glaze choices, and notes. A selected vase appears in a volume beside the relevant controls, with indirect rotation and reset actions usable with resting hands. An optional surrounding exhibit becomes a separately chosen moment with an explicit return preserving the selected vase. The storyboard annotates posture, targeting, and return-state tests; physical comfort remains unverified until device testing.

## Conditional handoffs

When a task needs Full Space, continue with [Immersive experiences](../../../apple-hig-foundations/.topics/apple-hig-immersive-experiences/SKILL.md). For placement, scale, and depth use [Spatial layout](../../../apple-hig-foundations/.topics/apple-hig-spatial-layout/SKILL.md). For custom eye-targeted affordances use [Eyes](../../../apple-hig-inputs/.topics/apple-hig-eyes/SKILL.md); for an assistive alternative use [Accessibility](../../../apple-hig-foundations/.topics/apple-hig-accessibility/SKILL.md). Use [SharePlay](../../../apple-hig-technologies/.topics/apple-hig-shareplay/SKILL.md) only if the requested experience includes shared participation.
