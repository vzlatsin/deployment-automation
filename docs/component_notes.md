# **Component-Level Implementation Notes**

## **Overview**
This document provides a breakdown of each major component, its responsibilities, dependencies, and implementation details. **Implementation is now in progress, with `GitHubRepositoryManager` fully implemented and the system redesigned to follow the Open-Closed Principle (OCP).**

---

## **1. GitHubRepositoryManager**
### **Status: ✅ Fully Implemented**

### **Responsibility:**
- Fetches the latest source code from GitHub.
- Downloads the GitHub repository as a ZIP file.
- Compares changes with Azure DevOps repositories.

### **Implemented Methods:**
- ✅ `fetch_latest_commit()` - Retrieves the latest commit hash.
  - Uses GitHub REST API to fetch the latest commit.
  - Handles API errors and network failures.
  - Integrated into `DeploymentOrchestrator`.
- ✅ `download_repository(target_directory)` - Downloads the GitHub repository as a ZIP file.
  - Fetches the latest repository snapshot.
  - Extracts the ZIP archive into a specified directory.
  - Handles API errors, network failures, and invalid ZIP files.

### **Dependencies:**
- ✅ `DeploymentOrchestrator` (fetch step integration)

### **Edge Cases:**
- GitHub API rate limit.
- Network connectivity issues.
- Invalid ZIP file handling.

### **Pipeline Execution:**
```yaml
- script: |
    python deployment-automation/src/deploy.py --steps fetch --app ${{ parameters.app }}
  displayName: "Fetch Latest Code"
```

---

## **2. AzureDevOpsManager**
### **Status: In Progress**

### **Responsibility:**
- Pushes updates from GitHub to Azure DevOps.
- Compares commits between GitHub and Azure DevOps.
- Triggers CI/CD pipelines if necessary.

### **Key Methods:**
- `authenticate()`: ✅ Implemented – Authenticates with Azure DevOps API.
- `fetch_repositories()`: ✅ Implemented – Retrieves all repositories from Azure DevOps.
- `get_latest_commit()`: ✅ Implemented – Fetches the latest commit from a specified repository.
- `compare_with_github()`: ⚠️ In Progress – Integrates with pipeline execution.
- `trigger_pipeline()`: ⚠️ Planned – Will execute as a dedicated pipeline stage.

### **Dependencies:**
- `GitHubRepositoryManager`

### **Edge Cases:**
- Authentication failures.
- Pipeline trigger failures.

### **Pipeline Execution:**
```yaml
- script: |
    python deployment-automation/src/deploy.py --steps compare --app ${{ parameters.app }}
  displayName: "Compare Versions"
```

---

## **3. Step Execution and Open-Closed Principle Implementation**
### **Status: Implemented**

### **Responsibility:**
- Allows deployment steps to be dynamically loaded and executed.
- Ensures **new steps can be added without modifying `deploy.py` or `DeploymentOrchestrator`**.

### **Key Design Elements:**
- **`STEP_REGISTRY` (Dynamic Step Loading)**: Steps are loaded dynamically based on `steps_config.json`, meaning **new steps can be registered without modifying existing code**.
- **Base Class (`DeploymentStep`)**: All steps inherit from `DeploymentStep` and register themselves, ensuring modularity.
- **Config-Based Execution (`steps_config.json`)**: Steps are configured externally, making the system extensible.

### **Example of Adding a New Step (`RollbackStep`)**
1. Create a new step file:
```python
from deployment_steps import DeploymentStep

class RollbackStep(DeploymentStep):
    def execute(self, app=None, target=None):
        print("[Stub] Rolling back deployment...")

RollbackStep.register("rollback")
```
2. Update `steps_config.json`:
```json
{
    "rollback": "RollbackStep"
}
```
✅ The new step is now available **without modifying any existing logic.**

---

## **4. JFrogUploader**
### **Status: Planned**

### **Responsibility:**
- Uploads deployment artifacts to JFrog Artifactory **with retry logic**.

### **Key Methods (Planned):**
- `upload_package(file_path, retry_count=3)` - Uploads package with retry mechanism.

### **Dependencies:**
- `AppPackager` (for packaging before upload).
- `DeploymentLogger` (for logging upload attempts and failures).

### **Edge Cases:**
- Network failures leading to retries.
- Authentication issues.

### **Pipeline Execution:**
```yaml
- script: |
    python deployment-automation/src/deploy.py --steps upload --app ${{ parameters.app }}
  displayName: "Upload to JFrog"
```

---

## **5. Next Steps**
✅ **Step 1: Implement Repository Cloning in Azure DevOps**  
✅ **Step 2: Modify `deploy.py` to correctly execute steps from the pipeline**  
✅ **Step 3: Implement `compare_with_github()` inside `AzureDevOpsManager`**  
✅ **Step 4: Expand unit and integration tests to validate pipeline execution**  

---

_Last updated: 2025-02-15_

