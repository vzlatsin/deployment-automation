import sys
import os
import argparse
from deployment_logger import DeploymentLogger
from github_manager import GitHubRepositoryManager
from deployment_orchestrator import DeploymentOrchestrator

# Ensure the correct module path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

def main():
    parser = argparse.ArgumentParser(description="Deployment Automation System")
    parser.add_argument("--steps", nargs="+", help="Specify which deployment steps to execute")
    parser.add_argument("--repo-owner", required=True, help="GitHub repository owner")
    parser.add_argument("--repo-name", required=True, help="GitHub repository name")
    parser.add_argument("--download-repo", action="store_true", help="Download the GitHub repository")
    parser.add_argument("--target-dir", help="Target directory to save the repository")

    args = parser.parse_args()

    logger = DeploymentLogger()  # Instantiate Logger
    github_manager = GitHubRepositoryManager(args.repo_owner, args.repo_name, logger)  # Dynamic repo input
    orchestrator = DeploymentOrchestrator(logger, github_manager)

    if args.download_repo:
        if not args.target_dir:
            logger.log_error("You must specify --target-dir to download the repository.")
            sys.exit(1)
        try:
            github_manager.download_repository(args.target_dir)
            logger.log_info(f"Repository {args.repo_name} downloaded successfully to {args.target_dir}")
        except Exception as e:
            logger.log_error(f"Failed to download repository: {str(e)}")
        return

    available_steps = ["fetch", "compare", "push", "package", "upload", "deploy"]

    if not args.steps:
        logger.log_warning(f"No steps specified. Available steps: {', '.join(available_steps)}")
        return

    executed_steps = orchestrator.execute_steps(args.steps)
    logger.log_info(f"Steps executed: {executed_steps}")

if __name__ == "__main__":
    main()
