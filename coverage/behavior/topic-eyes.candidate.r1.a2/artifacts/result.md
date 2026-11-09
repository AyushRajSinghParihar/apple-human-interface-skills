# Gallery specification repair

Patched interface.md in place. The original one-line specification required look-to-open, exact per-person gaze heatmaps, continuous staring, small controls, and controls that jump toward gaze. The revision replaces every assumption with a concrete targeting/activation contract, navigation state table, control geometry, alternative access requirements, and a data-purpose matrix.

## Decisions and support

- Looking targets a control; deliberate activation opens the artwork. Hover is private system presentation, not an app business event. Remove automatic opening and all gaze analytics. Supported by [Eyes](https://developer.apple.com/design/human-interface-guidelines/eyes) and [Privacy — visionOS](https://developer.apple.com/design/human-interface-guidelines/privacy#visionOS).
- Keep the image open until explicit Back navigation, with gallery context restored. No gaze-presence timeout. This persistence and return model is a product decision applying the separation between targeting and activation, and accessibility guidance favoring explicit dismissal: [Accessibility — Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive).
- Use stable image/title targets and standard hover/press feedback. Adopt at least 60 × 60 pt activation regions, 16 pt gaps between target bounds, and the button padding rule. These are specification requirements; no existing geometry was measurable. See [Eyes — Making items easy to see](https://developer.apple.com/design/human-interface-guidelines/eyes#Making-items-easy-to-see) and [Buttons — visionOS](https://developer.apple.com/design/human-interface-guidelines/buttons#visionOS).
- Use a movable Shared Space window and resting-hand indirect activation. Ordinary gallery browsing does not establish a need for immersion. This is a product choice applying [Designing for visionOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos#Best-practices).
- Specify complete alternative activation paths, meaningful control names, Zoom support, and enlarged-text reflow. These requirements follow [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility); their implementation remains unverified.

The local Eyes guide describes declarative custom hover applied outside the app process; the local Buttons guide says custom hover effects are unsupported for visionOS buttons. This revision conservatively uses standard feedback only, without claiming custom hover is universally unavailable. Accessibility lists a 60 × 60 pt default and a smaller 28 × 28 pt minimum, whereas Buttons requires 60 pt targeting. The revision adopts 60 × 60 pt for gallery actions rather than using the smaller minimum to justify dense controls. The 16 pt spacing choice is a conservative product choice from Eyes' margin-or-center-distance alternatives, not a universal requirement to satisfy both.

## Worked before/after

Before: A person scans past “Coast.” Merely looking opens it and is assumed to contribute exact coordinates to a personal heatmap. Looking toward a small control makes that control jump, and looking away closes the image.

After: Scanning past “Coast” produces only standard system hover feedback; app state and analytics remain unchanged. The person looks at the stable tile and pinches once, or activates “Open Coast” through supported assistive input. Detail opens. They look away and rest their hands; the image stays open. Activating the stable “Back to Gallery” button returns to the prior scroll position and tile. No gaze data or analytics event is stored or transmitted.

## Acceptance checks and status

Passed — static specification inspection:

- All five original problematic requirements are replaced in interface.md.
- The state table distinguishes system hover, navigation focus, deliberate activation, persistent detail, and return state.
- Controls have named outcomes, visionOS point-based target/separation constraints, and equivalent activation requirements.
- Privacy rules prohibit gaze heatmaps and proxies; allowed navigation state has an explicit in-memory lifetime and no analytics transfer.

Failed: No remaining contradiction found in the revised prose. This is not a claim that an implementation passed.

Not executed — implementation acceptance scenarios:

| Scenario | Required observable result |
| --- | --- |
| Scan tiles, linger, blink, and look away without activating | No image opens, state changes, or analytics writes; only system feedback changes. |
| Activate one tile using resting-hand indirect input | Exactly that artwork opens once; no repeated reach is required. |
| Look away from open detail for an arbitrary interval | Detail stays open with Back available; no app gaze timer exists. |
| Activate Back after scrolling and opening | Gallery scroll and last activated tile return; navigation focus returns appropriately. |
| Delay/fail image loading, retry, then leave before completion | Loading/error remains understandable; Retry works; Back always works; late completion never reopens detail. |
| Inspect normal, hover, and pressed layouts at constrained window sizes | Targets remain stable and nonoverlapping; 60 × 60 pt regions, 16 pt gaps, center spacing and padding satisfy the spec. |
| Complete open–inspect–return using supported keyboard, Switch Control, and hand/head Pointer Control | Every essential control is reachable and activatable with meaningful names, without eye targeting or speech. |
| Use system Dwell Control | Its deliberate activation invokes the same action; the app adds no gaze observation or custom dwell timer. |
| Enlarge text to 200% and use Zoom | Labels and Back/Retry remain available without clipped essential actions or overlapping targets. |
| Audit event handlers, telemetry schema, persistence, and network traffic | No gaze/hover/dwell/proxy collection; only specified in-memory navigation state exists. |
| Wear Vision Pro across seated postures and window placements | Targets and feedback are responsive and comfortable; controls do not chase gaze or require sustained staring. |

## Evidence limits and audit route

Only the supplied interface.md and installed local instructions/guides were used; no web browsing occurred. Official links above identify the articles referenced by the local snapshot, not pages fetched during this task. The installed references identify a 2026-10-25 snapshot/retrieval date and describe themselves as derived application guidance. Their existence does not establish independent review or current SDK support.

Auditable reads used one file per shell command. Read the installed apple-hig root SKILL.md explicitly, inspected interface.md, searched references/topic-index.md for gaze/eyes, visionOS, hover, accessibility and buttons, then read these owning family SKILL.md files: getting-started, inputs, foundations, menus-and-actions. Next read the routed topic SKILL.md files for Designing for visionOS, Eyes, Privacy, Accessibility, and Buttons before reading their corresponding reference articles. All paths were resolved within .agents/skills/apple-hig; no sibling package or network source was substituted.

No executable app, SDK project, measured layout, or telemetry implementation was supplied or exercised. No device, simulator, GUI, SDK compilation, Accessibility Inspector, assistive-technology execution, or physical comfort test was performed. Static prose inspection establishes only the revised contract's presence and consistency. API availability and all runtime checks above remain pending in an appropriate Apple environment.
