# Tool Contract

This document defines the minimal GitLab MCP capability expected by the MVP.

## Required Tools

### 1. List recent failed pipelines

Purpose:
Return recent failed pipelines for a project or branch.

Minimum inputs:

- project identifier
- optional branch
- optional time window

Expected outputs:

- pipeline id
- branch name
- status
- commit sha
- author or trigger source if available
- created time
- web url if available

### 2. Inspect pipeline or job

Purpose:
Return the jobs in a selected pipeline and identify failed jobs.

Minimum inputs:

- project identifier
- pipeline id

Expected outputs:

- job id
- job name
- stage
- status
- duration if available
- web url if available

### 3. Read job logs

Purpose:
Read logs for a failed job so the agent can diagnose the issue.

Minimum inputs:

- project identifier
- job id

Expected outputs:

- raw or chunked logs
- truncation signal if logs are incomplete

### 4. Read commit or merge request context

Purpose:
Read nearby code or review context when logs alone are not enough.

Minimum inputs:

- project identifier
- commit sha or merge request id

Expected outputs:

- commit title or merge request title
- summary of changed files if available
- discussion metadata if available

## Agent Guardrails

- The agent must use the smallest number of tools necessary to answer.
- The agent should fetch logs before inferring root cause.
- The agent should not perform reruns, merges, or modifications automatically.
- Any write-capable tool should remain disabled for the MVP unless explicit confirmation is added later.

