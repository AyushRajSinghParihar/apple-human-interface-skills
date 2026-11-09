Add this to `fastlane/Fastfile`, replacing the workspace and scheme names:

```ruby
default_platform(:ios)

platform :ios do
  desc "Build and upload to TestFlight"
  lane :beta do
    api_key = app_store_connect_api_key(
      key_id: ENV.fetch("ASC_KEY_ID"),
      issuer_id: ENV.fetch("ASC_ISSUER_ID"),
      key_filepath: ENV.fetch("ASC_KEY_FILEPATH")
    )

    ipa = build_app(
      workspace: "MyApp.xcworkspace",
      scheme: "MyApp",
      configuration: "Release",
      export_method: "app-store",
      clean: true
    )

    upload_to_testflight(
      api_key: api_key,
      ipa: ipa,
      skip_waiting_for_build_processing: true
    )
  end
end
```

Set credentials and run:

```bash
export ASC_KEY_ID="YOUR_KEY_ID"
export ASC_ISSUER_ID="YOUR_ISSUER_ID"
export ASC_KEY_FILEPATH="/absolute/path/to/AuthKey_YOUR_KEY_ID.p8"

bundle exec fastlane ios beta
```

This assumes your app exists in App Store Connect, the scheme is shared, and distribution signing is configured on the Mac. Use a unique build number for each upload. If you don’t use a workspace, replace `workspace:` with `project: "MyApp.xcodeproj"`.

The lane uploads and returns before Apple finishes processing. Keep the `.p8` key out of version control.

References: [build_app](https://docs.fastlane.tools/actions/build_app/), [TestFlight upload](https://docs.fastlane.tools/actions/upload_to_testflight/), [API authentication](https://docs.fastlane.tools/actions/app_store_connect_api_key/).