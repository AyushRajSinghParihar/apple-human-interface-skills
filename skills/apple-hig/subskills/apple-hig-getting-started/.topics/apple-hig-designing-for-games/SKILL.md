---
name: apple-hig-designing-for-games
description: Use when designing, reviewing, or porting a game across Apple platforms, including first play, display adaptation, input alternatives, and inclusive gameplay.
---

# Preserve the game while adapting how people play

Read [Designing for games](../../references/designing-for-games.md). Inspect the playable loop, first install, platform/input matrix, display assumptions, and accessibility options. Establish whether the request is a design, review, or port. Keep the engine/framework and game's identity unless the user authorizes a different scope.

Start with time to meaningful play. Include playable material in the initial install, use sensible defaults from the device/accessories/preferences, and teach actions in playable context. Move reference instructions out of the mandatory path. Request permissions when gameplay explains the benefit and ratings after meaningful play. Distinguish measured download time from the guide's target rather than inventing a network result.

For each target platform, map core actions to its normal input before adding controllers. Provide an alternative for players without a controller; watchOS does not share the source's physical-controller support. On touch devices, decide what can be manipulated directly and what needs an onscreen control. Do not copy a pointer game's tiny menus unchanged. Preserve safe areas and text/control readability across aspect ratios and supported orientations; resolve the guide's iOS control-size table/prose tension conservatively at 44 pt for touch rather than silently choosing the smallest value.

Review information channels and difficulty separately. Critical events need alternatives to color/sound alone; subtitles and adjustable mappings/motion/audio can preserve participation without changing the game's purpose. If cross-device progress, multiplayer, haptics, or purchases are in scope, choose relevant Apple integrations after the core loop works rather than adding every service.

**Before → decision → after:** A puzzle port waits for all later worlds to download, teaches through ten text pages, and requires a controller on iPad. Decision: the initial puzzle can teach direct tile manipulation immediately. After, one world ships locally, the first moves teach in context, touch selection and undo cover the loop, and a connected controller accelerates the same actions.

Deliver a revised first-play sequence and per-platform action/display contract or implementation. Fail if the first playable task is unnecessarily blocked, an advertised platform lacks a complete input route, or an essential cue remains single-sense. Report actual engine/device/controller testing separately from static review.

Use [Game controls](../../../apple-hig-inputs/.topics/apple-hig-game-controls/SKILL.md) for mappings, [Accessibility](../../../apple-hig-foundations/.topics/apple-hig-accessibility/SKILL.md) for accommodations, and [Game Center](../../../apple-hig-technologies/.topics/apple-hig-game-center/SKILL.md) for chosen social play.
