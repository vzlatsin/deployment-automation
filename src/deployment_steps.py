import json
import os
import importlib
from deployment_logger import DeploymentLogger

# Global registry for dynamically loaded steps
STEP_REGISTRY = {}

class DeploymentStep:
    """Base class for all deployment steps."""
    def __init__(self, logger):
        if logger is None:
            raise ValueError("Logger instance must be provided")  # Prevents missing logger
        self.logger = logger

    def execute(self, app=None, target=None):
        raise NotImplementedError("Each step must implement an execute method.")

    @classmethod
    def register(cls, name, logger):
        """Registers a deployment step in the global registry."""
        STEP_REGISTRY[name] = lambda logger=logger: cls(logger)  # ✅ Ensures correct logger!
        logger.log_debug(f"🔹 Step Registered: {name} -> {cls.__name__}")

# Load steps from configuration file in `config/`
def load_steps(logger):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(project_root, "config", "steps_config.json")

    if not os.path.exists(config_path):
        logger.log_error(f"❌ Configuration file {config_path} not found.")
        return

    with open(config_path, "r") as f:
        step_mapping = json.load(f)

    for step_name, class_name in step_mapping.items():
        try:
            module = importlib.import_module(f"src.steps.{class_name.lower()}")
            step_class = getattr(module, class_name)
            STEP_REGISTRY[step_name] = lambda logger=logger, step_class=step_class: step_class(logger)  # ✅ Ensures correct logger!

            logger.log_debug(f"✅ Step Loaded: {step_name} -> {class_name}")
        except Exception as e:
            logger.log_error(f"❌ Failed to load step '{step_name}': {str(e)}")

    logger.log_info(f"✅ Loaded steps: {list(STEP_REGISTRY.keys())}")


