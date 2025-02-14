from deployment_steps import STEP_REGISTRY
from deployment_logger import DeploymentLogger

class DeploymentOrchestrator:
    def __init__(self, logger):
        self.logger = logger

    def execute_steps(self, steps, app=None, target=None):
        """Executes deployment steps dynamically from config."""
        self.logger.log_info(f"Executing deployment steps: {steps}")

        for step in steps:
            if step in STEP_REGISTRY:
                step_instance = STEP_REGISTRY[step]()  # Find and execute the step
                step_instance.execute(app, target)
            else:
                self.logger.log_error(f"Unknown step: {step}")  # ✅ Use log_error() instead of log_warning()

        self.logger.log_info(f"Steps executed: {steps}")
        return steps
