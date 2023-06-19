import logging

from mla import run_remote_cmd
from modules.base import BaseModule


class ServiceModule(BaseModule):
    name = "service"

    def process(self, ssh_client):
        name = self.params.get("name")
        state = self.params.get("state")

        # Vérifier l'état du service
        check_command = f"sudo systemctl is-active {name}"
        check_result = run_remote_cmd(check_command, ssh_client, self.params.get("config"))

        if check_result.exit_code == 0 and check_result.stdout.strip() == "active":
            # Le service est déjà actif
            if state == "started":
                logging.info(f"Service {name} is already started")
            elif state == "stopped":
                # Arrêter le service
                stop_command = f"sudo systemctl stop {name}"
                stop_result = run_remote_cmd(stop_command, ssh_client, self.params.get("config"))

                if stop_result.exit_code == 0:
                    logging.info(f"Service {name} stopped successfully")
                else:
                    logging.error(f"Failed to stop service {name}. Error: {stop_result.stderr}")
        else:
            if state == "started":
                # Démarrer le service
                start_command = f"sudo systemctl start {name}"
                start_result = run_remote_cmd(start_command, ssh_client, self.params.get("config"))

                if start_result.exit_code == 0:
                    logging.info(f"Service {name} started successfully")
                else:
                    logging.error(f"Failed to start service {name}. Error: {start_result.stderr}")
            elif state == "stopped":
                logging.info(f"Service {name} is already stopped")

