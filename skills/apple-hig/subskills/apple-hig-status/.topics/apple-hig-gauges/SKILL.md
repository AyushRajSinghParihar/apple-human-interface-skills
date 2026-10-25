---
name: apple-hig-gauges
description: Use when creating, reviewing, or adapting a numerical value within a range, capacity display, or contextual level indicator.
---

# Explain the range as well as the value

Read [the gauge guide](../../references/gauges.md). The workflow is application advice; Mac level indicators and accessory styles have distinct capabilities.

Inspect the quantity, units, endpoints, scale, thresholds, platform, and create/review/adapt mode. Establish whether the value is a position, capacity, rating, or temporary work completion. Record true limits and freshness from evidence rather than guessing from a full track.

Choose positional versus filled-capacity presentation according to meaning. Supply concise descriptions of current value and both endpoints even when a style hides some visible labels, preserving accessible context. Use gradients/threshold colors only when they explain the range and pair essential meaning with text or another cue. On Mac select continuous capacity for large ranges that would make segments tiny; discrete units must remain wholly filled/empty. Ratings belong to their own topic. The source marks gauges unsupported on tvOS.

Implement the value/scale/labels or provide a gauge specification; reviews should identify the affected endpoint/mapping rather than vague visual polish. Do not turn an unknown scale into an authoritative “good/bad” range without domain evidence.

**Worked transformation:** Before: a storage gauge shows a red arc labelled `80` with no units or endpoints, and 1,000 tiny capacity blocks. Decision: capacity and threshold meaning are unreadable. After: show continuous `80 GB of 100 GB used`, explain the warning threshold, and expose numeric context without relying on red alone.

Deliver the artifact and quantity/range/style/threshold contract. Verify minimum, maximum, out-of-range/unknown input handling, compact layout, and noncolor meaning. Fail for reversed/unexplained scale, false precision, or unlabeled capacity. Distinguish accessible structure inspection from native announcements/rendering.

Load [progress-indicators](../apple-hig-progress-indicators/SKILL.md) for temporary work, [rating-indicators](../apple-hig-rating-indicators/SKILL.md) for ranking, or [widgets](../../../apple-hig-system-experiences/.topics/apple-hig-widgets/SKILL.md) for accessory contexts.
