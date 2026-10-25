---
name: apple-hig-ratings-and-reviews
description: Use when creating, reviewing, or adapting App Store review request timing, eligibility, standard prompts, and rating-summary decisions.
---

# Ask at an earned stopping point

Read [the ratings/reviews guide](../../references/ratings-and-reviews.md). This workflow is application advice; requesting the system prompt does not guarantee its presentation.

Inspect real engagement signals, task boundaries, prior candidate requests, target platform, and create/review/adapt goal. Distinguish asking for an app review from editing a content item's rating. Do not invent engagement or claim users saw a prompt merely because an API was invoked.

Choose demonstrated use and a natural stopping point after value, never first launch/onboarding or midtask/gameplay. Space candidate requests and require further engagement rather than repeatedly asking after every event. Prefer the standard prompt on the documented iOS/iPadOS/Mac platforms so system opt-out, feedback history, and frequency limits apply. Treat display as system-controlled, retaining normal functionality when no UI appears. Evaluate summary reset as a tradeoff between current-version relevance and visible volume rather than automatically resetting each release. The source adds no separate other-platform rules; verify API availability instead of extrapolating.

Implement the eligibility/request logic, provide a trigger/cadence/suppression specification, or review concrete interruption/overrequest defects. Do not submit ratings or publish a release reset without authorization.

**Worked transformation:** Before: a puzzle requests a rating at first launch and every failed level, then blocks Continue until the prompt appears. Decision: no demonstrated value or natural stop exists, and display is not guaranteed. After: consider a spaced request after meaningful completed play, keep continuation independent of prompt display, and respect system suppression.

Deliver the artifact, engagement trigger, timing, cadence, and no-display path. Verify fresh users, interrupted tasks, recent request, opt-out/no prompt, and ordinary continuation. Fail for coercive blocking, repeated midtask asks, or guaranteed-display claims. Actual StoreKit presentation/account feedback remains unverified without native client evidence.

Load [onboarding](../apple-hig-onboarding/SKILL.md) for first use or [rating-indicators](../../../apple-hig-status/.topics/apple-hig-rating-indicators/SKILL.md) for content-item rankings.
