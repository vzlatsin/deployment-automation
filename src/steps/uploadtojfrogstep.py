from deployment_steps import DeploymentStep

class UploadToJfrogStep(DeploymentStep):

    def __init__(self, logger):
        super().__init__(logger)  # ✅ Ensure logger is passed correctly

    def execute(self, app=None, target=None):
        print(f"[Stub] Uploading app to JFrog...")

