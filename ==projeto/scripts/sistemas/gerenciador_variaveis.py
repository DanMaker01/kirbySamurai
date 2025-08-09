##################################################
# Gerenciador de Variáveis
##################################################
# Armazena as variávei
##################################################
# Modular: Sim
# Finalizado: Sim
##################################################


class GerenciadorVariaveis:
    def __init__(self):
        self.vars = {}

    def set(self, chave, valor):
        print("chave",chave, "valor",self.vars[chave])
        self.vars[chave] = valor

    def get(self, chave, default=None):
        return self.vars.get(chave, default)

    def limpar(self):
        self.vars.clear()
