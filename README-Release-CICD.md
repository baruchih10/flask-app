# Release CI/CD to ACR + ACI + ACA (Port 5000)

## Goal
When we publish a GitHub Release with a tag (example: `v3.0.1`), GitHub Actions will:
1) Build a Docker image and push it to Azure Container Registry (ACR) with the same tag
2) Deploy that image to Azure Container Instances (ACI) for a smoke test (public on `:5000`)
3) If the smoke test passes, deploy the same image to Azure Container Apps (ACA)

✅ release tag == image tag == deployed version

---

## What is created by Terraform
Terraform creates:
- Resource Group
- ACR
- Log Analytics
- Container Apps Environment
- Container App (ACA) with external ingress and target port `5000`
- User-assigned managed identity (UAMI) for **runtime** ACR pulls
- Entra App + Service Principal + GitHub OIDC federated credential
- RBAC role assignments:
  - Service Principal: Contributor on RG, AcrPush on ACR (CI/CD time)
  - Managed Identity: AcrPull on ACR (runtime)

---

## 1) GitHub setup: Environments, Variables, Secrets

### A) Create GitHub Environments
Repo → Settings → Environments → create:
- `dev`
- `stage`
- `production`

We will use environments only to vary ACI naming (container group name + DNS label).

### B) Repository Variables (shared, same for all environments)
Repo → Settings → Secrets and variables → Actions → **Variables** → New variable

Add these as **Repository Variables**:

- `AZURE_LOCATION` = `westeurope`
- `RESOURCE_GROUP` = (Terraform output: `resource_group_name`)
- `ACR_LOGIN_SERVER` = (Terraform output: `acr_login_server`)   e.g. `myacr.azurecr.io`
- `ACA_NAME` = (Terraform output: `aca_name`)
- `RUNTIME_PULL_IDENTITY_ID` = (Terraform output: `runtime_pull_identity_id`)
- `IMAGE_REPO` = `flask-app`
- `CONTAINER_PORT` = `5000`

> Note: these are configuration values, not credentials.

### C) Environment Variables (only for ACI naming)
Repo → Settings → Environments → click each environment → **Environment variables**

Add:

#### production
- `ACI_CONTAINER_GROUP_NAME` = `flask-aci-prod`
- `ACI_DNS_LABEL` = `flask-aci-prod-demo-flask-57`  (must be unique in region)

#### stage (example)
- `ACI_CONTAINER_GROUP_NAME` = `flask-aci-stage`
- `ACI_DNS_LABEL` = `flask-aci-stage-demo-flask-57`

#### dev (example)
- `ACI_CONTAINER_GROUP_NAME` = `flask-aci-dev`
- `ACI_DNS_LABEL` = `flask-aci-dev-demo-flask-57`

> Only these two should change per environment.

### D) Secrets (sensitive)
Repo → Settings → Secrets and variables → Actions → **Secrets** → New repository secret

Add:
- `AZURE_CLIENT_ID` (Terraform output: `azure_client_id`)
- `AZURE_TENANT_ID` (Terraform output: `azure_tenant_id`)
- `AZURE_SUBSCRIPTION_ID` (Terraform output: `azure_subscription_id`)

---

## 2) Release flow (what students do)
1) Work in feature branches → PR → merge to `main`
2) Go to GitHub → Releases → Draft a new release
3) Create tag (example `v3.0.1`) and publish the release
4) Workflow runs:
   - Build & push: `<acrLoginServer>/flask-app:v3.0.1`
   - Deploy ACI: `http://<aci-fqdn>:5000/`
   - Deploy ACA: `https://<aca-fqdn>/`  (ACA forwards ingress to container port 5000)

---

## 3) Manual runs for dev/stage
You can also run the workflow manually:
Actions → “Release CI/CD - Build to ACR, Deploy ACI then ACA” → Run workflow → choose `dev` or `stage`.

---

## 4) Troubleshooting
- ACI fails to pull image:
  - verify `RUNTIME_PULL_IDENTITY_ID` is correct
  - verify identity has `AcrPull` on the ACR
- ACR push fails:
  - verify service principal has `AcrPush` on the ACR
  - verify OIDC federated credential matches repo/environment
- ACI/ACA up but no response:
  - ensure app binds to 0.0.0.0 and listens on port 5000
