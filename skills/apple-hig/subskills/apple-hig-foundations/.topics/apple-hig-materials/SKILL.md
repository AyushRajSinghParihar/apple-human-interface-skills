---
name: apple-hig-materials
description: Use when selecting or reviewing Liquid Glass, translucent surfaces, vibrancy, background blending, or material hierarchy on Apple platforms.
---

# Choose a material for the layer's job

Read [Materials](../../references/materials.md). Inspect the underlying content, navigation/control layer, text density, platform, and supported appearance/preferences. Establish whether the request is design, review, or adaptation. Preserve the existing implementation approach; the following selection workflow is application advice informed by the guide.

Classify the surface first. Use Liquid Glass for important functional navigation/controls; organize ordinary content with standard materials rather than turning every content card into glass. Prefer standard controls' automatic behavior when available. For uncertain or visually complex backgrounds and substantial text, choose regular glass. Clear glass belongs over rich media; consider the guide's dimming treatment for bright content, but do not double-dim already-dark media or controls whose media framework supplies that treatment.

Choose content materials by separation and readability: thicker/opaque surfaces support fine detail, while thinner surfaces retain context. Match vibrant foreground roles to the chosen material rather than sampling a static color. On iOS/iPadOS, avoid low-contrast quaternary labels on the thinnest materials. On Mac, decide whether context calls for behind-window or within-window blending. On TV, select the overlay treatment appropriate to light/dark and partial/full coverage. On visionOS, preserve adaptive window glass and awareness rather than filling every window opaquely; there is no separate Dark Mode. Keep Watch modal-sheet backgrounds that explain layering.

**Before → decision → after:** A travel journal puts small captions on clear glass over changing bright photos. Decision: captions need stable separation; clear glass suits a few media controls. After, reading surfaces use an appropriate regular material with semantic text, while restrained clear controls remain above the photo with only necessary dimming.

Deliver a surface-role/material mapping and corrected artifact. Check representative underlying images, scroll positions, appearances, Increase Contrast, and Reduce Transparency. Fail if text loses contrast, content and controls become indistinguishable, or a material blocks necessary surroundings. Native vibrancy/spatial appearance require supported rendering; static tokens establish design intent only.

Use [Color](../apple-hig-color/SKILL.md) for foreground roles, [Dark Mode](../apple-hig-dark-mode/SKILL.md) for supported appearance changes, or [Immersive experiences](../apple-hig-immersive-experiences/SKILL.md) when preserving spatial surroundings is the main issue.
