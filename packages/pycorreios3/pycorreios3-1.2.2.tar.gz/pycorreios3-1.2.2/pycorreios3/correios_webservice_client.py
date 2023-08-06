import zeep
from zeep.cache import InMemoryCache

URI_WSDL_CALC_PRECO_PRAZO = 'http://ws.correios.com.br/calculador/CalcPrecoPrazo.asmx?WSDL'
URI_WSDL_SRO = 'http://webservice.correios.com.br/service/rastro/Rastro.wsdl'
URI_WSDL_SIGEP_HOMOLOGACAO = 'https://apphom.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl'
URI_WSDL_SIGEP_PRODUCAO = 'https://apps.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl'


class CorreiosWSClient():
    api_preco_prazo: zeep.Client=None
    api_sro: zeep.Client=None
    api_sigep: zeep.Client=None
    api_sigep_homologacao: zeep.Client=None
    api_sigep_producao: zeep.Client=None
    cache: zeep.cache.InMemoryCache
    transport: zeep.Transport

    def __init__(self, load_api_preco_prazo: bool=False, load_api_sro: bool=False,
                 load_api_sigep: bool=False, producao: bool=False):

        self.producao = producao
        self.cache = zeep.cache.InMemoryCache(timeout=86400)
        self.transport = zeep.Transport(cache=self.cache, timeout=20, operation_timeout=15)

        if load_api_preco_prazo:
            self.load_api_preco_prazo()

        if load_api_sro:
            self.load_api_sro()

        if load_api_sigep:
            self.load_api_sigep()

    def load_api_preco_prazo(self):
        if self.api_preco_prazo is None:
            self.api_preco_prazo = zeep.Client(URI_WSDL_CALC_PRECO_PRAZO, transport=self.transport)

    def load_api_sro(self):
        if self.api_sro is None:
            self.api_sro = zeep.Client(URI_WSDL_SRO, transport=self.transport)

    def load_api_sigep(self):
        if self.api_sigep is None:
            uri = URI_WSDL_SIGEP_PRODUCAO if self.producao else URI_WSDL_SIGEP_HOMOLOGACAO
            self.api_sigep = zeep.Client(uri, transport=self.transport)

    def load_api_sigep_homologacao(self):
        if self.api_sigep_homologacao is None:
            self.api_sigep_homologacao = zeep.Client(URI_WSDL_SIGEP_HOMOLOGACAO, transport=self.transport)
