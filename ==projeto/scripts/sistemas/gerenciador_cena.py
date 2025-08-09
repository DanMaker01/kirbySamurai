#######################################################################
# Gerenciador_Cena
#######################################################################
# Controla os Roteiros, Atores, algo mais? Diálogos? 
# Interação do Jogador??? acho que não...
# 
####################################################################### 
#  
##### Atributos
# self.roteiros = []
# self.roteiro_atual : Roteiro
#  
##### Métodos 
# chama_roteiro(ev01)
# is_esperando()
# is_em_fade()
# update() 
# 
##### Obs.  
# vai ter duas páginas acontecendo ao mesmo tepmo? no RPGMaker tem, pq existem paralel process
# Fazer testes com roteiros
#######################################################################
from scripts.core.roteiro import Pagina, Roteiro
class Gerenciador_Cena:
    def __init__(self):
        self.fila_paginas = []
        self.pagina_atual : Pagina = None
    
    def update(self, dt):
        if self.pagina_atual:
            pass
        else:
            pass
