# CareKit visual examples

Source: [Apple HIG CareKit](https://developer.apple.com/design/human-interface-guidelines/carekit). Snapshot: 2026-10-25.

These original notes describe inspected primary/alternate images. The [main guide](../../subskills/apple-hig-technologies/references/carekit.md) retains care-task, chart, privacy, and communication guidance. Sample treatment names, quantities, schedules, people, and addresses are illustrative.

## Cards and task forms

The overview combines scheduled tasks and symptom/treatment charts in a vertical daily-care view. Its neighboring contacts screen separates communication into its own cards. The annotated card identifies a title/header, optional disclosure and separator, and content beneath; these parts need a coherent hierarchy rather than several unrelated controls.

| Inspected task form | Visible interaction |
| --- | --- |
| Simple | A short title and schedule beside one completion control. |
| Instructions | A title/schedule followed by an instruction and a large completed-state control. |
| Log | An action records a symptom event and shows its timestamp beneath. |
| Checklist | Individually labeled rows have separate completion states. |
| Grid | Compact labeled time choices fit side by side, with optional instruction text below. |

The checklist and grid examples both distinguish completed checks from pending empty circles, so state remains perceivable without relying only on pink tint. Their different space use supports choosing by label/detail needs.

## Charts

The bar, scatter, and line examples depict the same daily axis and dataset through different marks. Bars emphasize each day's amount; individual points show observations; the connected line emphasizes change between observations. Each keeps its title, axis markers, highlighted day, and dataset legend distinct. The daily letters are sample labels, not a reason to omit time-unit context when it would be ambiguous.

## Contacts and appearance

The simple contact card contains identity/role and a disclosure affordance. The detailed alternative adds a short professional description, separate Call/Message/Email actions, and an address with navigation affordance. The expanded contacts screen repeats that structure for multiple care-team members.

Across light/dark pairs, the card hierarchy, spacing relationships, completion shapes, chart marks, and contact actions remain stable. Surfaces and text contrast adapt; the sample accent color alone does not carry completion or role meaning.
