The workspace has no Swift package files, and filesystem access is read-only, so I couldn’t create the workflow.

Add `.github/workflows/tests.yml` to your repository:

```yaml
name: Swift Tests

on:
  push:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  test:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4

      - name: Show Swift version
        run: swift --version

      - name: Run XCTest suite
        run: swift test
```

This uses the macOS runner’s default Swift toolchain and assumes `Package.swift` is at the repository root.