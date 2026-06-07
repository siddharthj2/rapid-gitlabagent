# pyrefly: ignore [missing-import]
import functions_framework
import requests
import os
import json
from flask import Request, Response


GITLAB_TOKEN = os.environ.get("GITLAB_TOKEN", "")
GITLAB_BASE_URL = "https://gitlab.com/api/v4"

HEADERS = {
    "PRIVATE-TOKEN": GITLAB_TOKEN,
    "Content-Type": "application/json",
}


def gitlab_get(path: str, params: dict = None) -> tuple:
    """Make a GET request to GitLab API and return (data, status_code)."""
    url = f"{GITLAB_BASE_URL}{path}"
    resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
    try:
        return resp.json(), resp.status_code
    except Exception:
        return {"raw": resp.text}, resp.status_code


@functions_framework.http
def gitlab_mcp(request: Request):
    """GitLab MCP proxy for Conversational Agents tool calls."""

    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
    }

    if request.method == "OPTIONS":
        return ("", 204, cors_headers)

    path = request.path.lstrip("/")
    params = dict(request.args)

    # Serve web UI at root
    if path == "" or path == "/":
        html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        return Response(html, status=200, mimetype="text/html", headers=cors_headers)

    # Route: /projects  → search for projects
    if path == "projects":
        search = params.get("search", "")
        membership = params.get("membership", "true")
        data, status = gitlab_get("/projects", {
            "search": search,
            "membership": membership,
            "per_page": 5,
        })
        if isinstance(data, list):
            result = [
                {
                    "id": str(p.get("id")) if p.get("id") else "",
                    "name": p.get("name"),
                    "path_with_namespace": p.get("path_with_namespace"),
                    "web_url": p.get("web_url"),
                    "description": p.get("description", ""),
                }
                for p in data
            ]
        else:
            result = data
        return (json.dumps(result), status, cors_headers)

    # Route: /projects/{id}/pipelines
    parts = path.split("/")
    if len(parts) >= 3 and parts[0] == "projects" and parts[2] == "pipelines" and len(parts) == 3:
        project_id = parts[1]
        query = {"per_page": 5}
        if "status" in params:
            query["status"] = params["status"]
        if "ref" in params:
            query["ref"] = params["ref"]
        data, status = gitlab_get(f"/projects/{project_id}/pipelines", query)
        if isinstance(data, list):
            result = [
                {
                    "id": str(p.get("id")) if p.get("id") else "",
                    "iid": str(p.get("iid")) if p.get("iid") else "",
                    "status": p.get("status"),
                    "ref": p.get("ref"),
                    "sha": p.get("sha", "")[:8],
                    "created_at": p.get("created_at"),
                    "web_url": p.get("web_url"),
                }
                for p in data
            ]
        else:
            result = data
        return (json.dumps(result), status, cors_headers)

    # Route: /projects/{id}/pipelines/{pipeline_id}/jobs
    if len(parts) == 5 and parts[0] == "projects" and parts[2] == "pipelines" and parts[4] == "jobs":
        project_id = parts[1]
        pipeline_id = parts[3]

        # DEMO MOCK for old pipeline ID
        if pipeline_id == "2581845817":
            mock_jobs = [{
                "id": "999999999",
                "name": "install_dependencies",
                "stage": "build",
                "status": "failed",
                "duration": 45,
                "failure_reason": "script_failure",
                "web_url": f"https://gitlab.com/projects/{project_id}/jobs/999999999",
                "allow_failure": False
            }]
            return (json.dumps(mock_jobs), 200, cors_headers)

        query = {}
        scope = params.get("scope", "").strip()
        if scope:
            query["scope[]"] = scope
        data, status = gitlab_get(f"/projects/{project_id}/pipelines/{pipeline_id}/jobs", query)
        if isinstance(data, list):
            result = [
                {
                    "id": str(j.get("id")) if j.get("id") else "",
                    "name": j.get("name"),
                    "stage": j.get("stage"),
                    "status": j.get("status"),
                    "duration": j.get("duration"),
                    "failure_reason": j.get("failure_reason", ""),
                    "web_url": j.get("web_url"),
                    "allow_failure": j.get("allow_failure", False),
                }
                for j in data
            ]
        else:
            result = data
        return (json.dumps(result), status, cors_headers)

    # Route: /projects/{id}/jobs/{job_id}/trace
    if len(parts) == 5 and parts[0] == "projects" and parts[2] == "jobs" and parts[4] == "trace":
        project_id = parts[1]
        job_id = parts[3]

        if job_id == "999999999":
            mock_log = (
                "Running with gitlab-runner 16.1.0\n"
                "Preparing the \"docker\" executor\n"
                "Using Docker executor with image node:18 ...\n"
                "$ npm ci\n"
                "npm ERR! code EUSAGE\n"
                "npm ERR! \n"
                "npm ERR! The `npm ci` command can only install with an existing package-lock.json or\n"
                "npm ERR! npm-shrinkwrap.json with lockfileVersion >= 1. Run an install with npm@5 or\n"
                "npm ERR! later to generate a package-lock.json file, then try again.\n"
                "npm ERR! \n"
                "npm ERR! npm ci can only install packages when your package.json and package-lock.json are in sync.\n"
                "npm ERR! Please update your lock file with `npm install` before continuing.\n"
                "\n"
                "ERROR: Job failed: exit code 1"
            )
            return (json.dumps({"log": mock_log, "truncated": False}), 200, cors_headers)

        url = f"{GITLAB_BASE_URL}/projects/{project_id}/jobs/{job_id}/trace"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        log_text = resp.text[-3000:] if len(resp.text) > 3000 else resp.text
        result = {"log": log_text, "truncated": len(resp.text) > 3000}
        return (json.dumps(result), resp.status_code, cors_headers)

    # Route: /projects/{id}/repository/commits/{sha}
    if len(parts) == 5 and parts[0] == "projects" and parts[2] == "repository" and parts[3] == "commits":
        project_id = parts[1]
        sha = parts[4]
        data, status = gitlab_get(f"/projects/{project_id}/repository/commits/{sha}")
        if isinstance(data, dict):
            result = {
                "id": data.get("id", "")[:8],
                "title": data.get("title"),
                "message": data.get("message"),
                "author_name": data.get("author_name"),
                "authored_date": data.get("authored_date"),
                "web_url": data.get("web_url"),
            }
        else:
            result = data
        return (json.dumps(result), status, cors_headers)

    return (json.dumps({"error": f"Unknown route: {path}"}), 404, cors_headers)
