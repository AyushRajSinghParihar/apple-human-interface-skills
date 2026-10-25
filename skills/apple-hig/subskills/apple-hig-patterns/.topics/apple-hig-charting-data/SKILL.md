---
name: apple-hig-charting-data
description: Use when deciding what a dataset should communicate visually, choosing overview and detail, or reviewing continuity across related charts.
---

# Turn the dataset into a visual argument

Read [the charting-data guide](../../references/charting-data.md). This workflow is application advice; distinguish computed evidence from interpretive claims.

Inspect the actual dataset, audience decision, existing artifact, platform, and create/review/adapt goal. Examine overview, meaningful groups, and individual observations before choosing a takeaway. Record provenance, aggregation, missing values, and uncertainty; do not invent a pattern from sample screenshots.

Use a chart when trends/comparisons/state matter; choose a table when searching/sorting records is the task. Prefer familiar visual language, teaching novel encodings only when justified. Start with a simple important insight, then reveal relevant subsets/detail. Size the chart to the intended interaction: a small snapshot can open an exploratory view. Preserve encodings, naming, and relative structure across views of the same dataset so zooming into detail does not require relearning. Supply both accessible explanation and interaction; a summary alone does not expose values.

Implement the requested overview/detail experience, produce a data-to-question/encoding specification, or review exact mismatch between claim and displayed evidence. The source adds no separate platform rules; adapt input/detail density without inventing platform restrictions.

**Worked transformation:** Before: a school attendance dashboard shows every student as a tiny mark, with a district average pie chart opening into an unrelated colored line chart. Decision: neither overview nor continuity explains the trend. After: present an evidence-supported attendance trend and takeaway, allow school/student drill-down, and retain consistent metric/series language across levels.

Deliver the artifact, computed takeaway, aggregation rationale, and overview-to-detail map. Verify the claim against data, subgroup meaning, selection continuity, and accessible value access. Fail for unsupported conclusions, inconsistent same-data encodings, or detail that changes metric silently. Report dataset computation separately from native chart/assistive execution.

Load [charts](../../../apple-hig-content/.topics/apple-hig-charts/SKILL.md) for marks/scales or [lists-and-tables](../../../apple-hig-layout-and-organization/.topics/apple-hig-lists-and-tables/SKILL.md) for record-oriented work.
