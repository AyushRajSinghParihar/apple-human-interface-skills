# Generative AI

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/generative-ai) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Use generation or transformation only where it clearly improves creativity, communication, or task completion. Nondeterministic outputs need care throughout design, evaluation, and maintenance.

<a id="Best-practices"></a>
## Best practices
Consider direct/indirect effects on people and society, including unexpected outcomes from small input changes. Keep people in charge with dismissal, reversal, and retries, and disclose AI use. Avoid inferring sensitive personal/cultural traits; ask for needed information and test across varied people for stereotypes. Provide a usable non-AI route when generation is complementary or unavailable, while recognizing some core-AI experiences lack an equivalent substitute.

<a id="Transparency"></a>
## Transparency
Identify AI-generated interaction/content so it cannot be mistaken for human authorship, following applicable regional disclosure rules. Explain capabilities and limitations early with a short introduction or curated examples, and help people understand weak results.

<a id="Privacy"></a>
## Privacy
Weigh on-device speed, offline use, and privacy against server model capacity/context. Keep as much processing local as possible and minimize transfers; show what leaves the device and explain retention or training. Ask before using personal/usage information, provide opt-out, and obtain explicit permission for sensitive storage or improvement uses. Understand third-party privacy practices, recognize outputs can reveal sensitive data, and apply stricter child-data rules where relevant. Explain benefits, use, storage, and training in concise understandable consent information.

<a id="Models-and-datasets"></a>
## Models and datasets
Evaluate actual model/data capabilities early rather than assuming suitability. Availability can depend on hardware, network, battery, and settings; Foundation Models needs compatible hardware with Apple Intelligence enabled. Choose diverse, licensed training/evaluation data with known provenance and appropriate choices for personal data. Allow time to detect bias and misinformation in imperfect real-world datasets.

<a id="Inputs"></a>
## Inputs
Offer varied example prompts that teach useful scope. Explain that plausible-sounding output may be false. Narrow factual generation to verified current information and avoid generated claims where error could harm people. Assess whether errors or irreversibility would cause extra work or stress. Avoid automating destructive operations, such as deleting photos, and hard-to-reverse operations, such as making purchases for someone. Generally obtain confirmation before significant actions on a person’s behalf. Follow model policies and applicable local AI rules.

<a id="Outputs"></a>
## Outputs
Put Edit/Undo/Retry/Adjust near generated content and acknowledge corrections. When a result is blocked or poor, explain and coach a better request, with examples where useful. Test ambiguous, sensitive, controversial, out-of-scope, malicious, and underrepresented requests against policies. Reduce copying risks with protective models, curated/preapproved prompts, or instructions against imitation. Design for generation latency through useful loading or background work. Describe actual ongoing work instead of vague processing messages, and offer a clear recovery step on failure. Consider meaningfully different alternatives so people can choose an interpretation.

<a id="Continuous-improvement"></a>
## Continuous improvement
Plan data/policy updates, prompt tuning, retraining/fine-tuning, and full reevaluation when swapping base models. Provide voluntary, unobtrusive positive/negative feedback plus optional details for complex issues, and respond to reported problems. Keep model integration flexible enough for replacement without destabilizing the experience.

<a id="Platform-considerations"></a>
## Platform considerations
No additional platform rules are provided.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/generative-ai) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Videos"></a>
#### Videos
Apple’s linked design sessions provide demonstrations and additional implementation context; no video review is implied here.

<a id="Change-log"></a>
## Change log
Source revision dates: June 8, 2026, June 9, 2025.
