# Machine learning

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/machine-learning) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

An ML experience depends jointly on model behavior and interface design. Plan for changing data rather than a finite list of hard-coded outcomes.

<a id="Planning-your-design"></a>
## Planning your design
Define the model’s role, needed data, evaluation metrics, and intended experience together; model adjustments can take time, so design changes may require data/metric changes. Choose input patterns for calibration/feedback and output patterns for results, mistakes, and corrections deliberately.

<a id="The-role-of-machine-learning-in-your-app"></a>
## The role of machine learning in your app
<a id="Critical-or-complementary"></a>
### Critical or complementary
Determine whether the app works without the feature. Core functionality needs stronger reliability than optional suggestions; make fallbacks appropriate to dependency.

<a id="Private-or-public"></a>
### Private or public
Classify sensitivity and consequences of error. A mistaken health recommendation can be far more harmful than an unwanted song. Protect all data, with especially rigorous accuracy for sensitive uses.

<a id="Proactive-or-reactive"></a>
### Proactive or reactive
Unrequested proactive suggestions must meet a higher relevance bar to avoid intrusion; reactive assistance follows an explicit action and existing task context.

<a id="Visible-or-invisible"></a>
### Visible or invisible
Visible options let people judge reliability and provide feedback; invisible personalization needs another means to communicate and learn without demanding unnecessary choices.

<a id="Dynamic-or-static"></a>
### Dynamic or static
Some models improve live through use; others change with offline training/app releases. Match calibration and feedback expectations to that update model.

<a id="Explicit-feedback"></a>
## Explicit feedback
Request only necessary, voluntary feedback. Favorites/social reactions are implicit because they serve the person’s own purpose rather than a model-specific request. For explicit choices, explain concrete consequences in plain words, such as reducing a category or muting it for a time, rather than vague like/dislike alone. Icons may support descriptions but should not replace them. Offer progressively specific options if useful. Apply changes immediately and consistently across the app, persist them, and consider feedback about when/where a result is welcome as well as what it is.

<a id="Implicit-feedback"></a>
## Implicit feedback
Secure behavioral information and explain collection/sharing, particularly cross-app effects, with controls to restrict flow. Do not trap people in reinforced existing interests; preserve discovery and recognize confirmation bias. Combine signals because viewing/sharing does not prove positive sentiment. Suppress sensitive recommendations on shared accounts/devices. Favor recent feedback with historical fallback. Update on the feature’s expected cadence: typing assistance can be immediate while rapidly changing music recommendations undermine evaluation. Account for UI changes that alter interaction counts without changing preferences.

<a id="Calibration"></a>
## Calibration
Calibrate only when the feature cannot function without initial information. Explain benefit, collect essentials securely, and normally ask once early; object-based calibration may recur for new environments/equipment. Keep steps quick, avoid lookup-heavy questions/difficult actions, and infer secondary information where appropriate. Give clear goals/progress, immediate blame-free help if stalled, explicit success and an immediate path to the feature. Permit cancellation at any point without judgment or unnecessary cancellation messages. Let people update/delete supplied information outside recalibration.

<a id="Mistakes"></a>
## Mistakes
Anticipate errors and match recovery to their consequences. Make predictable mistakes easy to fix and update domain knowledge/preferences where doing so improves outcomes. Learning every mistake can also make behavior unpredictable, so judge its benefit. Use limitations, corrections, attribution, confidence, and feedback together to preserve trust rather than pretending errors cannot occur. Keep recovery simple: additional explanations can compound an error if, for example, their attribution is also wrong. Take extra care with proactive suggestions because people did not request them and may feel less control or tolerate fewer mistakes. Evaluate changes across categories and overall accuracy: improving recognition of one class can worsen another, so use people’s priorities to choose improvements and expect error patterns to change.

<a id="Corrections"></a>
## Corrections
Use familiar controls, exposing the automation’s choices where possible so people can refine them. Apply/persist a correction immediately and let it be corrected again. Keep correction effort below the value of automation; do not use endless correction as compensation for a poor model. Learn only where it improves results. Prefer guided alternatives when enough, with freeform controls for needs requiring flexibility.

<a id="Multiple-options"></a>
## Multiple options
Offer varied plausible choices for proactive suggestions, reactive next steps, and error correction. Balance diversity and accuracy, limit count to a scannable screen when possible, and rank the likely option first using validated confidence/context. Default selection can speed safe decisions. Explain meaningful differences and group large sets by category. Learn from choices where that improves the experience instead of repeatedly proposing known wrong options.

<a id="Confidence"></a>
## Confidence
Validate that confidence predicts actual quality before exposing or ranking by it, including across thresholds/model versions. Prefer understandable rationale, ordering, semantic categories, or actionable guidance over bare percentages. Numerical intervals make sense for statistical domains such as weather, sports, polling, and science. Vary presentation by confidence, perhaps asking confirmation for uncertain recognition, and suppress low-quality proactive results below a justified threshold.

<a id="Attribution"></a>
## Attribution
Explain the factual basis for a suggestion without technical model internals. Use it to build a mental model, distinguish options, explain mistakes, or guide useful behavior. Balance informative specificity with privacy and cognitive load. Describe observed behavior rather than judging emotion or beliefs; avoid jargon/statistics outside domains where they help.

<a id="Limitations"></a>
## Limitations
Distinguish weak capability from impossible tasks and design around both. Disclose rare serious limitations before reliance, using marketing or relevant context; minor limitations may be explained through attribution. Show useful input examples and contextual feedback, offer alternate paths rather than empty results, and explain conditions behind failures. Tell frequent users when a limitation is removed so they can try previously avoided actions again.

<a id="Platform-considerations"></a>
## Platform considerations
No additional platform-specific rules are provided.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/machine-learning) for linked Apple design assets and implementation resources.

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
Source revision dates: June 8, 2026, October 24, 2023, May 2, 2023.
