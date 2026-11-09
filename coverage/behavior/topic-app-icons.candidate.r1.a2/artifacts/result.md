# Journaling app icon family — revised specification

## Scope and decisions

This is a design contract for the app’s launcher identity on iPhone and Mac, not an in-app glyph set. `interface.md` reports a marketing screenshot containing tiny tagline text, a simulated platform corner mask, a baked-in drop shadow, and a seasonal badge covering half the mark. The screenshot itself and final artwork were not supplied. These are brief-reported properties, not visually verified findings.

Use one recognizable **closed journal with a bookmark** across both platforms. Remove the screenshot, tagline, seasonal badge, simulated corner mask, and baked-in drop shadow from the production icon. A journal is the proposed product metaphor; its distinctiveness and recognition remain to be tested. Keep seasonal messaging in marketing content, outside the launcher asset. Do not introduce an alternate-icon picker or seasonal icon switching in this revision.

Apple’s local guidance favors one simple concept, few shapes, a quiet background, and details that survive reduction. It advises against screenshots and temporary text; text is appropriate only when essential to identity. Here the tagline is not essential. [App icons — Design](https://developer.apple.com/design/human-interface-guidelines/app-icons#Design)

## Artwork and delivery contract

The following geometry and colors are project decisions, not Apple-prescribed measurements. Coordinates use a 1024 × 1024 canvas, origin at top left.

| Layer | Concrete specification |
| --- | --- |
| Background | Full-canvas opaque square, default deep teal `#174E52`; no transparent corners, frame, shadow, or simulated surface highlight. |
| Journal | Centered filled warm-paper silhouette `#F5E7CB`, bounds x=284–740, y=220–804; softly rounded corners, nominal radius 48. No lettering, page lines, or thin outline. |
| Bookmark | Filled coral ribbon `#D9654D`, x=564–644, y=220–440, ending in a broad V notch at y=400. Overlay the journal; keep the ribbon and notch crisp. |

Keep the journal and bookmark as separate foreground layers so their overlap can be tuned. Do not cut the bookmark out of the journal. Use opaque vector fills initially; test any later material/translucency changes before accepting them. Keep all essential content inside these bounds and validate against the actual production mask/template before release. The numeric inset is a starting composition, not a guaranteed system safe zone.

Deliver editable, unmasked square vector layers, with outlined paths and no embedded fonts, plus a manifest containing layer order, bounds, palette, and variant overrides. Use sRGB for this family. If raster content becomes necessary, use lossless PNG. Both iOS and macOS use a 1024 × 1024 unmasked canvas in the supplied guidance; the system applies the rounded-square mask and creates smaller appearances. Do not export a marketing screenshot as a production asset. [Layer design](https://developer.apple.com/design/human-interface-guidelines/app-icons#Layer-design), [Icon shape](https://developer.apple.com/design/human-interface-guidelines/app-icons#Icon-shape), [Specifications](https://developer.apple.com/design/human-interface-guidelines/app-icons#Specifications)

Leave dynamic highlights, shadows between layers, bevels, blur, and glow to the system. The selected design needs no custom shadow. Later Apple-side production should assemble and tune the layers in Icon Composer and export using the supported toolchain; this specification does not require that tool or an Apple SDK on this Linux server. [Visual effects](https://developer.apple.com/design/human-interface-guidelines/app-icons#Visual-effects)

## Family and appearance inventory

Use identical silhouette, bookmark location, proportions, and layer order on iPhone and Mac. Adapt the surrounding system presentation rather than creating a different Mac logo.

| Appearance, for each platform | Authored intent |
| --- | --- |
| Default | Teal background, warm-paper journal, coral bookmark as above. |
| Dark | Background `#12383C`, journal `#BFAF91`, bookmark `#C87860`; quieter brightness while retaining separation. |
| Clear light / clear dark | Separate appearance recipes using the same journal and bookmark geometry; restrain color and tune material against both light and dark surroundings in Apple previews. |
| Tinted light / tinted dark | Monochrome tonal recipes using the same geometry; journal and ribbon remain distinguishable through tone and silhouette without depending on coral. |

Deliver all six appearance intents for each platform. Clear/tinted material values are deliberately pending preview tuning; flat colors cannot establish their final appearance. The guide permits system-generated variants, but this project requires reviewing every resulting variant before acceptance. If the bookmark merges with the journal, adjust its tone/material or enlarge the ribbon consistently across the family; do not substitute a seasonal badge. [Appearances](https://developer.apple.com/design/human-interface-guidelines/app-icons#Appearances)

## Interaction and state contract

The icon communicates app identity, not unread counts, seasonal status, or whether an entry is saved. Appearance changes affect presentation only. No extra tap, hover action, or onboarding step is attached to the artwork.

Framework-agnostic pseudocode:

```text
on systemAppearanceChanged(appearance):
    present corresponding icon recipe through platform packaging
    preserve journal silhouette and bookmark placement
    do not change app route, selected entry, draft, or window state

on ordinaryLauncherActivation(platform):
    if a live workspace exists:
        activate it and preserve its current editing context
    else if restorable workspace exists:
        restore selected entry, draft, and editing context
    else:
        open journal home
    never create a new entry merely because the icon was activated
```

On iPhone, ordinary activation is a Home Screen tap; on Mac, it is an ordinary Dock/Finder launch or activation. Let the platform handle launch mechanics. Bringing the Mac app forward must not create duplicate windows or replace an unsaved draft. Preserve existing authentication requirements, if any; the brief supplies no authentication model. These are proposed activation requirements, not observed app behavior. Context preservation follows the platform guidance for interruptions and activation. [Designing for iOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices), [Designing for macOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Best-practices)

## Worked before → after

**Before, as reported:** A person looks for the journaling app among other apps. A screenshot-derived mark has tiny tagline text, pre-rounded corners, a fixed shadow, and a seasonal badge occupying half the mark. The text may disappear under reduction and the badge may dominate recognition; actual rendering has not been inspected.

**After, specified:** The person sees the same warm journal silhouette and upper-right bookmark on iPhone and Mac. Reduction leaves two broad filled shapes rather than text. The supplied square background reaches the canvas edges, and the platform applies its own mask and effects. Switching to a tinted appearance retains the journal/bookmark relationship. Activating the icon returns to the existing draft; it does not open seasonal marketing or start another entry.

## Acceptance checks and current status

**Passed — specification inspection only:** The revised contract defines one concept, two foreground layers, an opaque unmasked background, shared platform geometry, six appearance intents per platform, and activation transitions. It explicitly removes all four reported marketing treatments. No SDK dependency appears in the pseudocode.

**Failed / unresolved release gates:** No final artwork, assembled icon family, or runtime build exists in the supplied evidence. Production readiness is therefore unestablished. Clear/tinted material tuning is intentionally incomplete. No runtime failure is asserted.

**Not executed — required before accepting production assets:**

1. Inspect exported layers: correct canvas/profile, background opaque to all edges, no pre-mask, tagline, seasonal badge, or baked shadow; journal and bookmark remain separate.
2. Preview both platform masks and every appearance. Fail if any essential shape is clipped, a highlight obscures the bookmark, or lighting changes the intended journal shape. Tune using actual Apple tools rather than treating a flat mockup as proof.
3. Inspect actual smallest system-generated settings/notification appearances and launcher/search/Dock presentations where applicable. Fail if the journal becomes an indistinct block or the bookmark disappears. Use actual target sizes; do not infer them from the 1024-pixel source canvas.
4. Compare default, dark, clear light/dark, and tinted light/dark on light and dark surroundings. Fail if recognition depends solely on the coral hue or a variant changes the core composition.
5. Ask people unfamiliar with the artwork to locate the same app across iPhone and Mac and across appearance variants. Record confusion with other app icons and revise the silhouette if needed. This is a proposed recognition test, not a completed study.
6. With an unsaved draft active, switch apps and activate the launcher icon again on each platform. Pass only if the same entry and draft return with no duplicate entry/window. Repeat after termination using the app’s persistence contract; verify appearance changes do not alter content state.

## Evidence limits and routing record

Only supplied local files and installed instructions were used; no web browsing occurred. Official URLs above identify the source sections recorded in the local snapshot, not pages fetched during this work. No artwork, screenshot pixels, Icon Composer preview, Apple SDK build, GUI, device, accessibility execution, or user study was available or performed. Color separation, small-size recognition, material behavior, export compatibility, and final system rendering remain unverified. No minimum OS version was supplied; release packaging and appearance availability must be checked against the eventual deployment targets rather than inferred from this design guide.

Audited reading order: installed root `apple-hig/SKILL.md`; `interface.md`; relevant icon/symbol rows in `references/topic-index.md`; Foundations and Getting started family procedures; Designing for iOS, Designing for macOS, and App icons topic procedures; then their three supporting source guides. All paths resolved within `.agents/skills/apple-hig/`, and each file was read with its own command. The route selected App icons because this brief concerns launcher identity; interface glyphs, document icons, and custom launch commands are outside the supplied scope.
