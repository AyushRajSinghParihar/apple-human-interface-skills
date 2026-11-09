The workspace has no Swift package and is read-only, so I couldn’t create the workflow. Add this as `.github/workflows/tests.yml` in your package repository:

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
    name: XCTest on macOS
    runs-on: macos-latest
    timeout-minutes: 20

    steps:
      - uses: actions/checkout@v4

      - name: Show Swift version
        run: swift --version

      - name: Run tests
        run: swift test
```

This uses the runner’s default Swift toolchain and builds and runs your XCTest suite on every push and pull request. It assumes `Package.swift` is at the repository root.