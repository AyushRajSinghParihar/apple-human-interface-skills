# Repair decisions and patch summary

Edited `interface.md` in place, replacing the original three behaviors with a concrete macOS section contract. Each title and triangle now owns a single inline expansion; triangle orientation indicates state, multiple sections can remain open, and collapsed headers retain summaries and actionable validation text. The specification also defines initial states, independent state retention, validation recovery, focus handling, keyboard activation, semantic state, and layout under constrained space.

The confirmed specification defects were the non-orienting decorative triangle, conflicting title/triangle destinations, and missing indication of hidden invalid fields. No application implementation or screenshot was supplied. The word “panel” alone does not establish native floating-panel behavior; this change stays within its sections.

## Worked before/after

Illustrative data, not observed application content: Income has a subtotal of $72,000 and an empty required employer ID.

Before: collapsing Income hides the invalid field without an indication. The triangle changes position without changing orientation. Clicking “Income” opens another window; clicking the triangle expands details.

After: the collapsed header reads “Income details · $72,000 · 1 issue — Enter employer ID,” with an inward-pointing triangle. Clicking its title or triangle, or pressing Space while its header is focused, expands the same inline fields and points the triangle down. The empty employer ID shows its correction instruction. Entering a valid ID and revalidating removes the issue text. Collapsing and reopening retains the entered ID and subtotal. Expanding another section leaves Income unchanged. If the existing continue action finds this error while collapsed, it opens the section and focuses the employer ID field.

## Acceptance checks and status

Passed — static specification review:

- Both original activation paths now have one explicit inline result and ownership.
- Collapsed and expanded states specify distinct triangle orientations and stable placement.
- Common summaries/actions remain visible; invalid collapsed content has persistent text and a repair path.
- State retention, validation-triggered expansion, focus recovery, and independent sections have explicit contracts.
- Narrow layout, enlargement, keyboard activation, and exposed name/state have acceptance requirements.

Failed — no remaining contradiction identified in the revised text. This is not a runtime pass.

Not executed — implementation acceptance on macOS:

1. Click title and triangle separately; each toggles once, opens no window, and leaves other sections unchanged. Confirm actual orientation and inline reflow.
2. Traverse and toggle every header with keyboard input. Verify focus visibility, hidden-field exclusion, and focus recovery when collapsing a focused descendant.
3. With Accessibility Inspector and assistive input, verify one labelled header control, accurate state/content relationship, available error text, and usable field order.
4. Create an error in a collapsed section; confirm persistent issue text without focus theft. Invoke existing blocked continuation; confirm affected sections expand and the first invalid field receives focus. Correct and revalidate; confirm status clears.
5. Enter values, collapse/reopen, and toggle neighboring sections; verify values, calculations, and independent states survive.
6. Resize the panel and enlarge text to 200%; verify wrapping, scrolling, visible active header, and no clipping/overlap. Measure activation areas against the specified macOS 28 pt starting size.

## Sources and evidence limits

Read the installed [root skill](.agents/skills/apple-hig/SKILL.md), searched its topic index, then read the layout-and-organization family, disclosure-controls topic procedure, and disclosure source guide in that order. Also read the foundations family, accessibility topic procedure, and accessibility source guide before applying accessibility requirements. Each read used a separate single-file command. All paths resolved inside the installed package.

Material source support: [Disclosure controls](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#Disclosure-triangles), including its distinct [disclosure-button convention](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#Disclosure-buttons), and [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility). Links identify official articles; only supplied local snapshots were consulted, with no web access. Product choices about retained values, initial state, error recovery, and header hit areas are explicitly specified rather than attributed to automatic platform behavior.

Only Markdown was changed and statically inspected on the headless Linux server. No device, SDK compilation, GUI, Accessibility Inspector, VoiceOver, keyboard runtime, geometry measurement, or contrast execution occurred. Local guidance is a dated snapshot, not SDK verification or proof of current native behavior. Runtime checks above remain necessary before claiming the repair works in an app.
