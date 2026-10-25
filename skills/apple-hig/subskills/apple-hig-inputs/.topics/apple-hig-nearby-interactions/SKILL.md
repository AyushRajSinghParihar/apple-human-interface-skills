---
name: apple-hig-nearby-interactions
description: Use when designing or reviewing compatible-device proximity tasks with Nearby Interaction, including distance/direction feedback, permission, degraded sensing, and alternatives.
---

# Guide a real proximity task through changing signal quality

Read [Nearby interactions](../../references/nearby-interactions.md). Inspect the intended nearby object/person, hardware capabilities, distance/direction use, activity context, and requested design/review/adaptation. Preserve the stack and verify device support before promising UWB. This source excludes macOS/tvOS/visionOS; Watch supplies distance only and participating watch apps must remain foregrounded.

Decide what proximity improves: finding an intended recipient, locating an object, or handing off audio is more useful than sensing for novelty. Combine distance, available direction, and task context before identifying a target; session-scoped identifiers are not permanent identities. Request appropriate permission while the app is in use and offer another way to complete the task.

Define feedback that becomes more precise as the person approaches and remains continuous while moving. Choose visual, sound, and haptic channels according to whether attention belongs on the display or surroundings. On iPhone, direction may disappear outside the sensor field while distance remains; do not replace a missing bearing with a confident invented arrow. Guide device holding implicitly where possible and explain degraded availability caused by obstacles/people when it affects the task.

**Before → decision → after:** A museum finder keeps pointing left after the direction signal disappears and blocks exhibit lookup when UWB is unavailable. Decision: uncertain bearing must not look authoritative, and finding information does not require sensing. After, the UI shows available distance with a clear direction-unavailable state and holding guidance, then restores directional feedback when valid; search/list selection remains a complete alternative.

Deliver a capability/signal-state feedback map and corrected artifact. Fail if distance-only data implies direction, loss of signal freezes misleading guidance, a Watch workflow assumes background participation, or the alternative cannot finish the task. Actual accuracy, sensor field, obstruction response, and haptic guidance require compatible hardware tests; mock data verifies state handling only.

Use [Privacy](../../../apple-hig-foundations/.topics/apple-hig-privacy/SKILL.md) for permissions and [Accessibility](../../../apple-hig-foundations/.topics/apple-hig-accessibility/SKILL.md) for feedback/input alternatives.
