# Tide companion: revised interaction specification

## Scope and decisions

The supplied `interface.md` specifies watchOS, promises replacement of all system faces, treats a complication as a full interactive map, and allows unknown stations and stale readings. No implementation, device matrix, provider contract, or screenshots were supplied.

Replace the product promise with: **“Check your selected station’s next tide from your watch face. Tap for tide details.”** Offer a curated configuration of an existing system face, with user-controlled installation and selection. Do not advertise an unrestricted proprietary face renderer or replacement of every system face. Shared configurations configure system faces; they do not create new face types. [Watch faces — Best practices](https://developer.apple.com/design/human-interface-guidelines/watch-faces#Best-practices).

The recurring wrist task is identifying the next high or low tide, its time, and whether the information is usable. A complication is a glance and entry point into the corresponding station, rather than a map workspace. The independently useful Watch app supplies station identity, the next two predicted events, freshness, and recovery. This follows the brief-glance and shallow-navigation guidance. [Designing for watchOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices).

No map appears inside a complication. The optional app-level station-location screen uses a static snapshot with one station annotation, the smallest region showing its context, and the entire map visible without scrolling. Tapping it opens Maps at that station; no in-app map pan, zoom, or station selection is promised. If coordinates or map delivery are unavailable, show the station name and “Map unavailable”; tide details remain usable. [Maps — watchOS](https://developer.apple.com/design/human-interface-guidelines/maps#watchOS).

## Face configuration and compatibility

Offer a “Tide glance” configuration: an existing system face with a rectangular next-tide complication; keep system time prominent and leave other slots available for the person’s choices. A compact alternative uses a circular slot on a compatible system face. Exact face names and supported devices remain release-time verification items, not universal promises.

| Condition | Required outcome |
|---|---|
| Compatible configuration | Explain the system face and tide slot; hand configuration to the system for the person to add. |
| Face unavailable, circular slot supported | Immediately offer the compact configuration, explaining “This watch uses a different face layout.” |
| No verified configuration | Open station details and provide instructions to choose a supported tide complication in the system face editor; never loop through a failed installation. |
| Tide app absent on recipient | Explain the dependency and allow the system installation path; if declined, preserve the existing face and provide a return path. |
| Sharing | Share layout and app dependency only; do not embed the sender’s selected station or readings. Recipient chooses their own station. |

Any preview produced before device verification must say “Simulated layout — compatibility unverified.” Production previews must reflect the actual accepted configuration. Historical device examples in the local watch-face guide do not establish current compatibility. Installation, substitution, and missing-app behavior require later system testing. [Watch faces — Best practices](https://developer.apple.com/design/human-interface-guidelines/watch-faces#Best-practices).

## Surface and content contract

Use these as semantic families, not SDK declarations. Prefer modern complication families for a watchOS 9-or-later implementation; an older-system release requires separately verified legacy templates. The initial design covers rectangular, circular, inline, and corner content; actual face slots determine availability. [Complications — Best practices](https://developer.apple.com/design/human-interface-guidelines/complications#Best-practices).

| Family | Usable data | Unknown station | Known station, unusable data |
|---|---|---|---|
| Rectangular | Station short name; “High 14:20”; “Prediction · updated 12:00” | “Choose tide station” | Station; “Tide data outdated” or “No tide data” |
| Circular | “High” and “14:20” | Tide glyph + “Set” | Tide glyph + “Old” or “—” |
| Inline | “High 14:20” | “Choose station” | “Tide outdated” or “No data” |
| Corner | “High 14:20”, shortened only if necessary | Tide glyph + “Set” | Tide glyph + “Old” or “—” |

If useful content cannot fit a verified template, use a recognizable tide launcher rather than illegible text. Do not invent a percentage ring for tide height. No gauge or chart is required. Keep status words meaningful in monochrome/tinted presentation, not color alone. Supply a separate static placeholder for every supported family, using a tide glyph and neutral dashes with no plausible real reading. Placeholder dimensions must be checked against the chosen template, separately from content assets. The local guide generally recommends lines at least 2 pt thick for glanceability in motion. [Complications — Visual design](https://developer.apple.com/design/human-interface-guidelines/complications#Visual-design).

All populated complication taps carry the configured station ID and open `StationDetail(stationID)`, including stale states. An unknown-station tap opens `ChooseStation(returnTo=StationDetail)`. Never silently redirect a deleted station to a different station: explain “Station unavailable” and offer selection. Each slot retains its own station identity even if the app’s last-viewed station differs.

The detail screen shows, in priority order: full station name; usable next high/low and local time; next following event; “Predictions” or “Observed reading” according to provider metadata; source timestamp and validity; actions to refresh, change station, and view station location. Never label a prediction as a live measurement. Heights are omitted unless the provider supplies units and datum; when shown, include both. Times use the station’s time zone, with zone and date on detail, and a day qualifier in the complication when the event is not today. If the compact slot cannot retain essential qualifiers, show a launcher instead.

## State and freshness model

The following are product decisions, not HIG-prescribed tide thresholds. A provider contract must define validity; until then, fail closed rather than inventing an age limit.

```text
Station = { id, name, shortName?, coordinates?, timeZone }
TideData = { stationID, kind, sourceTime, validUntil,
             events: [{ kind: high|low, instant, height?, units?, datum? }] }

state(now, station, data):
  if station absent: UNKNOWN_STATION
  if data absent or data.stationID != station.id: NO_DATA
  if sourceTime/validUntil missing or sourceTime > now: UNVERIFIED
  if now >= validUntil: STALE
  next = first validated event with instant > now
  if next absent or next.instant > validUntil: NO_NEXT_EVENT
  return USABLE(next)
```

Validate event order, time zone, and provenance before publishing. At the event instant, advance to the next valid event; never leave a past event labeled “next.” STALE, UNVERIFIED, and NO_NEXT_EVENT suppress numeric/current tide claims on the face. Detail may retain historical data under “Outdated — last received [date/time]”; it must not present it as current. UNKNOWN_STATION takes precedence over any cached data.

Prepare timeline entries for event transitions and validity expiry. Request reloads after station changes, successful refreshes, and meaningful provider changes, within system budgets. Do not assume continuous networking, second-by-second countdowns, unlimited reloads, or exact delivery. Include absolute time/validity context so delayed updates do not look live. The renderer must evaluate validity whenever invoked. If the system retains an old rendered entry beyond expiry, that is a verification risk; it cannot be solved by promising exact scheduling. [Complications — Best practices](https://developer.apple.com/design/human-interface-guidelines/complications#Best-practices).

Refreshing preserves existing content and station identity. Success atomically replaces only matching-station data; failure shows “Couldn’t update” and retains the correctly labeled historical data. An asynchronous response for a previously selected station cannot overwrite the current selection. Offline operation uses still-valid cached predictions; without those, show the appropriate unavailable state and allow retry.

## Selection, continuity, and exposure

The Watch selection route offers named stations from a locally available catalog or saved list; selection confirms the full name and region, persists the station ID, and returns directly to its detail. Cancel preserves the previous station. If the catalog is unavailable, say “Station list unavailable” with retry; already configured stations continue working. Phone configuration may supplement this flow but is not required for basic Watch use. No automatic nearest-station inference or location permission is part of this revision.

Store only the selected station IDs and required tide cache locally. A remote tide request, if implemented, uses the station ID rather than device coordinates. Public tide values are not inherently private, but a selected station can reveal routines; shared previews omit it. In privacy-redacted system contexts, show the generic tide glyph and “Tides,” hiding station, values, and times. These are product exposure choices based on data minimization. No account, tracking, or protected sensor access is required. [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices).

On supported Always On hardware, retain layout, station context subject to redaction, and meaningful absolute event time/status. Dim secondary details and map imagery; avoid animation and frequent updates. Keep app controls in place with an unavailable appearance while inactive. Wrist raise restores the same station and route, re-evaluates freshness, and enables controls; lowering the wrist or interruption must not reset selection. Devices without Always On resume into the same context without requiring that capability. [Always On — Best practices](https://developer.apple.com/design/human-interface-guidelines/always-on#Best-practices).

## Worked before/after

**Before, as supplied:** The product promises a proprietary replacement for all faces and a fully interactive complication map. The station can be unknown and readings stale; the brief defines no recovery or freshness behavior. No actual UI behavior is evidenced.

**After, illustrative fixture:** At 13:00 station “Harbor A” has predictions received at 12:00, valid until 18:00, with high tide at 14:20 and low tide at 17:40, all in the station’s local zone. The rectangular slot shows “Harbor A / High 14:20 / Prediction · updated 12:00.” One tap opens Harbor A detail with both events and validity. At 14:20 the prepared timeline advances to “Low 17:40.” If no refresh succeeds, the 18:00 entry becomes “Harbor A / Tide data outdated”; tapping opens that station’s historical detail and retry. The optional map is a one-pin snapshot opening Maps. If the fixture instead has no station, no cached number is shown: “Choose tide station” opens selection, and choosing Harbor A returns to its detail. These are specified outcomes, not executed results.

## Acceptance checks and evidence limits

**Passed — static specification inspection:** The revised contract removes the unrestricted-face promise, bounds map behavior, defines unknown/stale recovery, maps slot taps to station identity, separates placeholders from readings, specifies compatibility fallbacks, and preserves context across wrist transitions. These verdicts establish document coverage only.

**Failed — supplied brief against the local guidance:** Its all-face replacement claim and full interactive complication map model conflict with the supported surface model described in the local watch-face and Watch map guides. This is a brief-level finding, not a runtime defect report.

**Not executed — required implementation acceptance:**

| Check | Acceptance outcome |
|---|---|
| No station, cached data present | All families suppress cached values; tap enters selection. |
| Valid fixture and event boundary | Correct local next event; matching detail destination; advances at boundary when rendered. |
| Exact validity boundary, offline, missing validity, future source timestamp | Stale/unverified status; no current numeric claim; retry remains available. |
| Two station slots and delayed response | Each opens its own station; late responses cannot cross-contaminate data. |
| Long name, long localized time, next-day event, tint, all supported slot sizes | Essential meaning fits or launcher fallback appears; no color-dependent status; placeholders cannot be mistaken for readings. |
| Old rendered entry after reload delay | Absolute timing reveals its age; verify actual expiry presentation and document system scheduling limits. |
| Compatible/unsupported watch and missing app | Actual face accepted or immediate explained fallback; declining installation leaves a useful return path. |
| Map unavailable and map tap | Detail remains usable; complete one-pin snapshot fits; successful tap opens Maps at the selected station. |
| Wrist down/up, interruption, redaction | Stable layout and station/route; redacted fields hidden; freshness rechecked on return. |
| Physical wrist readability and assistive technology | Verify actual readability, labels, focus order, and action reachability on the eventual implementation. |

No device, SDK, GUI, accessibility, networking, reload-budget, face installation, or physical comfort execution occurred. No SDK availability or API compilation is claimed. The supplied files contain no real tide provider or hardware/OS support matrix; those remain implementation dependencies. Provider validity and prediction accuracy cannot be established by HIG.

All source links above identify official article sections but were supported solely by the installed local snapshots, not visited online. The installed root, selected families, and topic procedures were explicitly read before their source guides. Routes used: Getting started → Designing for watchOS; System experiences → Watch faces and Complications; Technologies → Maps and Always On; Foundations → Privacy. The topic index was searched for watch, complication, tide, and widget concepts. No newer-release verification or independent source review is implied. The complications guide contains a conflicting legacy 41-mm inline dimension and a malformed placeholder dimension; neither is resolved here or used to size production art.
