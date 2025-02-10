# **Implementation Roadmap**

## **Phase 1: GitHub Integration** ✅ Completed
- **GitHubRepositoryManager** implemented.
- `fetch_latest_commit()` integrated with `DeploymentOrchestrator`.
- **Command-line execution now supports dynamic repository selection.**
  ```powershell
  python src/main.py --steps fetch --repo-owner vzlatsin --repo-name deployment-automation
  ```

## **Phase 2: Azure DevOps Integration** 🔄 In Progress
### **Objective:**
- Implement `AzureDevOpsManager.compare_with_azure()`.
- Fetch commit from Azure DevOps and compare it with GitHub.

### **Tasks:**
✅ Define `compare_with_azure()` method in `AzureDevOpsManager`.  
✅ Identify necessary API calls for Azure DevOps integration.  
🔄 Implement commit comparison logic.  
🔄 Write unit tests for Azure DevOps comparison.  

## **Phase 3: Deployment Automation** 🔜 Not Started
### **Objective:**
- Automate packaging, artifact storage, and deployment.

### **Tasks:**
🟡 Implement `AppPackager` to bundle deployment artifacts.  
🟡 Implement `JFrogUploader` to upload artifacts to Artifactory.  
🟡 Implement `RemoteDeployer` to deploy packages via SSH.  

## **Phase 4: Logging & Monitoring** 🔜 Not Started
### **Objective:**
- Implement logging and monitoring for all components.

### **Tasks:**
🟡 Enhance `DeploymentLogger` with structured logging.  
🟡 Implement failure tracking and automated retries.  

---
**Next Steps:**
- Proceed with `compare_with_azure()` implementation.
- Finalize API integration for Azure DevOps.
- Update documentation as development progresses.

_Last updated: 2025-02-11_
