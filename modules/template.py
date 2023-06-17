import logging
from jinja2 import Template

from mla import run_remote_cmd
from modules.base import BaseModule


class TemplateModule(BaseModule):
    name = "template"

    def process(self, ssh_client):
        src = self.params.get("src")
        dest = self.params.get("dest")
        vars = self.params.get("vars", {})

        # Lecture du fichier source
        with open(src) as file:
            template_content = file.read()

        # Templatisation du contenu du fichier
        template = Template(template_content)
        rendered_content = template.render(vars)

        # Écriture du fichier templatisé sur l'hôte distant
        command = f"echo '{rendered_content}' | sudo tee {dest}"
        result = run_remote_cmd(command, ssh_client)

        # Vérification du résultat de l'exécution de la commande
        if result.exit_code == 0:
            logging.info(f"Template {src} applied successfully to {dest}")
        else:
            logging.error(f"Failed to apply template {src} to {dest}. Error: {result.stderr}")
