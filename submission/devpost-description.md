# Devpost Description

## One-Line Pitch

GitLab Pipeline Fixer Agent is a Gemini-powered troubleshooting assistant that uses Google Cloud Agent Builder and the GitLab MCP server to investigate failed CI/CD pipelines and recommend the next best action.

## What It Does

Developers waste time jumping between pipeline dashboards, raw logs, and recent commits just to answer one question: why did the build fail? GitLab Pipeline Fixer Agent turns that manual investigation into a guided workflow.

The agent:

- finds recent failed GitLab pipelines
- inspects the failed job and its logs
- reads related commit or merge request context when needed
- explains the likely root cause with evidence
- recommends safe next steps without taking destructive actions automatically

## Why It Matters

This project moves beyond chat by using tools to complete a real operational task. Instead of only answering a question, the agent gathers context, reasons across multiple steps, and returns an actionable diagnosis that saves developer time.

## How We Built It

- `Google Cloud Agent Builder` for managed agent orchestration
- `Gemini` for reasoning and response generation
- `GitLab MCP server` for pipeline, job, log, commit, and merge request access
- `Secret Manager` for credentials
- grounding documents for troubleshooting patterns and response consistency

## Key Workflow

1. User asks about a failed pipeline.
2. The agent fetches recent failed pipelines from GitLab.
3. The agent identifies the failed job and reads the logs.
4. The agent correlates the evidence with commit or merge request context if needed.
5. The agent returns the likely root cause, confidence, and recommended next steps.

## What Makes It Different

- Focused on a real developer pain point
- Uses MCP meaningfully instead of as a superficial integration
- Structured, evidence-based outputs
- Designed to keep the user in control of any follow-up action

## Future Work

- add safe rerun workflows with explicit confirmation
- support merge request review and release readiness workflows
- learn from recurring pipeline failure patterns across repositories

