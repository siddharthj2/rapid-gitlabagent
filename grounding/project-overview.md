# Project Overview

GitLab Pipeline Fixer Agent is designed for developers and DevOps teams that lose time reading raw CI/CD logs. The agent shortens time-to-diagnosis by pulling the relevant pipeline context, locating the failed job, extracting the most likely cause, and suggesting the next debugging step.

## Primary User

- software engineer investigating a failed pipeline
- developer experience engineer supporting multiple repositories
- DevOps engineer triaging recurring build or deployment failures

## Core Value

Instead of asking a user to manually open GitLab, inspect the pipeline, read logs, and correlate the failure with the latest commit, the agent does this in a guided conversational flow and returns a usable diagnosis.

## Main Supported Jobs

- identify the latest failed pipeline
- explain the most likely reason a job failed
- highlight evidence from logs
- suggest safe next steps

