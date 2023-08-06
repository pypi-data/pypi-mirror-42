from qsa.ext.base import BaseExtension
from qsa import const


class Extension(BaseExtension):
    name = command_name = 'docker'

    def can_handle(self, codebase):
        return codebase.exists('Dockerfile')

    def on_setup_makefile(self, mk):
        """Adds the common QSA Makefile targets."""
        mk.target('docker-image-local')
        mk.target('docker-push-local')
        mk.target('docker-image')
        mk.target('docker-push')

    def on_setup_makefile_target_docker_image_local(self, make, target):
        name = self.quantum.get('project.name')
        target.execute(f'docker build -t {name} .')
        target.execute(f'docker tag {name} {const.QUANTUM_DOCKER_REGISTRY}/{name}')

    def on_setup_makefile_target_docker_push_local(self, make, target):
        name = self.quantum.get('project.name')
        target.execute(f'make docker-image-local')
        target.execute(f'docker push {const.QUANTUM_DOCKER_REGISTRY}/{name}')
