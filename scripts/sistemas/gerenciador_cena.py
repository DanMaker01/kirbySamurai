#######################################################################
# Gerenciador_Cena
#######################################################################
# Controla os Roteiros, Atores, Interação do Jogador?
####################################################################### 
# # Atributos
# self.roteiros = []
# self.roteiro_atual : Roteiro
#  
# # Métodos 
# chama_roteiro(ev01)
# is_esperando()
# is_em_fade()
# update() 
# 
# - Provavelmente vai ser integrado ao Gerenciador_Cena ??? implementar
#######################################################################
from scripts.core.roteiro import Pagina
class Gerenciador_Cena:
    def __init__(self):
        self.fila_paginas = []
        self.pagina_atual = None
    
    def update(self, dt):
        if self.pagina_atual:
            pass
        else:
            pass
