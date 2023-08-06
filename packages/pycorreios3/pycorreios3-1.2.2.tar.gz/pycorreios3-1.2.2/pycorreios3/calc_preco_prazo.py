from .correios_webservice_client import CorreiosWSClient
from .CEP import CEP
from .volume import Volume


class CalcPrecoPrazo:
    def __init__(self, credenciais=None, cartao_postagem=None, nCdEmpresa: str=None, sDsSenha: str=None,
                 nCdServico: list=None, sCepOrigem=None, sCdMaoPropria: bool=True,
                 sCdAvisoRecebimento: bool=True, client=None):

        if sum(nCdEmpresa is None, sDsSenha is None) not in (0, 2):
            raise(RuntimeError('nCdEmpresa e sDsSenha precisam estar ambos definidos ou ambos indefinidos'))

        if sum((credenciais is None, cartao_postagem is None, (nCdEmpresa is None or sDsSenha is None))) != 2:
            raise(RuntimeError('E necessario definir um e apenas um dentre: \
                                credenciais, cartao_postagem e nCdEmpresa/sDsSenha'))

        if credenciais is None and cartao_postagem is not None:
            credenciais = cartao_postagem.get_credenciais()

        if credenciais is not None:
            self.nCdEmpresa, self.sDsSenha = credenciais.get_cred_calc()
        else:
            self.nCdEmpresa = nCdEmpresa
            self.sDsSenha = sDsSenha

        sCepOrigem = self.ajuste_cep(sCepOrigem)
        nCdServico = self.ajuste_nCdServico(nCdServico)

        if cartao_postagem is not None:
            self.nCdServico = nCdServico if nCdServico is not None else cartao_postagem.lista_codigo_servicos()
            self.sCepOrigem = sCepOrigem if sCepOrigem is not None else cartao_postagem.cep_origem_padrao.cep8
        else:
            self.nCdServico = nCdServico
            self.sCepOrigem = sCepOrigem

        self.sCdMaoPropria = sCdMaoPropria
        self.sCdAvisoRecebimento = sCdAvisoRecebimento

        self.client = client if client is not None else CorreiosWSClient()
        self.client.load_api_preco_prazo()
        self.api = self.client.api_preco_prazo.service
        self.auth_dict = {'nCdEmpresa': self.nCdEmpresa, 'sDsSenha': self.sDsSenha}

    def CalcPrazo(self, sCepDestino, sCepOrigem=None, nCdServico=None):
        sCepOrigem = self.ajuste_cep(sCepOrigem, self.sCepOrigem)
        sCepDestino = self.ajuste_cep(sCepDestino)
        nCdServico = self.ajuste_nCdServico(nCdServico, self.nCdServico)
        return self.api.CalcPrazo(sCepOrigem=sCepOrigem, sCepDestino=sCepDestino, nCdServico=nCdServico)

    def CalcPrecoPrazo(self, volume, sCepDestino, sCepOrigem=None, nCdServico=None, sCdMaoPropria: bool=None,
                       sCdAvisoRecebimento: bool=None, nValDeclarado = None):
        if not isinstance(volume, Volume):
            raise(RuntimeError('Calc: Parametro volume precisa ser um objeto Volume.'))

        if not volume.peso:
            raise (RuntimeError('Calc: Informacao de peso é obrigatória em um volume.'))

        nValDeclarado = nValDeclarado if nValDeclarado is not None else volume.valor_declarado
        sCepDestino = self.ajuste_cep(sCepDestino)
        sCepOrigem = self.ajuste_cep(sCepOrigem, self.sCepOrigem)
        nCdServico = self.ajuste_nCdServico(nCdServico, self.nCdServico)

        sCdMaoPropria = sCdMaoPropria if sCdMaoPropria is not None else self.sCdMaoPropria
        sCdAvisoRecebimento = sCdAvisoRecebimento if sCdAvisoRecebimento is not None else self.sCdAvisoRecebimento

        r = self.api.calcPrecoPrazo(nCdServico=nCdServico, sCepOrigem=sCepOrigem, sCepDestino=sCepDestino,
                                    sCdMaoPropria=sCdMaoPropria, sCdAvisoRecebimento=sCdAvisoRecebimento,
                                    nValDeclarado=nValDeclarado, StrRetorno='XML', nIndicaCalculo='3',
                                    **volume.params_calc(), **self.auth_dict)

    def get_client(self):
        return self.client

    @classmethod
    def ajuste_nCdServico(cls, nCdServico, value_if_none=None):
        if nCdServico is not None:
            if isinstance(nCdServico, str):
                nCdServico = [nCdServico]
            elif not isinstance(nCdServico, list):
                raise(RuntimeError('Parametro nCdServico invalido!'))
        else:
            nCdServico = value_if_none
        return nCdServico

    @classmethod
    def ajuste_cep(cls, cep, value_if_none=None):
        if cep is not None:
            if isinstance(cep, str):
                cep = CEP(cep).cep8
            elif isinstance(sCepOrigem, CEP):
                cep = cep.cep8
            else:
                raise(RuntimeError('Parametro sCepOrigem ou sCepDestino invalido!'))
        else:
            cep = value_if_none
        return cep
