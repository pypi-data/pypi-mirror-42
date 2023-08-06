FORMATO_CAIXA_OU_PACOTE = 1
FORMATO_ROLO_OU_PRISMA = 2
FORMATO_ENVELOPE = 3


class Volume:
    def __init__(self, formato, comprimento, altura, largura, diametro, peso, valor_declarado):
        self.formato = formato
        self.comprimento = comprimento
        self.altura = altura
        self.largura = largura
        self.diametro = diametro
        self.peso = peso
        self.valor_declarado = valor_declarado

        self.caixa_pacote = False
        self.rolo_prisma = False
        self.envelope = False

        if formato == FORMATO_CAIXA_OU_PACOTE:
            self.caixa_pacote = True
            if self.diametro: raise(RuntimeError('Diâmetro não deve ser especificado para uma caixa/pacote.'))
        elif formato == FORMATO_ROLO_OU_PRISMA:
            self.rolo_prisma = True
            if self.altura: raise (RuntimeError('Altura não deve ser especificada para um rolo ou prisma.'))
            if self.largura: raise (RuntimeError('Largura não deve ser especificada para uma caixa/pacote.'))
        elif formato == FORMATO_ENVELOPE:
            self.envelope = True
            if self.altura: raise (RuntimeError('Altura não deve ser especificada para um envelope.'))
            if self.diametro: raise (RuntimeError('Diâmetro não deve ser especificado para um envelope.'))
        else:
            raise(RuntimeError('Tipo inválido'))

    def params_calc(self, inclui_val_declarado: bool=False):
        d = {'nCdFormato': self.formato,
             'nVlPeso': self.peso,
             'nVlComprimento': self.comprimento,
             'nVlAltura': self.altura,
             'nVlLargura': self.largura,
             'nVlDiametro': self.diametro}
        if inclui_val_declarado:
            d['nVlDeclarado'] = self.valor_declarado
        return d

    @classmethod
    def new_caixa_ou_pacote(cls, comprimento=20, altura=20, largura=20, peso=0, valor_declarado=0):
        return cls(formato=FORMATO_CAIXA_OU_PACOTE, comprimento=comprimento, altura=altura, largura=largura, peso=peso,
                   valor_declarado=valor_declarado)

    @classmethod
    def new_envelope(cls, comprimento=20, largura=20, peso=0, valor_declarado=0):
        return cls(formato=FORMATO_CAIXA_OU_PACOTE, comprimento=comprimento, largura=largura, peso=peso,
                   valor_declarado=valor_declarado)

    @classmethod
    def new_rolo_ou_prisma(cls, comprimento=20, diametro=20, peso=0, valor_declarado=0):
        return cls(tipo=FORMATO_CAIXA_OU_PACOTE, comprimento=comprimento, diametro=diametro, peso=peso,
                   valor_declarado=valor_declarado)

