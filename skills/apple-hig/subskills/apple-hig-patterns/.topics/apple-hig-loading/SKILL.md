---
name: apple-hig-loading
description: Use when creating, reviewing, or adapting useful partial content, placeholders, background asset loading, and unavoidable waits.
---

# Keep useful content ahead of the wait

Read [the loading guide](../../references/loading.md). This workflow is application advice; timing and download availability require implementation evidence.

Inspect content dependencies, cached/partial data, asset sizes, initial interaction, platform, and create/review/adapt mode. Separate indispensable work from independent/background work and record measured waits when available. Do not infer duration or success from a skeleton screen.

Show useful structure promptly and replace placeholders as real content arrives. Keep other features usable while loading, retaining known content where appropriate. Schedule large assets nondisruptively with supported background mechanisms instead of blocking every startup. For unavoidable waits beyond a moment, communicate ongoing work and estimate only when measurable. Match optional engaging content to duration without a repetitive loop that disguises a stall. Games can use thematic loading, but truthful status/recovery still matters. On watch immediate content is preferable; brief indicators beat blank screens, while longer waits should not encourage wrist watching.

Implement content/dependency/loading states or provide a partial-content/placeholder/progress specification; reviews identify exact unnecessary blocking and misleading-placeholder defects. Define error/retry/available-data behavior according to the task rather than leaving a permanent fake skeleton.

**Worked transformation:** Before: a catalog blocks browsing until all preview videos download and replaces cached products with blank placeholders on refresh. Decision: independent assets should not remove useful content. After: show cached/current product information promptly, load previews in background, and give honest localized wait/retry feedback only for content that actually needs it.

Deliver the artifact, readiness/partial-content policy, asset schedule, and wait resolution. Verify slow/offline, partial success, refresh with existing data, retry, and completion. Fail for unnecessary whole-screen blocking, placeholders mistaken for real values, or an unresolved wait with no recovery. Report measured runtime timing separately from a proposed loading design.

Use [launching](../apple-hig-launching/SKILL.md) for startup or [progress-indicators](../../../apple-hig-status/.topics/apple-hig-progress-indicators/SKILL.md) for measurement and cancellation details.
