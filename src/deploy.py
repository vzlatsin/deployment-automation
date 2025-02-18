import sys
import os

# Ensure Python can find `src/` as a package
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import argparse
from deployment_logger import DeploymentLogger
from deployment_orchestrator import DeploymentOrchestrator

def main():
    parser = argparse.ArgumentParser(description="Deployment Automation System")
    parser.add_argument("--steps", nargs="+", help="Specify deployment steps (e.g., fetch compare upload)")
    parser.add_argument("--app", type=str, required=True, help="Application name")

    args = parser.parse_args()

    logger = DeploymentLogger()
    orchestrator = DeploymentOrchestrator(logger)

    # Print parameters for debugging
    logger.log_info(f"🔍 Debug Parameters: app={args.app}")


    executed_steps = orchestrator.execute_steps(args.steps, args.app)

if __name__ == "__main__":
    main()
