# iPhone route planner: loading and retry audit

## Scope and decisions

Audit input: `interface.md`, a textual description of an iOS interface. Findings below are verified against that description, not observed in a running app. Priority reflects task impact, not measured frequency. All five should be corrected before accepting this flow.

Keep cached routes visible while refreshing, acknowledge actions promptly, use honest indeterminate activity when completion is unknown, and provide contextual recovery. Coordinate requests so retries cannot duplicate results or overwrite a newer route search. Use framework-agnostic state and rendering; no Apple SDK is required by this specification.

The installed apple-hig root was read explicitly, followed by the Patterns and Status family procedures, the topic-index entries for loading/progress/feedback, and their local source guides. Source links below identify the official articles recorded in those local guides; no web content was fetched.

## Ranked verified findings

| Rank | Supplied evidence | Effect and decision | Guidance and qualification |
| --- | --- | --- | --- |
| 1 — High | “retry creates overlapping requests and duplicates results” | Retrying corrupts the route list and can allow stale responses to win. Permit one active request for the current query, ignore obsolete responses, and replace results atomically with unique route identities. | [Feedback — Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices) supports understandable state and outcomes. Request tokens, deduplication, and atomic replacement are engineering decisions, not prescribed HIG mechanisms. |
| 2 — High | “failure leaves no retry” | A failed search becomes a dead end. End activity, explain the failure in context, retain query and cached content, and offer Retry. | [Progress indicators — Best practices](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices) calls for explaining stalls with recovery; [Feedback — Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices) calls for explaining why a command cannot run and how to proceed. |
| 3 — High | “Cached routes disappear behind an indefinite spinner” | Existing useful routes become unavailable during refresh. Keep the list usable, identify it as saved content, and place refresh status beside it. | [Loading — Best practices](https://developer.apple.com/design/human-interface-guidelines/loading#Best-practices) supports useful content and background loading without interrupting interaction. A spinner is appropriate for unknown duration; obscuring useful content and leaving an unexplained wait are the problems. |
| 4 — Medium | “a fake 90% bar never advances” | The completion estimate is misleading. Remove fabricated percentages; show an animated indeterminate indicator until work ends. | [Progress indicators — Best practices](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices) requires honest reporting across the whole operation and warns against an early rush to 90%. Determinate progress is preferred only when measurable. |
| 5 — Medium | “no initial acknowledgment appears for five seconds” | People cannot tell whether their action registered and may repeat it. Update visible request state in the initiating UI transaction. | [Loading — Best practices and Showing progress](https://developer.apple.com/design/human-interface-guidelines/loading#Showing-progress) supports prompt content and ongoing feedback for waits beyond a moment or two. Immediate acknowledgment is the chosen product behavior; HIG does not supply a universal millisecond deadline here. |

## Corrected behavior

Keep destination, origin, preferences, and navigation position throughout loading and errors. Cache entries must match the current query. If showing older-query results is useful, clearly separate and label them rather than presenting them as the current answer.

| State | Content and status | Available actions |
| --- | --- | --- |
| Loading, matching cache | Keep saved routes visible and usable. Show “Updating routes…” in a stable status area and identify the routes as saved. Show last-update time only if known. | Edit search, leave screen, cancel update. Disable repeated refresh/retry activation. |
| Loading, no cache | Keep search controls visible; show “Finding routes…” with an indeterminate indicator and useful structure, without fabricated routes or percentages. | Edit search, leave screen, cancel. |
| Slow request | Continue the same indicator; say “This is taking longer than usual.” Preserve content. | Cancel; retry becomes available after cancellation or failure, not alongside an active request. |
| Failure, matching cache | Stop activity. “Couldn’t update routes. Showing saved routes.” Add a known, actionable cause when available. | Retry, edit search, use saved routes with their saved status visible. |
| Failure, no cache | Stop activity. “Couldn’t find routes. Try again.” Do not misreport a network failure as no routes found. | Retry, edit search. |
| Success | Replace the current query’s list once, clear error/activity, and mark freshness using actual metadata. A valid empty response says “No routes found” and offers editing. | Normal route selection and search. |
| Cancelled | Stop activity; preserve existing content and inputs. Without content, return to ready-to-search state. | Search again, edit. |

Use a product-configured slow threshold and finite request deadline, validated against real service behavior; neither timing value is specified by the supplied HIG. A deadline transitions to failure and recovery instead of leaving an endless spinner. Cancel is appropriate here for a read-only route lookup; it need not discard saved routes. Keep feedback near the route list, without a blocking alert for routine refresh failure. The progress guide recommends safe cancellation; the feedback guide reserves alerts for critical information.

Status must convey meaning in text as well as animation or color. Expose the status and named actions through the host platform’s accessibility semantics, announce meaningful loading/error/completion transitions without repeated animation announcements, and preserve focus during refresh. These are proposed acceptance requirements, supported generally by [Feedback — Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices), not verified accessibility defects in the supplied interface.

## Framework-agnostic request specification

```text
state = { query, phase, routes, savedMetadata, activeToken, error }
generation = 0

start(query):
    if activeToken exists and query == state.query:
        return                          // repeated activation is a no-op
    invalidateAndCancelActive()
    token = ++generation
    state.query = normalized(query)
    state.routes, savedMetadata = matchingCache(state.query)
    state.phase = loading
    state.error = none
    state.activeToken = token           // assign before dispatching work
    publish()                           // acknowledgment, no five-second timer
    request(state.query, token, deadline)

onSlow(token):
    if token == activeToken: publishSlowStatus()

onSuccess(token, response):
    if token != activeToken: return
    routes = uniqueByStableRouteIdentity(validate(response.routes))
    atomically:
        state.routes = routes           // replace, never append retry results
        updateMatchingCache(query, routes, response.metadata)
        state.phase = success           // includes valid empty result
        state.activeToken = none
        state.error = none
    publish()

onFailure(token, cause):                // includes deadline expiry
    if token != activeToken: return
    state.activeToken = none
    state.phase = failure
    state.error = safeActionableMessage(cause)
    publish()                           // preserve routes, inputs, and position

retry():
    if phase == failure and activeToken is none: start(query)

invalidateAndCancelActive():
    old = activeToken
    activeToken = none                  // invalidate before best-effort abort
    abortTransport(old)                 // late callbacks must still be ignored

cancelOrLeave():
    invalidateAndCancelActive()
    state.phase = ready
    publishIfStillVisible()
```

Serialize state transitions. A query edit that starts a new search uses `start(newQuery)`; changing inputs must invalidate any old request before it can publish results. Define stable route identity from the service contract or a documented canonical route key, not display text or list position. Deduplication must preserve genuinely distinct alternatives. These are implementation choices requiring service-contract validation.

## Worked before/after

**Before (illustrative sequence consistent with the supplied description):** A person has two cached routes and requests an update. Both disappear. Nothing acknowledges the action for five seconds, then an indefinite spinner and fake 90% bar provide no credible completion estimate. Failure supplies no retry. Where retry is invoked through the described retry mechanism, repeated attempts overlap and duplicate routes. The description does not explain how that retry mechanism is reached despite the missing failure action.

**After (specified sequence):** The same two saved routes remain visible. Refresh immediately displays “Updating routes…” with indeterminate activity. The request fails; activity stops and “Couldn’t update routes. Showing saved routes.” appears with Retry. Tapping Retry twice starts exactly one request, B. A late callback from the previous request A is ignored. B returns three route records, two sharing the same stable identity; the list is atomically replaced by the two distinct routes, with fresh metadata. No retry result is appended to the saved list. If B reaches its deadline, the failure state and Retry return while saved routes remain available.

## Acceptance checks

These are checks to run against an implementation, not completed tests.

1. With matching cached routes, start refresh: content remains visible/selectable, saved status is explicit, and loading acknowledgment appears in the first state publication, before waiting for the network.
2. Without cache, start a delayed lookup: search context remains visible, meaningful status appears promptly, and no fabricated percentage or route content appears.
3. Hold a response past the configured slow threshold: contextual slow status appears. Hold it past the deadline: activity ends and actionable failure with Retry appears.
4. Fail with and without cache: preserve inputs; retain available saved routes; stop indicators; expose Retry. Do not present failure as a valid empty result.
5. Activate Retry repeatedly before the response: observe one active request for that query and one result publication. Verify the handler guard as well as the disabled visual control.
6. Start A, then change the query and start B; deliver A after B and again after B fails. A never changes the current list, error, or loading state. Repeat with cancellation and a transport that ignores abort.
7. Return duplicate stable identities: publish one item per identity, replacing existing results. Distinct valid alternatives remain distinct. A successful empty response shows the empty state.
8. Cancel or leave during loading: preserve saved content and inputs, remove activity, and reject late callbacks. Reentry uses the correct query’s cache.
9. Inspect semantics and then test with an actual assistive technology: named Retry/Cancel controls, readable status, meaningful transition announcements, and stable focus. Confirm animation/color are not the only feedback. This execution remains outstanding.

## Evidence limits

Only `interface.md` and the relevant installed instructions/source guides were inspected. The interface supplies assertions, not screenshots, source code, traces, service contracts, or an executable prototype. No device, SDK, GUI, network-service, performance, or accessibility execution occurred. The five-second delay and duplicate behavior are reported facts from that file, not independent measurements. Their root causes and frequency are unknown.

The local source guides identify snapshot date 2026-10-25 and are derived guidance, not SDK documentation or independently verified current web pages. No newer-release claims are made. No additional iOS rules are stated in the loading guide; the macOS indeterminate-bar advice is not applied to iPhone. Retry coordination, cache labeling, deadlines, route identities, and focus behavior are concrete design/engineering decisions rather than invented numerical or API requirements from HIG.
