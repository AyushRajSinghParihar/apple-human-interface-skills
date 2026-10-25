---
name: apple-hig-airplay
description: Use when designing or reviewing AirPlay playback, remote commands, background streaming, destination quality, or AirPlay controls and compatibility artwork.
---

# Send the intended media and preserve playback control

Read [AirPlay](../../references/airplay.md). Inspect the player's media purpose, rendition inventory, remote-command handling, background behavior, and requested design/review/adaptation. Keep the current media stack where it can meet the contract. The source excludes watchOS; verify implementation availability for the targeted OS.

Prefer standard playback controls with captions, chapters, and AirPlay. A custom player must preserve familiar starting/playing/unavailable controls rather than substituting branding artwork for an interactive control. Use Apple's provided control symbols; the guide places the control at lower right on iOS/iPadOS 16+.

Separate intended media from incidental app clips. The chosen stream should continue when the device locks/backgrounds; browsing another area must not replace it with an inline loop or expose unrelated private activity through automatic mirroring. Do not interrupt another app's playback merely on launch. Handle play/pause/seek from system remote surfaces, and supply available HLS resolutions so destination selection is not limited to a phone-sized rendition.

If the request concerns acceptance marketing, use noninteractive compatibility artwork according to neighboring icon color/container rules. Keep app identity more prominent and use AirPlay as a correctly capitalized noun. Do not turn the downloaded compatibility mark into a custom route-picker button.

**Before → decision → after:** A lecture app streams a 720p-only video, replaces it with home-screen previews during browsing, and uses a compatibility logo as its route button. Decision: the receiver needs the selected lecture, destination-quality media, and a real control. After, the standard AirPlay control manages routing, available renditions reach the receiver, and previews remain local without replacing the lecture.

Deliver the media/routing/remote-state contract or corrected player. Fail if locking stops intended playback, remote commands affect another item, or unrelated media replaces the stream. Report actual receiver/background/Lock Screen tests separately; file inspection cannot establish AirPlay transport or television quality.

Use [Images](../../../apple-hig-foundations/.topics/apple-hig-images/SKILL.md) for compatibility assets and [SharePlay](../apple-hig-shareplay/SKILL.md) only when synchronized shared playback is also requested.
