import argparse
import logging

import yaml

from mla import connect_ssh
from modules.apt import AptModule
from modules.copy import CopyModule
from modules.service import ServiceModule
from modules.template import TemplateModule


def execute_tasks(todos_file, inventory_file):
    global ssh_client, module
    with open(todos_file) as file:
        tasks = yaml.safe_load(file)

    # Lecture du fichier inventory.yml
    with open(inventory_file) as file:
        inventory = yaml.safe_load(file)

    # Connexion SSH aux hôtes
    for host, host_info in inventory['hosts'].items():
        ssh_address = host_info.get('ssh_address')
        ssh_port = host_info.get('ssh_port')
        ssh_username = host_info.get('ssh_username')
        ssh_password = host_info.get('ssh_password')
        ssh_private_key = host_info.get('ssh_private_key')

        ssh_client = connect_ssh(ssh_address, ssh_port, ssh_username, ssh_password, ssh_private_key)
        if ssh_client:
            for task in tasks:
                module_name = task.get("module")
                params: dict = task.get("params", {})
                params.update({"config": {"password": ssh_password}})

                if module_name == "apt":
                    module = AptModule(params)
                elif module_name == "copy":
                    module = CopyModule(params)
                elif module_name == "service":
                    module = ServiceModule(params)
                elif module_name == "template":
                    module = TemplateModule(params)
                module.process(ssh_client)

            # N'oubliez pas de fermer la connexion SSH
            ssh_client.close()


if __name__ == "__main__":
    # create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    parser = argparse.ArgumentParser(description='Program description')
    parser.add_argument('-f', '--todos', type=str, help='Path to todos.yml file')
    parser.add_argument('-i', '--inventory', type=str, help='Path to inventory.yml file')

    args = parser.parse_args()

    todos_file = args.todos
    inventory_file = args.inventory

    execute_tasks(todos_file, inventory_file)
