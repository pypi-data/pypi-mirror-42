import yaml


class Base64DER(str):

    @classmethod
    def represent(self, dumper, data):
        """Represents the base64-encoded DER string as YAML."""
        return dumper.represent_scalar('tag:yaml.org,2002:str',
            data, style='|')


yaml.add_representer(Base64DER, Base64DER.represent,
    Dumper=yaml.SafeDumper)
