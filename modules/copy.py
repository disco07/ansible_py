import logging
import os

from mla import run_remote_cmd
from .base import BaseModule

logger = logging.getLogger(__name__)


class CopyModule(BaseModule):
    name = "copy"

    def process(self, ssh_client):
        source = self.params.get("src")
        destination = self.params.get("dest")
        backup = self.params.get("backup", False)

        if source and destination:
            self.copy_files(ssh_client, source, destination, backup)
        else:
            logger.error("Source and destination paths are required for the copy module.")

    def copy_files(self, ssh_client, source, destination, backup):
        command = f"mkdir -p {destination}"
        result = run_remote_cmd(command, ssh_client)
        if result.exit_code != 0:
            logger.error(f"Failed to create destination directory '{destination}'.")
            logger.error(f"Error: {result.stderr}")
            return

        if os.path.isdir(source):
            self.copy_directory(ssh_client, source, destination, backup)
        else:
            self.copy_file(ssh_client, source, destination, backup)

    def copy_file(self, ssh_client, source, destination, backup):
        remote_path = os.path.join(destination, os.path.basename(source))
        if backup:
            self.backup_existing_file(ssh_client, remote_path)
        self.upload_file(ssh_client, source, remote_path)

    def copy_directory(self, ssh_client, source, destination, backup):
        for root, dirs, files in os.walk(source):
            relative_path = os.path.relpath(root, source)
            remote_path = os.path.join(destination, relative_path)
            remote_path = remote_path.replace("\.", "")
            self.create_remote_directory(ssh_client, remote_path)

            for file in files:
                local_file = os.path.join(root, file)
                local_file = local_file.replace("\\", "/")
                remote_file = os.path.join(remote_path, file)
                remote_file = remote_file.replace("\\", "/")
                if backup:
                    self.backup_existing_file(ssh_client, remote_file)
                self.upload_file(ssh_client, local_file, remote_file)

    @staticmethod
    def create_remote_directory(ssh_client, remote_path):
        command = f"mkdir -p {remote_path}"
        result = run_remote_cmd(command, ssh_client)
        if result.exit_code != 0:
            logger.error(f"Failed to create remote directory '{remote_path}'.")
            logger.error(f"Error: {result.stderr}")

    @staticmethod
    def backup_existing_file(ssh_client, remote_path):
        command = f"mv {remote_path} {remote_path}.bak"
        run_remote_cmd(command, ssh_client)

    @staticmethod
    def upload_file(ssh_client, local_path, remote_path):
        sftp = ssh_client.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()
        logger.info(f"Successfully copied '{local_path}' to '{remote_path}'")
