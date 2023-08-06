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
        make.setvariable('K8S_KUBECTL_CTX',
            "$(shell kubectl config current-context)")
        make.setvariable('K8S_NAMESPACES',
            "find k8s/ -type f -name namespaces.yml | xargs cat")
        for env in self.quantum.get('deployment.environments'):
            target = make.target(f'deploy-{env.name}')
            kubeconfig = env.annotations.get('k8s.quantumframework.org/kubeconfig')
            cmd = f"KUBECONFIG={kubeconfig} kubectl apply -f -"\
                if (kubeconfig and env.name != 'local') else 'kubectl apply -f -'
            context_name = env.annotations.get('k8s.quantumframework.org/context')
            if env.name == 'local':
                context_name = '_quantum-local'
            if context_name:
                target.execute(f'kubectl config use-context {context_name}')
            target.execute(f"$(K8S_NAMESPACES) | {cmd}")
            target.execute(f"qsa k8s secrets {env.name} | {cmd}")
            if context_name:
                target.execute(f'kubectl config use-context $(K8S_KUBECTL_CTX)')
