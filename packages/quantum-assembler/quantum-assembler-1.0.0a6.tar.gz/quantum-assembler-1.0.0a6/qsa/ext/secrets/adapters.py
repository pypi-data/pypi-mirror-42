import requests

from qsa.lib.serializers import Base64DER
from .secret import SecretAdapter


class PublicFacingServerCertificateAdapter(SecretAdapter):
    secret_type = 'PublicFacingServerCertificate'
    base_url = 'https://raw.githubusercontent.com/wizardsofindustry/'
    urls = {
        'tls.key': 'k8s-devenv/develop/pki/http.crt',
        'tls.crt': 'k8s-devenv/develop/pki/http.rsa'
    }

    def create(self, source):
        """Clone the secret and replace the certificates with the standard
        Quantum Development Environment (QDE) certificates.
        """
        target = self.clone(source)
        for key, url in self.urls.items():
            self.logger.debug("Fetching %s", url)
            response = requests.get(self.base_url + url)
            assert response.status_code == 200
            target.data[key] = Base64DER(response.text)
        return target
