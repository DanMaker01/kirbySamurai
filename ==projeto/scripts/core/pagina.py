##################################################################
# Pagina
##################################################################
# Modular: Não
# Finalizada: Não
##################################################################
# A Fazer:
# - 
# - 
##################################################################
# Pensar em implementar:
# - Lista de condições
# - Animação fica na pagina, mas também vai haver Evento de trocar animação
# - Tipos de trigger: Click, Touch, Auto (? futuro ?) (talvez não precise)
# - 
# - 
##################################################################


# from scripts.core.animacao import Animacao
class Pagina:
    # def __init__(self, condicao=None, lista_eventos=None, animacao=None):
    def __init__(self, condicao=None, lista_eventos=None):
        # self.animacao :Animacao = animacao
        self.condicao = condicao  # Ex: "fase>=2" ou "invisivel==False"
        self.lista_eventos = lista_eventos if lista_eventos else []
        pass

    def __repr__(self):
        return f"Pagina(condicao='{self.condicao}', num_eventos={len(self.lista_eventos)})"
