# Revised interaction specification: iPhone family album

This replaces the behavior described in `interface.md`. It is a framework-agnostic design contract, not an implementation or an assertion that an Apple SDK is available.

## Decisions and source support

1. **Preserve the captured moment on import.** Store the still, surrounding frames, sound (when present), and their association as one logical album item. Generate thumbnails separately; never replace the source with a thumbnail or flatten it silently. If complete import cannot be supported, retain the source pending recovery and offer “Retry import”, “Import Still Photo”, or “Cancel”. Explain that importing a still omits motion and sound. Existing flattened imports cannot be reconstructed without their originals; offer reimport when available. Whole-asset identity and explicit still conversion follow [Live Photos — Best practices](https://developer.apple.com/design/human-interface-guidelines/live-photos#Best-practices). Retaining originals and these recovery labels are product decisions.
2. **Use a quiet grid.** Show still thumbnails; no automatic playback or sound, including during rapid scrolling. Mark known Live Photos with a consistently placed, unobtrusive corner badge and text identity “LIVE”; keep essential image content visible. A badge identifies the asset type, not download readiness. Avoid a video-style play triangle. This applies the badge guidance in [Live Photos](https://developer.apple.com/design/human-interface-guidelines/live-photos#Best-practices); disabling all grid autoplay is this product’s decision.
3. **Provide deliberate whole-asset preview.** Open detail on thumbnail activation. Show the still initially. Press-and-hold the image to play the captured moment; release stops and returns to the still. Also provide a labeled “Preview Live Photo” action, which plays once and becomes “Stop Preview”. Include synchronized sound when present, subject to the user’s audio setting; show “Sound On”/“Sound Off” and allow adjustment. Do not present sound or frames as separately browsable media. Preview remains available before export, including all before/after frames and sound. It is offered, not compulsory. See [Live Photos](https://developer.apple.com/design/human-interface-guidelines/live-photos#Best-practices).
4. **Make export format explicit.** Offer “Live Photo — Still, motion, and sound” and “Still Photo — No motion or sound” before handoff. Ordinary-photo export is always a route; it may require downloading the still. A supported live export includes the associated still and motion/sound, never motion alone. Unsupported destinations receive a still. Unknown support must not be treated as verified live support. See [Live Photos](https://developer.apple.com/design/human-interface-guidelines/live-photos#Best-practices).
5. **Use platform sharing when available.** A standard Share entry point opens the export preparation flow, then hands the chosen representation to the system share presentation when the host supports it. Do not imitate a system sheet or assume its ordering is controllable. Without such integration, use a clearly labeled app export destination flow with the same payload rules. No duplicate custom Print/Save activities. This follows [Activity views — Best practices](https://developer.apple.com/design/human-interface-guidelines/activity-views#Best-practices); the short format-preparation step is a product decision.

## Asset and readiness contract

```text
AlbumItem = {
  id, revision, kind: still | live,
  sourceStill, sourceMotionWithSound?, association?,
  stillState: absent | fetching | ready | failed,
  liveState: absent | fetching | validating | ready | failed,
  originalRetained, conversionExplicit
}
liveReady = stillState == ready AND liveState == ready
            AND associationVerified AND completeMomentValidated
```

`ready` requires readable, associated components, not merely a known file name. No SDK-specific encoding or association format is prescribed. The implementation must supply a validated live import/export adapter; without one, report live capability unavailable and offer explicit still conversion. Do not manufacture Live Photo playback from unrelated video files.

| State | Visible contract | Available actions and transition |
|---|---|---|
| Still ready, live remote | Still plus LIVE identity; “Download to preview motion and sound” | “Download Live Photo” starts fetch; still export remains available |
| Downloading | “Downloading Live Photo” plus measured progress if known; otherwise indeterminate status | “Cancel Download”; preserve still and any source originals |
| Validating | “Preparing Live Photo” | Cancel preparation; preview/live export unavailable |
| Fully ready | Still plus LIVE identity | Hold or Preview action; both export formats available |
| Download/validation failure | Still plus “Live Photo unavailable” and readable reason | “Retry”; still export; no enabled live playback affordance |
| Still unavailable | Placeholder identifying the item and its state | Fetch/retry still; do not export a nonexistent still |
| Permanently missing live data | “Only the still photo is available” | Still export; offer reimport if original can be supplied |

Canceling or failing a fetch does not change the asset’s type or convert it. Do not label a known Live Photo as an ordinary photo just because its motion is remote. Preview stops on navigation, scrolling away, interruption, or backgrounding; it does not resume automatically. Starting a new preview stops the old one. Playback completion returns to the still. No queued autoplay after a download completes.

If editing is later offered, apply edits consistently to the still and all frames, or explicitly offer “Save as Still Photo” while retaining the original. Poster-only edits must never masquerade as a consistently edited live asset.

## Export interaction and payload contract

Scope: the currently opened item. Batch export is outside this revision. Format selection is local to this export; default to Live Photo only when complete live export is available. Otherwise show why it is unavailable and offer Still Photo without silently selecting a lossy operation.

1. Activate Share. Show the selected item, format choices, whole-asset preview route, and a concise payload description. “Preview Live Photo” includes sound when enabled; disclose if sound is off. “Continue” prepares the selected format; “Cancel” returns to the item unchanged.
2. If chosen data is remote, expose download/preparation status and cancel/retry. Readiness gates handoff. A live failure offers “Retry” or an explicit “Use Still Photo”; never silently substitutes.
3. Resolve destination capability conservatively:

| Destination evidence | Export result |
|---|---|
| Verified complete Live Photo support | In Live Photo mode, hand off one associated logical asset containing still + motion + sound when present |
| Known still-only | Show “This destination supports still photos only. Motion and sound won’t be included.” Offer “Send Still Photo” or “Cancel” |
| Unknown or unverified | Show “Live Photo support can’t be verified.” Offer still export or return to choose a verified destination; do not promise live delivery |
| Any destination in Still Photo mode | Send only the still; retain the original album asset |

If destination capability cannot be inspected inside a system sharing integration, constrain that handoff to the explicitly chosen still format; expose live export only through a verified route. Do not claim the system sheet can supply capabilities it does not expose. Do not silently fall back after the user selected Live Photo.

4. Before dispatch, snapshot the item ID/revision and representation. If the item changes during preparation, discard the stale prepared copy and ask the person to review the updated item. Never combine components from different revisions.
5. Cancel before dispatch deletes temporary output and returns with the item and format choice intact. Preparation/dispatch failure retains the original and offers retry. Prevent duplicate dispatch while a request is pending. Dismiss system sharing through its supported lifecycle; show any app-owned continuing transfer status in the album, with cancel only where supported. Report “Handed to [destination]” when that is all the adapter can establish. Say “Sent” only with an actual completion result; do not claim recipient playback or receipt without evidence. Problems remain actionable in the album. See [Activity views — Share and action extensions](https://developer.apple.com/design/human-interface-guidelines/activity-views#Share-and-action-extensions).

```text
prepare(item, chosenFormat):
  snapshot = freeze(item.id, item.revision)
  require chosenFormat == still ? stillReady : liveReady
  payload = chosenFormat == still
      ? exportStill(snapshot)
      : exportAssociatedWholeMoment(snapshot)
  validate(payload, snapshot, chosenFormat)
  return payload   // no dispatch yet

handoff(payload, destination):
  if payload.isLive AND destination.support != verifiedLive:
    return explicitStillChoiceOrCancel
  dispatchOnce(payload, destination)
  recordOnlyObservedOutcome()
```

## Motion and accessible operation

These are specified requirements awaiting execution. Grid identity, readiness, errors, and export consequences use text or semantics as well as badges; no meaning relies solely on animation or sound. Use iOS default 44 × 44 pt activation areas for app-owned actions, with sufficient separation. Allow text enlargement to at least 200% without losing the format consequences, status, or cancel/retry controls. Label the image with its supplied family caption or neutral identity, asset type, and readiness; label actions by outcome. Do not invent descriptions of family members or audible content.

Press-and-hold is optional: assistive activation of Preview starts one complete preview and Stop ends it. All export decisions remain reachable without timed gestures. Reduce Motion uses a static badge and instant or restrained fades for interface transitions; explicit media preview remains optional and stoppable, never needed to identify the asset or choose an export. Honor applicable flashing-content accommodations when supported; expose any capability limit rather than claim compliance. Family captions/transcripts may describe meaningful sound or visual events when supplied; this design does not claim automatic media description or transcription.

Support and later verify the full task with assistive input, including VoiceOver, Switch Control, and Full Keyboard Access. Sources: [Accessibility — Vision, Mobility, Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility) and [Motion — Best practices / Providing feedback](https://developer.apple.com/design/human-interface-guidelines/motion). Removing grid autoplay and the precise control/state contract are product decisions, not quoted universal Apple rules.

## Worked before/after

Example fixture: “Grandma’s birthday” consists of still S, surrounding frames M, and birthday wishes A, associated as L. Aunt May’s destination accepts only still photos.

**Before, as reported in the brief:** Import flattens L without notice. Motion assets autoplay throughout a fast grid. Export drops the still without warning. The brief does not establish exactly which remaining files reach Aunt May or how her client renders them.

**After, specified:** Import retains S+M+A as L and shows one still thumbnail with LIVE identity. Scrolling causes no playback. Open L: if M+A are remote, download them with visible status; no preview is offered as ready until validation succeeds. Activate Preview to see all frames with synchronized birthday wishes, then stop or let it finish. Share describes the complete live payload and offers Still Photo. On selecting May’s known still-only destination, disclose the loss of motion and sound. “Send Still Photo” sends S alone; Cancel sends nothing. L remains S+M+A in the album for a later verified live destination. A failed download still permits S export when S is ready, with the same explicit choice.

## Acceptance checks and audit status

The following are implementation acceptance scenarios, not executed tests:

| Check | Required observation |
|---|---|
| Complete import and round trip | A known fixture retains associated still, all frames, sound when present, and timing through import and live export; decode and compare content/association, not file extensions alone |
| Import failure / existing flattening | No silent conversion; explicit still choice or retry/cancel; old flattened items do not acquire fabricated motion |
| Fast grid traversal | No cell starts motion/audio; badges stay consistently placed; rapid navigation never queues playback |
| Remote asset | Badge identifies type while readiness says download; preview/live handoff cannot run early; determinate progress is factual |
| Interrupted or failed fetch | Cancel/retry works; original and still survive; completion does not autoplay |
| Whole preview | Before/after frames and sound remain synchronized; hold/release and accessible Preview/Stop work; leaving stops playback |
| Live export | Verified destination receives still plus associated motion/sound; no component from another revision; export leaves source intact |
| Still / unsupported / unknown | Still choice produces an ordinary still; unsupported and unknown routes disclose limitations; no motion-only output or homemade live simulation |
| Cancel / error / pending dispatch | No dispatch on pre-handoff cancel; retry is possible; repeated activation cannot duplicate a pending dispatch; outcome text matches actual evidence |
| Preferences and assistive input | Reduce Motion retains identity/status; 200% text retains actions/consequences; actions have usable activation areas and can be reached/activated with assistive input |
| Future editing guard | Either every frame and still agree, or conversion to still is explicit |

**Passed — static specification review:** `interface.md` was read. This document supplies decisions addressing all three reported defects and the still-only recipient case, plus readiness, preview, payload, cancellation, and recovery contracts. Installed root, selected families, topic procedures, and source guides were read in order, one file per command. The topic index was searched for Live Photos and sharing/accessibility concepts.

**Failed — supplied design against this contract:** The brief explicitly reports silent flattening, indiscriminate grid autoplay, and still-dropping export. These are reported design failures, not independently reproduced runtime findings.

**Not executed:** Every runtime acceptance scenario above; real asset import/export/decoding, recipient compatibility, synchronization, download progress, system share integration, device playback, geometry/contrast measurement, assistive-technology operation, SDK compilation, GUI execution, and physical comfort testing.

## Evidence limits

Inputs were the short local `interface.md` and installed apple-hig guidance only. No source code, sample assets, screenshots, destination capability records, or running app were supplied. The installed guides are derivative snapshots dated 2026-10-25, not SDK documentation or independently verified current Apple behavior. Official links above identify source articles; they were not opened. No web, device, Apple SDK, GUI, or accessibility execution occurred. There is no evidence of source conflicts in the consulted passages; absence of a platform subsection is not proof of capability. Concrete formats, metadata preservation, transport support, recipient behavior, and framework feasibility require implementation evidence before shipping. This specification preserves the existing unknown framework and requires adapters rather than assuming Apple APIs exist.
