---
name: apple-hig-focus-and-selection
description: Use when designing or reviewing keyboard, remote, or controller focus navigation, persistent selection, directional reachability, or disappearing focused items.
---

# Keep the interaction target distinct from the chosen value

Read [Focus and selection](../../references/focus-and-selection.md). Inspect platform/input, focus groups, selected state, dynamic content, and supplied implementation. Establish design/review/adaptation mode. The guide's component-focus model excludes iOS/watchOS; visionOS gaze hover is a different system.

Map focus movement separately from activation and persistent selection. Focus may select automatically only when that does not unexpectedly shift context; tvOS normally needs separate activation. Use system effects and avoid moving focus without input. If an item disappears during discrete directional movement, choose a nearby one-step target; for other input, hide the indicator rather than inventing the next destination.

On iPad, group custom content so Tab moves among logical groups and arrows move within them in expected reading order; prioritize the likely entry item. Ordinary content focus coexists with Full Keyboard Access for all controls. On TV, every interactive item needs directional reachability and room for enlarged focus art. Keep unfocused, focused, pressed, selected, and unavailable states distinct. Full-screen gestures should manipulate visible content rather than invisible focus.

**Worked transformation:** Before, a TV watchlist opens each item as focus passes over it and uses the same glow for focus and Saved. Decision: navigation must not activate content, and persistent choice must survive focus movement. After, focus raises/highlights the item, Select opens it, and a filled saved indicator remains as focus moves; unavailable items are inactive and unreachable.

Deliver a focus-route/group map and state contract or implementation. Walk each entry, direction, activation, return, and removal scenario. Fail if a control cannot be reached/exited, focus jumps without input, selected state vanishes with focus, or enlargement obscures information. Source inspection can establish intended grouping; actual focus engines, remote behavior, and Full Keyboard Access need supported execution.

Use [Remotes](../apple-hig-remotes/SKILL.md) for TV button meanings, [Keyboards](../apple-hig-keyboards/SKILL.md) for shortcuts/access, or [Eyes](../apple-hig-eyes/SKILL.md) when the request actually concerns gaze feedback.
