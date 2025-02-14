from deployment_steps import DeploymentStep

class DeployToTargetStep(DeploymentStep):
    def execute(self, app=None, target=None):
        print(f"[Stub] Deploying app to target...")

DeployToTargetStep.register("deploy")
