import copy

import yaml
from ansible.plugins.filter.core import b64encode


class Secret:
    
    @property
    def base64(self):
        data = {}
        for key in self.data:
            data[key] = b64encode(self.data[key])
        return data

    def __init__(self, name, data, namespace=None):
        self.namespace = namespace or []
        self.name = name
        self.data = data
        if self.namespace and isinstance(self.namespace, str):
            self.namespace = [self.namespace]

    def __str__(self):
        template = {
            'apiVersion': 'v1',
            'kind': 'Secret',
            'metadata': {
                'name': self.name
            },
            'type': 'Opaque',
            'data': self.base64
        }
        result = ''
        for i, ns in enumerate(self.namespace):
            if i > 0:
                result += '\n\n\n---\n'
            spec = copy.deepcopy(template)
            spec['metadata']['namespace'] = ns
            result += str.strip(
                yaml.safe_dump(spec, indent=2, default_flow_style=False))
        return result
