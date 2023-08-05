import os

from qsa.ext.base import BaseExtension

from .model import Secret


class AnnotationController:

    def __init__(self, domain, annotations):
        self.annotations = annotations

    def get(self, path):
        return self.annotations[f'{self.domain}/{path}']


class Extension(BaseExtension):
    name = 'k8s'
    command_name = 'k8s'
    subcommands = [
        {
            'name': 'secrets',
            'args': [
                {'dest': 'vault'}
            ]
        }
    ]

    def handle_secrets(self, args, vaults):
        """Open the vault specified in the command-line arguments and
        create Kubernetes ``Secret`` objects.
        """
        vault = vaults.get(args.vault)
        for i, item in enumerate(vault):
            name, spec = item
            secret = Secret(name, spec.data, spec.metadata.namespace)
            if i > 0:
                print('\n')
            print('---')
            print(secret)

    def on_setup_makefile(self, make):
        for env in self.quantum.get('deployment.environments'):
            target = make.target(f'deploy-{env.name}')
            kubeconfig = env.annotations.get('k8s.quantumframework.org/kubeconfig')
            if kubeconfig:
                target.execute(f"KUBECONFIG={kubeconfig} kubectl get namespaces")
            context_name = env.annotations.get('k8s.quantumframework.org/context')
            if context_name:
                target.execute(f'kubectl config use-context {context_name}')
            target.execute(f"qsa k8s secrets {env.name}")
