from .CEP import CEP
from .credenciais import Credenciais


class CartaoPostagem:
    def __init__(self, num_cartao: str, credenciais, nome: str = None, cep_origem_padrao = None):
        self.num_cartao = num_cartao
        self.credenciais = credenciais
        self.nome = nome
        self.cep_origem = cep_origem_padrao

        if not isinstance(credenciais, Credenciais):
            raise (RuntimeError('Parametro credenciais invalido!'))

        if cep_origem_padrao is not None:
            if isinstance(cep_origem_padrao, str):
                self.cep_origem = CEP(cep_origem_padrao)
            elif not isinstance(self.cep_origem, CEP):
                raise(RuntimeError('Parametro cep_origem_padrao invalido!'))

    def get_credenciais(self):
        return self.credenciais

    def cep_origem_padrao(self):
        return self.cep_origem
