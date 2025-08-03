from scripts.core.janela import *

class GerenciadorJanelas:
    def __init__(self):
        self.janelas = {}  # nome: {instancia, ativa, pai}
        self.ordem_desenho = []  # ordem de adição (z-index implícito)
        self.nome_foco = None  # só uma janela com foco

    def adicionar_janela(self, nome, janela, ativa=True, pai=None, foco=False):
        self.janelas[nome] = {
            "instancia": janela,
            "ativa": ativa,
            "pai": pai
        }
        self.ordem_desenho.append(nome)

        if foco or self.nome_foco is None:
            self.definir_foco(nome)

    def remover_janela(self, nome):
        if nome in self.janelas:
            del self.janelas[nome]
            self.ordem_desenho.remove(nome)
            if self.nome_foco == nome:
                self.nome_foco = None

    def ativar(self, nome):
        if nome in self.janelas:
            self.janelas[nome]["ativa"] = True

    def desativar(self, nome):
        if nome in self.janelas:
            self.janelas[nome]["ativa"] = False
            if self.nome_foco == nome:
                self.nome_foco = None

    def esta_ativa(self, nome):
        return self.janelas.get(nome, {}).get("ativa", False)

    def definir_foco(self, nome):
        if nome in self.janelas and self.janelas[nome]["ativa"]:
            self.nome_foco = nome

    def tem_foco(self, nome):
        return self.nome_foco == nome

    def janela_com_foco(self):
        return self.janelas.get(self.nome_foco, {}).get("instancia", None)

    def get(self, nome):
        return self.janelas.get(nome, {}).get("instancia", None)

    def __getitem__(self, nome):
        return self.get(nome)

    def desenhar(self, surface):
        for nome in self.ordem_desenho:
            if self.esta_ativa(nome) and self.janelas[nome]["pai"] is None:
                self._desenhar_com_subjanelas(nome, surface)

    def _desenhar_com_subjanelas(self, nome, surface):
        janela = self.janelas[nome]["instancia"]
        janela.desenhar(surface)

        for subnome in self.ordem_desenho:
            if self.esta_ativa(subnome) and self.janelas[subnome]["pai"] == nome:
                self._desenhar_com_subjanelas(subnome, surface)

    def listar_ativas(self):
        return [n for n in self.ordem_desenho if self.esta_ativa(n)]

    def listar_todas(self):
        return self.ordem_desenho.copy()

    def resetar(self):
        self.janelas.clear()
        self.ordem_desenho.clear()
        self.nome_foco = None

    # def atualizar(self):
    #     if len(self.listar_ativas() >= 1):
