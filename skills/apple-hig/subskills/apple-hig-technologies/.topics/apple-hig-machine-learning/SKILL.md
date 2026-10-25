---
name: apple-hig-machine-learning
description: Use when designing or reviewing predictive features, personalization, calibration, recommendation confidence, feedback, corrections, attribution, and model limitations.
---

# Match automation and recovery to the consequences of error

Read [Machine learning](../../references/machine-learning.md). Inspect the model's task, data, validated quality metrics, update cadence, visible behavior, and requested design/review/adaptation. Preserve the existing stack. Do not infer actual accuracy, calibrated confidence, or privacy from a model name.

Classify the feature along the guide's consequential dimensions: critical/complementary, private/public, proactive/reactive, visible/invisible, and dynamic/static. A core sensitive function needs stronger reliability/recovery than an optional song suggestion; unsolicited recommendations need a higher relevance bar. Design fallbacks and disclosures accordingly rather than one generic error state.

Calibrate only when initial information is necessary. Explain the benefit, keep steps brief with progress/help/success, allow cancellation, and permit later update/deletion of supplied information. Separate voluntary explicit feedback from behavior that serves the person's own purpose. Explain feedback consequences concretely, apply/persist corrections promptly, and allow correction again. Do not force endless fixing to compensate for an unsuitable model.

Use multiple behavioral signals; viewing/sharing is not proof of approval. Protect sensitive recommendations on shared devices, preserve discovery beyond reinforced interests, and account for UI changes that alter counts. Before exposing confidence or ranking by it, validate its relation to quality. Prefer useful rationale/categories/alternatives over ungrounded percentages. Explain limitations before serious reliance and reevaluate tradeoffs when model changes shift errors among classes.

**Worked transformation:** Before, a music app treats opening a sad song as a lasting preference, shows “98% perfect,” and offers only a heart. Decision: behavior is ambiguous and confidence must be validated. After, diverse recommendations include a plain reason and specific voluntary actions such as “Less of this artist,” changes persist at an appropriate cadence, and unsupported numerical certainty is removed.

Deliver the role/error/feedback/calibration contract and an evaluation plan tied to actual consequences. Fail if corrections do not persist, unnecessary calibration blocks use or calibration blocks unrelated useful work, sensitive suggestions leak into shared contexts, or confidence is presented without validation. Static design does not establish model quality or representative evaluation outcomes; name actual evidence and pending tests.

Use [Generative AI](../apple-hig-generative-ai/SKILL.md) when creating content and [Privacy](../../../apple-hig-foundations/.topics/apple-hig-privacy/SKILL.md) for behavioral data flow.
