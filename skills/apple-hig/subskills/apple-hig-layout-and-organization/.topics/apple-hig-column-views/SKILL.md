---
name: apple-hig-column-views
description: Use when choosing, reviewing, or adapting a macOS multi-column hierarchy browser.
---

# Keep the hierarchy path inspectable

Read [the column-view guide](../../references/column-views.md). Treat the following as application advice, not extra component guarantees.

Inspect the hierarchy, traversal frequency, sorting needs, target platform, and create/review/adapt request. Obtain representative deep branches, leaves, and long names. If only a mockup is available, distinguish its visible path from unverified selection/resizing behavior.

Use columns for deep hierarchies frequently traversed forward and backward when table-style attribute sorting is unnecessary. Put the root first. Selecting a parent reveals children in the next column; selecting a leaf can use the following area for a meaningful preview and metadata. Allow widths to expose long names instead of making truncation the only access. If attribute comparison/sorting dominates, choose a table/outline. This component is macOS-specific; for iPadOS/visionOS evaluate a split view rather than claiming native column-browser support.

Implement the hierarchy browser, produce a selection-to-column contract, or review concrete path/preview defects. Define what happens to downstream columns when the selected ancestor changes so stale descendants cannot appear associated with the new branch.

**Worked transformation:** Before: an asset browser starts at the most recent folder, and selecting a different parent leaves the former leaf preview visible. Decision: the path is ambiguous and preview identity is stale. After: restore a visible root-first path and clear/recompute descendant columns and preview on ancestor changes.

Deliver the artifact with root, parent/leaf rules, resize policy, and preview contents. Traverse sibling branches, return to root, resize a long-name column, and select a leaf. Fail for detached descendants, a preview of the wrong item, or no route to root. State native keyboard/accessibility traversal as unverified if not exercised.

Load [outline-views](../apple-hig-outline-views/SKILL.md) for sorted hierarchy attributes or [split-views](../apple-hig-split-views/SKILL.md) for supported cross-platform adaptation.
