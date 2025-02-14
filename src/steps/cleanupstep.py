from deployment_steps import DeploymentStep

class CleanupStep(DeploymentStep):
    def execute(self, app=None, target=None):
        print("[Stub] Cleaning up temporary files...")

CleanupStep.register("cleanup")
