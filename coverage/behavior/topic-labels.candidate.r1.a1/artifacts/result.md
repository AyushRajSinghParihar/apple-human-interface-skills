# Revised Mac network-diagnostics labels and interactions

## Scope and evidence

The supplied `interface.md` describes macOS, four fields titled “Value,” units available only in help, overlapping localized labels, decorative headings announced as controls, and status changes replacing field titles. These are reported problems, not independently observed runtime defects. No field schema, help article, screenshot, implementation, dimensions, or diagnostic lifecycle was supplied.

The following is a framework-agnostic design contract. For a concrete worked configuration, assume the four editable fields configure a repeated network probe: destination, packet count, interval, and timeout. Those meanings, units, ranges, and examples are proposed product decisions, not facts recovered from the brief. Confirm them against the real diagnostic engine before implementation; never rename a field by its screen position alone. If the actual fields are measurements rather than inputs, retain their real meanings and expose them as read-only values instead.

## Decisions and replacement strings

Use the screen title **Network Diagnostics**. Keep each field’s identity unchanged across idle, editing, validation, running, and result states. Put runtime information in a separate **Status** region. Labels and units remain visible when a field contains text, has focus, is invalid, or is unavailable.

| Proposed stable ID | Persistent visible label | Value contract | Persistent supporting text | Example |
| --- | --- | --- | --- | --- |
| destination | Destination: | Required hostname or IPv4/IPv6 address; no URL scheme or path | Enter a hostname or IP address. | example.com |
| packetCount | Packet count: | Integer from 1 through 100 | Number of packets to send. | 10 |
| interval | Interval (ms): | Integer from 100 through 60000 milliseconds | Time between packets, in milliseconds. | 1000 |
| timeout | Timeout (ms): | Integer from 100 through 60000 milliseconds | Maximum wait for each reply, in milliseconds. | 3000 |

Examples are hints, not defaults or substitutes for labels. No automatic conversion of stored units is authorized. If the engine stores seconds, convert explicitly at the model boundary and verify round trips; do not merely append “ms” to existing numbers. The ranges above are proposed guardrails requiring engine confirmation.

Purpose-specific, persistent captions resolve ambiguity during entry. Keeping format guidance next to inputs follows [Writing — Best practices](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices) and [Text fields — Best practices](https://developer.apple.com/design/human-interface-guidelines/text-fields#Best-practices). These exact field names and ranges are design choices; HIG does not specify network settings.

Use real text for captions. Essential names and units use primary foreground treatment; supporting explanations use secondary treatment. Do not style required units as unavailable content. Prefer standard Mac control typography or the stack’s equivalent, with a readable fallback rather than an embedded image or required Apple font installation. Start essential labels at the Mac reference default of 13 pt and provide product text scaling through at least 200%. macOS has no Dynamic Type; this is an explicit product accommodation. See [Labels — Best practices](https://developer.apple.com/design/human-interface-guidelines/labels#Best-practices), [Typography — macOS](https://developer.apple.com/design/human-interface-guidelines/typography#macOS), and [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

## Layout and semantic contract

Use vertically stacked field groups: caption, input, supporting text, then any correction. Keep all four input leading edges aligned. Let captions and supporting text wrap to their measured height; the next element follows that height in normal layout flow. Do not overlay captions, shrink text to fit, or truncate essential names and units. This deliberately removes the side-by-side label/input collision described in the brief.

When height is constrained, allow vertical scrolling with focus scrolled into view. Preserve values, focus identity, and group order during resize or text scaling. Use available content width and actual text measurements, not a hard-coded English-label width or device-name breakpoint. Validate the smallest supported content width before setting a minimum window size. These choices apply [Layout — Adaptability](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability); actual fit remains untested.

Each input exposes a stable identity, editable-text role, accessible name derived from its visible caption, current value, required state, and associated help/error description. Accessible names omit punctuation-only colons and expand `ms` to “milliseconds”; for example, “Timeout, milliseconds.” Do not append status or the current value to the name. Expose the value separately. Bind by stable ID so resizing or localization cannot attach a caption to the wrong input. Avoid a second redundant accessibility stop for the associated caption where the stack supports that relationship.

Meaningful structural titles are headings with no activation action or button/link role. Purely ornamental heading text that conveys no unique structure is omitted from accessibility navigation and keyboard focus. Do not hide a useful heading merely because it is noninteractive. Reading order is title, each caption/input/help/error group in the table’s order, then Status. Tab and Shift-Tab traverse the four editable fields in that order and then any existing actions; decoration and status are excluded from Tab traversal. Preserve existing system shortcuts.

These semantics follow [VoiceOver — Descriptions and Navigation](https://developer.apple.com/design/human-interface-guidelines/voiceover#Navigation) and [Accessibility — Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Speech). They specify intended behavior, not a tested accessibility tree or exact spoken transcript.

## Editing, validation, and status transitions

Keep existing commit and cancel mechanisms; the brief supplies no action controls, so this revision does not invent a toolbar, panel window style, or diagnostic launch UI.

Allow partial input while typing. Validate on leaving a changed field and on the existing commit event. Parse numbers with a locale-aware integer parser; accept valid localized digits/grouping where supported, reject fractional or ambiguous values without stripping punctuation into a different number. Preserve the entered string when correction is needed. Validate destination syntax locally without treating DNS failure as malformed input.

On invalid commit, retain all drafts, prevent submission, and focus the first invalid input. Associate a nearby correction with that input:

- Empty destination: “Enter a hostname or IP address.”
- Malformed destination: “Enter a hostname or IP address without a URL scheme or path.”
- Invalid packet count: “Enter a whole number from 1 to 100.”
- Invalid interval or timeout: “Enter a whole number from 100 to 60000 milliseconds.” Localize the displayed numbers.

Commit valid parsed values atomically. Cancel restores the last committed configuration and clears draft errors. Do not alter the original network operation’s cancellation behavior. This validation timing and remedy follow [Text fields — Best practices](https://developer.apple.com/design/human-interface-guidelines/text-fields#Best-practices).

```text
onFieldEdit(id, text):
    draft[id] = text                 // label/name never changes
onFieldExit(id):
    errors[id] = validate(draft[id], schema[id], locale)
onExistingCommit():
    validate every field
    if errors: retain drafts; focus first invalid input; return
    commit parsed configuration atomically
onDiagnosticEvent(event):
    statusText = statusFor(event)    // separate node; never write field labels
    expose current status to accessibility
    notify meaningful state transitions without moving focus
```

Status copy is **Ready**, **Running diagnostics…**, **Diagnostics complete**, or **Diagnostics could not finish**. A failed operation adds the engine’s specific, actionable reason when known; do not invent “offline,” “DNS failure,” or another cause. A completed test with negative findings still says “Diagnostics complete”; completion does not mean the network is healthy. Status remains readable until superseded. Announce meaningful transitions once through the stack’s supported mechanism; do not repeatedly announce every packet or interrupt typing. If another run starts, use its identity to ignore stale events from previous runs. This event policy is a product recommendation applying [VoiceOver — Navigation](https://developer.apple.com/design/human-interface-guidelines/voiceover#Navigation).

## Worked before/after

**Before, as reported:** Four captions all read “Value.” A person entering `3000` must consult help to learn its unit. A longer translation overlaps its input. When the diagnostic state changes, a field title is replaced; the original purpose disappears. Decorative headings sound actionable.

**After, using the proposed probe schema:** The fourth group reads “Timeout (ms):” above an input containing `3000`, with “Maximum wait for each reply, in milliseconds.” beneath it. Its accessible name is “Timeout, milliseconds,” its role is editable text, and its value is `3000`. During a run, the separate Status reads “Running diagnostics…” while the timeout caption stays unchanged. When the run completes, Status becomes “Diagnostics complete,” without moving focus or implying healthy connectivity. At increased text size or with a longer translated caption, the caption wraps and pushes the input downward. Ornamentation has no action role; useful section headings retain heading semantics.

Entering `3.5` in this integer timeout model preserves that draft and displays the whole-number remedy on field exit. Replacing it with `3000` clears the error after successful validation. Cancel restores the last committed timeout rather than silently rounding or converting the draft.

## Acceptance checks and current results

**Passed — document inspection only:** All four proposed fields have unique, persistent captions; units are present in the panel specification; status has a separate identity; semantic association, wrapping, commit/cancel, correction, and focus rules are explicit. A manual trace of the worked example preserves the timeout label through running and completion. This establishes specification coverage only.

**Failed — supplied baseline description:** Generic field captions, help-only units, overlapping translations, actionable decoration, and status replacing titles fail the intended contracts above. These failures are reported by `interface.md`; no independent execution confirmed them.

**Not executed — implementation acceptance:**

| Check | Pass condition |
| --- | --- |
| Schema mapping | Each stable ID maps to the actual field meaning, stored unit, editable/read-only state, and supported range; no positional guessing or unit relabeling |
| Input states | Empty, partial, fractional, out-of-range, valid, pasted, and localized values preserve drafts and produce the specified correction/commit behavior; valid boundaries succeed |
| Status sequence | Ready → running → completion/failure changes only status; duplicate/stale events do not rename fields, repeat announcements, or steal focus |
| Resize/localization | At smallest, intermediate, and largest supported widths; normal and 200% text; longer pseudo-localized and actual supported translations: no overlap, clipping, detached units, or lost input |
| Visual access | Standard and emphasized text remains legible; measure actual foreground/background contrast in light, dark, and increased-contrast presentations; essential status is textual |
| Keyboard | Tab/Shift-Tab follow task order, every necessary existing action remains reachable, and focused content is visible after resize/scroll |
| Accessibility on Mac | Inspect names/roles/values/relationships; use VoiceOver to read all four fields and status, navigate meaningful headings, and verify decoration has no action; verify updates and correction focus without duplicate speech |
| Copy | Input values remain selectable/copyable; useful error text can be copied without requiring a new action control |

## Evidence limits and guidance audit

Only local supplied text and installed instructions were used; no web browsing occurred. Official links above identify the source articles represented by the local snapshot, not newly verified online content. No Apple SDK, GUI, Mac device, rendering, network probe, contrast measurement, keyboard session, Accessibility Inspector, or assistive-technology execution was performed. No implementation exists here to establish runtime acceptance. Localization pronunciation, exact geometry, font shaping, announcement behavior, and diagnostic-engine compatibility remain unverified.

Installed root explicitly read: `.agents/skills/apple-hig/SKILL.md`. The complete topic index was searched for labels, writing, fields, accessibility, and layout. Family → topic procedure → supporting reference routing was followed for Layout and organization → Labels; Selection and input → Text fields; Foundations → Writing, Accessibility, Layout, Typography; Technologies → VoiceOver. All paths resolve inside the installed `apple-hig` package. Each instruction/reference read used a separate one-file shell command. The word “panel” alone does not establish a floating macOS inspector, so this specification makes no window-type or platform-feasibility change.
