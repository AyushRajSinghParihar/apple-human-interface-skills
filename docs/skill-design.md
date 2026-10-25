# Skill authoring research and design choices

The initial research used the [Agent Skills specification](https://agentskills.io/specification)
and Anthropic's [skill authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
Both were checked again before publication on 2026-10-25.

The specification establishes a portable folder with YAML-frontmatter `SKILL.md`,
clear name/description metadata, relative references, and progressively loaded
resources. It recommends a small entry point and focused reference files.
Anthropic emphasizes concise instructions, domain-based organization, shallow
reference chains, and evaluation through actual use rather than plausible prose.

This package applies that research as follows:

| Decision | Purpose |
|---|---|
| One installed `apple-hig` entry point | Make discovery predictable across clients |
| Thirteen explicitly read family skills | Load the context relevant to the task |
| One primary guide per article | Preserve ownership and support narrow retrieval |
| Direct article links in the topic index and each family | Keep the large corpus navigable without recursive exploration |
| Explicit platform and source boundaries | Preserve qualifications when combining topics |
| Local Markdown with no runtime dependencies | Support copied and symlinked installations |
| Fresh-context baseline and installed-package trial | Observe retrieval and application with concrete prompts |
| Independent source/unit/media reviews | Assess substantive fidelity separately from format checks |

The requested router/subskill architecture adds a deliberate family layer. It is
not dependent on automatic nested-skill discovery. A direct topic index provides
an alternate path to every article, and the installed-package trial exercises the
explicit routing. The evaluation evidence does not establish equal performance
across every client or model.
