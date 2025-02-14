from deployment_steps import DeploymentStep

class FetchCodeStep(DeploymentStep):
    def execute(self, app=None, target=None):
        print(f"[Stub] Fetching latest code...")

FetchCodeStep.register("fetch")
