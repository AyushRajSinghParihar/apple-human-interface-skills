---
name: apple-hig-gyro-and-accelerometer
description: Use when designing or reviewing motion-sensor input, fitness sensing, tilt gameplay, purpose explanations, or alternatives to gyroscope and accelerometer control.
---

# Use movement data for a task that benefits from it

Read [Gyroscope and accelerometer](../../references/gyro-and-accelerometer.md). Inspect the proposed sensor data, task benefit, active duration, platform, and existing input route. Establish design, review, or adaptation mode. Availability here covers Core Motion on iOS/iPadOS/watchOS and Siri Remote gyroscope data on tvOS; do not infer general Mac or visionOS availability from this source.

Separate sensing from direct UI control. Fitness feedback or active gameplay can justify real-time motion. Ordinary menus, forms, and navigation usually should not depend on precise device movement: it can be difficult to reproduce, physically inaccessible, and costly in battery use. If sensing does not change a meaningful result, remove the dependency rather than adding permission copy around it.

Define when collection starts and ends around the actual activity. Explain the specific use and reason for the first permission request. Provide an ordinary input or other accessible route to complete the task when motion is unavailable, declined, or unsuitable. For gameplay, state the mapping from motion to action and how the person can switch to an alternative without losing progress; calibration/range choices should follow the task and actual sensor evidence rather than invented universal thresholds.

**Before → decision → after:** A recipe app scrolls steps by tilting the phone, requires motion permission at launch, and offers no touch navigation. Decision: tilt precision is unnecessary for reading instructions. After, visible previous/next controls and normal scrolling complete the recipe; an optional motion-assisted cooking activity, if retained for a real benefit, requests access only when invoked and has an equivalent control path.

Deliver a sensing lifecycle and action mapping or a corrected non-motion interaction. Fail if routine navigation still requires movement, declined access blocks unrelated work, or sensing continues beyond its justified activity. Report source/code evidence separately from measured accuracy, latency, battery, and physical usability; those require supported hardware.

Use [Privacy](../../../apple-hig-foundations/.topics/apple-hig-privacy/SKILL.md) for permission purpose and minimization, [Game controls](../apple-hig-game-controls/SKILL.md) for alternate gameplay bindings, or [Accessibility](../../../apple-hig-foundations/.topics/apple-hig-accessibility/SKILL.md) for motor access.
