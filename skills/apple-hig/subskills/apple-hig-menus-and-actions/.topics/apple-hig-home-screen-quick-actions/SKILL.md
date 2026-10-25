---
name: apple-hig-home-screen-quick-actions
description: Use when designing, reviewing, or adapting iOS and iPadOS app-icon shortcuts and their dynamic destinations.
---

# Make app-icon shortcuts land precisely

Read [the quick-action guide](../../references/home-screen-quick-actions.md). Treat the workflow as application advice; the documented component belongs to iOS/iPadOS.

Inspect high-value launch tasks, recent/context data, existing deep links, target platform, and create/review/adapt request. Identify whether actions are stable or dynamic and what happens if their referenced content disappears. Do not claim recent-item ordering or launch resolution is verified from labels alone.

Choose up to four useful shortcuts, preferably at least one when the app has a suitable task. Use concise outcome-oriented titles without app-name filler, adding a subtitle only to clarify. Prefer SF Symbols or template-derived monochrome glyphs rather than emoji. Update dynamic actions predictably from context and keep identity/destination consistent. Separate action dispatch from merely opening the app; a shortcut must resolve to its named task, including after a cold launch. These resolution details are application decisions to specify explicitly.

Implement the shortcut set/handlers, supply an action-to-destination specification, or review concrete wrong-target and stale-action defects. For Mac adaptation evaluate Dock menus; do not assert Home Screen quick actions exist on unsupported platforms.

**Worked transformation:** Before: a journal app offers six emoji-labelled actions including a deleted recent entry and `Open Journal App`. Decision: shortcuts should accelerate meaningful tasks, with reliable targets. After: keep `New Entry`, `Search Entries`, and valid recent entries within four actions; use meaningful monochrome icons and refresh stale references.

Deliver titles/subtitles/icons, update policy, and warm/cold destination behavior. Verify long localization, changed account, removed recent content, and interrupted launch resolution. Fail for exceeding the supported design limit, misleading destination, personal content from a former account, or a shortcut that only opens a generic home screen. Mark device Home Screen execution separately from handler inspection.

Load [launching](../../../apple-hig-patterns/.topics/apple-hig-launching/SKILL.md) for launch continuity or [dock-menus](../apple-hig-dock-menus/SKILL.md) for Mac entry points.
