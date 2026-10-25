---
name: apple-hig-top-shelf
description: Use when creating, reviewing, or adapting Apple TV Top Shelf recommendations, previews, focus assets, fallback art, and content deep links.
---

# Showcase content that can be acted on

Read [the Top Shelf guide](../../references/top-shelf.md), including the chosen layout's asset specifications. The procedure is application advice for tvOS.

Inspect available content, relevance/resume state, licensing/purchase context, assets, target platform, and create/review/adapt mode. Determine whether familiarity permits a simple carousel or decision-supporting metadata is needed. Record actual Play/More Info destinations; artwork alone does not prove precise linking.

Favor fresh personalized content or meaningful resume/active content, not ads or prominent prices. Choose carousel actions/details, a sectioned row, or banners according to content. Use layered imagery and correct focused/unfocused safe zones from the reference, not a single arbitrary crop. For banners provide the supported image count, embedded text plus accessible equivalent, and cycling that stops on focus. Supply a static fallback, preserving its nonfocusable nature rather than drawing fake buttons on it. Keep large asset tables in the guide.

Implement content/asset/deep-link behavior or produce a layout/asset-state specification; reviews identify exact unsafe crop, missing identity, or wrong-target defects. Adapt outside tvOS using an appropriate supported showcase rather than claiming Top Shelf.

**Worked transformation:** Before: a streaming app's static fallback includes painted Play buttons, while every dynamic poster opens generic home. Decision: fallback is not interactive and dynamic selection should reach named content. After: use honest static showcase art and direct carousel Play/More Info links for fresh relevant titles, with focus-safe imagery.

Deliver the artifact, chosen layout, content policy, asset/fallback mapping, and destinations. Verify focus/unfocus crops, unavailable dynamic content, consumed-item policy, banner accessibility, and direct launch. Fail for fake fallback interaction, misleading purchase promotion, or deep links to the wrong item. Native Home Screen/remote preview behavior requires actual TV/client evidence.

Load [lockups](../../../apple-hig-layout-and-organization/.topics/apple-hig-lockups/SKILL.md) for in-app focus units or [playing-video](../../../apple-hig-patterns/.topics/apple-hig-playing-video/SKILL.md) for playback continuation.
