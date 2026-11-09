# Tide companion: revised interaction specification

This replaces the promises in `interface.md`: “replace all system watch faces” and “complication as a full interactive map.” The watch task is to glance at the next tide event for a deliberately selected station, then tap for its details. This is a framework-agnostic design contract, not an SDK implementation.

## Decisions and surface ownership

| Surface | Revised contract | Basis |
|---|---|---|
| Watch face | Offer an optional curated configuration of an existing system face, with a Tide slot. The user chooses whether to add it; existing faces remain user controlled. Product copy: “Add tide information to a compatible watch face.” | [Watch faces — Best practices](https://developer.apple.com/design/human-interface-guidelines/watch-faces#Best-practices). Sharing a configuration does not establish unrestricted custom rendering. |
| Complication | Show next high/low event and absolute time; tap opens that station’s tide detail. No map gestures or embedded controls. | [Complications — Best practices](https://developer.apple.com/design/human-interface-guidelines/complications#Best-practices). |
| Watch app | Independently useful station detail, next event, data status, station change and refresh. No phone required for these core tasks. | [Designing for watchOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices). |
| Geography | Optional station-location screen contains a static snapshot with one station annotation, smallest useful region, entirely onscreen. Tap opens Maps for that station. If snapshot/handoff unavailable, retain station name and coordinates with “Map unavailable.” | [Maps — watchOS](https://developer.apple.com/design/human-interface-guidelines/maps#watchOS). The supplied snapshot’s Watch qualification governs over its general interactive-map advice. |

No map implementation, face artifact, target OS, watch model or station provider was supplied. Family choices below are intended variants, conditional on actual slot support. Do not advertise universal device support or infer APIs from HIG.

## Content and state contract

Store each slot’s explicit `stationID` independently so multiple slots can represent different stations. Never silently substitute a nearby station. Data carries station identity, source, kind (prediction or observation), generation/observation timestamp, retrieval timestamp, validity interval, event timestamps and heights with unit and datum. Retrieval time alone does not establish freshness. Use station-local time, indicate its zone in app detail, and include the date when an event is not today. A prediction is labelled “Predicted”; do not present it as a measured reading.

Product policy: only classify data as usable when the provider supplies an applicable validity interval, the payload matches the selected station, timestamps are coherent and a future event is present. A provider-approved maximum age for observations is required before observations can be labelled current; none is supplied here. Missing validity/age policy means freshness unknown, not fresh. These are proposed product rules, not Apple numerical requirements.

| State | Face content | Tap destination / app behavior |
|---|---|---|
| Station unknown | “Choose station”; compact variant uses a recognizable tide glyph plus “?” | Station chooser. Saved/catalog station names are selectable without location permission. Select → bind slot, load station detail. Cancel preserves prior binding or unknown state. |
| Loading, no cache | “Loading tides” / “…” | Bound station detail, explicit loading status. No invented event or zero height. |
| Usable prediction | “High 14:20” (example only) | Same station detail: “Predicted high tide,” time, height/unit/datum, source, validity and update information. |
| Stale or freshness unknown | “Tides outdated” or “Freshness unknown”; compact “Old” or “?” | Same station detail with status first. Cached values may appear only under “Last available,” with their timestamps; no current trend or countdown. Refresh and change station remain available. |
| Missing, malformed or expired event coverage | “Tides unavailable” / “—” | Same station detail, explanation and Retry. No next-event claim. |
| Refresh failure with cache | Preserve stale/unknown classification and show “Couldn’t refresh” in app | Retry; retain station and labelled historical values. A successful network request cannot alone clear the status. |
| Privacy redaction | Tide glyph and “Tides” | Restore permitted content on activation; retain slot destination. |

State priority: redaction controls presentation; unknown station controls routing; otherwise invalid/missing payload → unavailable, freshness unknown → unknown, expired validity/age → stale, no future event → unavailable, else usable. A mismatched station payload is never displayed as that station’s historical data.

```text
onComplicationTap(slot):
    if slot.stationID absent: open ChooseStation(slot.id)
    else: open TideDetail(slot.stationID, slot.id)

onStationSelected(slot, station):
    persist slot.stationID = station.id
    invalidate old station presentation
    open TideDetail(station.id, slot.id)
    request station data; request surface update within system budget

onRender(now, slot, payload):
    state = classify(now, slot.stationID, payload, providerPolicy)
    return presentation(slot.family, state, privacyContext)

onRefreshResponse(requestStation, response):
    cache only under response's validated station identity
    never overwrite a newer station selection with a late response
    reclassify; request permitted surface update
```

The first app screen shows station name, status, next event when usable, and a “Change station” action. Refresh is available in detail; show progress and then success/failure inline, preserving the station. App launch without a slot uses the last selected station, or the chooser. Complication entry always takes precedence over last-viewed app state. Back from chooser returns to its invoking detail; station-location view returns to the same detail. Lowering the wrist or interruption preserves route, station and any selection in progress.

## Family, update and appearance contract

| Intended family | Usable content | Loss of data / fallback |
|---|---|---|
| Rectangular | Station short name; “Predicted high 14:20”; height with unit if space permits | Full status phrase and station when known |
| Inline | “High 14:20”; station abbreviation only if it fits | “Tides outdated,” “Choose station,” or “Tides unavailable” |
| Circular | “High” and event time | Short status from table; recognizable tide launcher if meaningful text cannot fit |
| Corner | High/low label and time, tailored to available slot | Same semantic fallback; omit optional height before event type/time |

Do not squeeze or truncate event type/time into ambiguity. Long station names may shorten in the slot; detail retains the full name. Avoid a percentage ring: tide height is not percentage completion. No decorative chart is required. Tinted appearance retains event words and status, so color never carries the only distinction. Supply separate static, nonnumeric placeholders for each supported family, visibly distinct from live content. Use selected family/template dimensions only after the deployment target is known; do not transfer legacy dimensions into modern layouts. The local guide’s conflicting legacy inline dimensions remain unresolved and are not used here. See [Complications — Visual design and family sections](https://developer.apple.com/design/human-interface-guidelines/complications#Visual-design).

Build finite timeline entries at meaningful changes: next-event rollover, validity expiry and provider-approved observation-age expiry. At rollover, choose the next future event from valid cached coverage; when none remains, show unavailable. Absolute event times avoid per-second countdown reloads. Request replenishment within system budgets; no guaranteed update cadence, unlimited reloads or continuous live readings. If the system delays an update, the last delivered face content can persist: include expiry/status information where space permits and always reclassify on app entry. Exact prevention of stale face presentation requires runtime verification.

On supported Always On devices, preserve layout and station context; dim secondary detail, simplify the snapshot, keep event/status legible and show unavailable controls in place. There is no ongoing animation. Wrist raise restores the same route and active controls. This is conditional behavior, not a claim that every watch supports Always On. See [Always On — Best practices](https://developer.apple.com/design/human-interface-guidelines/always-on#Best-practices).

Station choice can reveal interests/location. Default to manual selection, with no GPS collection, account or background location requirement. Persist only slot bindings, user display preference and necessary station cache; this specification introduces no telemetry. Honor system redaction; offer “Hide station and tide details when inactive,” replacing those fields with neutral labels in wrist-down/face contexts when selected. Public tide values alone are not treated as sensitive by default. Verify available privacy mechanisms before implementation. See [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices).

## Curated configuration and compatibility

Proposed configuration: an existing system face with one rectangular Tide slot; alternate configuration: a compatible existing face with a circular Tide slot. Additional slots remain user configurable. Resolve actual face names, OS/model support and slot availability against the eventual deployment environment before shipping; these are slot specifications, not tested downloadable faces.

Configuration flow: explain required Tide app installation and possible substitution → system configuration/install flow → user confirms or cancels. Missing app follows the system installation path where supported; failed/cancelled installation preserves the current face and offers “Open Tide” / “Set up later.” Unsupported preferred face immediately offers the compatible circular arrangement when verified. If no verified configuration exists, offer app detail and instructions to add a supported Tide complication manually; never end at only an error. Offline setup retains explanation and Retry.

All current previews must say “Illustrative configuration — compatibility unverified.” Do not depict an interactive map in a slot. Before release, replace these with previews from the actual configured face, accurately showing installed complications and device framing. Verify preview fidelity, installation and face acceptance on each advertised target. This fallback map follows [Watch faces — Best practices](https://developer.apple.com/design/human-interface-guidelines/watch-faces#Best-practices); historical device examples in the local source are not a current compatibility matrix.

## Worked before/after

**Before (supplied claims):** A person is promised replacement of every system face and a full interactive map inside a complication. The station may be unknown and readings stale. No supplied behavior explains either condition; no actual rendering or observed user failure is asserted.

**After (synthetic fixture):** At 12:00 on 25 October, the user has no station. The face shows “Choose station.” One tap opens the chooser; selecting “Harbour A” binds that slot and opens its detail. A fixture prediction generated at 10:00, valid until 18:00, contains high tide at 14:20, 2.1 m relative to fixture datum D. Detail shows those labels and source; rectangular face shows “Harbour A / Predicted high 14:20 / 2.1 m.” Tapping it opens Harbour A even if the last app visit was Harbour B.

At 18:00, without replacement data, the scheduled entry becomes “Tides outdated.” App entry independently checks expiry, shows the old data only under “Last available,” and offers Refresh. A failed refresh preserves that status. Selecting “Station location” opens the single-marker snapshot; tapping opens Maps. Lowering and raising the wrist retains Harbour A and the current route. These are specified outcomes using invented data, not executed results.

## Acceptance checks and evidence limits

**Passed — static specification review:** The revised contract removes unrestricted face replacement; separates glance from map; binds taps to slot identity; specifies unknown, stale, loading, failure and redaction states; includes finite timeline/expiry rules, compatibility fallback and preview provenance. The worked fixture traces unknown → selected → usable → expired → refresh failure without substituting a station. Passed means covered and internally inspected in this document.

**Failed — supplied brief against the revised design criteria:** Its universal proprietary-face promise and interactive-map complication conflict with the local guidance’s supported surface model. Unknown-station and stale-data recovery are unspecified. These are findings about the supplied prose, not runtime defects.

**Not executed — implementation acceptance:**

| Check | Required observable result |
|---|---|
| Two independently bound slots; late request returns after station change | Each tap opens its own station; old response never changes the new binding. |
| Missing validity, expired observations, expired predictions, wrong station, empty future events, failed refresh | Correct distinct state; no stale/unknown value presented as current; retry preserves context. |
| Timeline rollover, offline operation, budget exhaustion, delayed reload, clock/zone changes | Correct event/date and expiry classification; no continuous-update promise; record actual system delay behavior. |
| All advertised families and sizes, longest names/times, tinted and placeholder states | Status/type/time remain distinguishable; useful fallback rather than ambiguous clipping; placeholders cannot be mistaken for readings. |
| Wrist down/up, interruption, privacy setting, Always On unavailable | Stable route/layout, correct redaction and restored controls; normal active experience without Always On. |
| Supported/unsupported face, missing app, cancelled install, offline setup | Honest preview, explained substitution, usable fallback and preserved existing configuration. |
| Watch map and unavailable handoff | Entire static snapshot visible, one correct annotation, correct Maps destination or text fallback. |
| Physical wrist readability and assistive-technology use | Validate text, reading order, actionable labels, target usability and state announcements in the eventual implementation. |

Only `interface.md` and installed local instructions/guides were used. The root router, selected family files and each named topic procedure were read before their respective guides. Routes: getting-started/designing-for-watchos; system-experiences/watch-faces and complications; technologies/maps and always-on; foundations/privacy. Official links above are attribution from those local snapshots, not browsed verification. The package is independent application guidance; its retrieval/snapshot dates do not establish current API availability or independent review. No code, SDK, device, GUI, face installation, map service, accessibility execution, energy measurement or real tide-provider validation was performed. Production readiness depends on those unresolved checks and a real provider freshness policy.
