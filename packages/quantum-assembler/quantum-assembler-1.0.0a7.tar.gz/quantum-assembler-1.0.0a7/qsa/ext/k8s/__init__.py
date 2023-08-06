import os
import glob

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
        vaults = self.injector.call(lambda vaults: vaults)

        # TODO: Kubernetes targets only for projects of type
        # application or k8s.
        if self.quantum.get('project.type') not in ('k8s', 'application'):
            return

        make.setvariable('K8S_LOCAL_CTX', '_quantum-local')
        make.setvariable('K8S_KUBECTL_CTX',
            "$(shell kubectl config current-context)")
        make.setvariable('K8S_NAMESPACES',
            "find k8s/ -type f -name namespaces.yml | xargs cat")
        make.setvariable('K8S_KUBECTL',
            "KUBECONFIG=$(K8S_KUBECONFIG) kubectl")
        make.setvariable('K8S_SECRETS', "$(QSA) k8s secrets $(QUANTUM_DEPLOYMENT_ENV)")
        make.setvariable('K8S_KUBECONFIG', "~/.kube/config")
        make.setvariable('K8S_DEPLOYMENTS',
            "find k8s/ -type f -name deployment* | xargs cat | envsubst")
        make.setvariable('K8S_CONFIGMAPS',
            'find k8s/ -type f \( -name config.common.yml -o -name '
            '*config.$(QUANTUM_DEPLOYMENT_ENV).yml \) | xargs cat | envsubst')
        make.setvariable('K8S_SERVICES',
            "find k8s/ -type f -name service* | xargs cat | envsubst")
        if self.quantum.get('project.type') == 'k8s':
            make.setvariable('K8S_INGRESSES',
                "find k8s/ -type f -name ingress* | xargs cat | envsubst")

        # Create the deploy-k8s target which is then wrapped by
        # environment-specific targets.
        target = make.target('deploy-k8s')
        target.execute("$(K8S_KUBECTL) config use-context $(K8S_CTX)",
            ifdef="K8S_CTX")

        # Namespaces are only deploy for projects of type 'k8s';
        # applications may not have ownership over namespaces in the
        # Quantum Framework.
        if self.quantum.get('project.type') == 'k8s':
            target.execute("$(K8S_NAMESPACES) | $(K8S_KUBECTL) apply -f -",
                ifneq='"$(wildcard k8s/namespace*)", ""')

        if self.quantum.get('project.type') == 'application':
            target.execute("make docker-image-$(QUANTUM_DEPLOYMENT_ENV)")
            target.execute("make docker-push-$(QUANTUM_DEPLOYMENT_ENV)")
        target.execute('$(K8S_CONFIGMAPS) | $(K8S_KUBECTL) apply -f -',
            ifneq='"$(wildcard k8s/*config*.yml)", ""')
        if self.quantum.get('project.type') in ('application', 'k8s'):
            target.execute(f'$(K8S_SECRETS) | $(K8S_KUBECTL) apply -f -',
                ifneq=f'"$(wildcard vault/$(QUANTUM_DEPLOYMENT_ENV).yml)", ""')
        if self.quantum.get('project.type') == 'application':
            target.execute("$(K8S_DEPLOYMENTS) | $(K8S_KUBECTL) apply -f -")
        target.execute("$(K8S_SERVICES) | $(K8S_KUBECTL) apply -f -",
            ifneq='"$(wildcard k8s/service*.yml)", ""')
        if self.quantum.get('project.type') == 'k8s':
            target.execute("$(K8S_INGRESSES) | $(K8S_KUBECTL) apply -f -",
                ifneq='"$(wildcard k8s/ingress*.yml)", ""')

        # Reset the kubectl context.
        target.execute("$(K8S_KUBECTL) config use-context $(K8S_KUBECTL_CTX)",
            ifdef='K8S_CTX')

        for env in self.quantum.get('deployment.environments'):
            target = make.target(f'deploy-k8s-{env.name}')
            context_name = env.annotations.get('k8s.quantumframework.org/context')\
                or "$(K8S_KUBECTL_CTX)"
            if env.name == 'local':
                context_name = '$(K8S_LOCAL_CTX)'
            cmd = f"make deploy-k8s K8S_CTX={context_name}\\\n\t\tQUANTUM_DEPLOYMENT_ENV={env.name}"
            if env.name == 'local':
                cmd += '\\\n\t\tDOCKER_QUALNAME="$(DOCKER_LOCAL_REGISTRY)/$(DOCKER_REPOSITORY)"'
            if context_name:
                cmd += f'\\\n\t\tK8S_CTX={context_name}'
            target.execute(cmd)

        #for env in self.quantum.get('deployment.environments'):
        #    target = make.target(f'deploy-{env.name}')
        #    kubeconfig = env.annotations.get('k8s.quantumframework.org/kubeconfig')
        #    cmd = f"KUBECONFIG={kubeconfig} $(K8S_KUBECTL_STDIN)"\
        #        if (kubeconfig and env.name != 'local') else '$(K8S_KUBECTL_STDIN)'
        #    context_name = env.annotations.get('k8s.quantumframework.org/context')
        #    if env.name == 'local':
        #        context_name = '$(K8S_LOCAL_CTX)'
        #    if context_name:
        #        target.execute(f'kubectl config use-context {context_name}')
        #    target.execute(f"$(K8S_NAMESPACES) | {cmd}")
        #    target.execute(f"qsa k8s secrets {env.name} | {cmd}")
        #    if context_name:
        #        target.execute(f'kubectl config use-context $(K8S_KUBECTL_CTX)')
