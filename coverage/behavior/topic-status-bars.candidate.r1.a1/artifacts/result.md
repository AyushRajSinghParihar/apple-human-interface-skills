# Status-bar repair decisions

Patched `interface.md` in place, replacing the defect-only brief with an implementable iPhone reader specification. It removes fake device status, keeps native status visible, defines deterministic fullscreen/control/error states, protects safe regions, and specifies network recovery and acceptance checks.

## Decisions

- Fullscreen hides app controls while native time, connectivity, and battery remain available. [Status bars](https://developer.apple.com/design/human-interface-guidelines/status-bars#Best-practices) permits temporary hiding for fullscreen media; always-visible status is our conservative product choice for reading.
- A stable contrasting status background and environmental safe-area constraints separate edge-to-edge decoration from important content, following [Layout](https://developer.apple.com/design/human-interface-guidelines/layout#Guides-and-safe-areas).
- A page tap reveals controls only; explicit commands hide controls or exit fullscreen. Preserve reading position and ordinary Home gestures, applying [Going full screen](https://developer.apple.com/design/human-interface-guidelines/going-full-screen#Best-practices). Exact transitions are product decisions.
- A failed content request gets persistent safe-area feedback and a truthful Retry lifecycle, applying [Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices). The brief does not identify the failed operation or loss consequences, so the revised specification explicitly assumes unavailable reading content. System-styled commands and target geometry follow [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons).

## Worked before/after

Before, as reported by the supplied brief: app-drawn time/battery overlays system status; page taps change status visibility unpredictably; critical network errors hide behind the overlay; content obscures safe areas.

After, specified scenario: the person enters fullscreen in section 3. Native status stays visible and app controls hide. One inactive-page tap reveals controls; two more taps leave them shown. The person explicitly hides controls, then loading section 4 fails. Controls reappear and “Couldn’t load the next section. Your current section is still available.” appears in reserved safe space below status. Section 3 stays readable at the same anchor. Retry displays “Retrying” and prevents duplicates. Repeated failure preserves the error; confirmed content delivery clears it without jumping to section 4 or hiding controls. This is a worked specification, not an observed runtime trace.

## Acceptance and evidence status

**Passed — document inspection:** the revised artifact covers native-only status ownership, hidden/revealed app controls, restoration, safe-area layout, tap precedence, explicit exit/return, and error priority with pending/failure/success recovery. Each reported defect has a concrete correction. The six acceptance checks in `interface.md` define observable outcomes.

**Failed — supplied baseline:** the original brief reports fake status, hidden errors, unpredictable visibility, and safe-area overlap. These are reported baseline defects, not independently reproduced failures. No runtime pass or failure is established.

**Not executed — implementation acceptance:** execute all six checks against the actual iOS app, covering bright/dark/mixed content, themes, repeated taps, links/scrolling/selection, injected network outcomes, orientations, camera housings, text sizes, Display Zoom, Home departure, foreground return, and explicit exits. Verify actual status contrast, unobscured controls/errors, hit geometry, and position retention.

## Evidence limits and route audit

Read the installed root `.agents/skills/apple-hig/SKILL.md` explicitly, searched its topic index, and read each owning family and topic procedure before the corresponding source guide. Routes: System experiences → Status bars; Patterns → Going full screen and Feedback; Foundations → Layout; Menus and actions → Buttons. Each instruction/source read used a separate single-file command. Supporting guides were the corresponding installed `references/*.md` files, dated 2026-10-25.

Only supplied local files and installed instructions were used. The original artifact was one sentence, without app source, framework details, screenshots, SDK documentation, or runtime evidence. No web browsing, device, SDK compilation, GUI, or accessibility execution occurred. Apple links attribute the installed snapshot; they were not verified live. This work repairs the specification, not a running app. API integration and availability remain to be verified in the existing stack.
