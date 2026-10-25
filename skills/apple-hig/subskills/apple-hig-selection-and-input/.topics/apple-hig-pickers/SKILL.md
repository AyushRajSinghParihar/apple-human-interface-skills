---
name: apple-hig-pickers
description: Use when creating, reviewing, or adapting ordered value choices, date or time entry, and multipart picker behavior.
---

# Match the choice structure to its scale

Read [the picker guide](../../references/pickers.md). This workflow is application advice; consult the source for supported date styles/modes rather than assuming every combination works.

Inspect the option count/order, value constraints, locale/calendar/time zone needs, platform/input, and create/review/adapt mode. Establish whether the task is selecting an instant, date, duration, or ordinary option. Record stored semantics separately from displayed formatting.

Use a picker for medium/long ordered lists, simpler controls for short sets, and searchable/indexed layouts for very large datasets. Put it near the edited value and arrange hidden choices predictably. For minute intervals choose a divisor of 60. On iOS/iPadOS select a supported date style/mode combination: countdown cannot use inline/compact and has a bounded duration. Let locale determine order instead of hardcoding month/day assumptions. On Mac choose textual precision versus graphical calendar browsing. On watch choose Crown-friendly wheels or navigation-link lists. Do not invent unsupported API behavior in the user's stack.

Implement the value/display/commit behavior, supply a concrete choice/date specification, or review exact constraint and locale failures. Define invalid/out-of-range incoming values without silently changing the person's meaning.

**Worked transformation:** Before: a scheduling form hardcodes month/day/year, uses 7-minute wheel steps, and offers a compact countdown. Decision: order must localize, minute steps must divide 60, and the chosen mode/style is unsupported. After: use locale ordering, a suitable interval such as 5 minutes, and an allowed duration presentation.

Deliver the artifact, ordered choices, stored semantics, bounds, and commit policy. Verify locale/calendar changes, boundary values, keyboard entry where supported, and edits/cancellation. Fail for a wrong date meaning, unreachable valid option, unsupported mode/style, or silent constraint violation. Separate logic checks from native calendar/Crown/keyboard execution.

Use [pop-up-buttons](../../../apple-hig-menus-and-actions/.topics/apple-hig-pop-up-buttons/SKILL.md) for compact single choice or [lists-and-tables](../../../apple-hig-layout-and-organization/.topics/apple-hig-lists-and-tables/SKILL.md) for very large sets.
