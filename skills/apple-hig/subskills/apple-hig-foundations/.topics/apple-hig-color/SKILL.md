---
name: apple-hig-color
description: Use when choosing or reviewing Apple-platform color semantics, custom palettes, contrast, Liquid Glass tint, color profiles, or cross-appearance color behavior.
---

# Assign color by meaning and viewing context

Read [Color](../../references/color.md). Inspect the actual foreground/background pairs, semantic roles, assets, appearances, and supported platforms. Establish design, review, or adaptation mode. Record unknown rendered colors instead of inventing contrast measurements. Preserve the current stack while expressing the requested palette or implementation change.

Classify each color as content, interactive accent, state, text, separator, or background hierarchy. Reuse semantic system roles where they fit; do not borrow a separator color for text or copy dated RGB swatches into production constants. Keep meanings consistent and pair important color distinctions with words/shapes/icons.

For custom colors, specify light/dark and increased-contrast variants, including local glass appearances even in a single-appearance app. Inspect resting and scrolled compositions against real underlying content. On glass, keep ordinary labels/symbols monochrome and tint sparingly for primary action or important status; prefer a colored primary-button background to colored button text.

Branch by context: honor user accents on Mac, use motion/scale as well as color for TV focus, check visionOS glass against varied surroundings without isolated glaring elements in darkness, and keep Watch complications useful in a single-color tint. For image fidelity, preserve embedded profiles and choose sRGB or appropriate wide-gamut assets based on actual display tests; do not assume two close P3 colors survive sRGB conversion.

**Before → decision → after:** A finance graph uses red/green lines and the same green for inactive labels and a Buy button. Decision: distinguish data from interactivity and retain meaning without hue. After, named/dashed series accompany color, neutral semantic labels describe values, and one accent marks the actionable control, with appearance-specific tested variants.

Deliver a role-to-color mapping plus corrected artifact. Fail if a noninteractive element resembles a link, a state disappears without color, or measured text/icon contrast falls short of the applicable guide. Report calculator inputs/results; hardware, ambient-light, TV-brand, or spatial-background claims require actual checks.

Continue with [Dark Mode](../apple-hig-dark-mode/SKILL.md) for appearance transitions, [Materials](../apple-hig-materials/SKILL.md) for glass surfaces, or [Accessibility](../apple-hig-accessibility/SKILL.md) for broader sensory access.
