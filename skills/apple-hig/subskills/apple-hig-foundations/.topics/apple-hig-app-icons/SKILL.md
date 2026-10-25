---
name: apple-hig-app-icons
description: Use when creating, reviewing, or adapting an app icon, its layered construction, platform mask, small-size identity, or appearance variants.
---

# Preserve an icon's identity through system treatments

Read [App icons](../../references/app-icons.md). Inspect the actual artwork/layers, target platforms, smallest appearances, and requested mode: design, review, or adaptation. If only a flat image exists, distinguish visible composition findings from unverified layer behavior. Produce the requested icon specification, revised assets, or scoped review; preserve existing tools unless a platform export requires another one.

Choose one identifiable concept and remove detail that cannot survive reduction. Decide which shapes need distinct foreground layers and which can remain a quiet opaque background. Supply unmasked artwork: the system supplies the rounded or circular mask. Leave highlights, bevels, and shadow treatment to the system unless an intentional custom effect has been checked for conflicts.

Select construction by platform. Use the guide's Icon Composer workflow for iOS/iPadOS/macOS/watchOS and image-stack workflow for tvOS/visionOS; consult its canvas/variant table rather than copying dimensions from a different platform. tvOS needs crop-safe layered foreground content during focus motion; visionOS should avoid a background hollow that system lighting could make appear raised. A Watch icon's black background must separate from surrounding display black. Keep identifying features stable through applicable dark, clear, tinted, or alternate variants.

**Before → decision → after:** A book-club icon is a pre-rounded screenshot containing a tiny “New” badge and five book titles. Small-size identity needs one silhouette. The corrected specification uses unmasked layers with a simple overlapping-book mark, an opaque background, and stable mark placement across appearance variants; temporary text moves into app content.

Deliver the layer/variant inventory with the corrected artwork or review. Fail if system masking removes the identifying mark, reduction erases it, or focus/lighting changes its intended shape. Actual Icon Composer/device previews are needed to establish parallax, material effects, and platform export quality; a raster mockup alone does not verify them.

For supporting image formats use [Images](../apple-hig-images/SKILL.md); for in-app glyphs instead of launcher identity use [Icons](../apple-hig-icons/SKILL.md); for brand consistency use [Branding](../apple-hig-branding/SKILL.md).
