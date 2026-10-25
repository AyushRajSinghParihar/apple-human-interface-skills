---
name: apple-hig-launching
description: Use when creating, reviewing, or adapting startup, launch screens, first usable content, restoration, and launch-to-task continuity.
---

# Make the first usable screen the launch outcome

Read [the launch guide](../../references/launching.md). This workflow is application advice; timing claims require measurement and launch screens apply only to specified platforms.

Inspect startup dependencies, first usable state, prior-state restoration, launch destinations, platform/orientation, and create/review/adapt mode. Distinguish launch from onboarding and initial downloads from readiness. Record measured time if available; do not call an unresponsive splash “launched.”

Remove unnecessary blocking work and provide useful interaction promptly. On iOS/iPadOS/tvOS match the static launch screen closely to first content/appearance/orientation to avoid flashes; omit unlocalized text and branding absent from the first screen. Place necessary branded splash/onboarding after launch rather than extending launch imagery. Restore meaningful prior detail, scroll, and window configuration. On TV use static rather than layered launch imagery. On visionOS consider an initial Shared Space window with explicit Full Space transition; Mac/watch/visionOS do not require the launch-screen component.

Implement the startup/restoration route, produce a dependency/first-screen/state specification, or review exact delay/mismatch defects. Preserve shortcut/deep-link intent so restoration cannot replace a newly requested target.

**Worked transformation:** Before: a recipe app shows a branded slogan until every photo downloads, then opens home instead of the previously read recipe. Decision: startup blocks useful content and loses continuity. After: match launch imagery to a usable initial structure, load nonessential photos progressively, and restore the recipe/scroll position unless a fresh external task overrides it.

Deliver the artifact, readiness definition, deferred work, launch-screen mapping, and restoration precedence. Verify cold/warm start, no network, rotation, appearance, prior state, and external launch target. Fail for false readiness, flash-inducing mismatch, lost task identity, or branded launch delay. Report measured versus estimated timing and actual native launch execution separately.

Load [loading](../apple-hig-loading/SKILL.md), [onboarding](../apple-hig-onboarding/SKILL.md), or [app-shortcuts](../../../apple-hig-system-experiences/.topics/apple-hig-app-shortcuts/SKILL.md) for the next stage.
