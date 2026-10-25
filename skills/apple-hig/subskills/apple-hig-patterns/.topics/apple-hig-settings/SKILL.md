---
name: apple-hig-settings
description: Use when creating, reviewing, or adapting app-wide configuration, task-local options, system preferences, and settings access or persistence.
---

# Put an option where its effect is understood

Read [the settings guide](../../references/settings.md). This workflow is application advice; platform locations and system preference scope constrain the design.

Inspect option inventory/frequency, affected scope, defaults, system counterparts, platform, and create/review/adapt intent. Classify task-local, document-wide, app-wide, and system-wide choices. Record actual capability detection/persistence rather than treating a displayed toggle as proof.

Choose sensible defaults and detect capabilities instead of asking for information already known. Keep frequent view/task options beside their visible effect and rare app-wide choices in settings. Do not duplicate system accessibility/authentication/scrolling preferences with misleading scope. Reserve system Settings entries for rare changes. On Mac place app Settings in the app menu with expected access, document setup in File, and use stable settings-pane navigation/title/restoration rather than a customizable main toolbar. Watch cannot add custom entries to system Settings; keep only essential in-app options. Preserve familiar game access where appropriate.

Implement option placement/persistence or provide a scope/default/location contract; reviews identify exact misplaced or contradictory settings. Do not expand a settings redesign into unauthorized global configuration changes.

**Worked transformation:** Before: a Mac map app puts its layer filter in app Settings and a global Reduce Motion copy in the main toolbar, while document scale changes every map. Decision: frequency and scope are inverted. After: keep layers local, respect system motion preference, and separate document scale from app-wide defaults.

Deliver the artifact, option scope, defaults/detection, access, and restoration policy. Verify default/changed values, reopen/last pane, per-document independence, and capability changes. Fail for misleading global/local scope, duplicated conflicting system preference, or lost expected settings access. Native settings/shortcut behavior requires execution evidence.

Load [the-menu-bar](../../../apple-hig-menus-and-actions/.topics/apple-hig-the-menu-bar/SKILL.md), [toggles](../../../apple-hig-selection-and-input/.topics/apple-hig-toggles/SKILL.md), or [onboarding](../apple-hig-onboarding/SKILL.md) for access, state controls, or deferred setup.
