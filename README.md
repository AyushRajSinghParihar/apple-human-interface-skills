# Apple Human Interface Skills

**Help your coding agent make better Apple interfaces.**

[![Validate skill package](https://github.com/AyushRajSinghParihar/apple-human-interface-skills/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/AyushRajSinghParihar/apple-human-interface-skills/actions/workflows/validate.yml)
[![skills.sh](https://skills.sh/b/AyushRajSinghParihar/apple-human-interface-skills)](https://skills.sh/ayushrajsinghparihar/apple-human-interface-skills/apple-hig)

Designing an iPhone app, reviewing a Mac interface, or adapting a screen for Apple
Watch? `apple-hig` gives your agent practical guidance from Apple’s Human Interface
Guidelines. It covers **158 topics across 13 areas**, from buttons and navigation
to accessibility, privacy, and platform conventions.

Ask for what you need. The skill finds the relevant guidance, applies it to your
project, and helps the agent explain its design choices. It works with your
existing framework and architecture.

## Install

Run this in your project’s terminal:

```bash
npx skills add AyushRajSinghParihar/apple-human-interface-skills --skill apple-hig
```

The [Skills CLI](https://github.com/vercel-labs/skills#supported-agents) handles
installation for supported agents. Follow its prompts if it asks you to choose
an agent. This installs the complete skill, including all 158 topics.

You’ll need **Node.js 22.20+ and Git** for the installer. Add `-g` to the command
if you want the skill available across projects.

### Claude Code marketplace

You can also install the same complete bundle through Claude Code's plugin system:

```text
/plugin marketplace add AyushRajSinghParihar/apple-human-interface-skills
/plugin install apple-hig@apple-human-interface-skills
```

Start a new session and invoke `/apple-hig:apple-hig`, or ask Claude to use
`apple-hig` for an Apple interface task. Use either this method or the Skills CLI
for a given installation to avoid loading duplicate copies.

This is a community marketplace hosted in this repository. It is not an
Anthropic directory listing or an Apple endorsement. The plugin loads only the
complete `skills/apple-hig` folder, with no hooks, MCP servers, or install scripts.

### Cursor plugin packaging

The repository includes a `.cursor-plugin/plugin.json` manifest that points to
the same `skills/` folder. Marketplace availability depends on Cursor's review;
the manifest alone does not mean the plugin is listed. In the meantime, use the
Skills CLI installation above. Cursor runtime behavior has not yet been verified.

## Try it

After installation, start a new agent session and ask something like:

```text
Use apple-hig to review this screen for iOS conventions and accessibility.
Explain the problems and make concrete improvements.
```

```text
Use apple-hig to design the settings page for our macOS app.
Keep our existing framework and explain the important interaction states.
```

```text
Use apple-hig to adapt this iPad media browser for Apple TV.
Preserve the main task while changing navigation and input where needed.
```

You don’t need to pick individual topic skills. The main `apple-hig` skill routes
to the topics your task needs. Your agent may also offer its own skill menu or
invocation shortcut.

## What it helps with

- **Design a new screen:** choose the layout, navigation, controls, and interaction states.
- **Improve an existing interface:** find specific problems and propose or implement corrections.
- **Review a flow:** check accessibility, feedback, error recovery, privacy, and platform conventions.
- **Adapt to another Apple platform:** preserve the product’s purpose while adjusting its presentation and input.

Each topic includes decisions to make, a worked example, a useful output, and
checks for the result. For example,
[Buttons](skills/apple-hig/subskills/apple-hig-menus-and-actions/.topics/apple-hig-buttons/SKILL.md)
helps resolve action prominence and loading behavior;
[Modality](skills/apple-hig/subskills/apple-hig-patterns/.topics/apple-hig-modality/SKILL.md)
covers dismissal and unsaved work; and
[Widgets](skills/apple-hig/subskills/apple-hig-system-experiences/.topics/apple-hig-widgets/SKILL.md)
covers useful content, freshness, privacy, and tap destinations.

## What’s included

| Area | Topics | Examples |
|---|---:|---|
| Getting started | 9 | Design principles and platform conventions |
| Foundations | 18 | Accessibility, typography, color, materials, privacy |
| Patterns | 25 | Onboarding, accounts, feedback, recovery, media |
| Content | 4 | Charts, images, text, web content |
| Layout and organization | 10 | Lists, containers, hierarchy, disclosure |
| Menus and actions | 12 | Buttons, commands, menus, toolbars |
| Navigation and search | 5 | Destinations, search, state restoration |
| Presentation | 8 | Alerts, sheets, popovers, dismissal |
| Selection and input | 11 | Pickers, text fields, validation, correction |
| Status | 4 | Progress, ratings, values, Activity goals |
| System experiences | 10 | Widgets, notifications, system surfaces |
| Inputs | 13 | Touch, keyboard, focus, gestures, alternatives |
| Technologies | 29 | Integration, prerequisites, consent, recovery |

Browse the [full topic index](skills/apple-hig/references/topic-index.md) or
[platform guide](skills/apple-hig/references/platforms-and-tasks.md).

Only the relevant instructions are loaded for a task. The complete bundle also
contains local source guides and explanations of important visual examples.

## Coverage and checks

The package covers **158 English HIG articles** in the **October 25, 2026** source
snapshot, with **173 routes** accounted for. Every topic procedure has an
independent instruction review. The repository also has **75 automated tests**
and CI checks for source coverage, instruction reviews, routing, and links.

Installation and skill loading were tested with **Codex CLI 0.164.0**, including
a complete bundle, symlinks, and paths with spaces. The Skills CLI installation
was also checked to preserve the entire bundle, including hidden topic files.
Other agent runtimes and native Apple device behavior have not been verified.

Claude Code 2.1.310 marketplace installation and component discovery were also
checked: one skill loaded, with no agents, hooks, or MCP servers. This checks
packaging and discovery, not task performance in Claude Code.

[Source report](coverage/REPORT.md) · [Package review](coverage/package-review.json) ·
[Client installation checks](coverage/client-integration/README.md)

Development [traces and artifacts](coverage/behavior/) are available for inspection.
The full comparative grading study was not completed, so they are not a quality
benchmark. Actual rendering, assistive technology behavior, and physical input
still need checks in the appropriate Apple environment.

The source snapshot excludes translations, historical documentation, and complete
linked SDK/WWDC libraries. Use current API documentation for implementation details.
Raw Apple source exports and downloaded media are not redistributed.

## Update or remove

Update installed skills:

```bash
npx skills update
```

Remove this skill:

```bash
npx skills remove apple-hig
```

Follow the CLI prompts for the installation you want to manage. If you installed
with `-g`, add `-g` when removing it.

<details>
<summary>Manual installation</summary>

If you prefer to install without the Skills CLI:

1. [Download the repository](https://github.com/AyushRajSinghParihar/apple-human-interface-skills/archive/refs/heads/main.zip) or clone it.
2. Place the complete `skills/apple-hig` folder in your agent’s documented skills location. Keep its hidden `.topics` directories.
3. Refresh your agent’s skill discovery or start a new session.

For agents that load instruction files directly, start with `apple-hig/SKILL.md`.
To update a manual installation, replace it with the complete updated folder.

</details>

<details>
<summary>For contributors</summary>

Authoring checks need Python 3.11+ and PyYAML:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/hig.py check
.venv/bin/python scripts/hig.py check-skills --instructions-only
```

`check --live` checks upstream drift. The optional `check-skills` command without
`--instructions-only` additionally requires independently graded behavioral
evidence; that extended study remains incomplete.

[Contributing](CONTRIBUTING.md) · [Authoring research](docs/skill-design.md) ·
[Source method](docs/source-method.md) · [Development history](docs/operational-progress.md)

</details>

## Attribution and license

An independent community project, unaffiliated with Apple. Original code and
guidance are [MIT licensed](LICENSE). Apple documentation, trademarks, and
referenced media remain their owners’ property. The skill includes source
attributions and its own license copy.
