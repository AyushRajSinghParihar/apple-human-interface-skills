# iPadOS conservation-photo detail

Framework-agnostic specification for identifying a specimen and inspecting its photographed condition. No photo, intrinsic dimensions, metadata or implementation was supplied; do not invent specimen facts.

## Correct image sizing and scale evidence

Decode orientation first. For oriented image dimensions W × H pixels and available viewport Vw × Vh logical points, use s = min(Vw/W, Vh/H). Display at sW × sH, centered. The viewport excludes safe areas, captions, status and controls. Preserve the aspect ratio at all zoom levels; never stretch or aspect-fill this scientific image. A square viewport may letterbox with a neutral background.

Remove the decorative border that hides the scale marker. Do not crop, round-mask or overlay any image pixels with decoration, controls, captions or status. Any separator belongs outside the photo bounds. Initial fit and Reset View must reveal all edges and the entire photographed marker. At higher zoom the marker can move offscreen through deliberate inspection; show “Zoomed view — parts of photo may be outside view” and retain the scale caption outside the image.

The embedded marker transforms with the specimen, never as a fixed-size screen ruler. Transcribe verified scale information, including units, into the caption: for example, “Photographed scale bar: 10 mm.” Say “Scale marker absent,” “Scale marker unreadable,” or “Scale information unverified” as appropriate. Do not infer specimen measurements from display size or fabricate calibration.

## Identification and accessible descriptions

Show a persistent text heading with the verified specimen name/identifier; show photo view and date when known. Use “Specimen identifier unavailable” for missing identity. Pixels are never the only label.

Group the photo and its caption. Give the image an image role and a concise curator-verified description of conservation-relevant visible features, their location and orientation. Expose that description as readable text as well. Do not diagnose unseen damage or derive observations from a filename. If missing, show “Photo description unavailable” and retain verified metadata; description authoring remains outstanding.

Avoid repeating heading and caption verbatim in the image description. Expose scale information once in the photo group. Exclude decoration from accessibility navigation. Reading order: heading/identity, image description, scale caption, readiness/zoom status, inspection controls, error/retry when present. Controls expose button roles, names matching visible labels, enabled states and perceptible press/focus feedback. Current zoom reads “Zoom: N percent of fit,” not physical magnification or native pixel size. Announce meaningful ready/error transitions once without stealing focus or repeatedly announcing progress ticks.

## Zoom, reset and alternative input

Fit is z=1. This product's proposed useful zoom limit is z=4, to be validated against actual asset resolution; enlargement creates no additional evidence. Pinch changes z continuously in [1,4], anchored at the pinch point. Drag pans overflowing axes, clamped so the image cannot be dragged past its boundary to expose additional empty space. Double-tap toggles 2× fit at the tapped location and reset. Preserve reserved system-edge, multitasking and accessibility gestures.

Provide ordinary visible buttons outside the photo:

| Label and accessible name | Outcome | Availability |
| --- | --- | --- |
| Zoom In | Multiply z by 1.25, clamped to 4; preserve center image point | Ready image and below maximum |
| Zoom Out | Divide z by 1.25, clamped to 1; preserve center point, then clamp position | Ready image and above fit |
| Reset View | Set z=1; center and show complete photo/marker | Ready image and not already fitted/centered |
| Pan Left / Right / Up / Down | Move viewed region in named direction by 25% of viewport axis, clamped at image edge | Ready image with further content in that direction |

Touch buttons, pointer clicks, keyboard focus/activation and assistive activation invoke the same operations. Maintain focus after activation. No essential action requires hover, speech, pinch or drag. Use separate, nonoverlapping hit regions of at least 44 × 44 pt, following the iPadOS default rather than treating smaller minima as a density goal. Status explains why inspection is unavailable.

## iPad adaptation

At generous widths keep photo and caption/controls alongside when readable. At narrow widths or larger text, stack and wrap them without removing actions. Base sizing on current available space, not a full-screen iPad assumption. Keep important content within safe regions. If the detail overflows vertically, use one detail scroller; reserve photo dragging for zoomed image panning and avoid competing nested vertical page scrollers. All controls remain reachable independently of photo manipulation.

On resize/rotation preserve specimen, photo, readiness, zoom factor and normalized center point, clamping only as necessary; at z=1 recompute whole-image fit. Switching inputs preserves state. Selecting a different photo starts at fit and atomically changes its metadata. Preserve the existing route back to specimen context.

Support at least 200% text enlargement without clipped descriptions or actions. Use adaptive semantic colors outside the photograph and verify contrast in light/dark and Increase Contrast. Never recolor scientific pixels. Avoid automatic spring/repeated motion; programmatic zoom/reset changes are immediate with Reduce Motion.

## Honest loading and recovery

| State | Presentation and actions | Transition |
| --- | --- | --- |
| Loading, no image | Show known record text immediately and neutral photo placeholder labeled “Loading specimen photo.” No stock imagery or fabricated specimen. Inspection disabled; navigation usable. | Matching decoded asset → ready; verified matching preview → preview; failure/timeout → error |
| Preview | Only a verified preview for the same record/photo; label “Preview — full-resolution photo loading.” Retain verified scale text and disclose if marker unreadable in preview. Inspection disabled. | Full asset → ready at fit; failure → retained preview with error and Retry |
| Ready | Matching decoded, rendered image with description, scale and controls; remove loading only when usable, not merely after byte transfer. | Same-asset refresh retains image/inspection with “Updating photo” |
| Error, no image | “Couldn’t load specimen photo.” State an actionable cause such as offline only if detected. Retain record text; offer Retry. | Retry → loading; success → ready |
| Error with available image | Retain preview labeled “Preview — full-resolution photo unavailable,” or ready cache labeled “Saved photo — update failed.” Preview inspection stays disabled; ready cache retains inspection. Offer Retry. | Retry retains available content while loading; success updates status honestly |

For unknown duration, use an indeterminate indicator and text after a brief wait; never invent percentages or completion estimates. Any later measured progress must name its measured stage and not equate download completion with rendering. A request with no transfer/decode progress for 30 seconds exits to error; this is a proposed product timeout, not an Apple rule.

Retry is a normal button that shows “Retrying…” and activity feedback while pending and prevents duplicate requests. Failure re-enables it. Navigation cancels or invalidates obsolete requests; a response must match the current photo and request identity. Same-asset refresh preserves inspection; an actual replacement starts at fit and announces the change. Never flash an unrelated image or leave an endless loading placeholder.

## Guidance basis

Read from installed local guidance only; links identify official sources without implying live verification. The fit equation, scientific scale policy, zoom factors, pan steps and timeout are product decisions implementing the guidance, not universal Apple mandates.

- [Designing for iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados#Best-practices) and [Layout](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability): mixed input, available space and preserved context.
- [Image views](https://developer.apple.com/design/human-interface-guidelines/image-views#Content): image presentation and legibility; the installed topic procedure also advises whole-image framing when cropping loses meaning and avoiding stretched photographs.
- [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) and [VoiceOver](https://developer.apple.com/design/human-interface-guidelines/voiceover): meaningful descriptions, semantic order, text enlargement and alternative actions.
- [Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures#Best-practices), [Scroll views](https://developer.apple.com/design/human-interface-guidelines/scroll-views#Best-practices), [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices): familiar input, bounded zoom and reachable controls.
- [Loading](https://developer.apple.com/design/human-interface-guidelines/loading#Showing-progress): useful partial content and truthful progress.
