# 🎬 Demo Script — GitLab Pipeline Fixer Agent
## Google DevPost Hackathon — 3 Minute Video

---

## BEFORE YOU HIT RECORD — Open these tabs in your browser:
1. Tab 1: https://gitlab.com/siddharthjindal456-group/payments-service/-/pipelines
2. Tab 2: https://console.cloud.google.com/run/detail/us-central1/gitlab-mcp-proxy/source?project=gmail-479812
3. Tab 3: Open Conversational Agents → GitLab Pipeline Fixer Agent → click "Test Agent" to open the simulator

---

## 🎬 START RECORDING

---

### ⏱️ [0:00 – 0:30] — The Problem (Show GitLab)

**GO TO: Tab 1 — GitLab Pipeline page**

**SAY OUT LOUD:**
"In real software teams, CI/CD pipeline failures can block deployments for hours.
Developers have to manually dig through dozens of log lines to find the root cause.
Here I have a real failed pipeline in my GitLab project — the build stage has failed.
With our AI Agent, diagnosing this takes seconds."

---

### ⏱️ [0:30 – 1:00] — The Architecture (Quick Flash)

**GO TO: Tab 2 — Cloud Run Source Code**

**SAY OUT LOUD:**
"Our solution is a GitLab Pipeline Fixer Agent built on Google Cloud's Conversational Agents platform.
A Cloud Run proxy securely handles all GitLab API authentication — 
the token never leaves our Cloud Function.
The agent uses an OpenAPI tool definition to intelligently call the GitLab API."

---

### ⏱️ [1:00 – 2:30] — The Live Demo (THE MAIN PART!)

**GO TO: Tab 3 — Conversational Agent Simulator**

**SAY OUT LOUD:**
"Let me show you a live demo. I'll give the agent only the project ID and pipeline ID — 
nothing else. Watch it figure out everything on its own."

**TYPE THIS EXACTLY in the simulator chat box:**

I have a failed pipeline. Project ID is 82951540, Pipeline ID is 2582798425. Find the failed job, get its trace, and diagnose the root cause for me.

**WHILE IT IS LOADING, SAY:**
"The agent is now autonomously calling our GitLab tool.
First — getPipelineJobs to find which job failed.
Then — getJobTrace to fetch the actual error log from the GitLab runner."

**WHEN THE ANSWER APPEARS, POINT TO THE SCREEN AND SAY:**
"The agent identified the exact failing job: install_dependencies.
Root cause: npm ci requires a package-lock.json file which is missing from the repository.
It pulled this from the real GitLab logs — no hardcoding, no guessing.
And it gives us the exact fix: run npm install locally and commit the lock file."

---

### ⏱️ [2:30 – 3:00] — Wrap Up

**SAY OUT LOUD:**
"This is the GitLab Pipeline Fixer Agent. It connects Google Cloud's Conversational Agents
to the GitLab API through a secure Cloud Run proxy.
A developer simply describes their problem in plain English —
and the agent fetches real data, reads real logs, and gives a real diagnosis.
Built for the Google Cloud DevPost Hackathon. Thank you."

---

## 🎬 STOP RECORDING

---

## Checklist before uploading:
- Video is under 3 minutes
- Agent correctly called getPipelineJobs
- Agent correctly called getJobTrace
- Agent gave a clear root cause diagnosis
- Your voice is clear
- Screen resolution is at least 1080p
