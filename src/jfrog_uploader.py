class JFrogUploader:
    def __init__(self, repo_url, logger=None):
        """Initialize JFrogUploader with repo URL and optional logger."""
        self.repo_url = repo_url
        self.logger = logger

    def upload_package(self, package_path, retry_count=3):
        """Uploads a package to JFrog with retries."""
        attempts = 0
        while attempts < retry_count:
            attempts += 1
            if self.logger:
                self.logger.info(f"Attempt {attempts} of {retry_count} to upload {package_path}")
            print(f"[DEBUG] Attempt {attempts} of {retry_count}")  # 🔍 Print attempt count
            success = self._attempt_upload(package_path)
            if success:
                print("[DEBUG] Upload successful!")  # 🔍 Confirm success
                return True
            print("[DEBUG] Upload failed, retrying...")  # 🔍 Retry message
        print("[DEBUG] Upload failed after retries.")  # 🔍 If all retries fail
        return False  # Fail after retries
