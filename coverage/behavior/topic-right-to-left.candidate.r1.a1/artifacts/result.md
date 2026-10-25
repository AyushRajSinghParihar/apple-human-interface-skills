# RTL adaptation result

Patched `interface.md` in place, replacing the supplied single-paragraph defect description with a concrete iPadOS specification. The patch defines semantic RTL hierarchy and navigation, per-asset mirroring rules, mixed-language alignment, locale-formatted money, growing Arabic labels, narrow/wide state preservation, and observable acceptance criteria.

## Decisions and support

| Decision | Reason and source |
|---|---|
| Mirror reading-order navigation and hierarchy, preserve logical data order | Back/forward semantics must match Arabic reading direction. [Right to left — Controls](https://developer.apple.com/design/human-interface-guidelines/right-to-left#Controls); [Layout — Visual hierarchy](https://developer.apple.com/design/human-interface-guidelines/layout#Visual-hierarchy). |
| Preserve Play and physical-direction meaning; classify every arrow | Blanket reflection changes meaning. Play preservation is the applied semantic decision for the supplied media icon; it is not a claim that every media control is identical. [Right to left — Interface icons](https://developer.apple.com/design/human-interface-guidelines/right-to-left#Interface-icons). |
| Preserve digit order; format currency by region and numeral preference | Arabic is not one universal currency/numeral convention. Bidirectional isolation and round-trip checks are implementation requirements proposed here. [Right to left — Numbers and characters](https://developer.apple.com/design/human-interface-guidelines/right-to-left#Numbers-and-characters). |
| Separate alignment from text direction | Short labels/list entries track the interface; long paragraphs track their language. Standalone email gets an explicit LTR value field. [Right to left — Text alignment](https://developer.apple.com/design/human-interface-guidelines/right-to-left#Text-alignment). |
| Wrap labels, grow rows and stack values; retain state during resizing | Correct Arabic layout must survive longer text and smaller windows. [Typography — Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type), [Layout — Adaptability](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability), [iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados). |

## Worked before/after

The input describes defects without actual labels, amounts or coordinates. This is a constructed fixture illustrating those defects, not an observed screenshot.

Task: open `المصروفات المنزلية والاشتراكات الشهرية`, inspect its `Cloud Storage` child with amount 1234.50 SAR and contact `finance@example.com`, then return.

| Before, as characterized by the brief | Revised specification |
|---|---|
| Hierarchy still starts left; navigation retains LTR assumptions | Parent starts right; child inset is measured from right. Child navigation points left; Back sits right and points right. Return restores selection. |
| Mechanical flip reflects Play along with arrows | Navigation direction adapts; Play remains right-pointing and keeps its action. |
| Currency digits reorder | Numeric sequence remains 1234.50 in the selected numeral system, with locale-derived separators and currency placement. For Eastern digits the illustrative numeric run is `١٬٢٣٤٫٥٠`; the whole formatted SAR string remains formatter-defined. |
| Every text value right aligned | Arabic label and English category title share the list's right leading edge. Standalone email is an LTR, left-aligned value; an English paragraph of three or more lines is left aligned. |
| Long Arabic title clips | Title wraps fully; row grows and amount moves below when required. Narrowing/widening retains the selected child and draft. |

## Acceptance status

**Passed — static specification review:** All five reported defect classes have explicit replacement rules in `interface.md`. The revised contract distinguishes Back, child disclosure, expand/collapse, Play and literal direction. It includes locale/numeral money fixtures, mixed-text fixtures, long-label reflow and state preservation. Both requested project files were written and read back.

**Failed:** No revised-specification failure identified in this static review. The five original defects are supplied descriptions, not independently reproduced runtime failures.

**Not executed:** Every runtime acceptance scenario in `interface.md`, including actual formatter outputs, native Arabic shaping, punctuation rendering, copy/paste and bidirectional editing; all window/text-size measurements; touch/keyboard/pointer operation; accessibility navigation and activation; device comfort; SDK compilation. These remain acceptance gates for implementation, not passed tests. No GUI, simulator, Apple device, SDK or accessibility execution is claimed.

## Evidence and route limits

Explicitly read the installed root `.agents/skills/apple-hig/SKILL.md`, then searched its complete topic index. Read the Getting started family → Designing for iPadOS procedure → source guide; Foundations family → Right to left procedure → source guide; and routed Layout, Typography and Accessibility procedures before their corresponding source sections. Each read used a separate single-file command. Typography's applicable opening sections were read separately after a longer output was truncated; no numerical style-table claim depends on the truncated material.

Only the supplied `interface.md` and installed guidance informed this work. Source links above identify the official articles referenced by the local snapshot; no website was opened. The package is independent guidance, not an SDK reference or proof of current API behavior. There is no supplied implementation, screenshot, layout measurement, selected Arabic region or native-language review. Pane behavior, fixture copy and exact state rules are concrete proposed product decisions, not discovered existing features. Keep the existing framework; confirm region, numeral preferences, translation and Arabic optical balance during implementation. The patch is a revised specification, not an implemented or verified app.
