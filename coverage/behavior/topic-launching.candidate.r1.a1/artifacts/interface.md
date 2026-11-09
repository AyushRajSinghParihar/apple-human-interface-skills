# iPhone news reader: launch and resume specification

Platform: iOS on iPhone. This replaces the previous 12-second animation, fake launch-screen Sign In button, fixed yesterday headline, and blank offline launch.

## Readiness and launch screen

A launch is usable when the reader can navigate and open available stories, or can understand an explicit empty/error state and retry. A splash or placeholders alone do not count as readiness. Remove the 12-second animation entirely, including on foreground entry; no minimum display timer or network completion gate may replace it. Aim for interaction within a few seconds, following HIG guidance; actual timing must be measured.

Use the iOS system static launch screen with the same background and structural chrome geometry as the initial app screen. Match light/dark appearance and the app's supported orientation. Omit headlines, dates, text, buttons, advertising, and added branding. It must contain neither Sign In nor anything implying interaction. Real headlines appear only in the running app from identified content records, with their publication dates. The system launch screen is not an onboarding surface and is not replayed by the app on resume.

Only local content/state retrieval and building the destination are startup dependencies. Fetching current news, images, analytics and optional configuration must not block interaction. Text stories remain usable without downloaded images; show neutral image placeholders only where assets are missing, replacing them individually.

## Entry and restoration contract

Persist the selected feed, feed anchor story ID and offset, open article ID, and article reading anchor/offset as navigation or reading position changes, and when entering background. Store stable IDs rather than relying on list indices. Retain the corresponding cached text where available. Do not depend solely on a termination callback.

Resolve entry in this order:

1. A newly requested article/deep-link destination takes priority over saved navigation. If unavailable offline, show the requested article identity and “This story isn't available offline,” with a route to cached stories and Retry. Do not silently replace it with a saved article.
2. Otherwise, resume the existing in-memory screen on foreground entry. After process termination, restore the saved article and reading anchor, or feed and anchor.
3. If a saved article was removed or cannot be recovered, show “This story is no longer available” with a return to its feed. If its cached text exists but refresh fails, keep the cached article readable instead. If a feed anchor disappeared, use the nearest surviving saved neighbor; otherwise start that feed at the top without inventing a position.
4. With no saved state, open the default news feed. A first install has no mandatory tutorial, sign-in step, preference setup, or branded splash. Reading public stories is assumed not to require an account; confirm this product assumption before implementing any account prerequisite.

Background/foreground cycles retain current content and position. Refresh must not replace an open article, reset scroll, or reorder rows beneath the reader. Stage updated feed ordering until the person next explicitly refreshes or reopens the feed; merge missing images without moving text. Interrupted fetches may resume/retry in the background, with at most one active refresh per destination.

## Content and network states

| Condition | Visible, usable state | Transition and recovery |
|---|---|---|
| Cached feed/article exists | Render cached content immediately after local retrieval; show publication dates and “Last updated {localized date/time}.” | Refresh independently when online. Never clear content for refresh. |
| Offline with cache | Same readable content plus “Offline — showing saved stories.” | Cached stories open normally. An uncached story explains its unavailability and offers return to saved stories and Retry. |
| First install, no downloaded cache | Show bundled sample stories, visibly labeled “Sample story” with original dates; they are not live headlines. | Load current news independently. Keep samples usable until actual content can replace them without disrupting reading. Bundled samples are an added product requirement. |
| No usable downloaded or bundled content, request pending | Show real navigation and “Loading stories…” in the content area. Do not display fabricated headlines or dates. | On success render available stories; partial success renders each available story without waiting for every asset. |
| No content and offline/failure | Show “You're offline. Connect to load stories.” or “Couldn't load stories,” as appropriate, with Retry. | Retry starts one request and reports pending status in place. Restore Retry after failure. No indefinite blank screen or repeating animation. |
| Refresh fails with existing content | Retain all available content and position; show “Couldn't update stories. Showing saved stories,” last-update time and Retry. | Retry updates independently; failure does not erase the last successful timestamp. |

Use localized copy and dates in the running app. “Last updated” means the last successful content refresh, not launch time; sample publication dates remain distinct. A successful refresh removes offline/error status only when current data is actually received. Network reachability alone is not success.

For pending requests, provide truthful text status without percentages or invented completion estimates. Use a 15-second foreground request deadline as a product recovery policy, not an Apple timing rule: after it expires, retain available content and expose Retry with a failure message. A late response from a superseded request must not overwrite newer data or navigation. Connectivity recovery may retry once automatically; further failures leave explicit Retry available. The content area is never a permanent skeleton.

## First use and re-entry

The first task is opening a story from the default feed or labeled samples. No passive tutorial is required. Do not introduce optional permission, rating or purchase prompts during startup. If optional learning is added later, it must follow usable launch, offer Skip, persist skipped/completed status across launches, and remain available through Help. It must not recur on foreground entry.

## Design basis

These are implementable product decisions informed by the installed local HIG snapshot; they do not assert an implementation exists. Apple recommends prompt interaction and detailed restoration in [Launching: Best practices](https://developer.apple.com/design/human-interface-guidelines/launching#Best-practices), appearance/orientation continuity and restrained static content in [Launch screens](https://developer.apple.com/design/human-interface-guidelines/launching#Launch-screens), useful content during background loading in [Loading](https://developer.apple.com/design/human-interface-guidelines/loading), and optional first-use learning and initial content in [Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding). The request deadline, sample-content choice, persistence fields, refresh staging and failure copy are product choices rather than quoted HIG requirements.
