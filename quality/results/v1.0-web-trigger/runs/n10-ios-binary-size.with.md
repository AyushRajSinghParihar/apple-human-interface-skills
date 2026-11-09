Start by finding **what makes up the 180 MB**. Assets, embedded SDKs, and compiled code need different fixes.

1. **Measure a Release build after app thinning.** An `.xcarchive`, exported IPA, download, and installed app can have very different sizes. Export with “All compatible device variants” and inspect `App Thinning Size Report.txt`, or check App Store Connect’s size report. [Apple’s measurement guide](https://developer.apple.com/documentation/xcode/reducing-your-app-s-size).

2. **Find the largest bundle contents.** Run this against the archived `.app`:
   ```sh
   du -ah "/path/to/YourApp.app" | sort -hr | head -40
   ```
   Look for large `Assets.car` files, frameworks, videos, fonts, databases, and ML models.

3. **Fix the biggest contributors first:**

   | Contributor | What to try |
   |---|---|
   | Images and media | Remove unused files, resize oversized images, compress media, and use asset catalogs for device-specific assets. |
   | SDKs and frameworks | Remove unused dependencies, use smaller SDK modules, and check for duplicated resources. |
   | Bundled content | Download optional content when needed, while keeping essential offline functionality available. |
   | App executable | Check Release optimization settings; investigate large libraries and generated code with a linker map. |

   Apple covers these approaches in its [basic](https://developer.apple.com/documentation/xcode/doing-basic-optimization-to-reduce-your-app-s-size) and [advanced optimization guidance](https://developer.apple.com/documentation/xcode/doing-advanced-optimization-to-further-reduce-your-app-s-size).

4. **Check Release settings.** Verify dead-code stripping is enabled and evaluate Swift’s **Optimize for Size (`-Osize`)**. Benchmark performance after changing optimization settings.

Re-measure the same device variant after each change so the comparison is meaningful.

**Where are you seeing 180 MB—archive, IPA, App Store download, or installed size—and is the app native, Flutter, React Native, or Unity?**