---
name: apple-hig-images
description: Use when preparing, reviewing, or adapting image assets for Apple displays, densities, color profiles, TV parallax, or spatial photos and scenes.
---

# Match the image asset to its presentation

Read [Images](../../references/images.md). Inspect source dimensions, logical displayed size, supported densities/platforms, profiles, format, and whether the task is asset design, review, or adaptation. Preserve the chosen production pipeline where it can satisfy the requirements. Do not infer pixel quality from a filename or a scaled design preview.

Choose a format by content: scalable flat art/glyphs, photos, raster artwork, and stereo photos have different needs. Use the guide's platform density requirements and preserve embedded profiles. Calculate actual required pixels from logical points and density for 2D displays; visionOS points are angular, so distance and close inspection affect raster sufficiency. Balance higher resolution/filtering with file and runtime costs rather than maximizing every image.

For tvOS focus artwork, separate foreground information from supporting layers and provide an opaque background, crop-safe margins, and restrained depth. Distinguish bundled assets from downloadable runtime layers; `.lcr` is not the bundle format. For watchOS, flatten against a known solid background when possible, while retaining alpha for template imagery that must tint.

For visionOS stereo photos, preserve spatial metadata and choose presentation that permits comfortable depth adjustment. A generated spatial scene is a separate deliberate interaction; avoid generating many simultaneously or surrounding it with competing depth. Place photos/scenes in their own window/sheet where possible and keep immersive viewing UI restrained.

**Before → decision → after:** A TV gallery downloads a single transparent poster layer whose title clips when focused. Decision: focus movement needs a stable backing and safe foreground content. After, layered artwork uses an opaque background, separated title/subject, and enough crop margin verified through focus previews.

Deliver an asset/export manifest plus corrected assets or specific review. Fail if required-density output blurs at its intended size, profiles are absent, focus crops essential content, or stereo metadata is lost. Report file-level checks separately from actual TV/device/spatial comfort testing; Linux cannot establish the latter.

For launcher stacks use [App icons](../apple-hig-app-icons/SKILL.md); for color-space decisions use [Color](../apple-hig-color/SKILL.md); for spatial presentation use [Spatial layout](../apple-hig-spatial-layout/SKILL.md).
