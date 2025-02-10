# Deployment Automation System - Design Document

## 1. Overview
This document outlines the design for the **Deployment Automation System**, which automates the deployment of software applications across different environments. The system supports both **manual execution (work laptop)** and **Azure DevOps pipeline integration** while ensuring modularity, testability, and maintainability.

## 2. Expected System Behavior
- The system must allow **selective execution of deployment steps** rather than enforcing a rigid workflow.
- The system must support **manual execution from a work laptop** and **automated execution via Azure DevOps pipelines**.
- Each deployment step should be **independently executable** while allowing for a **full deployment workflow**.
- The system must provide **logging and error handling** to ensure traceability and debugging capabilities.
- The system should be **extensible**, allowing future integration with additional CI/CD tools.
- If any critical step fails, the system should **log the failure and halt execution**, preventing an incomplete deployment.

## 3. Deployment Workflow
The deployment system is responsible for:
- **Fetching the latest source code** from GitHub.
- **Downloading the GitHub repository** as a ZIP file.
- **Comparing changes** between GitHub and Azure DevOps repositories.
- **Pushing updates** to Azure DevOps repository.
- **Packaging the application** for deployment.
- **Uploading the package** to JFrog Artifactory **with built-in retry logic**.
- **Deploying the application** to the target production environment (`ldctlm01`).
- **Logging failures, retries, and successful deployments**.

Each step can be executed independently or as part of a full deployment pipeline.

### **3.1 Command-Line Execution Examples**
#### **Running `main.py` with No Arguments (Displays Available Steps)**
```powershell
PS C:\Users\Vadim\projects\deployment-automation> python .\src\main.py
No steps specified. Available steps: fetch, download-repo, compare, push, package, upload, deploy
```

#### **Downloading a Repository from GitHub**
```powershell
PS C:\Users\Vadim\projects\deployment-automation> python src/main.py --repo-owner vzlatsin --repo-name deployment-automation --download-repo --target-dir "./downloaded_repo"
Downloading repository: vzlatsin/deployment-automation from https://api.github.com/repos/vzlatsin/deployment-automation/zipball/main
Extracting repository ZIP file...
Repository extracted to ./downloaded_repo
Repository deployment-automation downloaded successfully to ./downloaded_repo
```

#### **Executing Specific Deployment Steps**
```powershell
PS C:\Users\Vadim\projects\deployment-automation> python .\src\main.py --steps fetch compare push
Executing step: fetch
Executing step: compare
Executing step: push
```

#### **Running Unit Tests**
To validate functionality, run:
```powershell
python -m unittest discover -s tests
```
Example output:
```powershell
PS C:\Users\Vadim\projects\deployment-automation> python -m unittest tests.test_jfrog_basics
[DEBUG] Attempt 1 of 3
[DEBUG] Simulating retry attempt 1
[DEBUG] Upload failed, retrying...
[DEBUG] Attempt 2 of 3
[DEBUG] Simulating retry attempt 2
[DEBUG] Upload failed, retrying...
[DEBUG] Attempt 3 of 3
[DEBUG] Upload Succeeded on Attempt 3
[DEBUG] Upload successful!
[DEBUG] Total Upload Attempts: 2
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
| `DeploymentOrchestrator`   | Manages overall deployment workflow, calling individual steps. |
| `GitHubRepositoryManager`  | Fetches the latest code from GitHub, downloads the repository as a ZIP file, compares with Azure DevOps. |
| `AzureDevOpsManager`       | Pushes updates to Azure DevOps, triggers pipelines (if applicable). |
| `AppPackager`              | Packages the application for deployment (ZIP/TAR). |
| `JFrogUploader`            | Uploads the package to JFrog Artifactory **with retry logic**. |
| `RemoteDeployer`           | Deploys the application to `ldctlm01` via SSH **and logs failures**. |
| `DeploymentLogger`         | Handles structured logging for all components. |

### **4.3 Class Interactions**
1. `DeploymentOrchestrator` **calls** `GitHubRepositoryManager` to fetch code.
2. `GitHubRepositoryManager` **downloads and compares repositories** before pushing to Azure DevOps.
3. `AzureDevOpsManager` **syncs repositories** and triggers pipelines if necessary.
4. `AppPackager` **prepares the deployment package**.
5. `JFrogUploader` **uploads the packaged artifact with automatic retry**.
6. `RemoteDeployer` **deploys the package** to the production environment **and logs SSH failures**.

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

This will serve as a **single-point validation test**, reducing the need to update multiple test files when adding or modifying components.

### **B.3 Evolution of System Architecture Through TDD**
Each test failure will guide refinements in system design:
| **Test Case** | **Impact on System Design** |
|--------------|--------------------------|
| Missing GitHub repo raises `ValueError` | Leads to explicit validation in `GitHubRepositoryManager`. |
| JFrog upload failure retries automatically | Leads to retry logic in `JFrogUploader`. |
| SSH connection failure logs error | Leads to logging improvements in `RemoteDeployer`. |
| Constructor signature mismatch | Ensures **all required dependencies are present** and correctly injected. |

By following this methodology, we ensure that **our system evolves in a testable, maintainable, and modular way while catching errors early in the design phase**.
