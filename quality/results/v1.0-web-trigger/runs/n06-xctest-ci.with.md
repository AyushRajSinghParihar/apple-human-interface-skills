The workspace has no Swift package and is read-only, so I couldn’t add the workflow or run tests.

Add this as `.github/workflows/tests.yml` in your repository, assuming `Package.swift` is at the root:

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
      - uses: actions/checkout@v5

      - name: Show Swift version
        run: swift --version

      - name: Run tests
        run: swift test
```

`swift test` builds the package and runs its XCTest suite, failing the workflow if any tests fail. See [GitHub’s Swift CI guide](https://docs.github.com/en/actions/tutorials/build-and-test-code/swift).