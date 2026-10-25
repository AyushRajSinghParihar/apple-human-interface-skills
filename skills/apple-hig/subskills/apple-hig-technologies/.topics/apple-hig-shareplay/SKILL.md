---
name: apple-hig-shareplay
description: Use when designing or reviewing synchronized SharePlay activities, invitation/join routes, entitlement prerequisites, shared versus personal state, or visionOS participant arrangements.
---

# Synchronize the activity while preserving each person's control

Read [SharePlay](../../references/shareplay.md). Inspect the simultaneous activity, content entitlements, join/leave paths, shared state, supported platforms, and requested design/review/adaptation. Preserve the existing stack. Watch is unsupported; later asynchronous collaboration needs saved state or links rather than SharePlay alone.

Choose which state is shared. Watching/browsing can use synchronized views; a game may need individual roles. Invite through recognizable controls/system sharing with concise accurate art/title/description. Bring joiners directly to the content, deferring nonessential profiles/onboarding and using dismissible necessary prerequisites. Account for each person's required purchased/subscribed entitlement instead of assuming the host grants access.

Explain who changed shared state and how a playback pause affects everyone. Retain per-person volume/subtitle/accessibility settings and a clear leave/rejoin route. Support phone/tablet Picture in Picture or a continuing Mac playback window where relevant.

For visionOS, distinguish ordinary window mirroring from volumes/immersive SharePlay. Keep shared objects/sound in consistent relative locations, handle simultaneous tools predictably, and ask before immersion changes interrupt other work. Choose side-by-side, surround, conversational, or custom seating by activity. Keep seats stable, sufficiently separated, and independent of player roles where possible; nearby real people cannot be virtually moved. Provide alternatives when gestures/facial expression or spatial Personas are unavailable.

**Worked transformation:** Before, a shared sculpture lesson forces every joiner through profile creation, steals another participant's tool on selection, and moves seats whenever someone leaves. Decision: participation needs direct entry and predictable shared context. After, required content access is clear, the lesson opens immediately after minimal prerequisites, tool ownership follows an explicit rule, and stable positions remain while people leave/rejoin.

Deliver join/shared-personal-state/leave contracts and spatial arrangements when applicable. Fail if joiners land generically, one person's accessibility preference is overwritten, tool collisions are unpredictable, or seat changes disorient. Actual synchronization, entitlements, FaceTime/Persona behavior, and multi-device comfort require supported participants/devices; static artifacts cannot verify them.

Use [Immersive experiences](../../../apple-hig-foundations/.topics/apple-hig-immersive-experiences/SKILL.md) for immersion transitions and [Apple In-App Purchase](../apple-hig-apple-in-app-purchase/SKILL.md) for entitlement clarity.
