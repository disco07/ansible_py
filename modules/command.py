import logging
from paramiko import SSHClient

from mla import run_remote_cmd
from modules.base import BaseModule


class CommandModule(BaseModule):
    name = "command"

    def process(self, ssh_client: SSHClient):
        commands = self.params.get("command", "")
        for command in commands.split('\n'):
            result = run_remote_cmd(command, ssh_client, self.params.get("config"))

            if result.exit_code == 0:
                logging.info(f"Command executed successfully on host.")
            else:
                logging.error(f"Error executing command on host.")
                logging.error(f"Exit code: {result.exit_code}")
                logging.error(f"Standard output: {result.stdout}")
                logging.error(f"Error output: {result.stderr}")
