---
name: apple-hig-generative-ai
description: Use when designing or reviewing generative features, AI disclosure, prompt scope, editable outputs, model availability, data transfer consent, or significant generated actions.
---

# Keep generation understandable and under the person's control

Read [Generative AI](../../references/generative-ai.md). Inspect the task benefit, actual model/data capabilities, input/output flow, significant actions, and requested design/review/adaptation. Preserve the existing stack; do not add generation just because a model is available. Separate measured model behavior from proposed safeguards and untested capability assumptions.

Decide whether generation is core or complementary. A complementary feature needs a usable non-AI path when unavailable; a core-AI product may need an honest unavailable/recovery experience instead of a fictitious equivalent. Check hardware/settings/network/battery conditions and explain limitations with useful varied examples. Disclose generated content/interaction so it is not mistaken for human authorship.

Choose local versus server processing from task capability, latency, privacy, and context needs. Explain what leaves the device, retention/training, and personal-data choices; obtain appropriate permission for sensitive reuse. Ask for needed context instead of inferring sensitive traits. Evaluate licensed/provenance-aware datasets and varied people/requests for stereotypes, misinformation, malicious/out-of-scope results, and copying risks.

Put Edit, Undo, Retry, or Adjust near outputs. Show actual ongoing work and recovery during latency/failure. Avoid automating destructive or hard-to-reverse operations such as deletion or purchase; generally obtain confirmation before significant action on a person's behalf. Narrow factual claims to verified current information where necessary. Plan voluntary feedback and reevaluation when models change.

**Before → decision → after:** A trip assistant silently sends personal notes to a server and books the first generated itinerary automatically. Decision: suggestions and purchases have different consequences. After, transfer/use are explained with appropriate choices, proposed itineraries are labeled and editable, and booking requires review/confirmation of the actual itinerary and cost.

Deliver a corrected generation/control/consent flow and evaluation acceptance criteria. Fail if outputs appear human-authored, unavailable generation blocks complementary work, or consequential actions occur without appropriate control. Static UI work cannot establish model safety, privacy, factual quality, or representative evaluation results; report actual datasets/tests and limits honestly.

Use [Privacy](../../../apple-hig-foundations/.topics/apple-hig-privacy/SKILL.md) for transfers and [Machine learning](../apple-hig-machine-learning/SKILL.md) for prediction rather than generation.
