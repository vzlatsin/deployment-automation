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
    parser.add_argument("--app", type=str, help="Application name")
    parser.add_argument("--target", type=str, help="Deployment target")

    args = parser.parse_args()

    logger = DeploymentLogger()
    orchestrator = DeploymentOrchestrator(logger)

    executed_steps = orchestrator.execute_steps(args.steps, args.app, args.target)
    logger.log_info(f"Steps executed: {executed_steps}")

if __name__ == "__main__":
    main()
