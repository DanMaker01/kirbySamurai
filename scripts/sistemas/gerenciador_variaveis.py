class GerenciadorVariaveis:
    def __init__(self):
        self.vars = {}

    def set(self, chave, valor):
        self.vars[chave] = valor

    def get(self, chave, default=None):
        return self.vars.get(chave, default)

    def limpar(self):
        self.vars.clear()
