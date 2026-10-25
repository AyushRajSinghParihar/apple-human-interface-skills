# Search repair decisions and evidence

Edited interface.md in place, replacing the supplied one-sentence failure description with an implementable iPhone search contract. The patch specifies visible downloaded-document scope and filters, generation-guarded asynchronous work, retained queries on zero matches, local search while offline, distinct indexing/error states, and clear/dismiss/detail-return behavior.

## Decisions

- Search downloaded titles and available extracted text independently of the network. This is an explicit scope decision for an offline archive; the supplied file gives no evidence of remote search requirements or OCR coverage.
- Invalidate obsolete work on every relevant state change and reject stale success and error callbacks. A 200 ms typing debounce reduces work; it is tunable and does not replace correctness guards.
- Preserve raw text on zero matches and expose removable filters. Fresh sessions start broad; detail return restores the same visible search context.
- Keep partial indexed results useful and qualify incomplete coverage. Distinguish search failure from zero results and offer Retry.
- Use stable document identity for opening results. Define unavailable-document recovery rather than redirecting silently.

Apple’s local guidance supports [clear scope and prominent search](https://developer.apple.com/design/human-interface-guidelines/searching#Best-practices), [typing updates and deliberate refinement](https://developer.apple.com/design/human-interface-guidelines/search-fields#Scope-bars-and-tokens), and [useful content during loading](https://developer.apple.com/design/human-interface-guidelines/loading#Best-practices). The precise race-control algorithm, matching policy, timing, and session rules are product decisions, not universal HIG mandates.

## Worked before/after

Synthetic fixture, not observed app data: downloaded document D1, title “Tax 2025”, contains “receipt”; D2, title “Travel”, contains “receipt”. A supported existing filter excludes D1.

Before, according to the supplied spec: typing “tax” then “receipt” launches untracked requests. A late “tax” response can replace the current results. An invisible retained filter can hide D1; a zero response erases “receipt”. Going offline hides available local matches.

After: type “tax” (generation 1), then “receipt” (generation 2). Even if generation 1 completes last, only generation 2 may publish. With no filters, the local result set is D1 and D2 in the specified stable order, including offline. Applying the fixture’s filter creates generation 3 and visibly names the filter; only D2 remains. Entering “zzzz” creates generation 4 and displays zero matches while retaining “zzzz” and the filter. Clear filters retains “zzzz”; changing it back to “receipt” restores both local matches. Clearing the field invalidates pending work and shows the downloaded-document list. An old completion cannot repopulate the search.

## Acceptance checks

Status: these are required implementation checks, not executed runtime tests.

| Check | Expected result |
| --- | --- |
| Deliver older success and older error after newer query success | Neither changes current rows, count, status, or text. Repeat with A → B → A to test generation identity. |
| Change filters/index revision while work is pending | Old completion rejected; current state rerun; visible filters match request parameters. |
| Clear, dismiss, or immediately press keyboard Search before debounce fires | Clear/dismiss invalidates old work; Search evaluates current state immediately. No duplicate stale publication. |
| Query with zero matches | Exact raw text, scope, and filters remain editable; no automatic reset. |
| Apply, remove, clear filters; begin fresh session | Count/results track visible refinements; fresh session has none. |
| Search and open fixture documents in airplane mode; lose/recover connectivity mid-query | Same local matches remain available; network state cannot erase them. |
| Slow search, partial index, index failure, retry | Editing remains usable; partial coverage is qualified; failure differs from empty results; retry has a new generation. |
| Open D1 and return; delete D1 before selection | Normal return restores query/filters/position with current-index validation; deletion gives unavailable recovery without opening D2. |
| Empty or whitespace input, repeated terms, case variants, equal titles | Defined matching, empty-query behavior, and stable identity/order hold. |
| Keyboard, narrow iPhone layout, long query/filter labels, assistive technology | Entry, query editing, clear/refinement actions and result identity remain operable and understandable; validate on implementation. |

## Audit and limits

Passed by static document inspection: interface.md now defines corrections for all four supplied failures and covers query lifecycle, scope, focus/clear, selection, zero results, offline/partial content, retry, and return. The worked example is consistent with the revised contract. No failed runtime checks are reported because none ran.

Read locally, in order: installed apple-hig root SKILL.md; interface.md; Patterns and Navigation and search family SKILL.md files; relevant searching/search-fields/loading rows of references/topic-index.md; each selected topic SKILL.md; then the three corresponding source guides. Each instruction/source file was read with a separate cat or rg command using its installed package path. The topic index’s iCloud route was not selected because no iCloud or synchronization integration is supplied. No platform adaptation, Spotlight, new history, or framework replacement is proposed.

Not executed: application code changes/builds, SDK compilation, device/simulator/GUI interactions, native keyboard behavior, offline execution, performance measurements, index coverage/relevance validation, or accessibility execution. Only interface.md and local installed guidance were supplied as evidence; there is no corpus, implementation, screenshot, or test harness. The local guides identify a 2026-10-25 snapshot and do not establish independent review or runtime conformance. Official links above are attribution only; no web browsing occurred. The delivered repair is a revised specification, not proof that an app implements it.
