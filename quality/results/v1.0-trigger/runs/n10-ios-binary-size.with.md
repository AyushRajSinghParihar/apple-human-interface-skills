Start by finding what makes up the **180 MB**. Assets and bundled SDKs often offer bigger savings than code changes.

1. **Measure the shipped app.** Use a Release archive and check App Store Connect’s download/install sizes, or export from Xcode with an **App Thinning Size Report**. An `.xcarchive` includes items such as debug symbols that users don’t download; a universal IPA can include resources for multiple devices.

2. **Inspect the largest files in the exported `.app`.** Separate the executable, `Frameworks`, asset catalogs, and other resources. This tells you where to focus.

   | Biggest contributor | Most useful changes |
   |---|---|
   | Images | Remove unused or duplicate assets, resize oversized images, use appropriate compression, and put device-specific images in asset catalogs so thinning can help. |
   | Video, audio, models, offline data | Compress or download optional content when needed. Keep essential first-launch content bundled. |
   | Third-party SDKs | Remove unused dependencies, choose smaller SDK modules, and audit their bundled resources. |
   | Executable | Enable Release optimizations and dead-code stripping; use a linker map to identify large libraries and symbols. |

3. **Check Release build settings.** Verify `DEAD_CODE_STRIPPING = YES`, appropriate symbol stripping, and Swift’s **Optimize for Size (`-Osize`)** if its performance tradeoff suits your app. Keep dSYMs separately for crash symbolication. Review broad linker flags such as `-all_load`; change them only after checking why they’re required.

4. **Re-measure after each change.** Compare the same device variant and test startup, resource loading, and offline behavior.

Apple’s [Reducing your app’s size](https://developer.apple.com/documentation/xcode/reducing-your-app-s-size) covers the measurement workflow.

Where does your **180 MB** figure come from: the archive, IPA, App Store download, or installed app? And is the app native, Flutter, React Native, or Unity?