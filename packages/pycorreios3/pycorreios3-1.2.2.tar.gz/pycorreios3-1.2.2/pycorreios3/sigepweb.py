from .correios_webservice_client import CorreiosWSClient
from .credenciais import Credenciais
from .cartao_postagem import CartaoPostagem

HOMOLOGACAO_USUARIO = 'sigep'
HOMOLOGACAO_SENHA = 'n5f9t8'
HOMOLOGACAO_COD_ADM = '17000190'
HOMOLOGACAO_CONTRATO = '9992157880'
HOMOLOGACAO_CARTAO = ['0067599079']
HOMOLOGACAO_CNPJ = '34028316000103'

class SigepWeb:
    def __init__(self, credenciais, lista_num_cartoes_postagem: list, producao: bool=False, client = None):
        if client is not None:
            if client.producao != producao:
                raise(RuntimeError("Cliente e Sigep com parametros 'producao' divergentes"))
            client.load_api_sigep()
        else:
            client = CorreiosWSClient(load_api_sigep=True, producao=producao)

        self.client = client
        self.api = self.client.api_sigep.service

        if not isinstance(credenciais, Credenciais):
            if producao:
                raise(RuntimeError("Paramentro 'credenciais' inválido!" ))
            else:
                credenciais = Credenciais(cnpj=HOMOLOGACAO_CNPJ, num_contrato=HOMOLOGACAO_CONTRATO,
                                          cod_adm=HOMOLOGACAO_COD_ADM, senha_sigep=HOMOLOGACAO_SENHA,
                                          usuario_sigep=HOMOLOGACAO_USUARIO)
                lista_num_cartoes_postagem = HOMOLOGACAO_CARTAO

        self.usuario, self.senha, self.cnpj, self.num_contrato, self.cod_adm = credenciais.get_cred_sigep()

        self.auth = {'usuario': self.usuario, 'senha': self.senha}

        self.cartoes_postagem = {}

        for c in lista_num_cartoes_postagem:
            self.add_cartao_postagem(c)

    def add_cartao_postagem(self, num_cartao: str):
        r = self.api.getStatusCartaoPostagem(numeroCartaoPostagem=num_cartao, **self.auth)
        resultado = r['return']
        if resultado == 'Cancelado':
            return None
        elif resultado == 'Normal':
            r = self.buscaCliente(num_cartao)
            print(r)

    def getStatusCartaoPostagem(self, numero_cartao_postagem: str):
        r = self.api.getStatusCartaoPostagem(numeroCartaoPostagem=numero_cartao_postagem, **self.auth)

        resultado = r['return']
        if resultado == 'Cancelado':
            return False
        elif resultado == 'Normal':
            return True
        else:
            raise(RuntimeError('Erro processando o retorno de getStatusCartaoPostagem.'))
