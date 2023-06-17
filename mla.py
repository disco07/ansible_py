import logging

import paramiko
from paramiko.client import SSHClient, AutoAddPolicy
from paramiko.rsakey import RSAKey
from paramiko.ssh_exception import AuthenticationException, PasswordRequiredException, SSHException


class CmdResult:
    def __init__(self, stdout, stderr, exit_code):
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code


def run_remote_cmd(command: str, ssh_client: SSHClient) -> CmdResult:
    stdin, stdout, stderr = ssh_client.exec_command(command)
    exit_code = stdout.channel.recv_exit_status()
    return CmdResult(stdout.read().decode(), stderr.read().decode(), exit_code)


def connect_ssh(hostname, port, username, password, private_key):
    ssh_client = SSHClient()
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())

    try:
        if private_key:
            private_key_obj = RSAKey.from_private_key_file(private_key)
            ssh_client.connect(hostname=hostname, port=port, username=username, pkey=private_key_obj)
        else:
            ssh_client.connect(hostname=hostname, port=port, username=username, password=password)

        return ssh_client
    except (AuthenticationException, PasswordRequiredException, SSHException) as e:
        logging.error(f"Failed to connect to {hostname}:{port} - {e}")
        return None
