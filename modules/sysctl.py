import logging

from mla import run_remote_cmd
from modules.base import BaseModule


class SysctlModule(BaseModule):
    name = "sysctl"

    def process(self, ssh_client):
        params = self.params.get("params", {})

        for key, value in params.items():
            # Modifier la valeur du paramètre sysctl
            command = f"sudo sysctl -w {key}={value}"
            result = run_remote_cmd(command, ssh_client)

            if result.exit_code == 0:
                logging.info(f"Sysctl parameter {key} set to {value}")
            else:
                logging.error(f"Failed to set sysctl parameter {key}. Error: {result.stderr}")

