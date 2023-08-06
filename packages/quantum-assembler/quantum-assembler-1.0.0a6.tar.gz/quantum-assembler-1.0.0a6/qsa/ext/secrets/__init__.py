import os

from qsa.ext.base import BaseExtension

from .adapters import PublicFacingServerCertificateAdapter
from .secret import SecretAdapterManager
from .schema import ConfigSchema
from .schema import VaultConfigSchema
from .vault import Vault
from .vault import VaultManager


class Extension(BaseExtension):
    name = 'secrets'
    command_name = 'secret'
    schema_class = ConfigSchema
    subcommands = [
        {
            'name': 'allow',
            'args': [
                {'dest': 'vault'},
                {'dest': 'keyid'},
            ]
        },
        {
            'name': 'updatevaults',
            'args': []
        },
        {
            'name': 'update',
            'args': [{'dest': 'vault'}]
        },
        {
            'name': 'edit-vault',
            'args': [
                {'dest': 'vault'}
            ]
        },
        {
            'name': 'synclocal',
            'args': [{'dest': 'vault'}]
        },
        {
            'name': 'checksync',
            'args': [{'dest': 'vault'}]
        }
    ]

    supported_projects = ['application', 'k8s']

    def setup_injector(self, injector):
        injector.provide('vaults', VaultManager(self.config))

    def on_project_init(self, quantum, typname, name, *args, **kwargs):
        pass

    def on_setup_secret_adapters(self, adapters):
        adapters.register(
            PublicFacingServerCertificateAdapter())

    def handle_update(self, codebase, args):
        """Updates a specific vault with secrets."""
        vault = Vault.open(codebase.abspath('vault'), args.vault)
        self.assembler.notify('secrets_update', args.vault, vault)

    def handle_updatevaults(self, codebase):
        """Ensure that all vaults are created."""
        if self.quantum.get('project.type') not in self.supported_projects:
            return

        if not codebase.exists('vault/open-vault'):
            dirname = codebase.mkdir('vault')
            with codebase.commit("Initialize secrets vault"):
                codebase.write('vault/open-vault',
                    self.render('vault/open-vault.j2'))
                codebase.make_executable('vault/open-vault')

        with codebase.commit("Create vaults for specified environments"):
            dirname = codebase.mkdir('vault')
            for name, opts in self.quantum.get('secrets.vaults').items():
                os.environ['QUANTUM_DEPLOYMENT_ENV'] = name
                if not opts.keys:
                    raise NotImplementedError
                if not codebase.exists(f'vault/{name}.yml'):
                    vault = Vault.create(codebase, dirname, name, **opts)
                    self.logger.debug("Created vault for environment %s", name)

            if not codebase.exists('vault/local.yml'):
                vault = Vault.createlocal(codebase, dirname, 'local', **opts)


    def handle_allow(self, codebase, quantum, args):
        os.environ['QUANTUM_DEPLOYMENT_ENV'] = args.vault
        if args.vault not in quantum.get('secrets.vaults'):
            self.spec['secrets']['vaults'][args.vault] = VaultConfigSchema.defaults()
        if args.keyid not in self.spec['secrets']['vaults'][args.vault]['keys']:
            self.spec['secrets']['vaults'][args.vault]['keys'].append(args.keyid)

        with codebase.commit(f"Allowed {args.keyid} to open vault {args.vault}"):
            quantum.update(self.spec)
            quantum.persist(codebase)
        #    vault = Vault.open(codebase.abspath('vault'), args.vault)
        #    vault.setkeys(codebase,
        #        quantum.get(f'secrets.vaults.{args.vault}.keys'))

    def handle_edit_vault(self, codebase, args):
        """Edit a vault using vim."""
        os.environ['QUANTUM_DEPLOYMENT_ENV'] = args.vault
        dst = codebase.abspath(f'vault/{args.vault}.yml')
        if not os.path.exists(dst):
            self.fail(f"No such vault: {args.vault}")
        vault = Vault.open(codebase.abspath('vault'), args.vault)
        with codebase.commit(f"Edit secrets for {args.vault} environment"):
            vault.editor(codebase)

    def handle_synclocal(self, assembler, codebase, args):
        """Synchronizes the local development environment vault with
        the specified environment for all known secret types.
        """
        adapters = SecretAdapterManager()
        sources = Vault.open(codebase.abspath('vault'), args.vault)
        targets = Vault.open(codebase.abspath('vault'), 'local')
        assembler.notify('setup_secret_adapters', adapters)
        for name, source in sources:
            target = adapters.adapt(source,
                targets.getsecret(name))
            if target is not None:
                targets.setsecret(name, target)
                continue
            self.logger.warning("Unable to adapt secret %s (kind: %s)",
                name, source.kind)

        with codebase.commit(f"Synchronize local vault with {args.vault}"):
            targets.persist(codebase)

    def handle_checksync(self, codebase, args):
        """Checks if all secrets from the source vault are present in the
        local vault.
        """
        sources = Vault.open(codebase.abspath('vault'), args.vault)
        targets = Vault.open(codebase.abspath('vault'), 'local')
        for name, spec in sources:
            present = name in targets
            print(f"checking if {name} (kind: {spec.kind}) is present in local vault....."
                + ('ok' if present else 'MISSING'))
