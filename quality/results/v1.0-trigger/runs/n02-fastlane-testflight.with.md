Add this to `fastlane/Fastfile`, replacing `MyApp` with your project and shared scheme names:

```ruby
default_platform(:ios)

platform :ios do
  desc "Build and upload to TestFlight"
  lane :beta do
    api_key = app_store_connect_api_key(
      key_id: ENV.fetch("ASC_KEY_ID"),
      issuer_id: ENV.fetch("ASC_ISSUER_ID"),
      key_filepath: ENV.fetch("ASC_KEY_PATH")
    )

    increment_build_number(
      xcodeproj: "MyApp.xcodeproj",
      build_number: ENV.fetch("BUILD_NUMBER")
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

Run on macOS with Xcode installed:

```sh
export ASC_KEY_ID="YOUR_KEY_ID"
export ASC_ISSUER_ID="YOUR_ISSUER_ID"
export ASC_KEY_PATH="/secure/path/AuthKey.p8"
export BUILD_NUMBER="42"

bundle exec fastlane ios beta
```

Use a unique, increasing build number for each upload. This assumes App Store distribution signing is already configured and the app exists in App Store Connect. For a project without a workspace, replace `workspace:` with `project: "MyApp.xcodeproj"`.

No app project was available here, so this lane hasn’t been run.