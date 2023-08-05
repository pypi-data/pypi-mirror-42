import copy
import logging


class SecretAdapter:
    """Mocks a secret of a known type for use in the local development
    environment.
    """
    secret_type = None
    logger = logging.getLogger('qsa')

    def __init__(self):
        pass

    def clone(self, secret):
        """Clones the secret into a new datastructure."""
        return copy.deepcopy(secret)

    def is_valid(self, source):
        pass

    def create(self, source):
        raise NotImplementedError

    def update(self, source, target):
        """Updates `target` with the metadata of `source`."""
        if not source.metadata:
            del target.metadata
            return target
        if not target.get('metadata'):
            target.metadata = {}
        target.metadata.update(source.metadata)
        return target


class SecretAdapterManager:
    """Collects :class:`SecretAdapter` instances and provides an interface
    to adapt secrets.
    """

    def __init__(self):
        self._registry = {}
        self._adapters = []

    def register(self, adapter):
        """Registers a :class:`SecretAdapter` implementation."""
        if adapter.secret_type:
            assert adapter.secret_type not in self._registry
            self._registry[adapter.secret_type] = adapter
        else:
            adapters.append(adapter)

    def adapt(self, source, target):
        """Adapts secrets from the source using the appropriate adapter,
        and updates target. Note that target may be ``None``.
        """
        adapter = self._registry.get(source.kind)
        if adapter is not None:
            adapter.is_valid(source)
            target = adapter.create(source) if target is None\
                else adapter.update(source, target)
        else:
            # Loop over all untyped adapters and find the first match.
            pass
        return target
