import os
import subprocess
import tempfile

import gnupg
from ansible import constants as C
from ansible.constants import DEFAULT_VAULT_ID_MATCH
from ansible.parsing.dataloader import DataLoader
from ansible.parsing.vault import AnsibleVaultError
from ansible.parsing.vault import VaultLib
from ansible.parsing.vault import VaultSecret
from ansible.cli import CLI
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from qsa.cli.exc import CommandError
from qsa.lib.datastructures import DTO
from qsa.lib.serializers import yaml


class Vault:
    """Provides an API to create and edit an encrypted container of
    secrets.
    """

    @staticmethod
    def get(key=None):
        """Returns a :class:`ansible.parsing.VaultLib` instance."""
        if key is None:
            loader = DataLoader()
            vault_secret = CLI.setup_vault_secrets(
                loader=loader,
                vault_ids=C.DEFAULT_VAULT_IDENTITY_LIST,
                vault_password_files=['vault/open-vault']
            )
        else:
            vault_secret = [(DEFAULT_VAULT_ID_MATCH, VaultSecret(key))]
        return VaultLib(vault_secret)

    @classmethod
    def create(cls, codebase, vault_dir, name, keys=None):
        """Create a new vault in the specified directory."""
        key = bytes.hex(AESGCM.generate_key(256))

        # Create the password file and encrypt it using the GPG
        # keys configured for this vault.
        gpg = gnupg.GPG()
        buf = str(gpg.encrypt(key, keys, always_trust=True))
        assert buf, keys
        codebase.write(f'{vault_dir}/{name}.gpg', buf)

        # Create a new VaultLib instance to write the initial
        # vault.
        vault = cls.get()
        buf = vault.encrypt('')
        codebase.write(f'{vault_dir}/{name}.yml', buf,
            mode='wb', newline=False)



    @classmethod
    def createlocal(cls, codebase, vault_dir, name, *args, **kwargs):
        """Creates the vault that is used in the local development
        environment. This vault is not used to store "real" secrets;
        it exists solely to provide integration with the local
        development tools.
        """
        key = bytes.hex(AESGCM.generate_key(256))
        codebase.write(f'{vault_dir}/{name}.txt', key)
        vault = cls.get(key=str.encode(key))
        buf = vault.encrypt('')
        codebase.write(f'{vault_dir}/{name}.yml', buf,
            mode='wb', newline=False)

    @classmethod
    def open(cls, dirname, name, keys=None):
        fp = os.path.join(dirname, f'{name}.yml')
        plain = os.path.join(dirname, f'{name}.txt')
        key = None
        if os.path.exists(plain):
            key = open(plain).read()
        vault = cls.get(key=str.encode(str.strip(key)) if key else None)
        try:
            buf = bytes.decode(vault.decrypt(open(fp).read()))
        except AnsibleVaultError as e:
            raise CommandError(str(e))
        return cls(dirname, name, vault, buf)

    @property
    def path(self):
        return os.path.join(self.vault_dir, f'{self.name}.yml')

    def __init__(self, vault_dir, name, codec, content):
        self.vault_dir = vault_dir
        self.name = name
        self.content = content
        self.data = None
        self.codec = codec
    
    def setkeys(self, codebase, keys):
        gpg = gnupg.GPG()
        args = ['vault/open-vault']
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        key, err = p.communicate()
        assert key, key

        buf = str(gpg.encrypt(key, keys))
        codebase.write(f'{self.vault_dir}/{self.name}.gpg', buf)

    def editor(self, codebase):
        """Edit the vault in the system editor."""
        src = tempfile.mktemp()
        with open(src, 'w') as f:
            f.write(self.content)
        args = ['vim', '-c', "'set syntax=yaml ts=2 sw=2 expandtab'", src]
        os.system(' '.join(args))

        # Read the temporary file and write it to the vault
        # destination.
        with open(src) as f:
            content = f.read()
        if content != self.content:
            self.content = content
            self.persist(codebase)

    def persist(self, codebase):
        """Persists the contents of the vault."""
        if self.data:
            self.content = '---\n' + yaml.safe_dump(self.data,
                default_flow_style=False, indent=2)
        codebase.write(self.path, self.codec.encrypt(self.content),
            mode='wb', newline=False)

    def setsecret(self, name, spec):
        if self.data is None:
            self.data = yaml.safe_load(self.content) or {}
        self.data[name] = spec.as_dict()

    def getsecret(self, name):
        """Return the decrypted secret identified by name."""
        if self.data is None:
            self.data = yaml.safe_load(self.content) or {}
            assert isinstance(self.data, dict)
        value = self.data.get(name)
        return DTO.fromdict(value) if value is not None else None

    def __iter__(self):
        for name, spec in (yaml.safe_load(self.content) or {}).items():
            yield name, DTO.fromdict(spec)

    def __contains__(self, value):
        if self.data is None:
            self.data = yaml.safe_load(self.content) or {}
        return value in self.data


class VaultManager:
    """Manages access to the vaults."""

    def __init__(self, config):
        self.config = config

    def get(self, name):
        """Return the vault identified by `name`."""
        return Vault.open('vault', name)
