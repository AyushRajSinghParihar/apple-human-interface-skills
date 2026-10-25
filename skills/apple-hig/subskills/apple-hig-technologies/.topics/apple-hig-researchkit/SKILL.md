---
name: apple-hig-researchkit
description: Use when designing or reviewing ResearchKit study onboarding, eligibility, informed-consent sequence, survey/active tasks, participant progress, or withdrawal access.
---

# Make study participation understandable before data access

Read [ResearchKit](../../references/researchkit.md). Inspect the approved study purpose, eligibility criteria, consent content, tasks, data needs, and requested design/review/adaptation. Preserve the existing research stack and supplied clinical/study content; do not invent ethics approval or consent sufficiency. The guide covers iOS/iPadOS, excluding other platforms.

Build onboarding in the source's order: introduction with a clear participation action and returning-participant sign-in; essential eligibility checks; informed consent; then critical device/data permissions. Ineligible people should not have to read a consent flow first. Use plain language and easy entry for criteria.

Break consent into understandable collection/use/risks/benefits/time/withdrawal sections with optional depth, allowing the whole form to be viewed before agreement. Follow agreement with necessary confirmation/signature/contact collection and an appropriate consent copy. Any quiz or signature mechanics must serve the actual study requirements; interface structure alone does not establish ethical/legal validity.

For surveys, show question count/duration and progress, choose response controls by answer type, use one question per screen, and confirm completion. For active tasks, explain action, timing, conditions, and endpoint clearly. Keep profile/progress accessible for changing participant information, upcoming work, consent/privacy information, and leaving the study. Encouragement should support continuation without hiding withdrawal.

**Worked transformation:** Before, a mobility study asks for Health access at launch, displays a dense agreement, then discovers ineligibility after ten questions. Decision: eligibility and understandable consent precede data access. After, the introduction explains the study, essential criteria resolve early, short navigable consent sections expose the complete form, and only eligible consenting participants encounter relevant permission requests and a clearly timed first task.

Deliver the onboarding/task/profile sequence or corrected implementation, distinguishing source content from proposed presentation. Fail if permission precedes meaningful consent context, eligibility is unnecessarily late, completion is ambiguous, or participants cannot find withdrawal/consent information. Actual consent review, ethics/legal approval, measurement validity, and device task performance remain separate evidence requirements.

Use [HealthKit](../apple-hig-healthkit/SKILL.md) for health-data access, [CareKit](../apple-hig-carekit/SKILL.md) for care-plan work, and [Writing](../../../apple-hig-foundations/.topics/apple-hig-writing/SKILL.md) for clear study language.
