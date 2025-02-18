import json
import os
from deployment_steps import STEP_REGISTRY, load_steps
from deployment_logger import DeploymentLogger

class DeploymentOrchestrator:
    def __init__(self, logger):
        self.logger = logger
        self.step_config = self.load_step_config()
        self.step_parameters = self.load_step_parameters()
        load_steps(logger)

    def load_step_config(self):
        """Loads step-to-class mapping from `config/steps_config.json`."""
        project_root = os.path.abspath(os.path.dirname(__file__))  # Fix the path to avoid `src/config`
        config_path = os.path.join(project_root, "..", "config", "steps_config.json")

        if not os.path.exists(config_path):
            self.logger.log_error(f"❌ Configuration file {config_path} not found.")
            return {}

        self.logger.log_info(f"✅ Loading step configurations from {config_path}")

        with open(config_path, "r") as f:
            return json.load(f)

    def load_step_parameters(self):
        """Loads step-specific parameters from `config/step_parameters.json`."""
        project_root = os.path.abspath(os.path.dirname(__file__))  # Fix the path
        parameters_path = os.path.join(project_root, "..", "config", "step_parameters.json")

        if not os.path.exists(parameters_path):
            self.logger.log_error(f"❌ Step parameters file {parameters_path} not found.")
            return {}

        self.logger.log_info(f"✅ Loading step parameters from {parameters_path}")

        with open(parameters_path, "r") as f:
            return json.load(f)

    def execute_steps(self, steps, app=None):
        executed_steps = []
        self.logger.log_info(f"🚀 Executing deployment steps: {steps}")

        for step in steps:
            if step in STEP_REGISTRY:
                step_instance = STEP_REGISTRY[step](self.logger)

                # Load step parameters dynamically
                step_params = self.step_parameters.get(step, {})

                # Debug log to check step parameters
                self.logger.log_debug(f"🔹 Parameters for {step}: {step_params}")

                formatted_params = {key: value.format(app=app) if isinstance(value, str) else value
                                    for key, value in step_params.items()}

                # Execute step with dynamically loaded parameters
                self.logger.log_info(f"🟢 Running step: {step} -> {step_instance.__class__.__name__}")
                step_instance.execute(app, **formatted_params)

                executed_steps.append(step)

        self.logger.log_info(f"✅ Steps executed: {executed_steps}")
        return executed_steps
