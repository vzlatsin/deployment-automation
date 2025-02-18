import os
from deployment_steps import DeploymentStep

class DeployToTargetStep(DeploymentStep):
    """Deploys an application package to a remote target using Azure DevOps SSH endpoint."""

    def __init__(self, logger):
        super().__init__(logger)

    def execute(self, app=None, **kwargs):
        """Executes remote deployment using parameters from `step_parameters.json`."""

        target = kwargs.get("target")  # Retrieve target dynamically
        local_package_path = kwargs.get("local_package_path")
        remote_package_path = kwargs.get("remote_package_path")

        # Validate required parameters
        if not target:
            self.logger.log_error("❌ Deployment target is missing in configuration.")
            return
        if not local_package_path or not remote_package_path:
            self.logger.log_error(f"❌ Missing required deployment parameters for {app}.")
            return

        self.logger.log_info(f"🚀 Deploying {app} to {target}...")

        # Run deployment command via Azure DevOps SSH step
        deployment_command = f"scp {local_package_path} {target}:{remote_package_path}"
        self.logger.log_info(f"Executing: {deployment_command}")

        exit_code = os.system(deployment_command)  # Execute the deployment
        if exit_code != 0:
            self.logger.log_error(f"❌ Deployment failed with exit code {exit_code}")
            return

        self.logger.log_info(f"✅ Deployment step completed for {app} -> {target}")
