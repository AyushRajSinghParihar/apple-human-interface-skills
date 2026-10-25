---
name: apple-hig-remotes
description: Use when designing or reviewing tvOS Siri Remote navigation, deliberate activation, playback/scrubbing, Back behavior, or compatible program-guide buttons.
---

# Preserve deliberate remote actions across browsing and playback

Read [Remotes](../../references/remotes.md). Inspect the TV hierarchy, playback/game state, remote mappings, and requested design/review/adaptation. This is tvOS-specific. Preserve the existing stack and distinguish a remote press from accidental surface contact or movement.

Map swipes to predictable directional focus/scrolling with corresponding feedback; strength can govern scrolling momentum. Use presses for deliberate activation. Avoid acting on taps during live playback because passing or resting a remote can produce them. Press-then-swipe enters scrubbing; preserve the relationship between gesture and visible media position.

Define Back by hierarchy and task state. In ordinary browsing, Back opens the parent, not necessarily the last screen visited; root returns Home. During gameplay, Back may open a pause menu, Back from that menu resumes, and an additional deliberate action can leave for the game menu. Holding Back retains its system Home behavior. Play/Pause must control active media; game-specific secondary/skip use needs appropriate context.

If an electronic program guide exists, guide/browse buttons open it and page buttons navigate it. During playback, those page requests change channels. Without a guide, preserve system routing to the default guide app rather than inventing unrelated meanings.

**Before → decision → after:** A streaming app treats every clickpad tap as Pause and makes Back jump to a recently searched page rather than the show's parent. Decision: accidental touches should not interrupt viewing and hierarchy must remain predictable. After, deliberate Play/Pause controls playback, presses activate, and Back from the episode returns to its show; guide/page behavior follows the active context.

Deliver a state-by-button/gesture mapping and corrected interaction artifact. Walk browse, play, scrub, pause, and return routes. Fail if incidental contact changes playback, Back strands the person or exits unexpectedly, or a program-guide button performs an unrelated action. Actual Siri Remote gestures, momentum, and across-room feedback need hardware testing; keyboard simulation is partial evidence.

Use [Focus and selection](../apple-hig-focus-and-selection/SKILL.md) for directional reachability or [Game controls](../apple-hig-game-controls/SKILL.md) for controller/menu consistency.
