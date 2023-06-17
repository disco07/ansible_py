class BaseModule:
    name: str = "anonymous"

    def __init__(self, params: dict):
        self.params = params

    def process(self, ssh_client):
        """Apply the action to `ssh_client` using `params`."""
        pass
