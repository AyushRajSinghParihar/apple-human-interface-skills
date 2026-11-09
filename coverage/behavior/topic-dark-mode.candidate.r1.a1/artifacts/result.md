# Dark appearance adaptation result

Patched interface.md in place, replacing its single-paragraph defect description with a concrete iOS/macOS specification for semantic surfaces/text, artwork fidelity, selection cues, adaptive alerts, live transitions, and acceptance checks.

## Decisions

- Replace inversion with system appearance and semantic foreground/background roles. Promote secondary metadata to primary if its measured contrast fails.
- Preserve watercolor pigments, portraits, profiles, and white paper. The local Dark Mode reference conditionally suggests slight dimming for glaring images; catalog fidelity warrants actual viewing and review before applying it.
- Add a checkmark, “Selected” label, and outline, separate from focus. Respect Mac user accents/inactive selection and iOS base/elevated depth.
- Use standard adaptive alerts while preserving existing actions. Unknown triggers and handlers remain implementation inputs; no new product action was invented.
- Preserve selection, scroll, focus, input, and alert state during automatic appearance changes.

The explicit selection treatment is a project design decision. The conservative 4.5:1 essential-foreground target follows the local Dark Mode reference, which also recommends aiming for 7:1 for custom colors. The Accessibility reference's Inspector table has size/weight qualifications; this specification uses a stricter project target without claiming comprehensive accessibility conformance. Official article links supporting the decisions appear in interface.md.

## Worked before/after

Illustrative fixture, not a supplied screenshot: a selected white-paper watercolor, artist portrait, and open alert during a change to Dark appearance.

| Before, from supplied description | Revised contract |
|---|---|
| Inversion alters pigments and portrait colors. | Original full-color content retains its profile and paper; semantic chrome changes appearance. |
| Fixed black text disappears on dark cards. | Semantic title/artist labels sit on a dedicated metadata surface; actual contrast must be measured. |
| Selection changes luminance only slightly. | Checkmark, “Selected” label, and outline identify selection independently of color; focus remains separate. |
| Temporary alert stays blinding white. | Standard adaptive alert updates in place, retaining input and existing actions. |

## Acceptance checks and status

**Passed — document inspection:** The edited specification addresses all four supplied defects, covers both stated platforms, preserves useful state, and defines observable acceptance conditions. Both output files were reread after writing.

**Failed — baseline description:** The original text reports inverted content, disappearing text, weak selection distinction, and light-only alerts. These are reported specification defects, not independently reproduced rendering failures.

**Not executed — runtime acceptance:** Run the eight appearance/Increase Contrast/Reduce Transparency combinations per platform in interface.md. Measure actual contrast pairs; inspect artwork fidelity, iOS elevation, Mac accents/inactive windows/wallpaper, live switching with selection and an alert active, 200% text enlargement, focus restoration, alert action outcomes, and accessibility selected-state exposure. No contrast measurements are available because no rendered colors were supplied.

## Evidence and limits

Audit route resolved from /tmp/hig-eval-aeob82zj/.agents/skills/apple-hig/: explicitly read root SKILL.md, inspected the supplied interface.md, and searched references/topic-index.md for dark, color, accessibility, image, and alert concepts. Read Foundations family, then its Dark Mode, Color, Accessibility, and Images topic procedures before their respective source references. Read Presentation family and Alerts topic procedure before that family's alert reference. Every instruction/reference file was consumed in an individual cat or rg command.

Only supplied local text and installed guidance were used; no web requests were made. Article links are provenance from the installed snapshot, not current online verification or evidence of independent source review. No screenshots, app code, assets, SDK, or deployment target were supplied. No GUI, Apple-device, compilation, or accessibility execution occurred. No native rendering, vibrancy, desktop tinting, physical glare, or display fidelity result is claimed. The requested specification revision is complete; application implementation and runtime validation remain pending.
