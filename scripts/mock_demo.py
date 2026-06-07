from pathlib import Path
import json


def derive_follow_up(stage: str) -> str:
    if stage == "build":
        return "Compare dependency files in the latest commit before rerunning the build."
    if stage == "test":
        return "Inspect the changed files in the latest commit to confirm the failing import or test path."
    if stage == "deploy":
        return "Check deployment startup logs and environment configuration before retrying deployment."
    return "Inspect the surrounding pipeline context before taking action."


def print_case(case: dict) -> None:
    print("=" * 72)
    print(f"Failure summary")
    print(f"- Pipeline: {case['pipeline_id']}")
    print(f"- Branch: {case['branch']}")
    print(f"- Failed job: {case['job_name']}")
    print(f"- Stage: {case['stage']}")
    print(f"- Commit: {case['commit']}")
    print()
    print("Likely root cause")
    print(case["expected_root_cause"])
    print()
    print("Supporting evidence")
    print(f"- {case['log_excerpt']}")
    print(f"- Expected issue pattern: {case['summary']}")
    print()
    print("Confidence")
    print(case["expected_confidence"])
    print()
    print("Recommended next actions")
    for action in case["expected_actions"]:
        print(f"- {action}")
    print()
    print("Optional follow-up")
    print(f"- {derive_follow_up(case['stage'])}")
    print()


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    sample_path = repo_root / "samples" / "pipeline_failure_cases.json"
    with sample_path.open("r", encoding="utf-8") as handle:
        cases = json.load(handle)

    print("GitLab Pipeline Fixer Agent mock demo")
    print("This script uses local sample failures to rehearse the expected output shape.")
    print()
    for case in cases:
        print_case(case)


if __name__ == "__main__":
    main()

