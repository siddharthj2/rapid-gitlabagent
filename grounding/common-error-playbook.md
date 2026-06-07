# Common Error Playbook

## `npm ci` Fails With Lockfile Error

Interpretation:
Dependency metadata changed without committing a matching lockfile.

Recommended actions:

- regenerate the lockfile locally
- commit the lockfile
- rerun the pipeline

## Python Test Import Error

Interpretation:
The code or test path changed and the runtime cannot import the expected module.

Recommended actions:

- verify package path and module naming
- check the job's Python path and install step
- confirm the changed file was included in the commit

## Docker Build Authentication Failure

Interpretation:
The pipeline cannot access the required registry or base image.

Recommended actions:

- verify registry credentials
- verify service account or CI variable scope
- check whether a token expired or lost permission

## Deployment Health Check Timeout

Interpretation:
The application did not start cleanly or did not bind to the expected port in time.

Recommended actions:

- inspect application startup logs
- verify port configuration
- check secret and environment variable presence

