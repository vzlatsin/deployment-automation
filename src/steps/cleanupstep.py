from deployment_steps import DeploymentStep

class CleanupStep(DeploymentStep):
    def __init__(self, logger):
        super().__init__(logger)  # ✅ Ensure logger is passed correctly

    def execute(self, app=None, target=None):
        print("[Stub] Cleaning up temporary files...")



