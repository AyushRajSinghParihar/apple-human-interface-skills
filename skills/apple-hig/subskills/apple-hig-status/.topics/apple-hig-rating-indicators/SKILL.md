---
name: apple-hig-rating-indicators
description: Use when creating, reviewing, or adapting a macOS ordered-symbol rating display or direct list-item rating editor.
---

# Distinguish ranking from a request for a review

Read [the rating-indicator guide](../../references/rating-indicators.md). This procedure is application advice for the Mac component, not an App Store review-prompt policy.

Inspect rated objects, scale, editable/read-only purpose, list context, platform, and create/review/adapt mode. Establish the meaning of zero/unrated and how stored fractional values map to the component's whole-symbol display. Do not present rounded stars as precise fractions without explanation.

Use recognizable ordered symbols, conventionally stars; a custom symbol must make ranking equally clear. Retain fixed symbol spacing rather than stretching glyphs to fill a wider row. Allow direct in-list rating where people edit list items instead of forcing a separate screen. Bind edits to stable item identity so sorting or selection cannot rate another row. For other platforms choose a supported rating design rather than assert this native component exists.

Implement display/edit behavior, provide object/value/rounding specifications, or review concrete editability and meaning defects. Keep aggregate reviews and a person's editable rating distinguishable if both appear.

**Worked transformation:** Before: a Mac recipe list stretches three symbols across each row, displays 3.6 as though exact, and requires opening Settings to rate a recipe. Decision: fixed scale and direct object editing are obscured. After: use fixed-spacing whole-symbol display with truthful value context and direct rating in the recipe row.

Deliver the artifact and scale, unrated, rounding, edit, and persistence contract. Verify endpoints, fractions, sort-after-edit, and keyboard/accessible value identification. Fail for rating the wrong item, symbols implying an undefined scale, or fractional precision falsely represented. Native editing/assistive behavior remains unverified without runtime execution.

Load [ratings-and-reviews](../../../apple-hig-patterns/.topics/apple-hig-ratings-and-reviews/SKILL.md) for requesting app reviews or [lists-and-tables](../../../apple-hig-layout-and-organization/.topics/apple-hig-lists-and-tables/SKILL.md) for row integration.
