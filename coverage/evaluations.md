# Retrieval and application evaluations

Status: the seven-task fresh-context control and package-enabled comparison are
executed, with two additional enabled application/media cases. The broader E1–E8
scenarios remain proposed. Selected automated maintenance boundaries were executed;
written scenarios are not passing test results.

## Observed baseline without this package

These observations were made during independent research before candidate package
content existed. They establish retrieval failure modes; they do not measure an
unassisted model's design knowledge.

| ID | Attempt | Observed result | Failure exposed |
| --- | --- | --- | --- |
| B1 | Open the public HIG root with a text web reader | JavaScript shell; linked Markdown rejected by the reader's MIME handler | The public URL alone did not yield substantive guidance |
| B2 | Guess `/tutorials/data/index/design/human-interface-guidelines` and its `.json` variant | Both returned 404 | A guessed navigator endpoint is not a source inventory |
| B3 | Fetch Apple's root `.md` and `/tutorials/data/design/human-interface-guidelines.json` directly | Both returned substantive first-party content | A representation fallback recovered access |
| B4 | Traverse current HIG indexes and in-HIG references | 173 canonical routes; no additional routes from cross-links | Navigation closure can be measured but does not account for history |
| B5 | Compare update-history links with the navigation closure | Found two redirects and two unavailable historical routes | Navigation-only discovery misses historical dispositions |
| B6 | Request localized root Markdown and Chinese structured JSON | Chinese/Japanese/Korean `.md` returned 404; Chinese JSON succeeded | Representation failure must not be mistaken for absent localization |

The independent auditor has already read source material. Its own answers cannot
honestly serve as clean, unassisted application controls. Fresh-context executions
must be recorded separately, including failures, before reporting comparative
application results. No invented baseline failure is acceptable.

## Executed fresh-context application control

The [seven-task no-package control](evaluations/baseline-control.md) records actual
answers from a fresh collaboration context without candidate files or research
tools. Its N1–N7 prompts are a separate smaller suite from the proposed E1–E8
scenarios below. They identify current topic ownership, platform-specific material
rules, unfamiliar current device/system topics, and actual historical URL outcomes
as useful retrieval gaps. The control already handles many general input,
localization, and cross-topic principles competently; improvement must be measured
against those actual outputs.

## Independent assessment of the enabled comparison

The [enabled trial](evaluations/enabled-trial.md) and its
[structured trace](evaluations/enabled-trial.json) record the same seven prompts,
plus a cross-family chart/editor proposal and a Materials demonstration-retrieval
case. A fresh agent read a copied installation from `/tmp`, starting with the
router. It opened 52 distinct package files using only shell text reads, including
12 of the 13 family entry points. It did not read the source checkout, authoring
cache, baseline answers, or other agents' output.

The [captured installation hash inventory](evaluations/installed-package-files.json)
contains 202 files and identifies the actual trial artifact. The independent
assessor initially compared all 52 opened files with those recorded hashes: all
matched. The final roster comparison found 51 still byte-identical; only
`references/media/index.md` expanded additively to link newly completed image
supplements. Its Materials link and the consumed Materials explanation remain
unchanged. The trial's stated source snapshot is
`2026-10-25T12:38:49+00:00`; later reports or additional media notes are not silently
treated as part of that execution.

| Case | Observed enabled result | Comparison with no-package control |
| --- | --- | --- |
| N1 accessibility ownership | Correctly retrieved Typography, Accessibility and the separate VoiceOver article; applied resizing, state, order, grouping and content checks | Resolved the control's uncertainty about current VoiceOver ownership |
| N2 Liquid Glass | Retrieved regular/clear material criteria, readable semantic foregrounds, watch inline/toolbar distinction and platform exceptions | Replaced admitted uncertainty with source-grounded current rules |
| N3 current topics | Found explicit Snippets, iPhone Duo and HomeView widget guidance, with height/platform, pose/state and household-privacy qualifications | Resolved the two unfamiliar topics and vague Siri ownership in the control |
| N4 historical URLs | Used current Toolbars and explicitly withheld unavailable Touch Bar rules | Supplied the actual snapshot dispositions the control had not established |
| N5 input comparison | Preserved remote focus versus private gaze-hover/hand activation, spacing, fatigue and connected-input qualifications | Added retrieved specifics to an already competent general control answer |
| N6 Arabic adaptation | Preserved layout/text mirroring versus content/numeral/object exceptions and hardware-side controls | Added traced, device-specific detail to an already nuanced control answer |
| N7 destructive Mac command | Composed toolbar/context/main-menu, undo, alert, role and accessibility guidance; retained platform scope and deliberate-destruction exception | Improved specificity and explicit exception handling over sensible general advice |
| Additional chart/editor case | Composed five component/pattern families plus foundations/platforms; gave concrete resizing, input, loading and editing decisions | Enabled-only execution; no matched unassisted comparison was run |
| Additional media case | Retrieved the original Materials sequence explanation and applied adaptive visionOS glass correctly | Enabled-only execution; evaluator explicitly did not claim to watch the raw video |

All seven repeated prompts successfully retrieved the relevant local material and
supported their main task-specific conclusions. This is a small qualitative trial,
not a statistical accuracy or productivity benchmark. The control record retains
condensed observations rather than a complete verbatim answer transcript.

One compression deserves qualification: N7 says to hide unavailable contextual
actions without mentioning Apple's macOS exception that Cut, Copy and Paste may
remain visible but unavailable. That exception does not alter its recommendation
for the asked destructive command, but the summary should not be reused as an
exhaustive context-menu rule. The underlying local article retains the exception.

The evaluator corrected one manually mistyped path and reread initially truncated
outputs; these were recorded transparently. All intentionally followed package
links opened. No network calls were used, and neither Python nor package runtime
tooling was needed. Network access was prohibited by the trial instructions, not
independently disabled at the operating-system level; this demonstrates file-only
consumption, not a separately proved network sandbox. No hardware behavior,
complete API correctness, or full-corpus accuracy is established by this trial.

## Execution and scoring contract

Use identical task prompts for baseline and package-enabled trials. Baseline gets
no candidate package; the enabled trial receives the installed root skill and
available local files. Record model/harness, date, prompt, permitted tools, opened
files/source URLs, answer, and reviewer observations. Keep unrelated configuration
stable. Claims of offline use require an enabled trial with network disabled.

Score observable outputs: correct source or local-reference retrieval, accurate
application to the requested platforms, preservation of important conditions and
exceptions, supported quantitative claims, and explicit treatment of unavailable
or out-of-scope guidance. Exact wording and private implementation choices are
not scoring targets. A plausible answer without the required retrieval trace does
not demonstrate router/module usability.

Each scenario owns a distinct failure risk. Mutation checks below validate the
maintenance contract rather than duplicating application scenarios.

## Application scenarios awaiting execution

| ID | Task prompt | Observable passing behavior | Credible failure |
| --- | --- | --- | --- |
| E1 | Design an adaptable reading app for iPhone, iPad, and Mac. Explain navigation, resizing, and keyboard decisions and identify the local guidance used. | Reads relevant platform, layout, and component guidance; applies differences instead of producing one universal layout | Platform guidance exists but cannot be retrieved or changes are flattened |
| E2 | Review a custom Liquid Glass playback control for iPhone, Apple TV, Apple Watch, and Vision Pro. Explain where its material and interaction choices need to differ. | Retrieves materials, color, controls/input, and platform guidance; preserves applicability and contextual constraints | Treats one visual effect as a universal platform rule |
| E3 | Our large-text reader claims accessibility because every button has a label. Review the claim for low vision, hearing, mobility, speech, and cognitive needs. Find the local owners for Dynamic Type and VoiceOver. | Finds accessibility, typography, and VoiceOver guidance; gives relevant concrete changes beyond labels | One accessibility summary hides moved or cross-cutting guidance |
| E4 | Adapt a controller-and-touch game to iPhone, Mac, Apple TV, and Vision Pro, including onboarding, feedback, and player accessibility. | Loads games plus relevant controls, focus, feedback, audio/haptics, and accessibility references | Games route exists but cross-family advice remains inaccessible |
| E5 | Localize a media-and-chart app for Arabic. Explain which layout, text, icon, media, and data-direction choices require care. | Reads right-to-left and relevant writing/layout/component guidance; preserves documented exceptions | Recommends mechanically mirroring every element |
| E6 | Give a current HIG review of navigation bars, in-app purchases, Touch Bar, and Messages for Business. Distinguish current advice from unavailable historical sources. | Uses current canonical guidance for redirected topics; identifies historical unavailable sources without inventing current guidance | Old paths silently disappear or receive fabricated content |
| E7 | Review a visionOS window whose material changes under different viewing angles and lighting. Explain the source demonstration and its design implication using the local guidance. | Retrieves the original explanation of the meaningful visual sequence; distinguishes observed guidance from implementation assumptions | The media record contains only a poster/caption or an unexamined claim of redundancy |
| E8 | Starting in an unrelated working directory with this installed package and no network, answer a design question requiring foundations, inputs, and a component. Show the local references read. | Resolves router, nested modules, and references relative to installation; needs neither cache nor authoring Python tools | Source-repository-relative paths or silent nesting assumptions break portability |

## Maintenance boundary scenarios and observed checks

| ID | Mutation or condition | Required result | Independent contract |
| --- | --- | --- | --- |
| M1 | Keep an article file and mapping but replace its substantive guidance with a title and source URL | Independent semantic review rejects it; completeness remains pending/failed | Existence is not substance |
| M2 | Remove only a platform-specific rule while keeping the article and common guidance | Platform-unit coverage or semantic review rejects the omission | Cross-platform distinctions survive summarization |
| M3 | Change source prose or a table value without changing its URL/headings | Review becomes stale until the change is reconciled | Approval is bound to source content |
| M4 | Change the reviewed local explanation without changing source content | Review becomes stale | Approval is also bound to destination content |
| M5 | Return timeout, 403, malformed data, or an unsupported content node for a known current article | Source remains accounted for and access/extraction failure is reported | Failures cannot shrink the denominator |
| M6 | Add a current route or change a redirect during final live discovery | Release requires explicit reconciliation | Offline snapshot consistency is distinct from freshness |
| M7 | Mark a meaningful video redundant without inspecting the sequence or showing equivalent local guidance | Independent media review rejects that disposition | Captions do not automatically discharge visual guidance |
| M8 | Include ignored raw source/media in a proposed release archive | Publication check rejects the artifact | The published package contains original local guidance and source attribution |

The independent auditor read and ran the maintenance suite on 2026-10-25:
**34 tests passed**. These included stale source/destination bytes, missing
substantive units, wrong platform-section association, changed supplementary
explanations, failed/malformed/removed sources, package relocation and link escape,
raw DocC publication, pending appearance review, changed live media bytes, and
changed historical redirects. The suite's fixtures are isolated; they do not
replace the independent review of the actual corpus.

An integrity gap was identified independently: deleting media provenance or its
appearance list could evade checks that only examined remaining fields. The final
gate corrects it by freezing source URL/trait groups and requiring actual binary,
method, occurrence and supporting-file bindings. New mutation tests reject deleted
provenance, placeholders, unrelated assets, missing occurrences and removed
appearance lists. Resolution-only variants and explicitly reasoned decorative
exceptions remain distinct. The independent auditor reran the final 34-test suite
and strict corpus check: all tests passed, with zero errors or pending reviews.
No separate fresh-agent deceptive-placeholder trial or malicious archive trial
has been executed. The final actual live comparison also returned zero errors or
pending items for 173 pages/158 articles, with 2,294 inspected media URLs verified
across the main and supplemental runs. See the dated
[release verification](release-verification.json); this is source freshness
evidence, not an additional model-application benchmark.

## Results ledger

| Trial group | State | Evidence |
| --- | --- | --- |
| B1–B6 no-package retrieval observations | Observed | Direct research observations above |
| N1–N7 fresh-context no-package control | Executed | [Actual control observations](evaluations/baseline-control.md) |
| N1–N7 package-enabled comparison | Executed, independently assessed | [Actual enabled output](evaluations/enabled-trial.md); 51/52 final bytes identical, one additive index expansion |
| Additional chart/editor and Materials cases | Executed | Concrete cross-family application and original-media retrieval; no matched baseline |
| E1–E8 broader fresh-agent baseline | Unexecuted | Proposed additional scenarios, separate from N1–N7 |
| E1–E8 broader package-enabled trials | Unexecuted | Proposed additional scenarios, including hardware/network limits |
| Selected M1–M8 automated integrity boundaries | 34 tests passed | Maintenance suite; precise observed subset described above |
| Full M1–M8 semantic/deceptive-artifact exercises | Unexecuted | Integrity fixtures are not fresh semantic-review trials |

Every future result must identify the exact package revision and reviewed source
snapshot. Report a failed or unexecuted scenario as such; a written scenario is
not a passing evaluation. Network-free tool usage demonstrates file-only retrieval;
only a technically disabled network justifies the stronger isolation claim.
