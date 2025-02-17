from deployment_steps import DeploymentStep

class FetchCodeStep(DeploymentStep):
    def __init__(self, logger):
        super().__init__(logger)  # ✅ Ensure logger is passed correctly

    def execute(self, app=None, target=None):
        self.logger.log_info("[Stub] Fetching latest code...")  # ✅ Uses shared logger


