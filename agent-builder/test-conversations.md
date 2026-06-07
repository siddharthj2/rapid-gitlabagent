# Test Conversations

## Happy Path

User:
Show me recent failed pipelines on the `main` branch.

Expected behavior:

- Agent lists recent failed pipelines.
- Agent asks which pipeline to inspect if more than one result exists.
- Agent inspects the selected pipeline.
- Agent reads logs for the failed job.
- Agent returns a structured diagnosis.

## Ambiguous Failure

User:
Why did the deployment fail today?

Expected behavior:

- Agent lists matching failures from today.
- Agent asks the user to confirm which pipeline or job they mean.
- Agent does not guess.

## Thin Evidence

User:
Investigate pipeline `8241`.

Expected behavior:

- Agent inspects the failed job.
- Agent detects the logs are truncated or incomplete.
- Agent states the diagnosis is uncertain.
- Agent recommends the next debugging step.

## Permission Issue

User:
Check the last failed pipeline in `payments-service`.

Expected behavior:

- Agent attempts the GitLab query.
- If access fails, it explains the permission issue clearly.
- Agent suggests verifying project access or token scope.

