from .correios_webservice_client import CorreiosWSClient
import requests
import json
import collections

class CEP:
    client: CorreiosWSClient=None

    def __init__(self, cep: str):
        cep = "".join(filter(lambda x: x.isdigit(), cep))
        assert len(cep) == 8

        if len(cep) != 8:
            raise(RuntimeError('CEP {} inválido'.format(cep)))

        self.cep8 = cep
        self.cep3 = cep[-3:]
        self.cep5 = cep[:5]
        self.cep9 = self.cep5 + '-' + self.cep3

        assert len(self.cep3) == 3
        assert len(self.cep5) == 5
        assert len(self.cep9) == 9
        self.consulta = collections.OrderedDict()

    def consulta_sigep(self, client=None):
        if client is None:
            if self.client is None:
                self.client = CorreiosWSClient(load_api_sigep=True, producao=True)
        else:
            self.client = client
            self.client.load_api_sigep()

        self.consulta['sigep'] = self.client.api_sigep.service.consultaCEP(self.cep8)

        return self.consulta['sigep']

    def consulta_viacep(self):
        url_api = ('http://www.viacep.com.br/ws/{}/json/unicode'.format(self.cep8))
        req = requests.get(url_api)
        if req.status_code == 200:
            self.consulta['viacep'] = json.loads(req.text, strict=False)
            return self.consulta['viacep']
        else:
            return None

    def consulta_postmon(self):
        url_api = 'https://api.postmon.com.br/v1/cep/{}'.format(self.cep8)
        req = requests.get(url_api)
        if req.status_code == 200:
            self.consulta['postmon'] = json.loads(req.text, strict=False)
            return self.consulta['postmon']
        else:
            return None

    def consulta_cepaberto(self, token):
        url_api = 'http://www.cepaberto.com/api/v3/cep?cep={}'.format(self.cep8)
        req = requests.get(url_api, headers={'Authorization': 'Token token={}'.format(token)})
        if req.status_code == 200:
            self.consulta['cepaberto'] = json.loads(req.text, strict=False)
            return self.consulta['cepaberto']
        else:
            return None
