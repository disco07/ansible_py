from mla import run_remote_cmd
import logging
from modules.base import BaseModule


class AptModule(BaseModule):
    name: str = "apt"

    def process(self, ssh_client):
        state = self.params.get("state")
        package_name = self.params.get("name")

        if state == "present":
            self.install_package(ssh_client, package_name)
        elif state == "absent":
            self.remove_package(ssh_client, package_name)
        else:
            logging.critical(f"Unsupported action for apt module: {state}")

    def install_package(self, ssh_client, package_name):
        command = f"sudo apt-get install -y {package_name}"
        result = run_remote_cmd(command, ssh_client)
        self.handle_command_result(result, package_name, ssh_client)

    def remove_package(self, ssh_client, package_name):
        command = f"sudo apt-get remove -y {package_name}"
        result = run_remote_cmd(command, ssh_client)
        logging.info(f"processing {result.stdout} tasks on hosts: {ssh_client.host}")
        self.handle_command_result(result, package_name, ssh_client)

    @staticmethod
    def handle_command_result(result, package_name, ssh_client):
        if result.exit_code == 0:
            logging.info(f"host={ssh_client.host} op=apt name={package_name} status=CHANGED")
        else:
            logging.error(f"Error: {result.stderr}")
