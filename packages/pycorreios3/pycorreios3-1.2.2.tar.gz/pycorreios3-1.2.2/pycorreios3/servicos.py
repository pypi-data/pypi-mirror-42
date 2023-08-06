import collections


DISPONIVEL_CONTRATO = 1
DISPONIVEL_VAREJO = 2

SENTIDO_ENTREGA = 1
SENTIDO_REVERSO = 2
SENTIDO_ENTREGA_E_COLETA = 3

PAGTO_A_VISTA = 1
PAGTO_NA_ENTREGA = 2
PAGTO_FATURADO = 3

PAGO_DESTINATARIO = 1
PAGO_REMETENTE = 2

CATEGORIA_STANDARD = "standard"
CATEGORIA_EXPRESSO = "expresso"
CATEGORIA_PREMIUM = "premium"

SERVICOS_VAREJO_A_VISTA =\
    [{"codigo": "04510", "categoria": "standard", "familia": "PAC", "nome": "PAC à vista"},
     {"codigo": "04014", "categoria": "expresso", "familia": "SEDEX", "nome": "SEDEX à vista"},
     {"codigo": "40169", "categoria": "premium", "familia": "SEDEX 12", "nome": "SEDEX 12 à vista"},
     {"codigo": "40215", "categoria": "premium", "familia": "SEDEX 10", "nome": "SEDEX 10 à vista"},
     {"codigo": "40290", "categoria": "premium", "familia": "SEDEX Hoje", "nome": "SEDEX Hoje"}]

SERVICOS_VAREJO_A_COBRAR =\
    [{"codigo": "04707", "categoria": "standard", "familia": "PAC", "nome": "PAC à vista pagamento na entrega"},
     {"codigo": "04065", "categoria": "expresso", "familia": "SEDEX", "nome": "SEDEX à vista pagamento na entrega"}]


CODIGOS_SERVICOS_VAREJO = list(map(lambda x: x.codigo, SERVICOS_VAREJO_A_VISTA + SERVICOS_VAREJO_A_COBRAR))

class Servico:
    def __init__(self, codigo, nome, categoria, familia='', quem_paga=PAGO_REMETENTE, quando_paga=None,
                 sentido=SENTIDO_ENTREGA, disponibilidade=None, id=None, cartoes_postagem=None):
        self.id = id
        self.cartoes_postagem = cartoes_postagem
        self.codigo = codigo
        self.categoria = categoria
        self.familia = familia
        self.nome = nome
        self.disponibilidade = disponibilidade
        self.sentido = sentido
        self.quem_paga = quem_paga
        self.quando_paga = quando_paga

        if not disponibilidade:
            if codigo in CODIGOS_SERVICOS_VAREJO:
                self.servico_varejo = True
            else:
                self.servico_contrato = True
        else:
            self.servico_varejo = (disponibilidade == DISPONIVEL_VAREJO)
            self.servico_contrato = (disponibilidade == DISPONIVEL_CONTRATO)

        if not (self.servico_contrato or self.servico_varejo):
            raise (RuntimeError('Parametro disponibilidade com valor invalido.'))

        self.entrega = (sentido == SENTIDO_ENTREGA)
        self.reverso = (sentido == SENTIDO_REVERSO)
        self.entrega_e_coleta = (sentido == SENTIDO_ENTREGA_E_COLETA)

        if not (self.entrega or self.reverso or self.entrega_e_coleta):
            raise (RuntimeError('Parametro sentido com valor invalido.'))

        self.remetente_paga = (quem_paga == PAGO_REMETENTE)
        self.destinatario_paga = (quem_paga == PAGO_DESTINATARIO)

        if not (self.remetente_paga or self.destinatario_paga):
            raise(RuntimeError('Parametro quem_e_cobrado com valor invalido.'))

        if not quando_paga:
            if self.servico_varejo:
                self.faturado = False
                self.a_vista = self.remetente_paga
                self.na_entrega = self.destinatario_paga
            if self.servico_contrato:
                self.a_vista = False
                self.na_entrega = self.destinatario_paga
                self.faturado = self.remetente_paga
        else:
            self.a_vista = (quando_paga == PAGTO_A_VISTA)
            self.na_entrega = (quando_paga == PAGTO_NA_ENTREGA)
            self.faturado = (quando_paga == PAGTO_FATURADO)

        if not (self.a_vista or self.na_entrega or self.faturado):
            raise (RuntimeError('Parametro quando_paga com valor inválido.'))

    @classmethod
    def new_servico_contrato(cls, codigo, nome, categoria, familia='', quem_paga=PAGO_REMETENTE, quando_paga=PAGTO_FATURADO,
                             sentido=SENTIDO_ENTREGA):
        return cls(codigo=codigo, nome=nome, categoria=categoria, familia=familia, quem_paga=quem_paga, quando_paga=quando_paga,
                   sentido=sentido, disponibilidade=DISPONIVEL_CONTRATO)

    @classmethod
    def new_servico_varejo(cls, codigo, nome, categoria, quem_paga, familia=''):
        if quem_paga == PAGO_REMETENTE:
            quando_paga = PAGTO_A_VISTA
        elif quem_paga == PAGO_DESTINATARIO:
            quando_paga = PAGTO_NA_ENTREGA
        else:
            raise(RuntimeError('Parametro quem_paga com valor invalido.'))

        return cls(codigo=codigo, nome=nome, categoria=categoria, familia=familia, quem_paga=quem_paga,
                   quando_paga=quando_paga, sentido=SENTIDO_ENTREGA, disponibilidade=DISPONIVEL_VAREJO)

    @classmethod
    def servicos_varejo(cls):
        arr = []

        for i in SERVICOS_VAREJO_A_VISTA:
            i['quem_paga'] = PAGO_REMETENTE
            arr.append(cls.new_servico_varejo(**i))

        for i in SERVICOS_VAREJO_A_COBRAR:
            i['quem_paga'] = PAGO_DESTINATARIO
            arr.append(cls.new_servico_varejo(**i))

        return arr


class CarteiraServicos:
    def __init__(self, array_de_obj_servico=[]):
        self.servicos = collections.OrderedDict
        self.add(array_de_obj_servico)

    def new_from_sigepweb(self, sigepweb):
        sigepweb.servicos.buscaCliente()

    def add(self, servico):
        count = 0
        if isinstance(servico, Servico):
            self.servicos[servico.codigo] = servico
            count = 1
        else:
            for s in servico:
                self.servicos[s.codigo] = s
                count += 1

        return count

    def codigos(self):
        return list(map(lambda x: x.codigo, self.servicos.items()))

    def filter(self, familias: list=None, categorias: list=None, ids: list = None, cartoes_postagem: list = None,
               nomes: list=None, contrato: bool=None, varejo: bool=None,
               entrega: bool=None, reverso: bool=None, entrega_e_coleta: bool=None,
               pago_destinatario: bool=None, pago_remetente: bool=None,
               pagto_a_vista: bool=None, pagto_na_entrega: bool=None, pagto_faturado: bool=None,
               arr_servicos: list=None):

        arr = self.servicos.items() if arr_servicos is None else arr_servicos

        if familias is not None:
            arr = filter((lambda x: x.familia in familias), arr)

        if categorias is not None:
            arr = filter((lambda x: x.categoria in categorias), arr)

        if ids is not None:
            arr = filter((lambda x: x.id in ids), arr)

        if cartoes_postagem is not None:
            arr = filter((lambda x: x.id in ids), arr)

        if nomes is not None:
            arr = filter((lambda x: x.nome in nomes), arr)

        if contrato is not None:
            arr = filter((lambda x: (x.servico_contrato == contrato)), arr)

        if varejo is not None:
            arr = filter((lambda x: (x.servico_varejo == varejo)), arr)

        if pago_destinatario is not None:
            arr = filter((lambda x: (x.destintario_paga == pago_destinatario)), arr)

        if pago_remetente is not None:
            arr = filter((lambda x: (x.remetente_paga == pago_remetente)), arr)

        if entrega is not None or reverso is not None or entrega_e_coleta is not None:
            arr = filter((lambda x: (x.entrega if entrega is not None else None,
                                     x.reverso if reverso is not None else None,
                                     x.entrega_e_coleta if entrega_e_coleta is not None else None)
                                    == (entrega. reverso. entrega_e_coleta)), arr)

        if pagto_a_vista is not None or pagto_na_entrega is not None or pagto_faturado is not None:
            arr = filter((lambda x: (x.a_vista if pagto_a_vista is not None else None,
                                     x.na_entrega if pagto_na_entrega is not None else None,
                                     x.faturado if pagto_faturado is not None else None)
                                    == (pagto_a_vista. pagto_na_entrega. pagto_faturado)), arr)

        return arr
