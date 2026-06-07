# 🤖 GitLab Pipeline Fixer Agent

> **Google Cloud Rapid Agent Hackathon — GitLab Partner Track**

An AI-powered Conversational Agent that **autonomously diagnoses GitLab CI/CD pipeline failures**. Give it a Project ID and Pipeline ID — it finds the failing job, fetches the real error logs, and tells you exactly what went wrong and how to fix it.

---

## 🎥 Demo Video
https://youtu.be/AaReo-3TuKE

---

## 🏗️ Architecture

```
User (plain English)
       │
       ▼
Google Cloud Conversational Agent (Gemini)
       │  calls tools via OpenAPI schema
       ▼
Cloud Run Proxy (gitlab-mcp-proxy)
       │  injects GITLAB_TOKEN securely
       ▼
GitLab REST API
  ├── GET /projects/{id}/pipelines
  ├── GET /projects/{id}/pipelines/{pipeline_id}/jobs
  └── GET /projects/{id}/jobs/{job_id}/trace
```

### Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Conversational Agent | Google Cloud Agent Builder | LLM reasoning + tool orchestration |
| Proxy API | Python 3.11 on Cloud Run | Secure GitLab API gateway |
| Schema | OpenAPI 3.0 | Tool definitions for the agent |
| CI Pipeline | GitLab CI/CD | Real failing pipeline for demo |

---

## ✨ Features

- 🔍 **Autonomous Pipeline Diagnosis** — The agent plans and executes multi-step tool calls without prompting
- 🔐 **Secure Token Handling** — GitLab API token stored in Cloud Run env vars, never exposed to the agent
- 📋 **Real Log Analysis** — Fetches actual job traces from GitLab runners and analyzes them
- 💡 **Actionable Fixes** — Provides specific, step-by-step remediation instructions
- 🔄 **ANSI-Safe Parsing** — Proxy handles binary/ANSI-encoded log output from GitLab runners

---

## 🚀 How It Works

1. **User asks in plain English:**
   > *"I have a failed pipeline. Project ID is 82951540, Pipeline ID is 2582798425. Find the failed job, get its trace, and diagnose the root cause for me."*

2. **Agent calls `getPipelineJobs`** → Finds the failing `install_dependencies` job in the `build` stage

3. **Agent calls `getJobTrace`** → Fetches real error logs from the GitLab runner

4. **Agent responds with a full diagnosis:**
   - Root cause: `npm ci` requires a `package-lock.json` that doesn't exist
   - Fix: Run `npm install` locally and commit `package-lock.json`

---

## 📂 Project Structure

```
├── agent-builder/
│   ├── gitlab-openapi-v2.yaml   # OpenAPI schema for the Conversational Agent tool
│   └── system-prompt.md         # Agent persona and instructions
├── cloudfunction/
│   ├── main.py                  # Cloud Run proxy (Flask/Functions Framework)
│   └── requirements.txt         # Python dependencies
├── samples/
│   └── demo-project/
│       ├── .gitlab-ci.yml       # CI config that intentionally fails (npm ci without lock file)
│       └── package.json         # Node.js project manifest
└── README.md
```

---

## 🛠️ Setup Guide

### Prerequisites
- Google Cloud Project with billing enabled
- GitLab account with a project
- GitLab Personal Access Token (with `read_api` scope)

### 1. Deploy the Cloud Run Proxy

```bash
cd cloudfunction/

# Deploy to Cloud Run
gcloud run deploy gitlab-mcp-proxy \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GITLAB_TOKEN=<YOUR_GITLAB_TOKEN>
```

### 2. Configure the Conversational Agent

1. Go to [Google Cloud Conversational Agents](https://conversational-agents.cloud.google.com)
2. Create a new Agent with Gemini
3. Create a new **Tool** with type `OpenAPI`
4. Paste the contents of `agent-builder/gitlab-openapi-v2.yaml` as the schema
5. Replace the `servers.url` with your Cloud Run URL

### 3. Test the Agent

In the Agent simulator, type:
```
I have a failed pipeline. Project ID is YOUR_PROJECT_ID, Pipeline ID is YOUR_PIPELINE_ID. 
Find the failed job, get its trace, and diagnose the root cause for me.
```

---

## 🔐 Security

- The GitLab API token is stored as a Cloud Run environment variable
- The token is **never** passed through the OpenAPI schema or visible to the agent
- The proxy injects the token server-side on every request
- Cloud Run allows unauthenticated access to the proxy (required for Agent Builder)

---

## 📦 Dependencies

**Cloud Function (`cloudfunction/requirements.txt`)**
```
functions-framework
requests
```

---

## 🏆 Hackathon Details

- **Event:** [Google Cloud Rapid Agent Hackathon](https://rapid-agent.devpost.com)
- **Track:** GitLab Partner Track
- **Built with:** Google Cloud Agent Builder, Gemini, Cloud Run, GitLab REST API
- **Partner Integration:** GitLab API via custom OpenAPI MCP-style proxy

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
