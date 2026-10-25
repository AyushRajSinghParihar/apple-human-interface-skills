# Editorial image repair

Patched `interface.md` in place. It now separates live text from photos, preserves panoramic landmarks, selects density-appropriate assets, caps undersized photos, replaces generic descriptions, and retains context during missing/loading/error states. Added metadata requirements, state transitions, reading order, stale-response protection and distinct iOS/macOS text behavior.

## Decisions

The supplied brief reports five defects; these are specification findings, not observations of a running application. Each now has a concrete replacement rule. Photos remain read-only content, without introducing editing or image actions. Headline text sits above the photo so it can reflow independently and does not depend on photographic contrast.

Official section links supporting the material recommendations are recorded in `interface.md`, based on local guides only. Full-photo fitting, editorial crop approval, no-upsample size caps, the 2:1 unknown-size placeholder and 15-second deadline are chosen product policies, not HIG mandates. macOS gets an explicit reader text-scale preference because the local typography guide states it has no Dynamic Type.

## Worked before/after

Synthetic fixture, not a supplied asset: a 2400 × 800 pixel panorama shows a lighthouse at the left harbor entrance and a mountain across the water on the right. Headline: “Across the harbor at dawn.” Caption: “The harbor at dawn.” Description: “A lighthouse at the left harbor entrance faces a mountain across the water on the right.”

Before, the supplied behavior flattens the title into the photo, crops landmarks, announces “Image,” and loses context on failure. After, the title is a separate wrapping heading and the full panorama is retained. At 360 × 120 points on a 3x iOS display it needs 1080 × 360 pixels, so the source is adequate. A 600 × 200 pixel fallback instead caps at 200 × 66.67 points at 3x, centered without stretching. At 720 × 240 points on a 2x Mac display the required rendition is 1440 × 480 pixels.

The description adds spatial information beyond the caption. On failure, the reserved figure shows “Photo unavailable,” keeps the caption and verified description as text, and leaves the headline, destination, introduction and body readable. The unavailable photograph is not represented as current visible pixels. If a caption already conveys all meaningful visual information, it is exposed once without a redundant image node.

## Acceptance checks

| Check | Expected result | Status |
|---|---|---|
| Document coverage | All five reported problems have explicit replacement rules in interface.md | Passed: static review |
| Fixture arithmetic | 360 × 120 at 3x needs 1080 × 360; 600 × 200 caps at 200 × 66.67 points; 720 × 240 at 2x needs 1440 × 480 | Passed: arithmetic review |
| Text | Headline can be selected/copied; complete headline/caption reflow at every supported iOS text size, Bold Text, and Mac 100/200% reader scale | Not executed |
| Framing | Both landmarks survive narrow/wide widths and iOS portrait/landscape; crops require valid approval metadata | Not executed |
| Assets | Inspect sufficient/undersized renditions at iOS 2x/3x and Mac 1x/2x, including display changes; verify profiles, compression and no distortion | Not executed |
| States | Exercise slow load, success, corrupt image, missing URL, offline cache hit/miss, timeout and late success; retain text, geometry and paragraph anchor | Not executed |
| Race | Navigate A to B while A loads; A's pixels and description never appear in B | Not executed |
| Semantics | VoiceOver reads heading, meaningful figure information and attached caption in order, without redundant/decorative nodes; failure is truthful and focus persists | Not executed |
| Input/context | Keyboard and assistive input can read, scroll and navigate without image traps; resizing, orientation and app switching preserve article/paragraph | Not executed |
| Appearance | Measure actual contrast in light/dark/Increase Contrast; inspect safe areas and device-distance readability | Not executed |

Failed checks: none found in static document review. Runtime behavior remains unverified; this is a specification repair, not an application implementation pass.

## Audit and evidence limits

Explicitly read the installed root `.agents/skills/apple-hig/SKILL.md`, then searched its topic index. Read Getting started, Content, Foundations and Technologies family routes and their selected topic procedures before supporting guides: Designing for iOS, Designing for macOS, Image views, Images, Accessibility, Typography, VoiceOver and Layout. Every read command targeted one file within the installed package. Typography's relevant introduction/platform sections were read separately after a larger tool response was truncated.

Only the supplied specification and installed local instructions/guides informed this work. Official links identify sources from the local snapshot; no web browsing or online verification occurred. No actual images, implementation, SDK configuration, rendered screens or runtime accessibility tree were supplied or inspected. The example is illustrative. No device, SDK compilation, GUI, Accessibility Inspector, VoiceOver, keyboard or other accessibility execution occurred. Local guides are dated derivative guidance, not evidence of current APIs or independent source review. The revised specification does not prove an application implements it.
