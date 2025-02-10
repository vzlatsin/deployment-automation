import sys
import os
import requests
import zipfile  
import io
from deployment_logger import DeploymentLogger  # Import the logger

# Add `src/` to Python's module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

class GitHubRepositoryManager:
    """
    Manages interactions with a GitHub repository.
    """

    def __init__(self, repo_owner, repo_name, logger: DeploymentLogger, access_token=None):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.access_token = access_token  # ✅ Fix: Ensure access_token is a parameter
        self.logger = logger
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
        self.class_name = self.__class__.__name__


    def fetch_latest_commit(self):
        """
        Fetches the latest commit hash from GitHub using the REST API.
        """
        try:
            self.logger.log_info(f"[{self.class_name}] Fetching latest commit for {self.repo_owner}/{self.repo_name}")
            
            # Make an API request to get the latest commits
            response = requests.get(self.api_url, timeout=10)
            
            # Check if the response is successful (HTTP 200 OK)
            if response.status_code != 200:
                raise Exception(f"GitHub API error: {response.status_code} - {response.text}")
            
            # Extract the latest commit hash
            latest_commit = response.json()[0]["sha"]
            self.logger.log_info(f"[{self.class_name}] Latest commit: {latest_commit}")
            return latest_commit
        
        except requests.exceptions.RequestException as e:
            self.logger.log_error(f"[{self.class_name}] Network error while fetching commit: {str(e)}")
            raise Exception("Network error while fetching commit")
        
        except Exception as e:
            self.logger.log_error(f"[{self.class_name}] Unexpected error: {str(e)}")
            raise

    def download_repository(self, target_directory):
        """
        Downloads the GitHub repository as a ZIP archive and saves it in the target directory.
        
        Steps:
        1. Constructs the download URL for the ZIP archive.
        2. Sends an HTTP request to fetch the ZIP file.
        3. Checks for any errors in the response.
        4. Saves and extracts the ZIP file to the specified directory.
        5. Logs the progress and handles errors if they occur.
        
        :param target_directory: The directory where the repository should be saved and extracted.
        """
        zip_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/zipball/main"
        headers = {"Authorization": f"token {self.access_token}"} if self.access_token else {}
        
        try:
            self.logger.log_info(f"Downloading repository: {self.repo_owner}/{self.repo_name} from {zip_url}")
            response = requests.get(zip_url, headers=headers, stream=True)
            
            # Check if the request was successful (HTTP 200 OK)
            if response.status_code != 200:
                self.logger.log_error(f"Failed to download repository: {response.status_code} {response.text}")
                raise Exception(f"Failed to download repository: {response.status_code}")
            
            # Save the ZIP file in memory and extract it
            self.logger.log_info("Extracting repository ZIP file...")
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                zip_ref.extractall(target_directory)
            
            self.logger.log_info(f"Repository extracted to {target_directory}")
        
        except requests.RequestException as e:
            self.logger.log_error(f"Network error during repository download: {e}")
            raise Exception(f"Network error during repository download: {e}")
        except zipfile.BadZipFile as e:
            self.logger.log_error(f"Invalid ZIP file received: {e}")
            raise Exception(f"Invalid ZIP file received: {e}")

