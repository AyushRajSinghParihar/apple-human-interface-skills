Add this to `fastlane/Fastfile`, replacing the workspace and scheme names:

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

    build_app(
      workspace: "YourApp.xcworkspace",
      scheme: "YourApp",
      configuration: "Release",
      export_method: "app-store"
    )

    upload_to_testflight(
      api_key: api_key,
      skip_waiting_for_build_processing: true
    )
  end
end
```

Set your App Store Connect API credentials, then run:

```sh
export ASC_KEY_ID="YOUR_KEY_ID"
export ASC_ISSUER_ID="YOUR_ISSUER_ID"
export ASC_KEY_PATH="/path/to/AuthKey.p8"

bundle exec fastlane ios beta
```

The scheme must be shared, distribution signing configured, and the build number unique for each upload. If you use an `.xcodeproj`, replace `workspace:` with `project: "YourApp.xcodeproj"`.

No Xcode project was available here, so I couldn’t customize or test the lane.