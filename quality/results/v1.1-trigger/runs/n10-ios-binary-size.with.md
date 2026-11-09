First, check what the **180 MB measures**. An `.xcarchive`, exported IPA, App Store download, and installed app can have very different sizes. Your archive includes debug symbols and other files users don’t download.

For a useful baseline, export a Release archive from Xcode using **App Thinning → All compatible device variants**, then inspect the **App Thinning Size Report**. App Store Connect also shows download and installed sizes for processed builds.

Then prioritize these changes:

| Area | What to do |
|---|---|
| **Images, audio, and video** | Find the largest bundled files. Resize images to their displayed resolution, compress media appropriately, and remove unused assets. Use asset catalogs so app thinning can select device-specific resources. |
| **Dependencies** | Audit bundled frameworks and SDKs. Remove unused ones, duplicate libraries, and optional modules you don’t need. Large analytics, media, ML, and cross-platform SDKs can dominate size. |
| **Optional content** | Deliver large models, tutorials, maps, or media when needed instead of bundling everything. Consider Background Assets or an appropriate download-and-cache flow. |
| **Release settings** | Confirm Release uses size optimization, dead-code stripping, and symbol stripping. For Swift, evaluate `-Osize` and measure the result. Keep dSYMs separately for crash symbolication. |
| **Fonts and data** | Remove unused font families, sample files, test fixtures, duplicate databases, and unnecessary bundled resources. Check font licenses before subsetting. |

To identify the biggest opportunity, inspect your exported `.app` package in Finder using **Show Package Contents**, and sort its files and frameworks by size. If assets dominate, compiler changes won’t help much; if the executable dominates, investigate dependencies and generate a linker map.

Avoid old advice about enabling Bitcode—it’s deprecated and isn’t a current size-reduction strategy.

Is your 180 MB figure from the archive, IPA, App Store download estimate, or installed app?