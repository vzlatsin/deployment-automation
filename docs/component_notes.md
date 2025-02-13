# **Component-Level Implementation Notes**

## **Overview**
This document provides a breakdown of each major component, its responsibilities, dependencies, and implementation details. **Implementation is now in progress, with `GitHubRepositoryManager` fully implemented. This document will be updated as more components are developed.**

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

### **Command-Line Execution:**
#### **Fetching Latest Commit**
```powershell
python src/main.py --steps fetch --repo-owner vzlatsin --repo-name deployment-automation
```

#### **Downloading a Repository from GitHub**
```powershell
python src/main.py --repo-owner vzlatsin --repo-name deployment-automation --download-repo --target-dir "./downloaded_repo"
```

---

### AzureDevOpsManager
- **Status**: In Progress (Implemented `get_latest_commit()`, authentication, and repository retrieval)


### **Responsibility:**
- Pushes updates from GitHub to Azure DevOps.
- Triggers CI/CD pipelines if necessary.

### **Key Methods (Planned):**

#### Key Methods (Implemented / Planned)
- `authenticate()`: ✅ Implemented – Authenticates with Azure DevOps API.
- `fetch_repositories()`: ✅ Implemented – Retrieves all repositories from Azure DevOps.
- `get_latest_commit()`: ✅ Implemented – Fetches the latest commit from a specified repository.
- `compare_with_github()`: ⚠️ Planned – Compare commits between Azure DevOps and GitHub.
- `trigger_pipeline()`: ⚠️ Planned – Start an Azure DevOps pipeline.


### **Dependencies:**
- `GitHubRepositoryManager`

### **Edge Cases:**
- Authentication failures.
- Pipeline trigger failures.

---

## **3. JFrogUploader**
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

---

## **4. RemoteDeployer**
### **Status: Planned**

### **Responsibility:**
- Deploys the package to `ldctlm01` using SSH.
- Logs SSH failures and prevents deployment if necessary.

### **Key Methods (Planned):**
- `deploy_package(target_host, package_path)` - Executes deployment over SSH.
- `_execute_ssh_command(command)` - Runs a remote command over SSH.

### **Dependencies:**
- `JFrogUploader` (ensures package is uploaded before deployment).

### **Edge Cases:**
- SSH authentication failure.
- Deployment script execution failure.

---

## **5. DeploymentLogger**
### **Status: Planned**

### **Responsibility:**
- Logs all operations, including failures and retries.

### **Key Methods (Planned):**
- `log_event(message, level="INFO")` - Logs a general event.
- `log_error(message)` - Logs an error message.

### **Dependencies:**
- **None**

### **Edge Cases:**
- Logging failures due to file permissions or missing log files.

---

### Next Steps
- Implement `compare_with_github()`.
- Extend test coverage for `AzureDevOpsManager`.
- Add error handling and retry logic for API calls.


---

_Last updated: 2025-02-11_
