---
name: apple-hig-live-photos
description: Use when designing or reviewing Live Photo editing, playback identity, whole-asset preview/sharing, download readiness, or still-image fallback.
---

# Preserve the captured moment as one asset

Read [Live Photos](../../references/live-photos.md). Inspect asset support, edits, download state, preview/sharing, and requested design/review/adaptation. Preserve the existing photo pipeline. The source excludes watchOS; visionOS viewing is supported but capture is not. Do not promise Live Photo behavior where only still-image support exists.

Treat still, surrounding frames, and sound as one captured moment. If an edit can apply consistently to every frame, preserve the live asset; otherwise offer an explicit conversion to a still instead of silently editing only its poster frame. Do not split audio and frames into separate presentations that change the asset's identity.

Expose whole-asset preview before sharing and always provide ordinary-photo sharing. Define download progress and readiness so a live affordance is not shown as available before the data is usable. Use a subtle motion hint or a system badge when movement cannot demonstrate the content. Avoid a video-style play button; keep badges consistently placed without obscuring the image. Unsupported destinations should receive/show a still rather than a homemade approximation of Live Photo playback.

**Worked transformation:** Before, a filter changes only the thumbnail, sharing immediately sends motion the person has not previewed, and a large video Play triangle covers the image. Decision: edits and sharing must represent the complete captured moment. After, the filter applies across frames or offers clear still conversion, preview includes the whole live asset, and a subtle appropriate indicator distinguishes it while ordinary-photo sharing remains available.

Deliver an edit/readiness/preview/share state contract and corrected artifact or implementation. Fail if poster and motion edits disagree, sharing exposes unpreviewed content without a preview route, or an unsupported environment implies live playback. Actual asset preservation, sound/frame synchronization, export, and device playback need supported tests; static UI evidence proves only the designed states.

Use [Photo editing](../apple-hig-photo-editing/SKILL.md) for extension cancel/save behavior and [Images](../../../apple-hig-foundations/.topics/apple-hig-images/SKILL.md) for format/density work.
