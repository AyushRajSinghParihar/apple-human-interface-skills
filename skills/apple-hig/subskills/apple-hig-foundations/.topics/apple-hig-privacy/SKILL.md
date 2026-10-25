---
name: apple-hig-privacy
description: Use when designing or reviewing permission timing, purpose strings, pre-permission explanations, tracking requests, data minimization, or private platform inputs.
---

# Ask for precise access when its purpose is clear

Read [Privacy](../../references/privacy.md). Inspect the feature's actual data needs, transfers, storage, current permission flow, and supported platform. Establish design, review, or adaptation mode. Produce the requested copy/flow/data-handling changes in the existing stack; distinguish documented platform restrictions from additional application recommendations.

Map each requested category to a specific feature and minimum necessary scope. Remove collection without a concrete benefit; prefer on-device work where it avoids unnecessary transfer. Explain collection/use accurately and flag App Store disclosure updates needed when behavior changes. Respect private email and tracking choices rather than designing around them.

Ask when the person invokes the feature. Launch-time requests need an essential, obvious dependency. Write a short active purpose sentence explaining use and reason. If context is sufficient, omit a custom pre-alert; if explanation is essential, use one clear continuation to the real system alert without imitating Allow/Don't Allow. Keep the guide's special pre-alert restrictions distinct from ordinary onboarding. Tracking requires its system authorization before collection and must not be incentivized or manipulated.

Choose one-time location access for suitable individual tasks using the system location button on supported platforms; preserve permitted customization and all localized/accessibility-sized text. Protect secrets with established authentication/keychain mechanisms. For Mac, account for sandboxing/distribution and fast user switching. For visionOS, separate system rendering assistance from permission-gated Full Space ARKit data; gaze remains private, and imported phone-camera assumptions may need removal or content import.

**Before → decision → after:** A bird journal asks for contacts, microphone, and continuous location at launch although only “Attach current location” uses location. Decision: request only the specific action's needed access. After, journaling works immediately; the attachment action offers the supported location control, and its purpose explains adding the sighting's location.

Deliver a data-purpose/access matrix and corrected permission sequence/copy or implementation. Fail if collection precedes required consent, copy obscures the real use, or unrelated work is gated on optional access. Report code/flow evidence separately from actual authorization prompts and privacy-setting behavior; this procedure does not certify security or legal compliance.

Use [Sign in with Apple](../../../apple-hig-technologies/.topics/apple-hig-sign-in-with-apple/SKILL.md) for that authentication choice and [Augmented reality](../../../apple-hig-technologies/.topics/apple-hig-augmented-reality/SKILL.md) when room/camera access is essential.

For health-related work, finish the domain decisions as well as the permission
sequence. Read [CareKit](../../../apple-hig-technologies/.topics/apple-hig-carekit/SKILL.md)
for care plans, scheduled treatment tasks, or symptom/event recording;
[HealthKit](../../../apple-hig-technologies/.topics/apple-hig-healthkit/SKILL.md)
for health-data access and sharing; and
[ResearchKit](../../../apple-hig-technologies/.topics/apple-hig-researchkit/SKILL.md)
for study participation and research consent. These experience procedures help
choose task, data, and consent behavior in the existing stack; consulting a
framework-named topic does not require adopting that SDK. General privacy,
language, and accessibility guidance alone does not resolve those domain choices.
