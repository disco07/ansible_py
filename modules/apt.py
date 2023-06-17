from mla import run_remote_cmd
import logging
from modules.base import BaseModule


class AptModule(BaseModule):
    name: str = "apt"

    def process(self, ssh_client):
        action = self.params.get("action")
        package_name = self.params.get("name")

        if action == "install":
            self.install_package(ssh_client, package_name)
        elif action == "remove":
            self.remove_package(ssh_client, package_name)
        else:
            logging.error(f"Unsupported action for apt module: {action}")

    def install_package(self, ssh_client, package_name):
        command = f"apt-get install -y {package_name}"
        result = run_remote_cmd(command, ssh_client)
        self.handle_command_result(result, package_name, "installed")

    def remove_package(self, ssh_client, package_name):
        command = f"apt-get remove -y {package_name}"
        result = run_remote_cmd(command, ssh_client)
        self.handle_command_result(result, package_name, "removed")

    @staticmethod
    def handle_command_result(result, package_name, action):
        if result["exit_code"] == 0:
            logging.info(f"Package '{package_name}' successfully {action}.")
        else:
            logging.error(f"Failed to {action} package '{package_name}'.")
            logging.error(f"Error: {result['stderr']}")
