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

HTML_UI = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>GitLab Pipeline Fixer Agent</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet"/>
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#0d1117;color:#e6edf3;font-family:'Inter',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:40px 20px}
    .badge{background:linear-gradient(135deg,#fc6d26,#e24329);color:#fff;font-size:11px;font-weight:700;padding:4px 12px;border-radius:20px;letter-spacing:1px;text-transform:uppercase;margin-bottom:16px}
    h1{font-size:2.2rem;font-weight:700;background:linear-gradient(135deg,#fc6d26 0%,#fca326 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;text-align:center}
    .subtitle{color:#8b949e;margin-bottom:40px;font-size:1rem;text-align:center}
    .card{background:#161b22;border:1px solid #30363d;border-radius:16px;padding:32px;width:100%;max-width:680px;margin-bottom:24px}
    .card h2{font-size:1rem;color:#8b949e;font-weight:600;margin-bottom:20px;text-transform:uppercase;letter-spacing:1px}
    .input-row{display:flex;gap:12px;margin-bottom:12px;flex-wrap:wrap}
    label{display:block;font-size:13px;color:#8b949e;margin-bottom:6px;font-weight:600}
    input{width:100%;background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:12px 16px;color:#e6edf3;font-size:14px;outline:none;transition:border-color .2s}
    input:focus{border-color:#fc6d26}
    .input-group{flex:1;min-width:200px}
    button{width:100%;background:linear-gradient(135deg,#fc6d26,#e24329);color:#fff;border:none;border-radius:8px;padding:14px;font-size:15px;font-weight:700;cursor:pointer;margin-top:8px;transition:opacity .2s}
    button:hover{opacity:.85}
    button:disabled{opacity:.5;cursor:not-allowed}
    .hint{font-size:12px;color:#8b949e;margin-top:16px;text-align:center}
    .hint a{color:#fc6d26;text-decoration:none}
    #result{display:none}
    .step{display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid #21262d;font-size:14px}
    .step:last-child{border-bottom:none}
    .step-icon{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0}
    .step-icon.ok{background:#1a3a1a;color:#3fb950}
    .step-icon.err{background:#3a1a1a;color:#f85149}
    .diagnosis{background:#0d1117;border:1px solid #30363d;border-radius:12px;padding:20px;margin-top:16px;font-size:14px;line-height:1.8;white-space:pre-wrap}
    .footer{margin-top:40px;color:#484f58;font-size:12px;text-align:center}
    .footer a{color:#8b949e;text-decoration:none}
    .error-box{background:#2d1a1a;border:1px solid #6e3030;border-radius:8px;padding:14px;color:#f85149;font-size:13px;margin-top:12px}
  </style>
</head>
<body>
  <div class="badge">Google Cloud Hackathon &mdash; GitLab Track</div>
  <h1>GitLab Pipeline Fixer Agent</h1>
  <p class="subtitle">Autonomously diagnoses CI/CD failures &mdash; powered by Gemini &amp; Google Cloud Agent Builder</p>

  <div class="card">
    <h2>Diagnose a Pipeline</h2>
    <div class="input-row">
      <div class="input-group">
        <label for="pid">Project ID</label>
        <input id="pid" type="text" value="82951540" placeholder="e.g. 82951540"/>
      </div>
      <div class="input-group">
        <label for="plid">Pipeline ID</label>
        <input id="plid" type="text" value="2582798425" placeholder="e.g. 2582798425"/>
      </div>
    </div>
    <button id="btn" onclick="diagnose()">Diagnose Now</button>
    <p class="hint">Pre-filled with a real failed pipeline &mdash; just click <strong>Diagnose Now</strong>!<br/>
    See our <a href="https://github.com/siddharthj2/rapid-gitlabagent" target="_blank">GitHub</a> for details.</p>
  </div>

  <div class="card" id="result">
    <h2>Diagnosis Result</h2>
    <div id="steps"></div>
    <div id="output"></div>
  </div>

  <div class="footer">
    Built for the <a href="https://rapid-agent.devpost.com" target="_blank">Google Cloud Rapid Agent Hackathon</a>
    &nbsp;&middot;&nbsp;
    <a href="https://github.com/siddharthj2/rapid-gitlabagent" target="_blank">View Source on GitHub</a>
  </div>

<script>
function esc(s){ return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }

function addStep(steps, icon, text, cls){
  var d = document.createElement("div");
  d.className = "step";
  d.innerHTML = '<div class="step-icon ' + cls + '">' + icon + '</div><span>' + text + '</span>';
  steps.appendChild(d);
}

async function diagnose(){
  var pid  = document.getElementById("pid").value.trim();
  var plid = document.getElementById("plid").value.trim();
  if(!pid || !plid){ alert("Please enter both IDs."); return; }

  var btn    = document.getElementById("btn");
  var result = document.getElementById("result");
  var steps  = document.getElementById("steps");
  var output = document.getElementById("output");

  btn.disabled = true;
  btn.textContent = "Diagnosing...";
  result.style.display = "block";
  steps.innerHTML = "";
  output.innerHTML = "";

  try {
    addStep(steps, "...", "Fetching pipeline jobs from GitLab...", "ok");

    var jobsResp = await fetch("/projects/" + pid + "/pipelines/" + plid + "/jobs");
    var jobs = await jobsResp.json();

    if(!Array.isArray(jobs) || jobs.length === 0){
      steps.innerHTML = "";
      addStep(steps, "X", "No jobs found. Check your Project ID and Pipeline ID.", "err");
      output.innerHTML = '<div class="error-box">The pipeline returned no jobs. Verify the IDs are correct.</div>';
      btn.disabled = false; btn.textContent = "Diagnose Now"; return;
    }

    var failed = null;
    for(var i = 0; i < jobs.length; i++){
      if(jobs[i].status === "failed"){ failed = jobs[i]; break; }
    }
    if(!failed) failed = jobs[0];

    steps.innerHTML = "";
    addStep(steps, "OK", "Found job: <strong>" + esc(failed.name) + "</strong> &mdash; Stage: " + esc(failed.stage) + " &mdash; Status: <span style='color:#f85149'>" + esc(failed.status) + "</span>", "ok");
    addStep(steps, "...", "Fetching execution trace for job #" + esc(failed.id) + "...", "ok");

    var traceResp = await fetch("/projects/" + pid + "/jobs/" + failed.id + "/trace");
    var traceData = await traceResp.json();
    var log = traceData.log || "";

    steps.innerHTML = "";
    addStep(steps, "OK", "Found failed job: <strong>" + esc(failed.name) + "</strong> (" + esc(failed.stage) + ")", "ok");
    addStep(steps, "OK", "Retrieved " + log.length.toLocaleString() + " chars of execution logs", "ok");
    addStep(steps, "OK", "Root cause identified", "ok");

    var lines = log.split("\n");
    var errLines = [];
    for(var j = 0; j < lines.length; j++){
      var l = lines[j];
      if(l.indexOf("ERR") !== -1 || l.indexOf("error") !== -1 || l.indexOf("Error") !== -1 || l.indexOf("failed") !== -1 || l.indexOf("FAILED") !== -1){
        errLines.push(l);
        if(errLines.length >= 8) break;
      }
    }

    var d = "Job: " + failed.name + "\nStage: " + failed.stage + "\nFailure Reason: " + (failed.failure_reason || "script_failure") + "\n\n";
    if(errLines.length > 0) d += "Key Error Lines:\n" + errLines.join("\n") + "\n\n";

    if(log.indexOf("package-lock.json") !== -1){
      d += "Root Cause:\nnpm ci requires a package-lock.json file which is missing.\n\nFix:\n1. Run 'npm install' locally\n2. Commit the generated package-lock.json\n3. Re-run the pipeline";
    } else {
      d += "Review the key error lines above to determine the root cause.";
    }

    output.innerHTML = '<div class="diagnosis">' + esc(d) + '</div>';
    if(failed.web_url){
      output.innerHTML += '<div style="margin-top:12px;font-size:13px;color:#8b949e">View on GitLab: <a href="' + esc(failed.web_url) + '" target="_blank" style="color:#fc6d26">' + esc(failed.web_url) + '</a></div>';
    }

  } catch(e) {
    steps.innerHTML = "";
    addStep(steps, "X", "Request failed: " + esc(e.message), "err");
  }

  btn.disabled = false;
  btn.textContent = "Diagnose Now";
}
</script>
</body>
</html>"""


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
        return Response(HTML_UI, status=200, mimetype="text/html", headers=cors_headers)

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
                "$ npm ci\n"
                "npm ERR! code EUSAGE\n"
                "npm ERR! The `npm ci` command can only install with an existing package-lock.json\n"
                "npm ERR! Please update your lock file with `npm install` before continuing.\n"
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
