from deployment_steps import STEP_REGISTRY, load_steps
from deployment_logger import DeploymentLogger

class DeploymentOrchestrator:
    def __init__(self, logger):
        self.logger = logger
        load_steps(logger)  

    def execute_steps(self, steps, app=None, target=None):
        executed_steps = []
        self.logger.log_info(f"🚀 Executing deployment steps: {steps}")
        

        for step in steps:
            if step in STEP_REGISTRY:
                step_instance = STEP_REGISTRY[step](self.logger)
                self.logger.log_info(f"🟢 Running step: {step} -> {step_instance.__class__.__name__}")
                step_instance.execute(app, target)
                executed_steps.append(step)

        self.logger.log_info(f"✅ Steps executed: {executed_steps}")
        return executed_steps  # ✅ Return executed steps explicitly

