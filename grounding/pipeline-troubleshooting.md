# Pipeline Troubleshooting Notes

Use this document as background grounding for common CI/CD failure patterns.

## Dependency Installation Failures

Typical symptoms:

- package not found
- lockfile mismatch
- authentication to private registry failed
- checksum mismatch

Recommended agent behavior:

- mention the exact dependency manager error
- suggest checking lockfiles, registry credentials, and recent dependency updates

## Test Failures

Typical symptoms:

- unit tests failing
- assertion mismatch
- snapshot mismatch
- integration test timeout

Recommended agent behavior:

- identify the failing test target
- distinguish product regression from flaky infrastructure if evidence supports it

## Build Failures

Typical symptoms:

- compiler error
- type mismatch
- missing import
- asset bundling failure

Recommended agent behavior:

- quote the highest-signal error
- link it to the likely changed area when commit context is available

## Deployment Failures

Typical symptoms:

- missing environment variable
- container image pull failure
- permissions or service account issue
- health check or startup timeout

Recommended agent behavior:

- separate application startup errors from infrastructure errors
- suggest checking deployment configuration and secrets

