from qsa.ext.base import BaseExtension

from .schema import ConfigSchema


class Extension(BaseExtension):
    name = command_name = inject = 'jenkins'
    schema_class = ConfigSchema
    weight = 9.1
    subcommands = [
        {
            'name': 'configure',
            'args': [
                ('--folder', {'dest': 'folder'}),
                ('--mounted-secret', {'action': 'append', 'default': [],
                    'dest': 'mounted_secrets'})
            ]
        }
    ]

    def handle(self, codebase):
        if self.quantum.get('ci.using') not in ('jenkins', 'gitlab+jenkins'):
            return
        template_name = f'Jenkinsfile.{self.quantum.get("project.type")}.j2'
        ctx = {
            'DOCKER_IMAGE_QUALNAME': (self.quantum.get('docker.registry') or 'docker.io')\
                + '/' + self.quantum.get('docker.repository')
        }
        with codebase.commit("Compile CI/CD pipeline"):
            codebase.mkdir('ci/jenkins')
            self.render_to_file(codebase, template_name, 'Jenkinsfile',
              ctx=ctx)
            self.render_to_file(codebase, 'ci/jenkins/init.groovy.j2',
                'ci/jenkins/init.groovy')

    def handle_configure(self, codebase, args, ci):
        if not self.spec:
            self.spec = self.schema_class.getfordump().dump()
        with codebase.commit("Configure Jenkins"):
            if args.folder:
                self.spec.jenkins.folder = str.strip(args.folder, '/')
            if args.mounted_secrets:
                secrets = []
                for secret in args.mounted_secrets:
                    kind, name, path = str.split(secret, ':')
                    secrets.append({'name': name, 'path': path})
                ci.configure({'mounted_secrets': secrets})
            self.quantum.update(self.spec)
            self.quantum.persist(codebase)

    def on_setup_makefile(self, mk):
        """Adds the ``deploy-jenkins`` target."""
        mk.target('deploy-jenkins')

    def on_setup_makefile_target_deploy_jenkins(self, make, target):
        target.execute(
            'curl -v --user "$(JENKINS_USER):$(JENKINS_TOKEN)"\\\n\t\t'
            '--data-urlencode "script=$$(<./ci/jenkins/init.groovy)"\\\n\t\t'
            '$(JENKINS_HOST)/scriptText')
