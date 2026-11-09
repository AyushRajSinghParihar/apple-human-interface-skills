# Decisions and changes

Patched interface.md in place into a concrete iPhone specification. Replaced the weather metaphor with `archivebox`; removed nonuniform scaling; specified outline, matched text weight, medium scale and monochrome rendering. Added a labeled system action, state transitions, redundant text, accessible semantics, target requirements and availability-aware text fallbacks.

The brief does not define status. The revision explicitly assumes archive-operation status and preserves separate read/unread and flag metadata. Exact wording, keeping the message until confirmed success, and duplicate-request handling are product decisions. HIG supports recognizable metaphors, coherent symbol configuration, redundant color cues and system controls; it does not prescribe this particular state machine.

# Worked before/after

Before, as supplied: Archive uses a decorative weather symbol; a system symbol is stretched nonuniformly; status depends on multicolor alone. Actual symbol names, colors and runtime behavior were not supplied.

After, proposed example: an Inbox message shows proportional outline `archivebox` with “Archive”. A tap replaces the glyph with an activity indicator and “Archiving…”, disabling duplicate requests. Confirmed success removes the message from Inbox and leaves `checkmark` plus “Archived” in the resulting view. Failure retains the message and shows “Couldn’t archive. Try again.” with an enabled Archive action. Without symbols or color, text still communicates every outcome.

# Acceptance audit

| Check | Result | Evidence or next step |
| --- | --- | --- |
| Required patch and concrete contract | Passed: static document inspection | interface.md defines symbol configuration, action, transitions and fallback behavior. |
| Redundant meaning specified | Passed: static document inspection | Every state has text; missing glyphs retain labels and semantics. |
| Known defects retained in revised contract | None found by static review | This is not implementation validation. |
| Compatibility and restrictions | Not executed | Minimum iOS and SDK absent; verify all symbols/features and force lookup failure. |
| Archive request behavior | Not executed | No app/backend supplied; exercise success, failure, retry, repeated taps and uncertain outcomes. |
| Rendering, targets, contrast and enlargement | Not executed | Requires rendered implementation and measurements in required appearances/settings. |
| Accessibility behavior | Not executed | Verify names, roles, task order, status reachability and assistive activation on Apple environments. |

No executed implementation test is reported as passed or failed. The baseline defects come from the supplied description, not measured runtime failures.

# Guidance and evidence limits

Explicitly read the installed root [.agents/skills/apple-hig/SKILL.md](.agents/skills/apple-hig/SKILL.md), searched its topic index, and followed Foundations and Menus and actions family routes. Read SF Symbols, Accessibility, Color and Buttons topic procedures before their respective source guides. Followed SF Symbols’ explicit metaphor handoff to Icons and read its procedure before the Icons guide. Each instruction/source read used a separate cat or rg command for one file.

Material recommendations use these official links, accessed only through installed local snapshots:

- [Icons — Other](https://developer.apple.com/design/human-interface-guidelines/icons#Other): Archive → `archivebox`.
- [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols): weight, scale, variants, rendering and individual availability.
- [Color — Inclusive color](https://developer.apple.com/design/human-interface-guidelines/color#Inclusive-color): words/shapes alongside color; semantic adaptive colors.
- [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons): familiar labels, standard states, activation regions and pending indication.
- [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility): redundant cues, enlargement, descriptions and usable controls.

The installed guides identify a 2026-10-25 snapshot and contain derived application guidance, not SDK documentation. Links provide attribution; no web browsing occurred. No device, SDK, GUI, native preview, contrast calculation or assistive-technology execution occurred. The local guidance cannot establish deployment target, actual symbol availability, rendering, server behavior or licensing clearance. Those remain explicit implementation checks. A specification-level pass does not establish runtime accessibility or compatibility.
