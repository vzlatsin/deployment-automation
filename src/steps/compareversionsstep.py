from deployment_steps import DeploymentStep

class CompareVersionsStep(DeploymentStep):
    def execute(self, app=None, target=None):
        print("[Stub] Comparing versions...")

CompareVersionsStep.register("compare")
