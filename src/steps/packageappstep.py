from deployment_steps import DeploymentStep

class PackageAppStep(DeploymentStep):
    def execute(self, app=None, target=None):
        print(f"[Stub] Packaging app...")

PackageAppStep.register("package")
