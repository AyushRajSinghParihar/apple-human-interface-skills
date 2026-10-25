---
name: apple-hig-image-views
description: Use when choosing, reviewing, or adapting image display, fitting, overlays, animation frames, or image activation behavior.
---

# Separate image presentation from action

Read [the image-view guide](../../references/image-views.md). Use the following as application advice, preserving the requested stack.

Inspect the image assets and container, target platform, intended focal content, and whether the request is to create, review, or adapt. Determine whether the image is decorative, informative, editable, or an action. Record intrinsic resolution/aspect ratio, crop/fit behavior, overlays, and animation source when available; a screenshot cannot establish frame preparation or input semantics.

Choose fitting from the content's purpose: preserve the whole image when cropping loses information; allow deliberate cropping when the focal subject survives. Do not stretch photographs to satisfy a container. If activation performs an action, use button semantics rather than attaching an unexplained gesture to a display image. On Mac, choose an image well for copy/paste/drag/Delete editing. Prefer symbols or template imagery for interface glyphs rather than embedding their appearance as arbitrary pictures.

Apply the choice in code or supply an annotated container/asset specification; reviews must identify a crop, semantic, or legibility defect with a concrete repair. For text overlays, inspect both bright and dark image regions and provide supporting treatment where needed. Prepare animation frames consistently rather than depending on repeated runtime rescaling. For tvOS retain intended layered transparency; for visionOS choose a window image, spatial presentation, or scene mechanism deliberately instead of flattening every image. The guide mentions implementation capabilities, not proof that a supplied framework supports them.

**Worked transformation:** Before: a museum map stretches into a portrait card, with a “View route” gesture on the picture. Decision: distortion damages map meaning and the action lacks button behavior. After: fit the complete map within the card and provide a named `View Route` image/button action; decorative framing remains outside its accessible name.

Deliver the changed asset/container behavior and semantic purpose. Verify key content survives aspect changes, overlays remain readable, and actionable imagery works through keyboard/assistive activation. Fail for hidden essential content, stretched meaning, or an actionable image with no name/role. Report native spatial/layered rendering as unverified without its runtime.

Load [image-wells](../../../apple-hig-selection-and-input/.topics/apple-hig-image-wells/SKILL.md) for editing, [buttons](../../../apple-hig-menus-and-actions/.topics/apple-hig-buttons/SKILL.md) for action, or [images](../../../apple-hig-foundations/.topics/apple-hig-images/SKILL.md) for asset strategy.
