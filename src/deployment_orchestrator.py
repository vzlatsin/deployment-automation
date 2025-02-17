from deployment_steps import STEP_REGISTRY
from deployment_logger import DeploymentLogger

class DeploymentOrchestrator:
    def __init__(self, logger):
        self.logger = logger

    def execute_steps(self, steps, app=None, target=None):
        """Executes deployment steps dynamically from config."""
        self.logger.log_info(f"🚀 Executing deployment steps: {steps}")

        for step in steps:
            if step in STEP_REGISTRY:
                step_instance = STEP_REGISTRY[step](self.logger)  # ✅ Pass logger to each step
                self.logger.log_info(f"🟢 Running step: {step} -> {step_instance.__class__.__name__}")
                step_instance.execute(app, target)
            else:
                self.logger.log_error(f"❌ Unknown step: {step}")

        self.logger.log_info(f"✅ Steps executed: {steps}")
