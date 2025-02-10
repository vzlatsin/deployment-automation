# Deployment Automation System - Design Document

## 1. Overview
This document outlines the design for the **Deployment Automation System**, which automates the deployment of software applications across different environments, supporting both **manual execution (work laptop)** and **Azure DevOps pipeline integration**.

## 2. Expected System Behavior
- The system must allow **selective execution of deployment steps** rather than enforcing a rigid workflow.
- The system must support **manual execution from a work laptop** and **automated execution via Azure DevOps pipelines**.
- Each deployment step should be **independently executable** while allowing for a **full deployment workflow**.
- The system must provide **logging and error handling** to ensure traceability and debugging capabilities.
- The system should be **extensible**, allowing future integration with additional CI/CD tools.

## 3. Deployment Workflow
The deployment system is responsible for:
- **Fetching the latest source code** from GitHub.
- **Comparing changes** between GitHub and Azure DevOps repositories.
- **Pushing updates** to Azure DevOps repository.
- **Packaging the application** for deployment.
- **Uploading the package** to JFrog Artifactory.
- **Deploying the application** to the target production environment (ldctlm01).

Each step can be executed independently or as part of a full deployment pipeline.

## 4. System Architecture (Object Design)
The system follows **object-oriented design best practices**, ensuring modularity, extensibility, and testability.

### **4.1 Key Design Principles**
- **Single Responsibility Principle (SRP)**: Each class has **only one responsibility**.
- **Dependency Injection**: Objects **receive dependencies instead of creating them internally**.
- **Separation of Concerns**: Each deployment step is managed separately.
- **Composition Over Inheritance**: Objects **collaborate via composition rather than deep inheritance**.
- **Open-Closed Principle**: The system **can be extended without modifying existing classes**.

### **4.2 Class Overview**
| **Class Name**          | **Responsibility** |
|------------------------|-------------------|
| `DeploymentOrchestrator` | Manages overall deployment workflow, calling individual steps. |
| `GitHubRepositoryManager` | Fetches latest code from GitHub, compares with Azure DevOps. |
| `AzureDevOpsManager`   | Pushes updates to Azure DevOps, triggers pipelines (if applicable). |
| `AppPackager`          | Packages the application for deployment (ZIP/TAR). |
| `JFrogUploader`        | Uploads the package to JFrog Artifactory. |
| `RemoteDeployer`       | Deploys the application to `ldctlm01` via SSH. |

### **4.3 Class Interactions**
1. `DeploymentOrchestrator` **calls** `GitHubRepositoryManager` to fetch code.
2. `GitHubRepositoryManager` **compares repositories** before pushing to Azure DevOps.
3. `AzureDevOpsManager` **syncs repositories** and triggers pipelines if necessary.
4. `AppPackager` **prepares the deployment package**.
5. `JFrogUploader` **uploads the packaged artifact**.
6. `RemoteDeployer` **deploys the package** to the production environment.

## **Appendix A: Execution Flexibility & Modular Design**
- The deployment system is designed to be **flexible**, allowing individual steps to be executed separately.
- The system supports **manual execution** via command-line arguments and **automated execution** via Azure DevOps pipelines.

## **Appendix B: How TDD Will Shape the System Design**
### **B.1 Overview**
Test-Driven Development (TDD) will be a guiding principle in shaping the architecture of the Deployment Automation System. By writing tests before implementing functionality, we will ensure that:
- Each component has a **clear and testable responsibility**.
- The design evolves **incrementally**, avoiding overengineering.
- Dependencies are **mocked and injected**, reducing tight coupling.

### **B.2 Initial Test Cases to Drive Design**
| **Test Case** | **Expected Outcome** |
|--------------|----------------------|
| `test_fetch_latest_code()` | Ensures GitHub code is retrieved correctly. |
| `test_compare_github_azure_changes()` | Ensures GitHub and Azure DevOps repositories are in sync. |
| `test_push_to_azure_repo()` | Validates pushing new changes to Azure DevOps. |
| `test_package_application()` | Ensures the app is correctly packaged. |
| `test_upload_to_jfrog()` | Confirms the package is uploaded to JFrog. |
| `test_deploy_to_ldctlm01()` | Ensures deployment is correctly executed on `ldctlm01`. |

### **B.3 Evolution of System Architecture Through TDD**
Each test failure will guide refinements in system design:
| **Test Case** | **Impact on System Design** |
|--------------|--------------------------|
| Missing GitHub repo raises `ValueError` | Leads to explicit validation in `GitHubRepositoryManager`. |
| JFrog upload failure retries automatically | Leads to retry logic in `JFrogUploader`. |
| SSH connection failure logs error | Leads to logging improvements in `RemoteDeployer`. |

By following this methodology, we ensure that **our system evolves in a testable, maintainable, and modular way while catching errors early in the design phase**.

