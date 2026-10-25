# Wellness app health-data access and empty-state audit

Review basis: `interface.md`, an iOS behavior brief, reviewed against the installed apple-hig instructions and local guidance snapshot dated 2026-10-25. This is a framework-agnostic correction specification, not an implemented or clinically validated app. “Verified” below means explicitly described in the supplied brief; no running interface was supplied.

## Ranked verified findings

Priority reflects likely harm and correction urgency; it is reviewer judgment, not an Apple severity scale.

| Rank | Observed evidence | Effect and decision | Guidance |
|---|---|---|---|
| 1 — Critical | “health history is used in unrelated promotions” | Sensitive data is repurposed beyond the health task. Stop using health history, derived health segments, and health-dependent targeting in promotions. Keep promotional pipelines independent of health data. Inventory existing transfers, recipients, retention, and disclosures; determine remediation from actual records. A new permission message alone does not repair this use. | [HealthKit: Privacy protection](https://developer.apple.com/design/human-interface-guidelines/healthkit#Privacy-protection), [Privacy: Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices). The explicit downstream exclusion is this audit’s protective product decision; the local guides do not establish a legal or App Store policy adjudication. |
| 2 — High | “missing readings are plotted as zero” | Fabricates a measurement and can imply a health change. Represent absence explicitly, omit missing marks, and break time-series lines at gaps. Exclude missing observations from numerical aggregates. Preserve genuine recorded zero values. | [Charts: Anatomy and Descriptive content](https://developer.apple.com/design/human-interface-guidelines/charts#Descriptive-content). Null handling and gap rendering are concrete engineering corrections to preserve data meaning, not a quoted universal chart rule. |
| 3 — High | “denied access shows a red Access granted label” | Text falsely reports success; red contradicts the text. Replace with an evidence-based status and recovery action. Do not repair only the color. Do not infer denial from an empty query or treat completion of a request as a read-access grant. | [HealthKit: Privacy protection](https://developer.apple.com/design/human-interface-guidelines/healthkit#Privacy-protection), [Writing: Best practices](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices), [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). No color-only dependency or contrast failure can be established from this brief. |
| 4 — High | “Launch requests all health categories before explaining why” | No category-to-feature justification is supplied; people cannot make a contextual choice. Remove the launch request. Request only the minimum types and directions needed when the person invokes the relevant feature, with a specific purpose. | [HealthKit: Privacy protection](https://developer.apple.com/design/human-interface-guidelines/healthkit#Privacy-protection), [Privacy: Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission). General privacy guidance allows essential, obvious launch dependencies; none is established here, and the health-specific guide favors contextual requests. |

**Separate evidence concern:** “Medical interpretation is not validated” establishes a validation gap, not an observed misdiagnosis or proof of inaccuracy. This audit does not validate medical efficacy. Product decision: keep unvalidated diagnostic/treatment interpretations out of the corrected flow; show factual readings, provenance, and availability only. A disclaimer is not validation. Clinical claims require a separate qualified evaluation outside these local materials.

## Decisions and data-purpose contract

Actual health categories, read/write directions, storage, and retention are unspecified. Do not invent an approved list. Before enabling any integration, complete this contract for each feature:

| Use | Permitted scope | Access/use decision |
|---|---|---|
| A user-selected health trend | Explicitly named metric, unit, relevant period, minimum underlying types; read-only unless a separate write task is justified | Approve only after a concrete benefit and category mapping exist. Reassess availability when needed. |
| Writing a health record | No write task is supplied | Request no write access in this specification. |
| Unrelated promotions | No health samples, derived health attributes, or health-dependent audience selection | Disallow independently of health authorization. |
| Other categories or unspecified background collection | No demonstrated benefit | Do not request or collect. |

Prefer on-device work when it avoids unnecessary transfers. Document any necessary transfer, recipient, retention, and deletion behavior before enabling it. Provide an accurate privacy-policy URL and update relevant App Store privacy disclosures to match actual behavior. These are design requirements pending implementation and data-flow inspection. [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices).

Launch into usable non-health-dependent content without a permission prompt. On the relevant feature screen, explain the selected metric’s purpose in ordinary content. Use the system-owned authorization surface through an available platform adapter. Do not imitate its permission choices. If a dedicated pre-permission explanation is essential, it has one Continue action leading to that surface, without extra cancel/close choices; ordinary feature navigation remains outside that pre-alert. Keep authorization management in system privacy settings, with guidance or a supported destination rather than app-owned permission switches. [Privacy: Pre-alert screens](https://developer.apple.com/design/human-interface-guidelines/privacy#Pre-alert-screens-windows-or-views), [HealthKit](https://developer.apple.com/design/human-interface-guidelines/healthkit#Privacy-protection).

## Corrected state and action contract

Access and data availability are independent dimensions. Use per-feature/per-type state rather than one global “granted” boolean. The adapter must document what it can actually observe; unavailable permission evidence remains unknown.

| State/evidence | Visible behavior and next action |
|---|---|
| Feature not connected | “Connect health data to view this trend.” Show the concrete metric and purpose; **Connect Health Data** initiates the contextual request. No automatic launch request. |
| Request/query pending | “Connecting…” or “Loading readings…” as appropriate. Retain context, prevent duplicate work, and show activity in the initiating button for delayed completion. Do not display zeros or success. |
| Access explicitly known to be unavailable | “Health data access is off.” Body: “Review access in system privacy settings to use this feature.” **Review Health Access** opens a supported system destination or accurate instructions. Preserve other features. Use this copy only when the unavailable-access claim is supported. |
| No readable samples; reason unknown | “No readings available for this period.” Body: “There may be no recorded readings, or access may be limited.” Offer **Choose Another Period** and a lower-emphasis **Review Health Access** action. Do not assert denial, grant, or a physiological zero. |
| Some samples missing | Show valid readings with visible gaps and a completeness summary. Missing details read “No reading,” including in text alternatives. Offer period selection. |
| Readable samples | Show factual values, units, dates, source context, and coverage. Say “Readings available,” if a status is useful; this does not promise future access or all-category permission. |
| Query error | “Readings couldn’t be loaded.” Offer **Retry**; distinguish it from empty data. Old cached readings, if retained, show their timestamp and stale status and never imply current access. |
| Integration unavailable | “Health data isn’t available in this environment.” Keep the rest of the app usable; do not show a fake system prompt. |

Button contracts: Connect Health Data is the primary nondestructive feature action; Retry reruns the failed query; Choose Another Period changes the query range; Review Health Access manages access rather than granting it inside the app. Each uses a visible text label and matching accessible name, button role, perceivable press/pending feedback, and a separate nonoverlapping activation area at least 44 × 44 pt on iOS. This adopts the buttons guide’s general target recommendation; the accessibility guide’s smaller stated minimum is not a reason to shrink these actions. No existing buttons or hit regions were supplied to audit. [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices).

Status meaning must survive removal of color. Preserve status, explanation, and actions at 200% text enlargement with reflow. Provide the chart’s question, units, dates, bounds, coverage, and exact readings in an accessible text alternative; critical facts must not require touch exploration. Verify actual semantics and navigation later. [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision), [Charts](https://developer.apple.com/design/human-interface-guidelines/charts#Enhancing-the-accessibility-of-a-chart).

## Framework-agnostic pseudocode

```text
onLaunch:
  showOrdinaryHome()                  // no health request

onConnect(feature):
  contract = approvedPurposeMap[feature]
  require contract is concrete and minimum-scoped
  if not adapter.available: showIntegrationUnavailable(); return
  adapter.requestAccess(contract.types, contract.directions, contract.purpose)
  // Request completion is not evidence of read permission.
  refresh(feature)

refresh(feature):
  generation = beginNewGeneration()   // ignore outdated asynchronous results
  showLoading()
  evidence = adapter.currentObservableAccessEvidence(feature)
  if evidence.explicitlyUnavailable:
    invalidateCurrentAccessClaims(); showAccessOff(); return
  result = adapter.read(feature.types, selectedPeriod)
  if generation is outdated: return
  if result.error: showQueryError(); return
  rows = normalize(result.samples)    // retain null; never coalesce null to 0
  if rows have no observed values: showNoReadingsUnknownReason(); return
  showObservedValuesAndGaps(rows)

onReturnFromAccessManagement, onFeatureReentry:
  refresh(feature)                    // previously readable is not permanently granted

renderAndAggregate(rows):
  draw marks only for observed values, including genuine zero
  break line segments across missing observations
  aggregate only observed values; report observed/expected coverage when known
  if expected count is unknown: say count available, not invented completeness
  if no observed values: aggregate = unavailable

promotionInput = independentlyCollectedNonHealthInputs
assert promotionInput excludes health history and derived health attributes
```

The adapter is an interface boundary, not an assumed Apple SDK implementation. Exact permission observability, system destinations, supported platforms, and SDK APIs require implementation documentation and runtime verification not available here. Revocation must not be diagnosed merely from disappearing samples.

## Worked before/after

**Supplied before:** Launch requests everything; after denial, the app displays red “Access granted”; absent readings become zero; history feeds unrelated promotions.

**Corrected sequence:** Launch shows home. The person opens a trend feature and sees a concrete explanation, for example “Read daily step counts from Apple Health to show your activity over time.” This is illustrative copy for a proposed steps feature, not evidence that the supplied app measures steps. Connect Health Data requests only the approved step-reading scope. If the result exposes no readable samples and the cause is unknown, show “No readings available for this period,” with period selection and access-review actions. Never label that outcome “Access granted” or “Access denied.” Health information never enters the promotional input.

**Synthetic rendering fixture, not supplied patient data:** For a daily-step bar chart, observations `[4200, missing, 0, 5300]` previously become `[4200, 0, 0, 5300]`. Afterwards, the second day has a gap labeled “No reading”; the third retains its real zero. Use a zero-baseline step-count axis and explicit dates. Sum available observations to 9,500 steps, label “Total across 3 of 4 days with readings,” and do not call it a complete-period total. The observed-day mean is approximately 3,167, not the zero-filled 2,375; preferably omit averages unless the feature needs them. An all-missing fixture yields unavailable totals, not zero. This demonstrates the data rule without claiming medical interpretation.

## Acceptance checks and status

**Passed — static review/specification only:** Read the supplied brief; ranked its four explicit behavioral defects; separated the clinical validation gap; specified purpose minimization, contextual authorization, independent access/data states, missing-value handling, promotion exclusion, and actionable empty-state copy. The synthetic fixture was worked arithmetically, not executed as application code.

**Failed — supplied behavior, as documented:** Launch timing/scope, truthful denied-state labeling, missing-value representation, and health-data purpose separation fail the criteria above. No runtime failure is claimed.

**Not executed — required implementation acceptance:**

| Check | Acceptance condition |
|---|---|
| Launch and purpose scope | Launch produces no health request. Invoking a feature requests only its approved types/directions, with specific use/reason copy. Unrelated features work without access. |
| Authorization outcomes | Cancelled, partial, changed, unknown, and unavailable outcomes never become blanket success. Returning from system settings refreshes evidence and samples. Empty reads alone never prove denial. |
| Data states | Loading, empty, error, partial, observed zero, and unsupported states remain distinct. Retry is duplicate-safe; outdated query results cannot overwrite the current period. |
| Missing-data fixture | `[4200, null, 0, 5300]` retains its gap and genuine zero, totals 9,500 over three observed days, and has the same meaning in text. All-null input has no numeric total. |
| Purpose isolation | Trace raw and derived health information through storage, analytics, network, and promotion systems; none reaches promotional targeting. Verify prior-use remediation and disclosures against actual records. |
| Actions and access | Each label reaches its named outcome; pending operations preserve context. Check target geometry, press feedback, 200% text reflow, contrast in actual light/dark appearances, and status without color. |
| Assistive operation | On a supported Apple environment, verify meaningful names/roles/states, readable chart values and missing entries, logical navigation, and activation with VoiceOver, Switch Control, and Full Keyboard Access. |
| Privacy and interpretation | Verify policy URL/disclosures, handling of changed access and stale data, and absence of unvalidated diagnostic/treatment output. UI review alone cannot certify security or clinical validity. |

## Evidence limits and instruction trail

Only the one-paragraph `interface.md` and installed instructions/guides were used. There were no screenshots, source implementation, patient datasets, runtime logs, authorization records, privacy policy, promotional transfer records, or validation studies. Consequently geometry, contrast, consent implementation, storage/security, actual SDK behavior, data accuracy, medical efficacy, localization, and accessibility execution remain unverified. No device, SDK, GUI, browser, or assistive-technology execution occurred; no web browsing occurred. Official links identify the local guides’ cited articles, not freshly verified web content.

Installed route consumed explicitly, one file per read command: apple-hig root `SKILL.md`; relevant rows of `references/topic-index.md`; Technologies → HealthKit, Foundations → Privacy/Writing/Accessibility, Content → Charts, and Menus and actions → Buttons. Each owning family and selected `.topics/.../SKILL.md` was read before its corresponding `references/*.md` source guide. HealthKit’s Privacy handoff was followed. No platform feasibility/adaptation claim or framework selection was needed; iOS was explicitly supplied. The label and plot are the supplied surfaces; no button, switch, alert layout, or accessibility tree was provided. Proposed recovery buttons were routed through Buttons rather than presumed to exist. Local references describe themselves as derived application guidance; their existence does not establish independent source review or current API verification.
