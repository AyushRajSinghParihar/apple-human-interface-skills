---
name: apple-hig-scroll-views
description: Use when creating, reviewing, or adapting overflow scrolling, reveal behavior, paging, zoom limits, and scroll-edge treatment.
---

# Keep hidden content reachable and location stable

Read [the scroll-view guide](../../references/scroll-views.md). The workflow is application advice; distinguish platform input capabilities from behavior actually enabled in the app.

Inspect overflow content, scroll axes/owners, selected or inserted content, floating controls, platform, and create/review/adapt intent. Record nested containers, indicators, zoom limits, and automatic reveal logic from evidence. A screenshot cannot prove gesture conflicts or Look to Scroll support.

Preserve system gestures/keys/elastic feedback and avoid same-axis nested scrolling; orthogonal nesting can be appropriate. Suggest offscreen content beyond transient indicators. Reveal search results, insertion points, and relevant selections only as far as necessary, preserving context. For paged content retain overlap/context and avoid a redundant same-axis scroll indicator when page controls serve that role. Bound zoom to useful scales.

Implement the scroll/reveal model or provide axis/ownership/position/edge-effect specification; reviews identify concrete unreachable or jumping content. Apply scroll-edge effects only where floating controls overlap content, generally automatic and one per view, with aligned split-pane heights. On TV scrolling follows focus. On watch favor vertical Crown content. On visionOS leave indicator space; Look to Scroll is per-view opt-in for suitable reading/browsing, requires clear boundaries and removal of custom parallax/scroll effects, and is unsuitable for precise secondary controls.

**Worked transformation:** Before: a long note scrolls inside a same-axis page scroller, and typing recenters the whole document on every character. Decision: competing owners and excessive reveal destroy location. After: use one primary vertical owner and scroll only enough to expose the insertion point, retaining surrounding lines.

Deliver the artifact and scroll-owner/reveal/zoom contract. Verify keyboard insertion offscreen, search reveal, selection extension, boundaries, and floating-control legibility. Fail for unreachable content, trapped input, excessive jumps, or claimed automatic eye scrolling. Separate source inspection from physical input, native effects, and eye-scrolling execution.

Load [page-controls](../apple-hig-page-controls/SKILL.md) for peer paging or [split-views](../../../apple-hig-layout-and-organization/.topics/apple-hig-split-views/SKILL.md) for independent pane scrolling.
