# **Implementation Roadmap**

## **Overview**
This document outlines the step-by-step implementation plan for the **Deployment Automation System**, ensuring alignment with the new Azure DevOps-based execution model. The roadmap ensures that development follows a structured approach, integrating testing and automation at each stage.

---

## **1. Initial Setup: Azure DevOps Pipeline and Repository Cloning**
### **Goal:** Ensure that the deployment automation app (`deploy.py`) is available inside the pipeline.

✅ **Step 1.1: Configure Azure DevOps Pipeline to Clone Deployment Repo**
- Modify the `test1` repo pipeline to **clone the deployment automation repository**.
- Ensure `deploy.py` is accessible from the pipeline execution.
- Validate that the repo cloning works before proceeding.

**Pipeline Configuration Update:**
```yaml
stages:
  - stage: FetchDeploymentRepo
    jobs:
      - job: CheckoutDeploymentAutomation
        steps:
          - checkout: self  # Checkout test1 repo (default)
          
          - script: |
              echo "[INFO] Cloning deployment automation repo..."
              git clone https://dev.azure.com/YOUR_ORG/YOUR_PROJECT/_git/deployment-automation deployment-automation
            displayName: "Clone Deployment Automation Repo"
```

✅ **Step 1.2: Modify Pipeline to Call `deploy.py` for Each Step**
- Update the pipeline to **call `deploy.py` instead of using echo commands.**
- Validate that `deploy.py` is receiving arguments correctly.

**Pipeline Execution Example:**
```yaml
- script: |
    python deployment-automation/src/deploy.py --steps fetch --app ${{ parameters.app }}
  displayName: "Fetch Latest Code"
```

✅ **Step 1.3: Verify Pipeline Execution Logs**
- Run the pipeline manually and confirm that logs show `deploy.py` execution.

---

## **2. Implement Deployment Steps in `deploy.py`**
### **Goal:** Ensure `deploy.py` correctly executes deployment steps in response to pipeline triggers.

✅ **Step 2.1: Implement Stub Methods for Deployment Steps**
- Modify `deploy.py` to **call stub functions** for each step.
- Add structured logging to capture execution.

✅ **Step 2.2: Implement Fetch Code Logic**
- Implement logic inside `deploy.py` to fetch code from GitHub or Azure DevOps.
- Ensure error handling for API failures, missing repositories.

✅ **Step 2.3: Implement Compare Versions Step**
- Implement version comparison between GitHub and Azure DevOps.
- Ensure logs capture differences between repositories.

✅ **Step 2.4: Implement Package Application Step**
- Modify `deploy.py` to package the application for deployment.
- Add validation for package structure.

✅ **Step 2.5: Implement Upload to JFrog Step**
- Ensure `deploy.py` interacts with JFrog Artifactory.
- Implement retry logic in case of upload failures.

✅ **Step 2.6: Implement Deployment Step to `ldctlm01`**
- Use SSH to deploy the application.
- Log execution results.

✅ **Step 2.7: Implement Cleanup Step**
- Ensure temporary files are deleted after execution.

---

## **3. Testing Strategy**
### **Goal:** Ensure test coverage for all implemented components.

✅ **Step 3.1: Unit Testing**
- Test `GitHubRepositoryManager` for commit fetching and API handling.
- Test `AzureDevOpsManager` for commit comparison and syncing.
- Test `JFrogUploader` for upload handling and retry logic.
- Test `RemoteDeployer` for SSH execution handling.

✅ **Step 3.2: Integration Testing**
- Validate that `deploy.py` executes correctly in a real pipeline run.
- Simulate API failures and verify system responses.
- Ensure logging captures failures and retries.

✅ **Step 3.3: CI/CD Integration**
- Run tests automatically in Azure DevOps on pull requests.
- Ensure deployment is blocked if any critical test fails.

---

## **4. Next Steps**
- **Ensure full integration with Azure DevOps.**
- **Monitor pipeline execution logs for potential failures.**
- **Expand error handling and retry logic for all deployment steps.**

---

_Last updated: 2025-02-15_

