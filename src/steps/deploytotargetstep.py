from deployment_steps import DeploymentStep
from remote_deployer import RemoteDeployer

class DeployToTargetStep(DeploymentStep):
    def __init__(self, logger):
        """Initialize with a logger to maintain consistency."""
        self.logger = logger

    def execute(self, app=None, target=None):
        """Simulates deployment execution (currently stub with diagnostics)."""
        self.logger.info(f"🟢 [Stub] Deploying {app} to {target}...")

        # Create RemoteDeployer instance with the same logger
        deployer = RemoteDeployer(target, "deploy_user", self.logger)

        # Simulate deployment
        try:
            deployer.deploy_to_server("job_tracking_system.tar.gz")
            self.logger.info(f"✅ [Stub] Deployment step complete for {app} -> {target}")
        except Exception as e:
            self.logger.error(f"❌ Deployment error: {e}")
