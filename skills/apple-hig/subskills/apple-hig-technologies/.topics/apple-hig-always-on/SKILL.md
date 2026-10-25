---
name: apple-hig-always-on
description: Use when designing or reviewing dimmed iPhone Lock Screen or Watch wrist-down information, privacy redaction, subtle updates, and return to active interaction.
---

# Keep a glance useful while reducing exposure and activity

Read [Always On](../../references/always-on.md). Inspect the active view, sensitive values, ongoing activity, update frequency, and supported device/OS. Establish design, review, or adaptation mode. The snapshot describes specific iPhone Pro Lock Screen surfaces and Watch frontmost/background-session apps; do not infer universal device support. Other platforms are excluded here.

Classify information by usefulness and sensitivity in the dimmed context. Redact private balances, health details, and sensitive notification contents, while retaining expected activity context such as workout metrics or an arrival update where appropriate. Explain any contextual choice; do not redact everything so the view becomes useless or expose everything because it was visible during active use.

Preserve layout and control positions. Dim secondary fills/detail, simplify rich images/large color areas, and show unavailable controls rather than removing them. Primary information must remain legible. Ease ongoing animation toward rest and reduce update frequency to meaningful summaries, avoiding peripheral play-by-play on a face-up phone. Define the return to active interaction on tap/wrist raise with the same task context.

**Worked transformation:** Before, a Watch medication view leaves a bright detailed chart moving at wrist down, reveals the medication name on a shared desk, and removes buttons so rows jump. Decision: retain task continuity with less activity and sensitive exposure. After, the dimmed state keeps a stable “Next reminder” structure, applies appropriate redaction, rests the chart, dims secondary detail, and restores active controls in place when interaction resumes.

Deliver active/dimmed pairs with per-field redaction and update rules or implementation. Fail if sensitive values remain unintentionally exposed, primary information becomes unreadable, layout jumps, or background updates overwhelm a glance. Static state specifications cannot prove device dimming, wrist transitions, or energy behavior; list supported-device checks actually performed.

Use [Privacy](../../../apple-hig-foundations/.topics/apple-hig-privacy/SKILL.md) for exposure decisions, [Motion](../../../apple-hig-foundations/.topics/apple-hig-motion/SKILL.md) for settling movement, or [Designing for watchOS](../../../apple-hig-getting-started/.topics/apple-hig-designing-for-watchos/SKILL.md) for glance task scope.
