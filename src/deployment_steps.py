import json
import os
import importlib

# Global registry for dynamically loaded steps
STEP_REGISTRY = {}

class DeploymentStep:
    """Base class for all deployment steps."""
    def execute(self, app=None, target=None):
        raise NotImplementedError("Each step must implement an execute method.")

    @classmethod
    def register(cls, name):
        """Registers a deployment step in the global registry."""
        STEP_REGISTRY[name] = cls

# Load steps from configuration file in `config/`
def load_steps():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(project_root, "config", "steps_config.json")

    if not os.path.exists(config_path):
        print(f"[ERROR] Configuration file {config_path} not found.")
        return

    with open(config_path, "r") as f:
        step_mapping = json.load(f)

    for step_name, class_name in step_mapping.items():
        try:
            # ✅ Use relative import for steps
            module = importlib.import_module(f"src.steps.{class_name.lower()}")
            step_class = getattr(module, class_name)
            STEP_REGISTRY[step_name] = step_class
        except Exception as e:
            print(f"[ERROR] Failed to load step '{step_name}': {str(e)}")

# Run the loader when the module is imported
load_steps()
