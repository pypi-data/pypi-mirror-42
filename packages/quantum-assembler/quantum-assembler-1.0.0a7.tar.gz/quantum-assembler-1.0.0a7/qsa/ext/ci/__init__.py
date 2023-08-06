from subprocess import Popen, PIPE

from qsa.ext.base import BaseExtension

from .schema import ConfigSchema


class Extension(BaseExtension):
    name = command_name = inject = 'ci'
    schema_class = ConfigSchema
    weight = 9.0
    subcommands = [
        {
            'name': 'configure',
            'args': [
                ('--origin-remote', {}),
                ('--origin-secret', {}),
                ('--publish-registry-secret', {}),
                ('--publish-registry-url', {}),
                ('--mounted-secret', {'action': 'append', 'default': [],
                    'dest': 'mounted_secrets'})
            ]
        }
    ]
    nodefault = True

    def handle_configure(self, args, codebase):
        if args.origin_remote:
            with codebase.commit("Set origin URL for CI/CD remote sources"):
                self.spec.ci.origin.remote = args.origin_remote
                self.quantum.update(self.spec)
                self.quantum.persist(codebase)
        if args.origin_secret:
            with codebase.commit("Configure secret for origin pull"):
                self.spec.ci.origin.credentials = args.origin_secret
                self.quantum.update(self.spec)
                self.quantum.persist(codebase)
        if args.publish_registry_secret:
            with codebase.commit("Set credential for artifact publication"):
                self.spec.ci.container_registries.publish.secret =\
                    args.publish_registry_secret
                self.quantum.update(self.spec)
                self.quantum.persist(codebase)
        if args.publish_registry_url:
            with codebase.commit("Set URL for artifact publication"):
                self.spec.ci.container_registries.publish.url =\
                    args.publish_registry_url
                self.quantum.update(self.spec)
                self.quantum.persist(codebase)
        if args.mounted_secrets:
            secrets = []
            for secret in args.mounted_secrets:
                kind, name, path = str.split(secret, ':')
                secrets.append({'name': name, 'path': path, 'kind': kind})

            self.spec.ci.mounted_secrets = secrets
            self.quantum.update(self.spec)
            self.quantum.persist(codebase)


    def configure(self, spec):
        if not self.spec:
            self.spec = self.schema_class.defaults()
        self.spec.ci.update(spec)
        self.quantum.update(self.spec)

    def on_autodetect(self):
        self.injector.call(self.autoconfigure)

    def autoconfigure(self, codebase):
        with codebase.commit("Configure remote sources"):
            args = ['git', 'config', '--get', 'remote.origin.url']
            p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
            output, error = p.communicate()
            if p.returncode != 0:
                raise RuntimeError(output, error)
            self.spec.ci.origin.remote = str.strip(bytes.decode(output))
            self.quantum.update(self.spec)
            self.quantum.persist(codebase)
