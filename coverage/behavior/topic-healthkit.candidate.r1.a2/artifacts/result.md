# Wellness health-data access and empty-state audit

Scope: iOS; static review of the single paragraph in `interface.md`. Findings below are verified against that supplied description, not a running app. This is a framework-agnostic correction specification; no Apple SDK is assumed.

## Ranked findings and decisions

Rank reflects potential privacy impact and misleading health information, not a measured incident rate.

| Rank | Verified evidence | Effect and decision | Source support |
| --- | --- | --- | --- |
| 1 — Critical | “health history is used in unrelated promotions” | Sensitive information crosses its health-purpose boundary. Stop health-history inputs to promotional selection, segmentation, derived audiences, and exports. Keep unrelated promotions independent of health data. Inspect existing downstream copies and retention before promising cleanup. | [HealthKit: Privacy protection](https://developer.apple.com/design/human-interface-guidelines/healthkit#Privacy-protection), [Privacy: Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices) support protecting data and collecting only for a specific feature. The explicit promotional pipeline exclusion is this audit’s concrete product correction; this review does not establish legal or App Store compliance. |
| 2 — High | “missing readings are plotted as zero” | Absence becomes a false measurement and can distort trends and summaries. Preserve missingness, omit numeric marks for missing observations, and explain gaps. Never infer a clinical condition from an absent value. | [Charts: Descriptive content and accessibility](https://developer.apple.com/design/human-interface-guidelines/charts#Descriptive-content) supports understandable, objective values. Null-preserving calculations and gaps are application decisions implementing truthful representation. |
| 3 — High | “Launch requests all health categories before explaining why” | Broad access lacks feature context and minimum scope. Remove the launch request; map each requested category and read/write scope to an invoked health function, explain its use and benefit, then use standard system authorization through an integration boundary. | [HealthKit: Privacy protection](https://developer.apple.com/design/human-interface-guidelines/healthkit#Privacy-protection), [Privacy: Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission). General privacy guidance permits essential, obvious launch dependencies; this brief supplies none for all health categories. |
| 4 — High | “denied access shows a red Access granted label” | The text falsely reassures and the color contradicts it. Replace with evidence-based availability wording and a useful recovery action; color must supplement the words. Never show a global granted claim from a completed request or previously readable data. | [Writing: Best practices](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices), [Color: Inclusive color](https://developer.apple.com/design/human-interface-guidelines/color#Inclusive-color), [HealthKit: Privacy protection](https://developer.apple.com/design/human-interface-guidelines/healthkit#Privacy-protection). |

**Separate validation limitation:** “Medical interpretation is not validated” is confirmed, but no interpretation text, algorithm, intended medical use, or validation evidence is supplied. It does not prove any particular diagnosis is wrong. Product decision: limit this correction to objective readings and availability; withhold diagnostic, treatment, and medical efficacy claims until appropriately validated. A disclaimer alone cannot validate them. HIG review cannot establish clinical safety.

## Access and data-purpose contract

Actual categories, metrics, units, storage, transfers, and read/write needs are unspecified. Do not invent a required category list.

| Input/use | Minimum scope | Decision |
| --- | --- | --- |
| A person opens a particular metric’s history | Only the category needed to display that metric; read access only | Explain “Read [metric] from Apple Health to show your [period] history.” Replace brackets with verified product facts before shipping. |
| Writing data | None in this brief | Request no write access until a specific user-invoked writing function exists. |
| Other health categories | None established | Do not request them speculatively. |
| Unrelated promotions | No health history or health-derived attributes | Enforce exclusion at data-processing boundaries as well as in UI. |

Maintain an accurate privacy policy and App Store privacy disclosures. Audit retention, derived data, recipients, and existing promotional stores; none are evidenced here. Prefer on-device processing where it avoids unnecessary transfer ([Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices)); do not claim that the current app already does so.

## Corrected behavior

Authorization and data availability are separate dimensions. An empty read is not proof of denial. The adapter must report only statuses that the actual integration can reliably expose; when read permission is intentionally undisclosed, retain `unknown`. A request completing is not proof that every category was granted.

1. Launch the app without a health request. Keep unrelated app tasks available.
2. On entry to a metric feature, show its purpose in ordinary feature content and offer **Connect Apple Health** when connection has not been requested. This opens the real authorization flow for the minimum scope; it does not itself grant access.
3. Usually feature context supplies enough explanation. If a dedicated pre-permission explanation is essential, use one **Continue** action to the standard authorization screen, without imitation consent choices or extra dismissal controls. This special restriction does not apply to ordinary feature content ([Privacy: Pre-alert screens](https://developer.apple.com/design/human-interface-guidelines/privacy#Pre-alert-screens-windows-or-views)).
4. On completion, cancellation, return from system settings, and subsequent access needs, refresh availability. Do not repeatedly prompt on launch or empty reads. Manage sharing through system privacy settings, without competing app permission toggles.
5. Render the following states per metric and selected period; partial access must not erase other available metrics.

| State/evidence | Visible content | Action and transition |
| --- | --- | --- |
| Request not yet made | “Connect Apple Health to view [metric] history.” Include the specific purpose above. | **Connect Apple Health** → minimum-scope system authorization → refresh. |
| Query pending | “Loading [metric] history…”; no zero placeholders | Preserve metric and period context; suppress duplicate requests. |
| Reliably known unavailable access | “Access to [metric] is off.” “You can review sharing in system settings.” | **Review Health Access** → supported system destination, then refresh on return. If direct navigation is unavailable, provide accurate, verified instructions instead of a broken link. |
| Successful query returns no readings; reason unknown | “No [metric] readings available for [period].” “There may be no recorded readings, or access may be limited.” | **Review Health Access**; retain a period-changing action if the product supports one. Do not label this as denial or consent success. |
| Some readings available | Show actual dated values and units; “Some readings are unavailable.” | Missing slots are gaps; no interpolation across them in this correction. Retain access-management entry. |
| Query failure | “Couldn’t load [metric] history.” | **Try Again** retries the query; failure does not become empty data or denial. |
| Integration unsupported | “Apple Health connection isn’t available here.” | Keep independent app features usable; do not invoke an unavailable API. |

All empty-state wording and actions are proposed corrections, not observations of existing screens. Useful next actions follow [Writing](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices).

### Framework-agnostic pseudocode

```text
onLaunch:
    renderIndependentFeatures()  // no authorization request

onConnect(metric):
    scope = auditedPurposeMap[metric]
    require scope exists and scope is minimum needed
    await healthAdapter.requestUsingSystemAuthorization(scope)
    refresh(metric)  // completion does not mean granted

onFeatureEntryOrSettingsReturn(metric):
    refresh(metric)

refresh(metric):
    render(loading, metric, selectedPeriod)
    evidence = healthAdapter.readCurrentEvidence(metric, selectedPeriod)
    if evidence.unsupported: render(unsupported)
    else if evidence.reliablyKnownUnavailable: render(accessUnavailable)
    else if evidence.queryFailed: render(errorWithRetry)
    else if evidence.readings.empty: render(noReadingsWithUnknownCause)
    else:
        slots = preserveMissingValues(evidence.readings) // null stays null
        renderActualValuesAndGaps(slots)
        summarizeObservedValuesOnly(slots, includeCoverage=true)

promotionInputs = generalNonHealthInputs
require no health values, history, or health-derived attributes in promotionInputs
```

Invalidate stale query results when the metric, period, or access context changes. If cached history remains visible during refresh, label its date and stale status explicitly; do not present it as newly available or evidence of continuing permission. Exact cache retention requires a separate privacy decision.

### Chart and control specification

Question: “Which readings are available over this period?” Select marks only after the actual metric is known: bars with a zero baseline for quantities such as totals; points or separated line segments for sampled time trends. Label metric, period, dates, units, and explicit bounds. Do not pick clinical ranges without evidence. Provide an objective text overview and chronological value list, including “No reading” for missing slots. Do not depend on chart exploration or color to convey availability ([Charts](https://developer.apple.com/design/human-interface-guidelines/charts)). No automatic Audio Graphs behavior is assumed.

Use neutral text roles for availability; reserve error emphasis for actual errors. Pair any status hue with explicit wording; no fixed RGB values are specified. Rendered contrast is unknown.

The supplied brief identifies a status label and chart, but no explicit buttons, toggles, or alerts. Proposed Connect, Continue, Review Health Access, and Try Again controls map to the Buttons procedure. Use normal nondestructive roles, one prominent likely action per state, visible action labels as accessible names, at least 44×44 pt hit regions for iOS, separated targets, and press feedback for custom controls. For delayed button work, show activity within the initiating button and prevent duplicate activation. These are specifications, not measured defects ([Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices)).

## Worked before/after

Illustrative fixture only; the brief supplies no real readings, metric, or units. Suppose three dated slots contain `12, missing, 18` in a verified metric’s units.

**Before:** Launch asks for all categories. After denied access, the UI says “Access granted” in red. The middle slot plots as `0`; if averaged over three slots, the result would be `10`. History feeds unrelated promotions. The average is an illustrative consequence, not a verified current calculation.

**After:** Launch requests nothing. Opening the metric explains the purpose and requests only its read category through system authorization. A successful empty read says “No readings available” with the cause left uncertain; a reliably known denied state uses the specific access-off wording. For the fixture when readings are actually returned, the chart shows `12, gap, 18`, with dated units and an equivalent text list. An optional observed-value mean is `15`, labeled “Average of 2 available readings; 1 slot unavailable”; it is not a complete-period average or clinical interpretation. With zero observed readings, the mean is absent, never zero. A genuine observed zero remains zero. Promotions receive no health-derived input.

## Acceptance checks and results

**Failed — supplied-interface static review:** purpose-limited timely access (rank 3), truthful status (rank 4), missing-value integrity (rank 2), and health-purpose data use (rank 1). These failures are established by the brief, not execution.

**Passed — document inspection:** this correction specifies minimum-purpose access, distinguishes empty reads from denied access, preserves missing values, excludes health data from promotions, and keeps clinical validation separate. The illustrative arithmetic is directly inspectable: `(12 + 18) / 2 = 15`. These passes establish specification coverage only.

**Not executed — implementation acceptance checks:**

- Launch produces no request; entering the metric requests exactly its audited scope after purpose context. Cancellation leaves independent tasks usable and does not claim access.
- Inject successful empty reads, unknown permission, known unavailable access, partial categories, query errors, and unsupported integration. Each yields its specified state; no empty read alone yields “denied” or “granted.”
- Revoke access in system settings and return. Refresh without stale global permission claims; retain only appropriately labeled cached content under the chosen retention policy.
- Inject `12, null, 18`, all-null, and a genuine zero. Verify gaps, coverage-aware aggregates, accessible text values, and no missing-to-zero conversion or bridging line.
- Trace promotional processing, exports, derived audiences, and retained copies. Confirm no health-data dependency. UI removal alone fails this check.
- Activate each proposed control: verify named destination, cancellation, retry, duplicate suppression, and failure recovery. Verify settings navigation against the chosen integration; no competing permission switches.
- On an actual iOS implementation, measure hit regions and separation; inspect large text, localization, appearance/contrast, keyboard and assistive traversal, readable chart alternatives, and status updates. No VoiceOver or other accessibility execution has occurred here.
- Review every actual medical interpretation and supporting validation independently before allowing such claims.

## Evidence and routing limits

Read the installed root `apple-hig/SKILL.md` explicitly, then searched `references/topic-index.md` for health, privacy, empty states, permissions, and affected components. Read owning family → topic procedure → local source guide for Technologies/HealthKit; Foundations/Privacy, Writing, Color; Content/Charts; and Menus and actions/Buttons. All paths resolve under `.agents/skills/apple-hig/`; each file was consumed with a separate `cat` or `rg` command. Links above identify official source articles; they were not visited. Local references identify themselves as derived guidance dated 2026-10-25, not SDK documentation or independent source verification.

Only `interface.md` supplies interface evidence. No code, screenshots, dataset, permission response contract, medical claims, privacy policy, promotional pipeline, or runtime is supplied. No device, SDK compilation, GUI, security, legal, medical, or accessibility execution is claimed. There is no basis to measure contrast, infer actual accessible semantics, determine which read-permission states a future adapter exposes, or assert successful deletion of existing promotional data. Framework-specific API selection and platform behavior must be verified during implementation.
