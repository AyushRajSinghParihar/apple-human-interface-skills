---
name: apple-hig-lists-and-tables
description: Use when creating, reviewing, or adapting text rows, multicolumn comparisons, selection, sorting, and row editing.
---

# Give row selection one understandable meaning

Read [the list/table guide](../../references/lists-and-tables.md). The workflow is application advice; apply only the destination's documented conventions.

Inspect representative data, row/column structure, target platform, and create/review/adapt mode. Identify whether rows navigate, choose an option, support editing, or compare attributes. Capture the actual selected item, sort order, and available edit operations; do not infer them from row color alone.

Use lists for scanning text and multicolumn tables for useful comparisons; choose collections for image-heavy variable items. Keep navigation selection visible, while a chosen option may use a persistent checkmark after brief highlight. Distinguish an info button from a hierarchy disclosure. Put long prose in details and preserve identifying string ends where truncation is necessary. Give columns meaningful noun headings.

Implement/specify row behaviors and useful editing, including reorder when relevant. On iOS/iPadOS use appropriate edit mode and avoid section-index collisions with trailing controls. On Mac allow useful heading sorting/reversal and resizing; choose an outline for hierarchy. On tvOS leave room for focused row imagery effects. On watch show relevant items first while preserving access to the expected full dataset; do not silently omit owned items or use page-to-page gestures that conflict with scrolling details.

**Worked transformation:** Before: a watch subscriptions list shows only five recent feeds and permanently hides the rest. Decision: brevity must preserve the expected dataset. After: show relevant feeds first and a clear route to all subscriptions; each row opens its own detail while the current path remains understandable.

Deliver the artifact plus selection/edit/sort contracts. Verify empty and long lists, narrow identifiers, sorting reversal, selection after deletion, and all-items access. Fail for misleading selection feedback, wrong detail identity, unusable column width, or silently lost items. Separate static checks from native focus and assistive traversal.

Use [collections](../apple-hig-collections/SKILL.md) for visual content or [outline-views](../apple-hig-outline-views/SKILL.md) for Mac hierarchy.
