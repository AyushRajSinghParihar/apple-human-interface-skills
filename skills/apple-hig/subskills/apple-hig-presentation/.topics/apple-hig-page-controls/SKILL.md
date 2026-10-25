---
name: apple-hig-page-controls
description: Use when creating, reviewing, or adapting page-position indicators, discrete paging, scrubbing, and peer-page navigation.
---

# Show position among genuine peers

Read [the page-control guide](../../references/page-controls.md). This procedure is application advice; indicator interactivity varies by platform.

Inspect page structure/count, navigation gestures, target platform, and create/review/adapt mode. Determine whether pages are flat ordered peers, hierarchy, or unrelated destinations. Record current index and synchronization with content from code/prototype; filled dots alone do not prove navigation works.

Use a page control for peers and evaluate direct-access layouts beyond roughly ten pages. Keep indicator meanings simple, with at most two image types, and allow system contrast/color treatment. On iOS/iPadOS choose background style according to navigation importance; avoid scrubbing with minimal style because feedback is absent. Animate discrete movement but avoid flashing/lag from animated rapid scrubbing. On visionOS indicators communicate position without direct interaction. On TV use full-screen peers without interfering focus controls. On watch prefer purposeful vertical Crown pages, keeping most near one screen tall. The guide marks Mac page controls unsupported.

Implement the page/index/input contract, supply an annotated indicator/page specification, or review exact mismatch and reachability failures. Keep position updates coordinated when pages are inserted or removed.

**Worked transformation:** Before: a spatial gallery shows twelve clickable dots labelled as navigation and separately opens nested albums through those dots. Decision: the component is noninteractive on visionOS and hierarchy is not paging. After: use supported controls for albums and show a simple position indicator only for a manageable peer sequence.

Deliver the artifact with page identity/order, index, and supported movement. Verify first/last, rapid movement, changed page count, and alternate accessible navigation. Fail for a dot pointing at the wrong page, unavailable navigation implied as interactive, or essential pages unreachable without precision. Mark device scrubbing/Crown/gaze execution separately.

Load [scroll-views](../apple-hig-scroll-views/SKILL.md) for paged content or [tab-bars](../../../apple-hig-navigation-and-search/.topics/apple-hig-tab-bars/SKILL.md) for top-level destinations.
