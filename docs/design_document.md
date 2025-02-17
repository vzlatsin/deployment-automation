# **Deployment Automation System - Design Document**

## **1. Introduction**
This document outlines the design and architecture of the Deployment Automation System, ensuring modularity, scalability, and maintainability. The system follows **Test-Driven Development (TDD)** and **Object-Oriented Design Principles (OCP, SRP)**.

---

## **2. System Overview**
The Deployment Automation System automates application deployment across different environments using a modular step-based architecture. Each deployment step is registered dynamically and executed as required.

### **2.1 Key Components**
| **Component**         | **Description** |
|----------------------|----------------|
| `DeploymentOrchestrator` | Manages the execution of deployment steps, ensuring dynamic registration. |
| `DeploymentStep` | Base class for all deployment steps. |
| `GitHubRepositoryManager` | Manages interactions with GitHub for version control. |
| `AzureDevOpsManager` | Integrates with Azure DevOps to track changes and trigger deployments. |
| `JFrogUploader` | **[STATUS: Planned]** Uploads the package to JFrog Artifactory with retry logic. |
| `RemoteDeployer` | Deploys the application to `ldctlm01` via SSH. |
| `DeploymentLogger` | Handles structured logging (`log_info()`, `log_error()`, `log_debug()`). |

---

## **3. Deployment Process & Step Execution**
The system follows a dynamic, step-based execution model:
1. **Step Registration**: Deployment steps are automatically discovered and registered in `STEP_REGISTRY`.
2. **Execution**: The orchestrator calls `execute_steps()` based on user input or pipeline configuration.
3. **Logging & Error Handling**: Logs execution progress and captures failures.

### **3.1 Deployment Command Execution**
🔹 **Pipeline & CLI Execution Syntax (Updated)**:
```sh
python -m src.deploy --steps fetch package upload deploy --app MyApp --target test-server
```

🔹 **Example Usage in Azure DevOps Pipeline**:
```yaml
- script: |
    python -m src.deploy --steps fetch --app MyApp --target test-server
  displayName: "Fetch Code from Repository"
```
✅ **Fixed incorrect usage of `src\deploy` → Corrected to `python -m src.deploy`**

---

## **4. System Architecture (Object Design)**

### **4.1 Deployment Orchestrator**
The **DeploymentOrchestrator** manages all deployment steps dynamically.

🔹 **Key Responsibilities:**
- Loads available steps dynamically (`load_steps()`).
- Executes requested steps sequentially.
- Logs execution status for traceability.

### **4.2 Step Execution Flow**
Each deployment step follows a standard execution flow:
1. `STEP_REGISTRY[step]()` creates an instance of the requested step.
2. The step executes using the provided `logger`.
3. If a step fails, `log_error()` captures the failure and execution stops.

### **4.3 Remote Deployment via SSH (`RemoteDeployer`)**
The **`RemoteDeployer`** handles SSH-based deployment to `ldctlm01`.

#### **Current Implementation**
- **Deployment is logged** using `log_info()`.
- **Failures are captured** using `log_error()`.
- **Currently, SSH connection always fails (simulated for testing)**.

#### **Next Steps for Full SSH Support**
- Implement **real SSH file transfer using `paramiko` or SCP**.
- Introduce **automatic retries** for intermittent SSH failures.
- Improve **error handling (e.g., distinguish between authentication failures and network issues).**

---

## **5. Logging & Error Handling (Updated)**
### **5.1 Logging Standardization**
The system enforces structured logging:
- **Info Logs** → `log_info()`
- **Error Logs** → `log_error()`
- **Debugging Support** → `log_debug()`

This ensures consistent log formatting across all components, making debugging easier.

### **5.2 Error Handling**
- If a step encounters an error, it logs using `log_error()` and stops execution.
- Failures in SSH deployment (`RemoteDeployer`) **are captured and re-raised**.

---

## **6. Future Improvements**
| **Feature** | **Planned Enhancements** |
|------------|---------------------|
| **JFrogUploader** | Implement package upload logic with retries. |
| **RemoteDeployer** | Introduce real SSH deployment and retries. |
| **Retry Mechanism** | Implement automatic retry logic for failed deployments. |
| **Logging Enhancement** | Add timestamped structured logs for improved visibility. |

---

## **Appendix A: System Dependencies**
- **GitHub API**: Used to fetch the latest commit hash and download repositories.
- **Azure DevOps API**: Used to push changes and trigger pipelines.
- **JFrog Artifactory** (**Planned**) Stores packaged deployment artifacts.
- **SSH (ldctlm01)**: Used for remote deployment to production.
- **DeploymentLogger**: Handles structured logging (`log_info()`, `log_error()`, `log_debug()`).

---

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

### **B.3 Logging & SSH Deployment Validation in Tests**
Recent improvements require additional test coverage:
- **Logging Validation**: Ensure all logs use `log_info()`, `log_error()`, `log_debug()`.
- **SSH Deployment Handling**:
  - Verify that `RemoteDeployer` **logs SSH failures** correctly.
  - Ensure SSH retry logic is tested once implemented.

### **B.4 Evolution of System Architecture Through TDD**
Each test failure will guide refinements in system design:

| **Test Case** | **Impact on System Design** |
|--------------|--------------------------|
| Missing GitHub repo raises `ValueError` | Leads to explicit validation in `GitHubRepositoryManager`. |
| JFrog upload failure retries automatically | Leads to retry logic in `JFrogUploader`. |
| SSH connection failure logs error | Leads to logging improvements in `RemoteDeployer`. |
| Logging does not follow standard format | Ensures `log_info()`, `log_error()`, `log_debug()` are used consistently. |
| Constructor signature mismatch | Ensures **all required dependencies are present** and correctly injected. |

By following this methodology, we ensure that **our system evolves in a testable, maintainable, and modular way while catching errors early in the design phase**.

✅ **This document now reflects the latest system updates and improvements.** 🚀

