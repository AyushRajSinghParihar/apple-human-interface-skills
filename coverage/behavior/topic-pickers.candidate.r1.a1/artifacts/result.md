# Revised medication reminder controls

Patched `interface.md` in place from a one-line problem statement into an implementable watchOS control specification. The patch replaces the unlabeled 1,440-value picker with labeled time wheels; makes Every day explicit; defines three named repeat choices; and adds draft persistence, Crown/touch mappings, Save/Cancel, validation, localization, and scheduling boundaries.

## Decisions and basis

- Use hour/minute wheels with optional AM/PM, retaining one-minute precision and all 1,440 time values. The brief requires a time of day, so a calendar date control adds no needed value. The installed [Pickers guidance](https://developer.apple.com/design/human-interface-guidelines/pickers#watchOS) supports watchOS wheels and locale-dependent display. It does not establish a particular SDK API or style/mode combination for this project.
- Use an explicit short single-selection list for Every day, Weekdays, and Weekends. The guide suggests simpler controls for short sets and supports watchOS navigation-link lists; direct named choices avoid numeric frequency encoding. The exact three presets and their day sets are proposed product scope because the supplied brief does not enumerate schedules. Closed-row Crown scrubbing is explicitly prevented by the interaction contract.
- Keep Time and Repeat one level from the summary and preserve the draft across interruptions, applying [Designing for watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices).
- Give Crown rotation one owner per context, visible response, precise slow adjustment, and a touch equivalent, following [Digital Crown](https://developer.apple.com/design/human-interface-guidelines/digital-crown#Apple-Watch). Remove the reset on every turn.
- Use system Done/Cancel and Save/Cancel buttons with clear commit scope, following [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#watchOS). The reminder changes only on successful Save.

Defaults, day sets, wheel wrapping, DST behavior, and time-zone policy are concrete design decisions rather than Apple rules. They require product and scheduler validation before shipping.

## Worked before/after

Scenario: the saved reminder is 08:30 Every day; the person wants 08:35 Weekdays.

Before: the single picker offers 1,440 unlabeled minute positions, its blank row means Every day, and each Crown turn resets it. The specification gives no dependable way to retain 08:35 or discover the repeat meaning; it does not establish that Weekdays exists.

After: the summary says `Time 8:30 AM` and `Repeat Every day` in a 12-hour locale. Open Time, select Minute, turn from 30 to 35, and tap Done. Hour remains 8 and AM remains selected. Open Repeat and select `Weekdays` with `Monday–Friday` beneath it. The summary now reads `8:35 AM · Weekdays`; Save persists hour=8, minute=35, repeat=weekdays. On a Friday after 08:35, the next eligible occurrence is Monday 08:35 local time. Cancel instead leaves the saved 08:30 Every day unchanged. No minute adjustment resets either value.

## Acceptance checks and status

Passed — static specification inspection:

- The required in-place patch exists and removes unlabeled values and the implicit blank default.
- All 1,440 daily minute values remain representable by the specified components; AM/PM meaning and locale formatting are distinct from storage.
- Repeat choices have stable identifiers, visible names, explicit day sets, and selection behavior.
- Crown ownership, touch equivalents, boundaries, interruption retention, local cancellation, global cancellation, and failed saving have concrete outcomes.
- Incoming invalid data and legacy blank repeat have separate handling; time-zone and DST policies are explicit.
- A worked scenario and executable acceptance scenarios are included. These passes establish specification completeness, not implementation behavior.

Failed — no revised-specification inconsistency was identified in static review. The original reset and unlabeled/blank choices are documented defects of the supplied specification; no running app was inspected.

Not executed — SDK compilation/API availability; native wheel rendering; Watch readability and target geometry; Crown speed/precision; touch selection; haptics; accessibility behavior; localization rendering; wrist interruption recovery; persistence; and notification/scheduler execution, including DST and time-zone tests. Acceptance checks in `interface.md` remain requirements for those validations.

## Evidence limits and audit trail

Used only supplied local files and installed instructions; no web browsing. Official links above are source attribution from the installed snapshot, not independently fetched pages. The local reference snapshots are dated 2026-10-25; their recorded Apple revision dates differ. No device, SDK, GUI, simulator, assistive technology, or notification delivery was executed. No framework, deployment version, source implementation, or clinical scheduling requirement was supplied, so native API feasibility and the proposed repeat presets remain unverified.

Instruction reads used one file per shell command. Read installed `.agents/skills/apple-hig/SKILL.md` first, then `interface.md`, then searched `references/topic-index.md` for watchOS, date, frequency, and picker-related concepts. All subsequent paths were resolved inside that installed apple-hig package. For each route below, read the family SKILL.md, then the topic SKILL.md, then its source guide:

- `subskills/apple-hig-getting-started/` → `.topics/apple-hig-designing-for-watchos/SKILL.md` → `references/designing-for-watchos.md`.
- `subskills/apple-hig-selection-and-input/` → `.topics/apple-hig-pickers/SKILL.md` → `references/pickers.md`.
- `subskills/apple-hig-inputs/` → `.topics/apple-hig-digital-crown/SKILL.md` → `references/digital-crown.md` (routed from the watchOS procedure for the selected Crown interaction).
- `subskills/apple-hig-menus-and-actions/` → `.topics/apple-hig-buttons/SKILL.md` → `references/buttons.md` (for explicit commit and cancellation actions).
