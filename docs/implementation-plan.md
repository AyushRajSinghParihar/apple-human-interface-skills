# Apple HIG Mega Skill implementation

Build one portable `apple-hig` router package containing 13 topic subskills,
original detailed references for every current English HIG article, a source
coverage manifest, independent audit evidence, maintenance tooling, and a README.

## Decisions

- Public repository: AyushRajSinghParihar/apple-human-interface-skills.
- Package: skills/apple-hig; nested subskills are explicitly router-loaded.
- Corpus: current English HIG, all six platforms and substantive media guidance.
- Discover from Apple's navigator, in-HIG links, and design update history.
- Historical routes and external references are accounted for separately.
- Original guidance and code use MIT; Apple raw content/media stay untracked.
- No global skill installation, GUI software, or connectivity changes.

## Work and acceptance

1. Refresh and preserve a dated source inventory in an ignored cache.
2. Author all 13 modules with direct article links and actionable original guidance.
3. Map source sections, platform variations, tables, notes and meaningful media to
   local treatment. Review is bound to both source and destination hashes.
4. Validate coverage, source extraction, installed-package links, source drift,
   and realistic agent retrieval/application with and without the package.
5. Publish a coverage report, README, contribution instructions, license, and CI.
6. Run final live discovery, reconcile changes, create the GitHub repo and push.

The independent coverage auditor remains separate from the two author workers.
No completeness claim is permitted while substantive or media review is pending.
