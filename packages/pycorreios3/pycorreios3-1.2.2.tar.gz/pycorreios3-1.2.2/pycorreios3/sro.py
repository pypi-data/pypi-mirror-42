from .correios_webservice_client import CorreiosWSClient
from .credenciais import Credenciais

TIPO_LISTA = 'L'
TIPO_INTERVALO = 'F'
RESULTADO_TODOS = 'T'
RESULTADO_ULTIMO = 'U'
LINGUA_PT = '101'
LINGUA_EN = '102'


class SRO:

    def __init__(self, credenciais=None, usuario: str=None, senha: str=None, tipo: str=TIPO_LISTA,
                 resultado: str=RESULTADO_TODOS, lingua: str=LINGUA_PT, client = None):

        if credenciais is not None:
            if not isinstance(credenciais, Credenciais):
                raise(RuntimeError('SRO: Parametro credenciais de tipo invalido!'))

            if (credenciais.usuario_sro is not None and usuario is not None and credenciais.usuario_sro != usuario) or \
               (credenciais.senha_sro is not None and senha is not None and credenciais.senha_sro != senha):
                raise(RuntimeError('SRO: Credenciais duplicadas e divergentes!'))

            self.usuario = usuario if usuario is not None else credenciais.usuario_sro
            self.senha = senha if senha is not None else credenciais.senha_sro
        elif usuario is None or senha is None:
            raise (RuntimeError('SRO: usuario e/ou senha não informados!'))
        else:
            self.usuario = usuario
            self.senha = senha

        self.client = client if client is not None else CorreiosWSClient()
        self.client.load_api_sro()
        self.api = self.client.api_sro.service
        self.tipo = tipo
        self.resultado = resultado
        self.lingua = lingua

    @classmethod
    def new_homologacao(cls):
        return cls(usuario="ECT", senha="SRO", resultado=RESULTADO_ULTIMO)

    def buscaEventosLista(self, objetos, tipo: str=None, resultado: str=None, lingua: str=None):

        tipo = tipo if tipo is not None else self.tipo
        resultado = resultado if resultado is not None else self.resultado
        lingua = lingua if lingua is not None else self.lingua

        if isinstance(objetos, str):
            objetos = [objetos]
        elif not isinstance(objetos, list):
            raise(RuntimeError('SRO: Parametro objetos de tipo invalido!'))
        elif len(objetos) == 0:
            return None

        r = self.api.buscaEventosLista(usuario=self.usuario, senha=self.senha, objetos=objetos,
                                                             tipo=tipo, resultado=resultado, lingua=lingua)

        return r
