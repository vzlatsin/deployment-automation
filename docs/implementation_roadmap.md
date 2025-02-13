# **Testing Strategy Document**

## **Overview**
This document defines the testing strategy for ensuring the reliability and correctness of the deployment automation system.

## **1. Unit Testing Strategy**
Each core component will have dedicated unit tests covering:
- **Success cases** (expected behavior).
- **Failure handling** (e.g., network failures, authentication errors).
- **Edge cases** (unexpected inputs, timeouts, etc.).

### **Key Areas for Unit Testing:**
| Component | Test Cases |
|-----------|-----------|
| `GitHubRepositoryManager` | ✅ Verify commit fetching, API failure handling. ✅ Test `download_repository()` for valid and invalid ZIP files. ✅ Handle network failures during download. |
| `AzureDevOpsManager` | Validate repo syncing, pipeline trigger failures. ✅ Now tested via `test_azure_devops_integration.py`. |
| `JFrogUploader` | Ensure retry logic works, handle API authentication errors. |
| `RemoteDeployer` | Simulate SSH failures, invalid command handling. |
| `DeploymentLogger` | Ensure correct logging, handle missing log files. |

### **Updated Tests for `GitHubRepositoryManager`** ✅ Implemented
- **Unit tests verify:**
  - `fetch_latest_commit()` retrieves the correct commit hash.
  - Handles **GitHub API failures** (HTTP 500 errors).
  - Handles **Network failures** (timeouts, no internet connection).
  - ✅ `download_repository(target_directory)` handles:
    - **Successful downloads and extractions.**
    - **Invalid ZIP file handling.**
    - **GitHub API failures when downloading.**
- **Mocking `requests.get` and `zipfile.ZipFile.extractall` ensures controlled test behavior.**
- **Command to run tests:**
  ```powershell
  python -m unittest discover -s tests
  ```

## **2. Mocking Strategy**
To isolate components, **mock external dependencies**:
- ✅ **GitHub API** (`requests.get` mock for fetching commits and downloading ZIP files).
- **Azure DevOps API** ✅ Now tested using `test_azure_devops_integration.py` instead of mocks.
- **JFrog Artifactory API** (mock `requests.post` for uploads).
- **SSH Client (`paramiko.SSHClient()`)** (mock SSH connections for deployment testing).
- **Logging framework** (mock logs to validate error messages).

## **3. Integration Testing**
Integration tests validate interaction between components.

### **Integration Test Cases:**
| Test Case | Components Tested |
|-----------|------------------|
| ✅ Fetch latest commit | `GitHubRepositoryManager`, `DeploymentOrchestrator` |
| ✅ Download repository and verify ZIP extraction | `GitHubRepositoryManager` |
| ✅ Fetch Azure DevOps Repositories | `AzureDevOpsManager` (using live API calls) |
| ✅ Fetch latest commit from Azure DevOps | AzureDevOpsManager.get_latest_commit() |
| ✅ Compare local repo with Azure DevOps | `AzureDevOpsManager.compare_with_azure()` |
| End-to-end deployment | `GitHubRepositoryManager`, `AzureDevOpsManager`, `JFrogUploader`, `RemoteDeployer` |
| Upload retry validation | `JFrogUploader`, `DeploymentLogger` |
| Deployment SSH error handling | `RemoteDeployer`, `DeploymentLogger` |

## **4. Expected Debug Output Samples**
Example of a **successful upload with retry**:
```powershell
[DEBUG] Attempt 1 of 3
[DEBUG] Upload failed, retrying...
[DEBUG] Attempt 2 of 3
[DEBUG] Upload successful!
```

Example of a **successful repository download**:
```powershell
[INFO] Downloading repository: vzlatsin/deployment-automation from https://api.github.com/repos/vzlatsin/deployment-automation/zipball/main
[INFO] Extracting repository ZIP file...
[INFO] Repository extracted to ./downloaded_repo
```

Example of an **SSH failure logged**:
```powershell
[ERROR] SSH Connection Failed
[ERROR] Deployment aborted.
```

## **5. CI/CD Testing Strategy**
Tests will be **automatically executed** in Azure DevOps pipelines:
- ✅ **Run unit tests on PR merges.**
- ✅ **Run integration tests before deployment.**
- ✅ **Abort deployment if tests fail.**

---
**Next Steps:**
- Expand unit tests for `AzureDevOpsManager.compare_with_azure()`.
- Monitor CI/CD test results.

_Last updated: 2025-02-12_
