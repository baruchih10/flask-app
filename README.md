# Flask + Docker + GitHub Actions (Mini Lab Pack)

This repo is designed for teaching GitHub Actions using a **real** tiny Flask app that can be containerized and pushed.

## What you get

- A minimal Flask server (`/health`, `/`)  
- A Dockerfile that builds and runs it
- Many GitHub Actions workflows, each **focused on one concept** (needs, fan-out, outputs, artifacts, reusable workflows, cross-repo triggers, conditions)

## Quick start (local)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
# open http://localhost:8080/health
```

## Quick start (Docker)

```bash
docker build -t flask-actions-demo:local .
docker run --rm -p 8080:8080 flask-actions-demo:local
# open http://localhost:8080/health
```

---

## How GitHub evaluates "which workflow runs" when you have multiple YAML files

In GitHub Actions:
- Each file under `.github/workflows/*.yml` is a **separate workflow**.
- A workflow runs **only when its `on:` section matches** the event (push, pull_request, schedule, workflow_dispatch, etc.).
- If multiple workflows match the same event (e.g., two workflows both say `on: push`), **both will run** (separately).
- You can narrow a workflow with:
  - `branches:` / `tags:` filters
  - `paths:` filters (run only when specific files changed)
  - job/step-level `if:` expressions

In this repo, most workflows use `workflow_dispatch` so you can run them manually one by one.

---

## GitHub Container Registry (GHCR) push

Workflows in this repo push images to **GHCR** (`ghcr.io/<OWNER>/<REPO>:<tag>`) using `GITHUB_TOKEN`.

### One-time settings (recommended for classroom)
1. In the repo settings, ensure Actions has **Read and write permissions**:
   - Settings → Actions → General → Workflow permissions → **Read and write**
2. Ensure the workflow has:
   - `permissions: packages: write`

---

## Cross-repo demos included

To fully demo cross-repo reuse/trigger, you also get a second repo ZIP:
- `02-ci-library` (reusable workflow repo)

See: `.github/workflows/07-reuse-remote.yml` and `.github/workflows/08-trigger-downstream.yml`.

---

## Suggested lecture flow (run in this order)

1. `00-mental-model.yml` (prints context + explains multi-workflow behavior)
2. `01-needs-chain.yml` (job dependencies)
3. `02-fanout-fanin.yml` (parallel + merge gate)
4. `03-outputs-and-artifacts.yml` (job outputs + artifacts)
5. `04-step-dependencies.yml` (step-to-step, action outputs)
6. `05-reuse-local.yml` + `reusable-build.yml` (same-repo reusable workflows)
7. `07-reuse-remote.yml` (cross-repo reusable workflow)
8. `08-trigger-downstream.yml` (repository_dispatch)
9. `09-conditions.yml` (success/failure/always + job conditions)

Have fun 😄
