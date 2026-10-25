---
name: apple-hig-search-fields
description: Use when creating, reviewing, or adapting search entry placement, scope, suggestions, clearing, and token or category refinement.
---

# Make search scope visible before entry

Read [the search-field guide](../../references/search-fields.md). This workflow applies the source; query policy and implementation details remain application decisions.

Inspect searchable content, navigation, platform/input, window sizes, and create/review/adapt mode. Establish global versus local scope, directed lookup versus discovery, and actual query/result behavior. Record placeholder, clear/cancel, suggestions, selected result, and keyboard activation from evidence.

Choose entry placement from scope and priority: local fields beside their content, dedicated discovery areas for browsing, and rapid focused entry for directed lookup. Explain scope in the placeholder and start broad before deliberate narrowing. Offer useful predictive/recent queries and teach token filters through suggestions. Prefer results during typing when feasible, but do not promise instant remote search without data/latency evidence.

Implement the field and query/refinement states or specify placement/scope/focus/result behavior; reviews must trace a misleading query or route. On iPad/Mac coordinate search with split-view selection and resizing. A dedicated iPad discovery area should not unexpectedly open its virtual keyboard. On iOS distinguish persistent search tab from transient button-style search returning to the prior tab. On TV reduce remote entry with suggestions; on watch preserve return after fullscreen Search/Cancel.

**Worked transformation:** Before: `Search` above a sidebar silently searches the whole library, then opens a keyboard over the iPad discovery grid. Decision: placement implies local navigation filtering and automatic focus obscures discovery. After: label a local sidebar search explicitly or move global search to a dedicated area; leave discovery unfocused with a virtual keyboard.

Deliver the changed artifact and scope/focus/clear/selection contract. Verify clearing, category changes, no results, returning from detail, and compact resize. Fail for unexplained scope changes, stale results presented as the current query, or lost result identity. Distinguish native keyboard/input execution from inspected handlers.

Load [searching](../../../apple-hig-patterns/.topics/apple-hig-searching/SKILL.md) for result strategy or [token-fields](../apple-hig-token-fields/SKILL.md) for Mac token entry.
