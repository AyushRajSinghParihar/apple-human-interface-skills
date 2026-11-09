# Journaling app icon family — revised specification

## Scope and evidence

This is a framework-agnostic design contract for the app’s launcher identity on iPhone (iOS) and Mac (macOS). It specifies artwork, appearance selection, and launch behavior; it does not implement an app or produce final icon assets.

`interface.md` reports a marketing screenshot with tiny tagline text, a simulated platform corner mask, a baked-in drop shadow, and a seasonal badge covering half the mark. No final artwork exists. The screenshot itself was not supplied for visual inspection. These are reported composition problems, not measured rendering defects.

## Decisions

1. **One recognizable concept:** use a closed journal silhouette with a single broad bookmark inset. Remove the tagline and seasonal badge. The journal remains the identity across both platforms and every appearance. The bookmark is part of the silhouette, not a status indicator. This proposed concept is a product design choice, pending brand approval; no existing logo or app name was supplied. Apple recommends a simple distinctive concept, few shapes, and avoiding temporary or tiny text. [App icons — Design](https://developer.apple.com/design/human-interface-guidelines/app-icons#Design)
2. **Deliver unmasked artwork:** use a full square canvas; do not draw rounded outer corners, transparent corner cutouts, a simulated device frame, or an external drop shadow. The system applies its mask. Leave highlights, bevels, glow, and interlayer shadows to system treatment. Any later custom effect requires preview evidence before acceptance. [Icon shape](https://developer.apple.com/design/human-interface-guidelines/app-icons#Icon-shape), [Visual effects](https://developer.apple.com/design/human-interface-guidelines/app-icons#Visual-effects)
3. **Separate identity from promotion:** no seasonal launcher alternate or seasonal overlay in this revision. Retain any campaign tagline in marketing copy outside the icon. A seasonal journal prompt, if separately commissioned, belongs in app content and must not alter launcher identity. No extra promotional launch screen is introduced. Preserve established launch and navigation conventions. [Branding — Best practices](https://developer.apple.com/design/human-interface-guidelines/branding#Best-practices)
4. **Shared geometry, appearance-specific treatment:** preserve journal position, scale, bookmark placement, and silhouette across default, dark, clear light/dark, and tinted light/dark. Color must not be the only identifying cue. These are appearance variants, not user-selectable alternate identities. The local guide allows system-generated variants; this specification instead requests explicit variant review to catch identity loss. [Appearances](https://developer.apple.com/design/human-interface-guidelines/app-icons#Appearances)

## Artwork and layer inventory

All coordinates below are proposed production starting points, not Apple-mandated safe zones. Use a 1024 × 1024 unmasked square design canvas for both targets, as listed in the supplied guide. Start with sRGB. Keep editable vector masters; supply crisp outlined SVG/PDF foreground artwork, or lossless PNG if rasterization is necessary. No fonts or raster screenshot embedded in the mark. [Specifications](https://developer.apple.com/design/human-interface-guidelines/app-icons#Specifications), [Layer design](https://developer.apple.com/design/human-interface-guidelines/app-icons#Layer-design)

| Layer | Concrete construction | Treatment |
|---|---|---|
| Background | Opaque full-canvas fill; initial default warm ivory `#F2E9DA` | Quiet, no paper grain, lettering, vignette, or baked lighting |
| Journal | Filled shape, bounds x=270…754, y=190…834; gently rounded internal object corners, nominal radius 56 canvas units | Default deep teal `#174E50`; no page lines, pen, spine strokes, or title |
| Bookmark detail | Broad inset cutout in the journal fill: x=574…650, y=190…430, V tip rising to y=388 at x=612 | Reveals background; belongs to the journal vector, not an independently moving layer |

The outer canvas stays square even though the illustrated journal has rounded corners. Use one foreground group to avoid independent lighting or movement splitting the journal and its bookmark. Begin with fully opaque shapes; tune system material effects later in the platform tooling. The inset is an illustration detail, not a claim of physical recess or a custom shadow.

| Appearance | Background starting direction | Journal/detail invariant |
|---|---|---|
| Default | Warm ivory | Deep teal journal; inset exposes background |
| Dark | Subdued deep teal `#153638` | Muted ivory `#D8D4C6` journal; same inset |
| Clear light / clear dark | Restrained platform clear treatment | Same silhouette and inset; tune luminance/material per preview |
| Tinted light / tinted dark | Platform-selected tint treatment | Monochrome shape separation; do not depend on the teal hue |

The hex colors are design seeds, not verified contrast values or final material recipes. Clear/tinted versions require separate light and dark previews; flattening the default palette is not acceptance. No geometry changes between platform exports unless documented preview evidence requires optical adjustment, in which case preserve the recognizable proportions.

The supplied guide describes Icon Composer assembly and Xcode export for iOS/macOS. Deliver neutral masters and a manifest now; a later Mac production step must assemble, tune, preview, and export with the appropriate Apple tools. Do not treat SVG files alone as installable app icons or assume any SDK/export API is available here.

## Interaction and state contract

The icon identifies and opens the journaling app. It is not a compose button, campaign link, progress display, or indication that an entry was saved. Product decision: preserve the host app’s existing launch destination and draft restoration behavior; the brief does not establish those behaviors, so this revision must not silently change them.

```text
IconFamily = {
  identity: journal_with_bookmark,
  targets: [iOS, macOS],
  canvas: [1024, 1024],
  geometry: shared_master,
  variants: [default, dark, clear_light, clear_dark,
             tinted_light, tinted_dark],
  promotional_overlays: none
}

on systemAppearanceChanged(appearance):
  present the corresponding platform-resolved family variant
  preserve identity geometry and application state
  do not navigate, open an entry, or modify a draft

on systemRequestsIcon(size, appearance, target):
  resolve the platform export for target and appearance
  allow the system to mask, treat, and reduce the icon
  do not overlay campaign artwork or tagline text

on launcherActivation:
  dispatch the existing application-open action exactly once
  let existing application lifecycle/restore policy choose destination
  do not route through a seasonal promotion
```

Variant resolution and system treatments above are behavioral requirements, not invented API names. Keep the app’s existing localized system display name; no text is baked into artwork. On iPhone, evaluate Home Screen, search, settings, and notification appearances where the app is presented. On Mac, evaluate Dock, application listings/search, and small system presentations where available. Platform sizing and export behavior must be verified during integration rather than inferred from this master canvas.

## Worked before → after

**Before (reported):** a person looking for their journal sees a screenshot-derived mark. At small size the tagline may become illegible, the seasonal badge competes with half the mark, and simulated corners/shadows can conflict with system masking and lighting. Actual severity cannot be established without the image.

**Decision:** identify the app with one stable journal silhouette; move temporary communication out of the launcher asset and delegate platform effects to the system.

**After (specified):** the default iPhone icon shows the teal journal and broad bookmark inset on ivory. Changing to a tinted appearance retains that geometry without requiring teal for recognition. The Mac icon uses the same master and identity in its platform export. Activating either invokes the existing open action. The seasonal campaign neither changes the mark nor intercepts launch. A small-size preview that loses the bookmark fails review and triggers simplification or enlargement of the inset, followed by rechecking every variant.

## Acceptance checks and current status

| Check | Pass condition | Current evidence/status |
|---|---|---|
| Brief coverage | Both targets, reported text/mask/shadow/badge, and missing artwork addressed | **Passed — specification inspection** |
| Construction contract | Unmasked 1024-square masters; opaque full background; separate foreground; inventory and variants specified | **Passed — specification inspection**, assets not produced |
| Asset inspection | Actual files contain no tagline, campaign badge, pre-mask, baked outer shadow, or fine page detail | **Not executed** — no artwork |
| Mask and reduction | In actual system previews, identifying journal and inset survive masks and smallest available presentations on both targets | **Not executed** — no exports or previews |
| Appearance coverage | All six appearance entries retain shape recognition in light/dark contexts; no lost inset or merged silhouette | **Not executed** — no material/rendering evidence |
| Layer effects | Motion, highlights, refraction, and shadows never obscure or split the identity | **Not executed** — requires platform tooling/device previews |
| Launch and appearance transitions | Activation dispatches one existing open action; changing appearance preserves destination/draft and does not show promotion | **Not executed** — no application implementation |
| Platform packaging | Correct platform exports accepted by the integration toolchain; inspect rendered results on iPhone and Mac | **Not executed** — SDK/build/device access not established |
| Recognition review | Reviewers recognize the same journal across platform/appearance pairs at real display sizes, without reading icon text | **Not executed** — requires artwork and human review |

**Failed executed checks:** none. This means no execution failures were observed; it does not establish that the unbuilt design passes runtime checks. Any asset that crops the identifying mark, loses it under reduction, or changes its intended shape under effects must fail acceptance and be revised.

## Evidence limits and audit trail

Read the installed package in this order: root `apple-hig/SKILL.md`; supplied `interface.md`; Foundations family `subskills/apple-hig-foundations/SKILL.md`; App icons topic `.topics/apple-hig-app-icons/SKILL.md`; its supporting `references/app-icons.md`; Branding topic `.topics/apple-hig-branding/SKILL.md`; its supporting `references/branding.md`. Each read used a separate `cat` command. All package-relative paths resolve under `.agents/skills/apple-hig/`; topic/reference paths after Foundations are relative to that family directory.

Only supplied local files and installed guidance were used. Official links above identify the source sections recorded by the local guides; they were not opened. The local App icons and Branding references record retrieval on 2026-10-25 and are application guidance based on Apple’s source, not SDK documentation. No independent source/media review is implied. No screenshot, final artwork, Icon Composer preview, GUI, SDK build, device run, assistive-technology run, or measured contrast test was performed. Export availability, minimum OS support, physical-size clarity, and actual system appearance behavior remain integration evidence requirements. No minimum deployment target was supplied; older-system packaging needs separate verification before release.
