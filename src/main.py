import sys
import os

# Add `src/` to Python's module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from deployment_logger import DeploymentLogger  # Import the new logger

import argparse
from deployment_orchestrator import DeploymentOrchestrator

def main():
    parser = argparse.ArgumentParser(description="Deployment Automation System")
    parser.add_argument("--steps", nargs="+", help="Specify which deployment steps to execute")
    
    args = parser.parse_args()

    available_steps = ["fetch", "compare", "push", "package", "upload", "deploy"]
    
    logger = DeploymentLogger()  # Instantiate Logger
    orchestrator = DeploymentOrchestrator(logger)

    if not args.steps:
        logger.log_warning(f"No steps specified. Available steps: {', '.join(available_steps)}")
        return

    executed_steps = orchestrator.execute_steps(args.steps)
    logger.log_info(f"Steps executed: {executed_steps}")

if __name__ == "__main__":
    main()
