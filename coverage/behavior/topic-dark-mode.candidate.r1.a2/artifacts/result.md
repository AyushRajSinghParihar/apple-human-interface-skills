# Dark appearance adaptation result

Patched interface.md in place, replacing the original one-paragraph defect description with a concrete iOS/macOS specification. The patch removes pixel inversion, maps surfaces and text to adaptive semantic roles, preserves full-color assets, defines selection/focus treatments, adapts alerts, and specifies live-switch state preservation and acceptance checks.

## Decisions

- Follow system appearance and resolve colors in context. On iOS preserve base/elevated hierarchy; on macOS respect user accents and inactive selection. Basis: [Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode) and [Color](https://developer.apple.com/design/human-interface-guidelines/color).
- Treat paper whites, watercolor pigment and portraits as content. Preserve original profiles and color; use surrounding chrome to separate edges. Optional glare mitigation requires actual review, rather than automatic dimming. Basis: [Dark Mode, icons and images](https://developer.apple.com/design/human-interface-guidelines/dark-mode) and [Images](https://developer.apple.com/design/human-interface-guidelines/images).
- Replace luminance-only selection with an outline, checkmark and programmatic selected state. The 2 pt outline and 3:1 state-cue target are project decisions. Semantic text replaces fixed black; 4.5:1 is the conservative project text target, with 7:1 an aim for custom text colors. The local Accessibility guide contains more qualified size/weight thresholds; the stricter project target avoids treating those as a universal conformance test. Basis: [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) and [Color](https://developer.apple.com/design/human-interface-guidelines/color).
- Replace fixed-white alerts with native adaptive presentation. Preserve existing actions and state; inventory actual alert contracts before implementation sign-off. No trigger or copy was supplied. Basis: [Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts).

## Worked before/after

Illustrative catalog item, not supplied production content: “River Wash” by “A. Lee,” selected when the system switches to dark while an alert is open.

| Aspect | Before, per supplied brief | Revised contract |
|---|---|---|
| Watercolor and portrait | Every pixel inverted, altering pigment and skin tones | Original full-color images, unchanged profiles and no filter |
| Title and artist | Fixed black disappears on dark cards | Primary semantic label on adaptive metadata surface |
| Selection | Only a slight luminance shift | 2 pt outline plus checkmark outside artwork; selected state persists |
| Alert | Blinding fixed-white surface | Platform adaptive alert, preserving copy, actions and pending decision |
| Live change | State behavior unspecified | Same selected ID, scroll, focus and unfinished input; no action fires |

The item names are illustrative; alert content and behavior remain dependent on the existing product. No invented alert default or destructive action is presented as implemented.

## Acceptance checks and status

**Passed — specification inspection:** the revised file explicitly addresses all four reported defects; includes iOS/macOS role mappings, original-image handling, noncolor selection, adaptive alerts, live changes, accessibility-setting combinations and state preservation. Both requested Markdown artifacts were written and reread. These are document checks only.

**Failed:** no executed runtime check is recorded as failed. The four original defects are supplied observations, not independently reproduced findings.

**Not executed — implementation acceptance:** interface.md’s seven checks cover appearance transitions with open alerts and selection; image fidelity/density; measured text and state-cue contrast; all four Increase Contrast/Reduce Transparency combinations in each appearance; grayscale, accents, wallpaper and inactive Mac selection; 200% text and assistive/keyboard use; alert action/cancellation outcomes and focus restoration. All remain pending on an actual implementation.

## Evidence and limits

Read the installed apple-hig root SKILL.md explicitly, read Foundations, searched the topic index, then read its Dark Mode, Color, Accessibility and Images procedures before their references. Read Presentation and its Alerts procedure before the Alerts reference. Each read used a separate single-file cat or rg command. All paths resolved inside .agents/skills/apple-hig. No web browsing was performed; official links above identify source articles from the local snapshot.

The only supplied interface evidence was a short prose brief. No source code, screenshots, asset files, rendered color pairs, dimensions, framework, SDK version or alert inventory was supplied. Consequently no numerical contrast measurement, profile/density validation, SDK build, device/GUI rendering, desktop tinting, physical glare review, Accessibility Inspector or assistive-technology execution is claimed. Semantic roles are implementation guidance, not compiled API verification. Local references are derived guidance dated 2026-10-25, not proof of independent source/media review or current SDK availability.
