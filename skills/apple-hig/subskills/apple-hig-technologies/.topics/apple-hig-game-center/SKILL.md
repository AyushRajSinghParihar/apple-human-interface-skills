---
name: apple-hig-game-center
description: Use when designing or reviewing Game Center access, achievements, leaderboards, challenges, invitations, party codes, or system social-game entrypoints.
---

# Connect system game entrypoints to the exact activity

Read [Game Center](../../references/game-center.md). Inspect game modes, progression/scoring, social entrypoints, art, and requested design/review/adaptation. Preserve the engine/network stack. Check sign-in/initialization at launch while maintaining a smooth start; Watch has GameKit APIs but no invokable system Game Center UI.

Choose system UI/access point or justified custom links. Put the access point in main/settings menus, not gameplay, splash, or cinematics. Leave room for expanded/collapsed forms and consider pausing behind the overlay/dashboard. Use official localized names/artwork rather than developer jargon or altered marks.

Define progression semantics before upload. Achievements need honest locked/in-progress/hidden/completed states, progressive reporting, meaningful ordering, concise two-line text, and distinctive rewards. Select classic leaderboards for lasting best scores or recurring boards for renewed daily/seasonal competition; group large sets sensibly. Consult source art/crop specifications, preserving its stated platform distinctions rather than silently resolving inconsistent crop details.

For challenges, use a short individual skill attempt and the latest attempt rather than lifetime advantage. Deep-link invitations/system entries to the precise mode/level, completing necessary first-time teaching before continuing as promised. Multiplayer codes should remain findable with manual entry, joining/leaving/rejoining, and late participation where supported.

**Worked transformation:** Before, an invitation opens the home screen, a weekly challenge scores lifetime points, and its overlay blocks an active jump sequence. Decision: system entry must reach a fair specific activity without disrupting play. After, the invite opens that challenge after any necessary tutorial, scores the relevant latest attempt, and Game Center access stays in a safe menu context.

Deliver corrected social/progression routes and scoring/state contracts or implementation. Fail if invitations land generically, achievement progress misstates accomplishment, codes disappear, or cropped artwork loses meaning. Actual sign-in, overlays, matchmaking, and server score behavior require supported tests; design files alone do not verify them.

Use [Game controls](../../../apple-hig-inputs/.topics/apple-hig-game-controls/SKILL.md) for input and [Images](../../../apple-hig-foundations/.topics/apple-hig-images/SKILL.md) for reward/focus artwork.
