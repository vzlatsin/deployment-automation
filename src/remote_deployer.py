import logging

class RemoteDeployer:
    def __init__(self, server_address, ssh_user, logger=None):
        self.server_address = server_address
        self.ssh_user = ssh_user
        self.logger = logger or logging.getLogger(__name__)

    def deploy_to_server(self, package_path):
        """Simulates remote deployment with SSH."""
        try:
            raise Exception("SSH Connection Failed")
        except Exception as e:
            print(f"[DEBUG] Inside except block, logger={self.logger}")  # 🔍 Debug print
            if self.logger:
                print("[DEBUG] Logging error now!")  # 🔍 Confirm logger is used
                self.logger.error("SSH Connection Failed")  # ✅ Log the error **before raising**
                print("[DEBUG] Log command executed!")  # 🔍 Extra confirmation
            else:
                print("[DEBUG] Logger is None!")  # ❌ Logger was never assigned
            raise  # ✅ Raise the exception AFTER logging
