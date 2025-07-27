##################################################################
# Pagina
##################################################################
# Modular: Sim
# Finalizada: Não
##################################################################
# A Fazer:
# - Tipos de trigger: Click, Touch, Auto
# - Animação fica na pagina, mas também vai haver Evento de trocar animação
# - 
##################################################################
from scripts.core.animacao import Animacao
class Pagina:
    def __init__(self, condicao=None, lista_eventos=None, animacao=None):
        self.condicao = condicao  # Ex: "fase>=2" ou "invisivel==False"
        self.lista_eventos = lista_eventos if lista_eventos else []
        
        self.animacao :Animacao = animacao
        TRIGGER = {
            'click':1,
            'touch':2,
            'auto':3,
        }
        self.trigger = TRIGGER['click'] #padrao

    def __repr__(self):
        return f"Pagina(condicao='{self.condicao}', eventos={len(self.lista_eventos)})"
