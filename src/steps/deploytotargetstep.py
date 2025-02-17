from deployment_steps import DeploymentStep
from remote_deployer import RemoteDeployer

class DeployToTargetStep(DeploymentStep):
    """Deploys an application package to a remote target via SSH."""

    def __init__(self, logger):
        super().__init__(logger)

    def execute(self, app=None, target=None, ssh_user=None, ssh_key_path=None, local_package_path=None, remote_package_path=None):
        """Executes remote deployment with parameters from `step_parameters.json`."""

        # Validate required parameters
        if not target:
            self.logger.log_error("❌ Deployment target is missing.")
            return
        if not ssh_user or not ssh_key_path or not local_package_path or not remote_package_path:
            self.logger.log_error(f"❌ Missing required deployment parameters for {app}.")
            return

        self.logger.log_info(f"🚀 Deploying {app} to {target} as {ssh_user}...")

        # Initialize RemoteDeployer with dynamic parameters
        deployer = RemoteDeployer(
            server_address=target,
            ssh_user=ssh_user,
            ssh_key_path=ssh_key_path,
            logger=self.logger
        )

        # Execute deployment
        deployer.deploy_to_server(local_package_path, remote_package_path)

        self.logger.log_info(f"✅ Deployment step completed for {app} -> {target}")
