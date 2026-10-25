---
name: apple-hig-dark-mode
description: Use when designing, reviewing, or adapting light and dark appearances, automatic appearance transitions, semantic surfaces, or mode-specific assets on supported Apple platforms.
---

# Adapt the hierarchy to appearance

Read [Dark Mode](../../references/dark-mode.md). Inspect supported platforms, semantic colors, elevated surfaces, asset variants, and live-switch behavior. This guide covers iOS/iPadOS/macOS/tvOS and marks visionOS/watchOS unsupported; do not impose its appearance model on those platforms. Choose design, review, or adaptation mode and distinguish rendered evidence from a proposed palette.

Start from system appearance rather than duplicating it with an app-only switch. If a permanently dark media context is proposed, establish the reason; do not turn that exception into a default for ordinary tasks. Define what happens when appearance changes while a sheet, selection, or text field is active.

Replace literal light/dark fills with semantic surface/text roles or matched custom color sets. Preserve base-versus-elevated distinction on iOS/iPadOS rather than mechanically inverting every value. Check custom glyph outlines and full-color artwork in both modes: reuse an asset if it works, otherwise provide variants under one identity. Reduce a bright image's harsh glow only when necessary without distorting its content.

Test Increase Contrast and Reduce Transparency independently and together. Use the guide's contrast targets for this scope; record actual color pairs and measurements. For Mac desktop tinting, a neutral custom surface may share subtle transparency, but colored states should not change meaning as wallpaper moves behind them.

**Worked transformation:** Before, a notes app inverts its white page to black but leaves fixed gray placeholder text and a white imported diagram. Decision: hierarchy and readable content must adapt together. After, system text/surface roles define the editor, elevated panels remain distinguishable, and a mode-appropriate diagram treatment avoids a glaring rectangle while preserving information.

Deliver corrected appearance tokens/assets or a review with precise failing pairs. Fail if runtime switching leaves a light-only element, an elevated panel merges into its parent, or accessibility settings reduce readability. A static palette cannot verify native vibrancy or desktop tinting; list those checks as pending.

Use [Color](../apple-hig-color/SKILL.md) for semantic role selection and [Images](../apple-hig-images/SKILL.md) when the problem lies in asset production.
