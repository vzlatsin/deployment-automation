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

    args = parser.parse_args()

    available_steps = ["fetch", "compare", "push", "package", "upload", "deploy"]

    logger = DeploymentLogger()  # Instantiate Logger
    github_manager = GitHubRepositoryManager(args.repo_owner, args.repo_name, logger)  # Dynamic repo input
    orchestrator = DeploymentOrchestrator(logger, github_manager)

    if not args.steps:
        logger.log_warning(f"No steps specified. Available steps: {', '.join(available_steps)}")
        return

    executed_steps = orchestrator.execute_steps(args.steps)
    logger.log_info(f"Steps executed: {executed_steps}")

if __name__ == "__main__":
    main()
