from pathlib import Path
import json
import sys


REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "agent-builder/system-prompt.md",
    "agent-builder/tool-contract.md",
    "agent-builder/response-template.md",
    "agent-builder/test-conversations.md",
    "grounding/project-overview.md",
    "grounding/pipeline-troubleshooting.md",
    "grounding/common-error-playbook.md",
    "samples/pipeline_failure_cases.json",
    "submission/demo-script.md",
    "submission/devpost-description.md",
    "submission/checklist.md",
]


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    missing = [path for path in REQUIRED_FILES if not (repo_root / path).exists()]
    if missing:
        print("Missing required files:")
        for path in missing:
            print(f"- {path}")
        return 1

    sample_path = repo_root / "samples/pipeline_failure_cases.json"
    with sample_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, list) or not data:
        print("Sample data file must contain a non-empty list of cases.")
        return 1

    required_case_keys = {
        "case_id",
        "pipeline_id",
        "branch",
        "job_name",
        "stage",
        "commit",
        "summary",
        "log_excerpt",
        "expected_root_cause",
        "expected_confidence",
        "expected_actions",
    }

    invalid_cases = []
    for case in data:
        missing_keys = sorted(required_case_keys - set(case))
        if missing_keys:
            invalid_cases.append((case.get("case_id", "<unknown>"), missing_keys))

    if invalid_cases:
        print("Invalid sample cases:")
        for case_id, missing_keys in invalid_cases:
            print(f"- {case_id}: missing {', '.join(missing_keys)}")
        return 1

    print("Acceptance check passed.")
    print(f"Validated {len(REQUIRED_FILES)} required files.")
    print(f"Validated {len(data)} sample pipeline failure cases.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

