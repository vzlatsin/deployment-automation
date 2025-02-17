import json
import os
import importlib
from deployment_logger import DeploymentLogger

# Global registry for dynamically loaded steps
STEP_REGISTRY = {}
logger = DeploymentLogger()  # Use the logger globally

class DeploymentStep:
    """Base class for all deployment steps."""
    def __init__(self, logger):
        self.logger = logger  # ✅ Ensure each step gets a logger

    def execute(self, app=None, target=None):
        raise NotImplementedError("Each step must implement an execute method.")

    @classmethod
    def register(cls, name):
        """Registers a deployment step in the global registry."""
        STEP_REGISTRY[name] = cls
        logger.log_debug(f"🔹 Step Registered: {name} -> {cls.__name__}")

# Load steps from configuration file in `config/`
def load_steps():
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
            STEP_REGISTRY[step_name] = step_class
            logger.log_debug(f"✅ Step Loaded: {step_name} -> {class_name}")
        except Exception as e:
            logger.log_error(f"❌ Failed to load step '{step_name}': {str(e)}")

# Run the loader when the module is imported
load_steps()
