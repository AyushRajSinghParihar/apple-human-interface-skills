# Revision result

Patched `interface.md` in place, replacing the one-paragraph problem description with an implementable macOS outline specification. The supplied description reports expansion selecting descendants, indistinguishable indentation, and collapse losing keyboard focus; no application code or rendered interface was supplied.

## Decisions and source support

- Separate expanded folder IDs, single selected item, and keyboard row target. Expansion never selects descendants. Single selection is a product assumption for source browsing, not an Apple mandate. Collapse alone replaces a hidden selected item with its visible ancestor to prevent invisible command targets.
- Preserve the tree through depth-first rendering, stable IDs, sibling-only sorting, and 16 pt additional leading indentation per level. The numerical indent is a product decision. [Outline views — Best practices](https://developer.apple.com/design/human-interface-guidelines/outline-views#Best-practices) supports primary-column hierarchy, hierarchy-preserving sorting, local/recursive expansion, and restored expansion.
- Use labelled inward/downward disclosure triangles. Empty folders have no active triangle; a 500-child folder expands into a bounded scrolling outline. [Disclosure triangles](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#Disclosure-triangles) supports the control’s meaning and direction; empty-folder treatment and bounded rendering are application decisions.
- Keyboard collapse keeps a visible ancestor target and the outline responder. Pointer collapse hides a now-invalid row focus indicator and retains a recovery anchor; the next arrow deliberately resumes on that ancestor. This preserves the source distinction between directional disappearance and other input, rather than asserting that every collapse should move focus. See [Focus and selection — Best practices](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices).
- Define arrow traversal, explicit opening, keyboard exit, and keyboard-accessible recursive commands. Avoid rename/open conflicts and preserve system shortcuts. Exact bindings require native verification. See [Keyboards — Best practices](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices).
- Require meaningful names, hierarchy and state exposure, complete alternative operation, and usability at 200% text scale. These are acceptance requirements, not demonstrated support. See [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility).

## Worked before/after

Illustrative fixture, not observed application data:

```text
Project                    depth 0
  Sources                  depth 1
    Utilities              depth 2
      Parser.swift         depth 3
  Empty                    depth 1, zero children
  Generated                depth 1, 500 children
```

Before, according to the supplied brief: expanding `Sources` selects every descendant; rows do not distinguish depth; collapse loses keyboard focus. The brief does not specify initial selection or exact key bindings.

After, by the revised contract:

1. Select `Project`, then click the `Sources` triangle. Its children appear while selection stays on `Project`. Each level advances another 16 pt. No file opens.
2. Expand `Utilities` and select `Parser.swift`. Press Left to select/target `Utilities`; press Left again to collapse it. `Utilities` remains the visible selected keyboard target. Up/Down continues traversal and Tab permits exit.
3. Alternatively, while `Parser.swift` is targeted, pointer-collapse `Sources`. Selection becomes `Sources`, the hidden row’s focus indicator disappears, and the outline retains its keyboard route. The next arrow resumes on `Sources` without an extra move. Reopening restores nested expansion, but does not reselect `Parser.swift`.
4. Select `Empty`: Right does nothing, Left returns to `Project`; no false expansion control appears. Expand `Generated`: its 500 children become reachable by scrolling and arrow navigation without selecting them en masse or enlarging the window to fit them.

## Acceptance checks and status

| Check | Status and evidence |
|---|---|
| Requested artifact patched | Passed by local file readback: `interface.md` contains the revised hierarchy, state model, transitions, and eight acceptance scenarios |
| Three reported defects covered | Passed as a specification review: independent expansion/selection; per-depth indentation; explicit keyboard and pointer collapse recovery |
| Edge cases covered | Passed as a specification review: empty source/folder, 500 children, deep/duplicate names, routine return, removal, local/recursive expansion, resizing and text enlargement |
| Document whitespace | Passed: `git diff --check` after the edits |
| Runtime acceptance scenarios 1–8 in interface.md | Not executed: no runnable implementation or Mac GUI was supplied |
| Native keyboard, Full Keyboard Access, assistive hierarchy/state, focus appearance, SDK compilation | Not executed; require an implementation and supported Apple environment |
| Measured geometry, contrast, rendering, responsiveness at 500 children | Not executed; no rendered UI or performance measurements exist |

Failed executed checks: none. A passed document review does not establish that the reported application defects are fixed in running software.

## Instruction audit and evidence limits

Explicitly read the installed root `.agents/skills/apple-hig/SKILL.md`, then the layout-and-organization family and its Outline views and Disclosure controls topic procedures before their source guides. Searched `references/topic-index.md` for outline, disclosure, keyboard, and accessibility concepts. Also read the Inputs family and Focus and selection / Keyboards procedures before their guides, and the Foundations family and Accessibility procedure before its guide. Every instruction/source read used a separate `cat` or `rg` command for one file, with paths resolved inside the installed package.

Used only the supplied local brief and installed guidance. The source guides identify a local snapshot/retrieval dated 2026-10-25; their existence does not establish independent source review. Official links above identify the basis of recommendations and were not fetched. No browser, device, GUI, SDK, Accessibility Inspector, VoiceOver, or Full Keyboard Access execution occurred. No framework/API availability, measured performance, or accessibility conformance is claimed. Single selection, indentation, opening destinations, and fallback rules are concrete product choices to validate against the real app’s requirements.
