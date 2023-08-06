
class Credenciais:

    def __init__(self, cnpj: str = None, num_contrato: str = None, cod_adm: str = None,
                 senha_sigep: str = None, senha_sro: str = None, senha_calc: str = None,
                 usuario_sigep: str = None, usuario_sro: str = None, usuario_calc: str = None,
                 usuario_idcorreios: str = None, senha_idcorreios: str = None):

        if cnpj is not None:
            cnpj = "".join(filter(lambda x: x.isdigit(), cnpj))
            assert len(cnpj) == 14

        if cnpj is not None and senha_calc is None:
            senha_calc = cnpj[:8]

        if senha_calc is not None and usuario_calc is None:
            usuario_calc = cod_adm

        if senha_sro is not None and usuario_sro is None:
            usuario_sro = num_contrato

        if senha_sigep is not None and usuario_sigep is None:
            usuario_sigep = cnpj

        self.cnpj = cnpj
        self.num_contrato = num_contrato
        self.cod_adm = cod_adm
        self.usuario_calc = usuario_calc
        self.senha_calc = senha_calc
        self.usuario_sro = usuario_sro
        self.senha_sro = senha_sro
        self.usuario_sigep = usuario_sigep
        self.senha_sigep = senha_sigep
        self.usuario_idcorreios = usuario_idcorreios
        self.senha_idcorreios = senha_idcorreios


    def get_cred_calc(self):
        if self.senha_calc is None or self.usuario_calc is None:
            raise(RuntimeError('Credenciais para serviço CalcPrecoPrazo não definidas.'))

        return self.usuario_calc, self.senha_calc

    def get_cred_sro(self):
        if self.senha_sro is None or self.usuario_sro is None:
            raise(RuntimeError('Credenciais para serviço SRO/Rastro não definidas.'))

        return self.usuario_sro, self.senha_sro

    def get_cred_sigep(self):
        #if self.senha_sigep is None or self.usuario_sigep is None or self.num_contrato is None:
        #    raise (RuntimeError('Credenciais para serviço SIGEP não definidas.'))

        return self.usuario_sigep, self.senha_sigep, self.cnpj, self.num_contrato, self.cod_adm

    def get_cred_idcorreios(self):
        return self.usuario_idcorreios, self.senha_idcorreios
