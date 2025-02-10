# src/deployment_orchestrator.py
import sys
import os

# Add `src/` to Python's module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from deployment_logger import DeploymentLogger  # Import the new logger

class DeploymentOrchestrator:
    """
    Manages execution of deployment steps.
    """

    def __init__(self, logger: DeploymentLogger):
        self.logger = logger  # Inject logger
        self.class_name = self.__class__.__name__  # Store class name dynamically

    def execute_steps(self, steps):
        """
        Simulates executing deployment steps.
        """
        self.logger.log_info(f"[{self.class_name}] Executing deployment steps: {steps}")
        return steps
