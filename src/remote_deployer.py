
class RemoteDeployer:
    def __init__(self, server_address, ssh_user, logger):
        """Initialize RemoteDeployer with a provided logger."""
        self.server_address = server_address
        self.ssh_user = ssh_user
        self.logger = logger  # ✅ Always require a logger

    def deploy_to_server(self, package_path):
        """Simulates remote deployment with SSH."""
        try:
            self.logger.info(f"🚀 Deploying {package_path} to {self.server_address} using SSH")
            raise Exception("SSH Connection Failed")  # Simulating failure
        except Exception as e:
            self.logger.error(f"❌ Deployment failed: {e}")  # ✅ Log the error before raising
            raise  # ✅ Re-raise exception
