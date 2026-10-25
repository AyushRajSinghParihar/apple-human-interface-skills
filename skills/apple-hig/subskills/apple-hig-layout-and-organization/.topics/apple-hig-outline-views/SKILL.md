---
name: apple-hig-outline-views
description: Use when creating, reviewing, or adapting a macOS hierarchy table with disclosure, attributes, sorting, and retained expansion.
---

# Preserve ancestry while sorting and editing

Read [the outline guide](../../references/outline-views.md). This workflow is application advice; the source marks the conventional component macOS-only.

Inspect the data tree, columns, navigation/edit intent, platform, and create/review/adapt mode. Obtain duplicate names, deep branches, and the operations people perform. Verify actual hierarchy and expansion state from data/code rather than assuming indented rows are functional.

Use an ordinary table for flat data. For a hierarchy keep parent/child structure in the primary column and attributes in other columns. Give columns descriptive headings, resizing, and useful sorting. Sort within each hierarchy level so descendants never become unrelated peers; secondary criteria can resolve ties. Provide local and recursive expansion where helpful and restore expansion when returning. Define single-click edit versus double-click open behavior so they do not conflict. Add insertion/removal/reorder only when appropriate to the task.

Implement the requested outline, specify tree/sort/selection behavior, or review identifiable ancestry and operation defects. On other platforms adapt to supported list/split arrangements; the existence of a framework type does not override the source's component qualification.

**Worked transformation:** Before: sorting a project outline by size globally moves child files above their folders. Decision: attribute sorting must preserve ancestry. After: sort siblings within each parent, show size in its own titled column, and restore expanded branches after returning from a file.

Deliver the artifact and sibling-sort, expansion, and editing contract. Verify deep expansion/collapse, duplicate names, sorting reversal, resize, and selection after removal. Fail for orphaned descendants, lost branch state on routine return, or click behavior that edits instead of opening unexpectedly. Mark keyboard/VoiceOver execution unverified unless exercised.

Use [column-views](../apple-hig-column-views/SKILL.md) for traversal without attribute comparison or [split-views](../apple-hig-split-views/SKILL.md) for detail coordination.
