---
name: apple-hig-searching
description: Use when creating, reviewing, or adapting app, document, or system search strategy, suggestions, scope, history, and indexed-content destinations.
---

# Make the finding route match the content

Read [the searching guide](../../references/searching.md). This workflow is application advice; described Spotlight support specifically concerns iOS/iPadOS/macOS.

Inspect content corpus/metadata, query tasks, local/global scope, history privacy, platform, and create/review/adapt request. Obtain representative queries and actual result/deep-link evidence. Do not invent search relevance or index coverage without data.

Prefer a clear app-wide search while retaining justified local filtering. Give important search a prominent route and explicit scope. Offer useful recents/predictions/completions/filters to reduce entry, allowing history to be cleared because it can expose private intent. Define result identity and destination so selecting a match opens the exact content. For systemwide finding, index descriptive metadata and appropriate custom-file metadata/Quick Look support, respecting the source's platform boundary. Prefer standard Open/Save views for their built-in search instead of rebuilding an incomplete file finder.

Implement query/scope/history/index behavior, provide a corpus-to-query/result specification, or review concrete scope/relevance/privacy defects. Tie suggested filters to actual supported attributes rather than decorative chips that do nothing.

**Worked transformation:** Before: a notes app has three indistinguishable Search boxes, private recent queries cannot be cleared, and Spotlight results open home. Decision: scope and destination do not match finding intent. After: identify one app-wide entry plus clearly local filters, allow history clearing, and route indexed matches to the named note.

Deliver the artifact, scope, suggestions/filters, history policy, metadata, and destinations. Verify representative queries, no results, cleared history, deleted/index-stale content, and external result activation. Fail for unexplained scope, private history with no clearing, or wrong-content links. Index freshness/relevance and native Spotlight execution require actual runtime evidence.

Load [search-fields](../../../apple-hig-navigation-and-search/.topics/apple-hig-search-fields/SKILL.md) for entry placement or [file-management](../apple-hig-file-management/SKILL.md) for document metadata/preview integration.
