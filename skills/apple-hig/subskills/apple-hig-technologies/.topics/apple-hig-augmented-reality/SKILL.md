---
name: apple-hig-augmented-reality
description: Use when designing or reviewing AR placement, coaching, object manipulation, relocalization, environmental feedback, or appropriate AR entrypoints and badges.
---

# Keep virtual objects grounded through placement and recovery

Read [Augmented reality](../../references/augmented-reality.md). Inspect device capability, optional versus AR-first task, surface/environment needs, object scale, and interruption behavior. Establish design/review/adaptation mode and preserve the existing AR stack. Most guidance here concerns iOS/iPadOS; visionOS needs its Full Space/privacy model rather than a phone camera flow.

Decide whether AR is essential. Require capable hardware for AR-first work; hide an optional unavailable feature instead of presenting repeated capability errors. Explain usable surroundings in ordinary language. Prefer system coaching for initialization/surface discovery/relocalization and hide unrelated UI during it.

Show an aligned placement indicator, place using current estimates, then refine gently. Do not depend on exact detected edges. Choose direct familiar manipulation with larger reasonable hit proximity for thin/distant objects and stationary indirect controls when touching is difficult. Keep realistic products at meaningful scale; enlarging a far object does not bring it closer. Preserve perspective, plausible light/shadow, and surface attachment as objects move.

Design explicit loss/recovery paths: interruption may require coaching and hiding unstable old objects; provide reset/cancel instead of indefinite relocalization. Explain lighting, texture, or slower-movement remedies without tracking jargon. If physical-image recognition is used, avoid flicker on brief disappearance and manage active reference sets appropriately. For shared AR, plan late joining/map merging and convincing people occlusion where applicable.

**Worked transformation:** Before, a furniture preview waits indefinitely for a perfect floor edge and leaves the chair floating after a call. Decision: estimated placement plus honest recovery is more useful. After, a floor-aligned indicator permits initial placement, the chair refines gently, and returning from interruption uses coaching with reset/cancel until the prior placement is stable.

Deliver a placement/manipulation/recovery storyboard or implementation. Fail if objects jump or detach, uncertain placement appears reliable, recovery cannot end, or movement demands unsafe/fatiguing use. Geometry and simulated tracking do not establish real surface quality, latency, performance, or physical comfort; report actual device checks separately.

Use [Gestures](../../../apple-hig-inputs/.topics/apple-hig-gestures/SKILL.md) for manipulation alternatives and [Privacy](../../../apple-hig-foundations/.topics/apple-hig-privacy/SKILL.md) for spatial/camera access.
