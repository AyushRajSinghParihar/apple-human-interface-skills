# visionOS research dashboard — revised layout contract

## Scope and assumptions

Repair the supplied layout: tall panels above/behind a seated person, critical text intersecting 3D objects, controls requiring a 2 m reach, and content rigidly following head turns. Room dimensions are unknown. This is a design specification, not a running implementation.

Preserve three research panels. Their names and roles were not supplied; assume Sources, Reading, and Notes as replaceable product labels. Preserve research data, selected source, reading position, and unfinished notes through every layout transition.

## Presentation and geometry

Use one movable, resizable standard window in Shared Space for ordinary research. Three panels are regions of that window, not three room-sized surfaces surrounding the person. Reading is primary; Sources and Notes support it. Full Space is unnecessary for this task.

Initial expanded layout proposal (product values, not Apple mandates): 1200 × 680 visionOS pt, with 24 pt outer insets, 24 pt gaps, and panel widths 240 / 624 / 240 pt. The usable panel height is 632 pt. Keep content within these bounds; long content scrolls inside its panel instead of growing upward, behind, or around the person. Do not shrink text to force a fit.

Use the system's initial window placement and user-controlled positioning. Aim for the active reading region centrally in the seated person's comfortable view. Do not prescribe a universal viewing angle or assume that 1200 pt fits every person's field of view. Provide an always-available “Compact layout” action: when selected, or when available width is below 1200 pt, show only the active panel with three labeled panel-selection actions. At widths below 480 pt, wrap these actions vertically. Each panel fills the remaining width and scrolls vertically. Never require horizontal room exploration to access a panel.

| Element | Anchor and scale | Depth / placement contract |
|---|---|---|
| Dashboard window and all reading/control surfaces | Stable in surrounding space; system dynamic window scaling | One coherent reading plane; no extruded text or independently floating glyphs. Sustained reading should normally be at least 1 m away; allow user positioning rather than enforcing a fixed distance. |
| Three panel regions | Local to dashboard window | Side by side in expanded mode; one active region in compact mode. No automatic placement above or behind the person. |
| Optional research 3D subject | Separate bounded inspection region in Reading, shown only by explicit “Inspect model” activation | Fit the object to its region, including rotation bounds. Its geometry must not enter text or control regions. Use consistent occlusion/shadow cues. Fixed physical scale is reserved for a justified life-size inspection task, not controls. |

While inspecting a model, replace the reading body with the bounded model view; keep the source title and “Return to reading” visible outside the object bounds. Returning restores the reading position. Supply a text description of the subject and labeled Rotate left, Rotate right, and Reset view actions outside the model bounds. Never place essential labels through or behind the model. Model inspection does not require walking around it or stronger immersion.

## Stationary interaction and state

- All selection, reading navigation, note entry, layout switching, model rotation/reset, and return actions must work while seated with hands resting in the lap or at the sides, using standard indirect targeting and activation. Remove the 2 m direct-reach requirement. Optional brief direct manipulation must never be the only path.
- Use standard controls and system hover feedback. For regular action buttons, use 60 × 60 pt activation bounds as the design starting point and at least 16 pt clear separation between bounds; this produces at least 76 pt center spacing for adjacent 60 pt buttons, also satisfying the spatial guide's 60 pt center-distance guidance. Hover regions must not overlap or displace neighboring targets. Looking alone never selects a source, edits notes, or changes stored state.
- Head turns change the person's view of stable content; they do not move the dashboard. No per-frame head-follow, automatic chasing, or automatic recentering. Preserve the system Digital Crown recenter behavior and standard window movement; do not recreate the system gesture.
- Expanded → compact: retain all panel state and show the most recently active panel, defaulting to Reading. Switching panels restores each panel's position and edits. Compact → expanded restores all three regions without resetting selection or model state. The user can retain compact mode at larger sizes.
- Unknown room dimensions must not block entry or trigger a room-sized arrangement. No room scan or floor/wall placement is required. If the arrangement feels too broad, compact mode and system positioning remain available without movement, calibrated room dimensions, or a permission grant. Do not infer clear physical space from virtual layout bounds.

## Reading and alternative access

Use platform text styles, with 17 pt body text as the starting point. Support at least 200% text enlargement without losing content or actions: reflow and use compact mode instead of clipping essential text. Controls have visible labels, accessible names/roles/states, and equivalent keyboard and supported assistive activation. Support hand/head Pointer Control and Zoom; neither depends on head-locked UI. Model actions provide an alternative to spatial dragging.

Keep layout changes immediate and stable; avoid automatic depth travel or peripheral animation. Preserve the same state under Reduce Motion. Actual accessibility behavior, target responsiveness, and seated comfort require implementation and Apple-environment testing.

## Source basis

These decisions apply the installed local HIG snapshot, without a web lookup:

- [Designing for visionOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos#Best-practices): standard windows, least necessary immersion, dynamic scaling, resting-hand interaction.
- [Spatial layout — Field of view, Depth, Scale, Best practices](https://developer.apple.com/design/human-interface-guidelines/spatial-layout): central important content, spatial anchoring, coherent depth, limited windows, target spacing, system recentering.
- [Eyes — Best practices](https://developer.apple.com/design/human-interface-guidelines/eyes#Best-practices): normally at least 1 m for sustained reading, standard hover and alternative input. This is reading-distance guidance, not a reach requirement.
- [Accessibility — visionOS](https://developer.apple.com/design/human-interface-guidelines/accessibility#visionOS) and [Vision / Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility): comfortable horizontal organization, no head lock, text enlargement and alternative activation.
