# Deployment Automation System - Design Document

## 1. Overview
This document outlines the design for the **Deployment Automation System**, which automates the deployment of software applications across different environments. The system supports both **manual execution (work laptop)** and **Azure DevOps pipeline integration** while ensuring modularity, testability, and maintainability.

## 2. Expected System Behavior
- The system must allow **selective execution of deployment steps** rather than enforcing a rigid workflow.
- The system must support **manual execution from a work laptop** and **automated execution via Azure DevOps pipelines**.
- Each deployment step should be **independently executable** while allowing for a **full deployment workflow**.
- The system must provide **logging and error handling** to ensure traceability and debugging capabilities.
- The system should be **extensible**, allowing future integration with additional CI/CD tools.
- The **Azure DevOps pipeline will first clone the deployment automation repository** before executing deployment steps.
- All deployment steps will be executed using `deploy.py`, which is responsible for managing the workflow.

## 3. Deployment Workflow
The deployment system is responsible for:
1. **Cloning the deployment automation repository** from Azure DevOps.
2. **Fetching the latest source code from GitHub or Azure DevOps.**
3. **Comparing changes** between GitHub and Azure DevOps repositories.
4. **Pushing updates** to Azure DevOps repository.
5. **Packaging the application** for deployment.
6. **Uploading the package** to JFrog Artifactory **with built-in retry logic**.
7. **Deploying the application** to the target production environment (`ldctlm01`).
8. **Logging failures, retries, and successful deployments**.

Each step is executed within Azure DevOps, triggering `deploy.py` for each stage.

### **3.1 Repository Cloning in Azure DevOps**
Before executing deployment steps, the **Azure DevOps pipeline will clone the deployment automation repository**, ensuring that `deploy.py` is available.

#### **Pipeline Steps**
1. **Checkout test1 repository (default behavior).**  
2. **Clone deployment automation repository.**  
3. **Run `deploy.py` with specific steps.**  

#### **Pipeline Configuration**
To clone the deployment automation repository, the pipeline will use:
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

### **3.2 Command-Line Execution in Azure DevOps**
Each stage in the pipeline will invoke `deploy.py` with the relevant step:
```yaml
- script: |
    python deployment-automation/src/deploy.py --steps fetch --app ${{ parameters.app }}
  displayName: "Fetch Latest Code"

- script: |
    python deployment-automation/src/deploy.py --steps compare --app ${{ parameters.app }}
  displayName: "Compare Versions"
```

## 4. System Architecture (Object Design)
The system follows **object-oriented design best practices**, ensuring modularity, extensibility, and testability.

### **4.1 Key Design Principles**
- **Single Responsibility Principle (SRP)**: Each class has **only one responsibility**.
- **Dependency Injection**: Objects **receive dependencies instead of creating them internally**.
- **Separation of Concerns**: Each deployment step is managed separately.
- **Composition Over Inheritance**: Objects **collaborate via composition rather than deep inheritance**.
- **Open-Closed Principle**: The system **can be extended without modifying existing classes**.

### **4.2 Class Overview**
| **Class Name**              | **Responsibility** |
|----------------------------|-------------------|
| `DeploymentOrchestrator`   | Calls `deploy.py` for executing deployment steps. |
| `GitHubRepositoryManager`  | Fetches the latest code from GitHub and compares with Azure DevOps. |
| `AzureDevOpsManager`       | Fetches the latest commit from Azure DevOps and syncs repositories. |
| `AppPackager`              | Packages the application for deployment. |
| `JFrogUploader`            | Uploads the package to JFrog Artifactory with retry logic. |
| `RemoteDeployer`           | Deploys the application to `ldctlm01` via SSH. |
| `DeploymentLogger`         | Handles structured logging for all components. |

### **4.3 Class Interactions**
1. **Azure DevOps triggers `deploy.py`** for each stage.
2. `DeploymentOrchestrator` **calls** the appropriate deployment step.
3. `GitHubRepositoryManager` **fetches and compares repositories**.
4. `AzureDevOpsManager` **syncs repositories**.
5. `AppPackager` **prepares the deployment package**.
6. `JFrogUploader` **uploads the artifact with retry logic**.
7. `RemoteDeployer` **deploys the package to production**.

## **Appendix A: System Dependencies**
- **GitHub API**: Used to fetch the latest commit hash and download repositories.
- **Azure DevOps API**: Used to push changes and trigger pipelines.
- **JFrog Artifactory**: Stores packaged deployment artifacts.
- **SSH (ldctlm01)**: Used for remote deployment to production.

## **Appendix B: How TDD Will Shape the System Design**

### **B.1 Overview**
Test-Driven Development (TDD) will be a guiding principle in shaping the architecture of the Deployment Automation System. By writing tests before implementing functionality, we will ensure that:
- Each component has a **clear and testable responsibility**.
- The design evolves **incrementally**, avoiding overengineering.
- Dependencies are **mocked and injected**, reducing tight coupling.

### **B.2 Validating System Metadata**
To prevent architectural inconsistencies, a **Metadata Validation Test** will be introduced at the **design stage**. This test will:
- Ensure all required classes exist.
- Validate constructor parameters and dependencies.
- Verify correct dependency injection.

### **B.3 Evolution of System Architecture Through TDD**
Each test failure will guide refinements in system design:
| **Test Case** | **Impact on System Design** |
|--------------|--------------------------|
| Missing GitHub repo raises `ValueError` | Leads to explicit validation in `GitHubRepositoryManager`. |
| JFrog upload failure retries automatically | Leads to retry logic in `JFrogUploader`. |
| SSH connection failure logs error | Leads to logging improvements in `RemoteDeployer`. |
| Constructor signature mismatch | Ensures **all required dependencies are present** and correctly injected. |

By following this methodology, we ensure that **our system evolves in a testable, maintainable, and modular way while catching errors early in the design phase**.

