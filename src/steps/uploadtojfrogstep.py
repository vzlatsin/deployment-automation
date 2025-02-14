from deployment_steps import DeploymentStep

class UploadToJfrogStep(DeploymentStep):
    def execute(self, app=None, target=None):
        print(f"[Stub] Uploading app to JFrog...")

UploadToJfrogStep.register("upload")
