# Apple Human Interface Skills

**One skill. The Apple Human Interface Guidelines, routed by the task at hand.**

An independent, portable Agent Skills package for designing, implementing, and
reviewing Apple interfaces. Start with `apple-hig`; it selects focused topic skills
and article references instead of loading an entire design manual into context.

The current source inventory contains **158 articles across 13 topic families**,
plus 15 organizational pages. Guidance is written originally, with official
sources, platform differences, factual specifications, and supplementary visual
explanations.

**Coverage is audited, not assumed.** See the generated [coverage report](coverage/REPORT.md)
for the snapshot date, article review results, and remaining work. File or route
counts alone do not establish complete substantive coverage.

## Install

Install on the machine where your coding agent runs. The package consumes only
local Markdown files; it does not require Python, an API key, a browser, or a
network connection for ordinary use.

```bash
git clone https://github.com/AyushRajSinghParihar/apple-human-interface-skills.git
cd apple-human-interface-skills
```

For **Codex**, link the complete package into the user skills directory:

```bash
mkdir -p ~/.agents/skills
ln -s "$PWD/skills/apple-hig" ~/.agents/skills/apple-hig
```

For **Claude Code**, use its personal skills directory:

```bash
mkdir -p ~/.claude/skills
ln -s "$PWD/skills/apple-hig" ~/.claude/skills/apple-hig
```

If the destination already exists, inspect it before replacing it. A full folder
copy works too. For project-scoped installation, copy the complete `apple-hig`
folder into the agent's project skills directory. Other Agent Skills clients can
use the same folder; follow that client's discovery rules.

Restart or refresh the agent's skill discovery after installation. Use `$apple-hig`
in Codex, `/apple-hig` in Claude Code, or ask explicitly to apply Apple HIG.
Runtime details: [Codex skills](https://learn.chatgpt.com/docs/build-skills),
[Claude Code skills](https://code.claude.com/docs/en/skills).

## Try it

```text
Use $apple-hig to review this iPadOS sidebar and toolbar for resizing,
keyboard access, and large text. Cite the relevant HIG guidance.
```

```text
Use $apple-hig to adapt this playback interface for Apple TV and Vision Pro.
Explain how focus, input, materials, and navigation should differ.
```

```text
Use $apple-hig to design an Arabic reading app for iPhone and Mac.
Check layout direction, typography, accessibility, and navigation.
```

The router reads the relevant family entry points and article files. Nested
subskills are **explicitly loaded by relative path**; the package does not assume
that every agent automatically discovers nested skills as separate commands.

## What's inside

| Family | Topics include | Articles |
|---|---|---:|
| Getting started | Six platforms, principles, games, device adaptation | 9 |
| Foundations | Accessibility, typography, layout, color, materials, privacy, RTL | 18 |
| Patterns | Onboarding, accounts, loading, feedback, search, sharing, media | 25 |
| Content | Charts, image views, text views, web views | 4 |
| Layout and organization | Lists, collections, split views, tab views, grouping | 10 |
| Menus and actions | Buttons, menus, toolbars, menu bar, ornaments | 12 |
| Navigation and search | Sidebars, tab bars, search fields, path/token controls | 5 |
| Presentation | Alerts, sheets, popovers, panels, scrolling, windows | 8 |
| Selection and input | Fields, pickers, sliders, toggles, selection controls | 11 |
| Status | Activity rings, gauges, progress, ratings | 4 |
| System experiences | Widgets, Live Activities, notifications, snippets | 10 |
| Inputs | Touch, focus, keyboard, pointer, eyes, gestures, sensors | 13 |
| Technologies | CarPlay, Siri, VoiceOver, payments, AI, system integrations | 29 |

Browse the [topic index](skills/apple-hig/references/topic-index.md) or
[platform and task routes](skills/apple-hig/references/platforms-and-tasks.md).

```text
skills/apple-hig/
  SKILL.md                       Small router
  LICENSE                        License retained when copying the package
  agents/openai.yaml             Optional Codex presentation metadata
  references/                    Topic index, task routes, media explanations
  subskills/apple-hig-*/
    SKILL.md                     Family-specific decisions and article links
    references/*.md              Original article-level guidance
coverage/                        Source manifest, independent reviews, report
scripts/hig.py                   Authoring and maintenance utility
tests/                           Extraction and package-contract tests
```

## What “complete” means

The bounded corpus is the **current English HIG**, discovered from Apple's
[navigator](https://developer.apple.com/tutorials/data/index/design--human-interface-guidelines),
in-HIG links, and [design update history](https://developer.apple.com/design/whats-new/).
The manifest accounts for sections, tables, notes, platform variations, media,
redirects, and external dependencies. Independent approvals are bound to source
and destination hashes, so later changes invalidate stale review.

Translated editions, archived guidelines, and the full libraries of linked SDK
documentation and WWDC videos are outside this corpus. Unavailable historical
pages are recorded explicitly. Original image/video explanations cover relevant
lessons; Apple assets and raw documentation are not distributed here.

This package preserves documented qualifications and source conflicts rather than
inventing universal rules. API names, SDK availability, and newer OS changes still
need the appropriate official implementation documentation.

## Maintain and verify

Maintainers need Python 3.11 or later. PyYAML enables stricter frontmatter parsing.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/hig.py check
```

Check for upstream changes without changing the tracked source snapshot:

```bash
.venv/bin/python scripts/hig.py check --live
```

Refresh the source inventory and coverage report:

```bash
.venv/bin/python scripts/hig.py discover
.venv/bin/python scripts/hig.py report
```

Discovery saves raw structured sources only in ignored `.cache/`. It retains
pending/failed sources in coverage accounting and does not rewrite article prose
or grant semantic approval. Resolve changed guidance and obtain independent review
before publishing a complete-coverage claim. `check --allow-pending` is a development
check only; the release check remains strict.

See [skill design research](docs/skill-design.md), [source and review method](docs/source-method.md),
[audit evidence](coverage/audit.md), [evaluations](coverage/evaluations.md), and
[contribution instructions](CONTRIBUTING.md).

## Sources and license

Skill structure follows the [Agent Skills specification](https://agentskills.io/specification)
and [authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):
small entry points, progressive disclosure, precise routing, and realistic tests.

Original code and guidance are [MIT licensed](LICENSE). This is an independent
community project, unaffiliated with Apple. Apple documentation, trademarks, and
referenced media remain their respective owners' property.
