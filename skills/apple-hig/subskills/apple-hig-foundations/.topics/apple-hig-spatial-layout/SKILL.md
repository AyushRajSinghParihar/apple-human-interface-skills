---
name: apple-hig-spatial-layout
description: Use when designing or reviewing visionOS field of view, depth, scale, window/object placement, spatial target separation, or stationary interaction.
---

# Place spatial work within comfortable view and reach

Read [Spatial layout](../../references/spatial-layout.md). This guidance is visionOS-specific. Inspect scene/window relationships, task duration, expected posture/movement, and supplied spatial dimensions. Establish design, review, or adaptation mode; retain the chosen implementation stack. A flat mockup does not establish perceived depth, reach, or comfort.

Choose an anchor and scale model for each object. Interactive windows generally benefit from dynamic scaling that preserves apparent size at distance. Fixed scale suits genuinely life-size, primarily noninteractive objects; explain that choice rather than using it for all controls. Anchor content to space, not rigidly to the head. Do not invent a universal field-of-view angle: the system does not expose its dimensions and people vary.

Use depth to clarify important relationships with consistent occlusion/shadow/distance cues. Keep reading surfaces and tiny glyphs free of unnecessary extrusion or floating depth. Avoid rapid/repeated refocusing across distances. Limit window count and bring the needed work into central comfortable view without blocking surroundings.

Design stationary indirect interaction first, with hands resting; nearby brief direct manipulation is a separate choice. For regular buttons, check the guide's 60 pt center spacing and 16 pt gap, plus distinct target/hover regions. Preserve system recentering instead of implementing a competing gesture. Floor-based large content should align to a flat plane matching the real floor.

**Before → decision → after:** A model viewer places every command on fixed-scale tags around a room-sized machine and requires walking behind it to reset. Decision: inspection may need real size, but commands need stable accessibility. After, the machine retains justified physical scale, an adjacent dynamically scaled control surface offers rotation/reset from rest, and essential labels stay in readable, coherent depth.

Deliver an anchor/scale/depth map and corrected scene specification or implementation. Fail if essential targets overlap, routine work requires repeated turns/reach, or position/scale changes destroy readability. Report source-level geometry separately from worn Vision Pro validation across postures; Linux cannot verify spatial comfort.

Use [Eyes](../../../apple-hig-inputs/.topics/apple-hig-eyes/SKILL.md) for targeting, [Immersive experiences](../apple-hig-immersive-experiences/SKILL.md) for scene transitions, or [Typography](../apple-hig-typography/SKILL.md) for spatial labels.
