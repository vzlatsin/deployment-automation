import sys
import os
import requests
from deployment_logger import DeploymentLogger  # Import the logger

# Add `src/` to Python's module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

class GitHubRepositoryManager:
    """
    Manages interactions with a GitHub repository.
    """

    def __init__(self, repo_owner, repo_name, logger: DeploymentLogger):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.logger = logger  # Inject logger
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
        self.class_name = self.__class__.__name__  # Store class name dynamically

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
