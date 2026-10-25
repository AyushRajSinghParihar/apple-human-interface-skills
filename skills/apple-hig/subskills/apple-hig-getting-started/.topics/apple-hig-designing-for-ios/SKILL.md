---
name: apple-hig-designing-for-ios
description: Use when creating, reviewing, or adapting an iPhone experience for handheld touch, interrupted use, orientation changes, and system entrypoints.
---

# Make the iPhone task usable in the hand

Read [Designing for iOS](../../references/designing-for-ios.md). Inspect the current task, its entry and return points, supported orientations, input, and any supplied implementation. Distinguish a brief check from extended work. For a review, anchor problems to supplied screens/behavior; for design or adaptation, revise the requested artifact in its existing stack.

Choose what must remain immediately visible during the task. A brief check needs its result and primary action close together; extended editing can expose additional controls without crowding the initial screen. Put frequent touch actions within comfortable reach, generally toward the middle/lower display, while preserving system navigation and swipe-back behavior. Move secondary commands into a short discoverable path rather than shrinking every control to fit.

Trace interruption and resumption: preserve the selected item, draft, or playback context when another app takes focus. Specify portrait/landscape and enlarged-text rearrangements without inventing a new navigation hierarchy for each orientation. Use touch and onscreen keyboard as the baseline, then offer appropriate voice or accessory paths. Add location, biometric, payment, or motion features only when their benefit reduces task effort and access is appropriate.

For repeated out-of-app actions, choose a relevant system entrypoint and a precise destination: a quick action starts an action, search opens the found content, and a widget exposes a useful glance. Do not add every entrypoint to every app.

**Before → decision → after:** A parcel app opens a dense desktop-style table and requires opening three menus to find the latest delivery. A handheld glance needs delivery state first. The revised home screen shows the active parcel and “Show pickup code,” keeps history one step away, and returns a widget tap to that parcel rather than a generic home screen.

Deliver a revised screen/flow or implementation plus interruption, orientation, and text-size acceptance checks. Fail if the primary action becomes unreachable, Back conflicts with a custom gesture, or resuming loses work. Screenshot review cannot establish touch comfort or actual system integration; state pending device checks.

For detailed adaptation use [Layout](../../../apple-hig-foundations/.topics/apple-hig-layout/SKILL.md); for custom touch gestures use [Gestures](../../../apple-hig-inputs/.topics/apple-hig-gestures/SKILL.md); for a chosen glance use [Widgets](../../../apple-hig-system-experiences/.topics/apple-hig-widgets/SKILL.md).
