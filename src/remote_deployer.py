import paramiko
from deployment_logger import DeploymentLogger

class RemoteDeployer:
    """Handles deployment of packages to remote servers via SSH."""

    def __init__(self, server_address, ssh_user, ssh_key_path, logger):
        """Initialize RemoteDeployer with SSH credentials and logging."""
        if not server_address:
            raise ValueError("❌ Server address is required.")
        if not ssh_user:
            raise ValueError("❌ SSH user is required.")
        if not ssh_key_path:
            raise ValueError("❌ SSH key path is required.")
        if logger is None:
            raise ValueError("❌ Logger instance must be provided.")

        self.server_address = server_address
        self.ssh_user = ssh_user
        self.ssh_key_path = ssh_key_path
        self.logger = logger

        self.logger.log_info(f"✅ RemoteDeployer initialized for {server_address} as {ssh_user}.")

    def check_remote_directory(self, remote_path):
        """Checks if the remote directory exists and logs its contents."""

        self.logger.log_info(f"🔍 Checking remote directory: {remote_path} on {self.server_address}...")

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.server_address, username=self.ssh_user, key_filename=self.ssh_key_path)

            stdin, stdout, stderr = ssh.exec_command(f"if [ -d {remote_path} ]; then ls -l {remote_path}; else echo 'DIRECTORY_NOT_FOUND'; fi")
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()

            if error:
                self.logger.log_error(f"❌ Error accessing remote directory: {error}")
            elif "DIRECTORY_NOT_FOUND" in output:
                self.logger.log_error(f"❌ Remote directory does not exist: {remote_path}")
            else:
                self.logger.log_info(f"📂 Remote Directory Structure:\n{output}")

            ssh.close()

        except paramiko.AuthenticationException:
            self.logger.log_error("❌ SSH Authentication Failed. Check credentials.")
        except paramiko.SSHException as ssh_exception:
            self.logger.log_error(f"❌ SSH Connection Error: {ssh_exception}")
        except Exception as e:
            self.logger.log_error(f"❌ Unexpected Error: {e}")


    def deploy_to_server(self, local_package_path, remote_package_path):
        """Stub: Simulates SSH deployment with validation and logging."""

        # 🔹 Validate required parameters
        if not local_package_path:
            self.logger.log_error("❌ Local package path is missing.")
            return
        if not remote_package_path:
            self.logger.log_error("❌ Remote deployment path is missing.")
            return

        self.logger.log_info(f"🚀 [STUB] Starting deployment of {local_package_path} to {self.server_address}:{remote_package_path}")

        # ✅ New Step: Check remote directory before deployment
        self.check_remote_directory(remote_package_path)

        # 🔹 Simulated Steps:
        self.logger.log_info(f"🔹 [STUB] Establishing SSH connection to {self.server_address} as {self.ssh_user}...")
        # TODO: In real implementation, use `paramiko.SSHClient` to establish a connection.

        self.logger.log_info(f"🔹 [STUB] Verifying package integrity before transfer...")
        # TODO: Implement file checksum verification before sending.

        self.logger.log_info(f"🔹 [STUB] Uploading {local_package_path} to {remote_package_path}...")
        # TODO: Use SFTP to transfer the file.

        self.logger.log_info(f"🔹 [STUB] Verifying file transfer success on remote server...")
        # TODO: Perform a remote checksum validation.

        self.logger.log_info(f"✅ [STUB] Deployment step completed successfully.")
