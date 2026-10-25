---
name: apple-hig-id-verifier
description: Use when designing or reviewing in-person iPhone mobile-ID verification, age-threshold requests, Display Only versus Data Transfer, or verifier outcomes.
---

# Verify only the identity fact the task requires

Read [ID Verifier](../../references/id-verifier.md). Inspect the in-person verification purpose, necessary attributes, storage/processing need, requester role, and requested design/review/adaptation. This source describes iOS 17+ iPhone reading of compatible mobile IDs; other platforms are excluded. Preserve the existing stack and verify current entitlement/eligibility requirements before implementation.

Choose the minimum fact that answers the task. If an age threshold is enough, request that result rather than date of birth or current age. Distinguish Display Only, where data/photo appear solely in system UI for visual checking, from Data Transfer, which requires a legal verification need to store/process information and an additional entitlement. Do not design app-side processing around information it never receives.

Start verification through a clear age/identity action rather than NFC/QR-specific artwork or an Apple logo. For eligible organizations, show the verified business identity supplied through appropriate registration. In Display Only, provide the requester a clear outcome action for the visual decision, such as portrait match/nonmatch; keep that human observation separate from any claimed automated identity verdict.

**Before → decision → after:** A venue requests a full birth date, labels the action with an NFC glyph, and assumes Display Only returns the portrait to app storage. Decision: entry needs only an age-threshold result and a visual match. After, “Verify age” launches the appropriate minimal system request, the operator records the supported match/nonmatch outcome, and no nonexistent photo-transfer path is promised.

Deliver a purpose-to-attribute/request-mode/outcome contract and corrected flow or implementation. Fail if unnecessary personal details are requested, Display Only data is treated as app-owned, or the action hides its identity-verification purpose. Static review cannot verify certificates, entitlement issuance, actual ID interoperability, or legal necessity; identify those evidence boundaries explicitly.

Use [Privacy](../../../apple-hig-foundations/.topics/apple-hig-privacy/SKILL.md) for minimization and [NFC](../apple-hig-nfc/SKILL.md) only for a separate tag-reading task, not as a substitute verification model.
