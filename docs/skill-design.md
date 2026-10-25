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
| One operational procedure and one primary guide per article | Separate task capability from source fidelity |
| Direct procedure links in the topic index and each family | Enter decision instructions before detailed source retrieval |
| Explicit platform and source boundaries | Preserve qualifications when combining topics |
| Local Markdown with no runtime dependencies | Support copied and symlinked installations |
| Fresh-context baseline and installed-package trial | Observe retrieval and application with concrete prompts |
| Independent source/unit/media reviews | Assess substantive fidelity separately from format checks |

The requested router/subskill architecture adds a deliberate family layer. It is
not dependent on automatic nested-skill discovery. A direct topic index provides
an alternate path to every topic procedure, and the installed-package trial exercises the
explicit routing. The evaluation evidence does not establish equal performance
across every client or model.

## Operational topic procedures

The first package preserved extensive source knowledge, while its family entry
points mostly provided short guidance followed by article links. Source fidelity
and file-read trials established useful boundaries but did not establish a
repeatable task procedure for each topic.

The operational upgrade preserves those references and adds one actual topic
skill per current article. Its instruction contract requires a topic-specific
branch, concrete artifact, worked transformation, failure-revealing checks,
applicability limits, conditional handoffs and independently assessed
noninterchangeable content. Framework-agnostic examples support the existing
project rather than choosing a new implementation stack.

The root, family and exact-topic index enter these procedures before references.
Topic skills are stored in hidden `.topics` directories within the complete
bundle. A read-only probe against Codex CLI0.164.0 showed ordinary nested skills
are automatically discovered, including ones under references, while dot-directory
skills are not. Actual runtime tests verify that topic bodies are still read on
demand. This is tested client behavior, not a guarantee for every client/version.

The topic index also carries every approved trigger description. The agent
matches the product task to those descriptions, even when the request uses
everyday language instead of an Apple topic or framework name. It reads the owning
family and procedure, then combines relevant platform, component and cross-topic
procedures for the decisions in scope. This selection follows written routing
instructions; the package does not run a separate search service or require
adopting the framework named by a technology topic.

Source coverage, independent instruction review, artifact-producing behavior,
client discovery and Apple hardware execution remain separate evidence dimensions.
The frozen195 behavioral-execution target includes158 topic cases,8 stress cases
with3 fresh repetitions, and13 matched published-package controls. Old-package
controls may already perform well; report ties and regressions honestly.
