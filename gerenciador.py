
###########################
# Gerenciador
###########################
# Orquestra os sistemas modulares
###########################
# Modular: Não
# Finalizada: Não
###########################
# A Fazer: 
# - Incluir sistemas
# - Assim que estiver funcionando, modularizar mais
# - 
###########################

from placar import Placar
from persistencia import Persistencia
# sub-sistemas
from gerenciador_atores import Gerenciador_Atores
from gerenciador_som import Gerenciador_Som
from gerenciador_eventos import GerenciadorEventos
from gerenciador_tela import GerenciadorTela
from config import *
from ator import Ator
from animacao import Animacao
import pygame
from evento import *

class Gerenciador:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.tempo_atual = pygame.time.get_ticks()
        self.controle_travado = False

        # Subsistemas
        self.placar = Placar()
        self.persistencia_placar = Persistencia()
        self.gerenciador_atores = Gerenciador_Atores()
        self.gerenciador_som = Gerenciador_Som()
        self.gerenciador_tela = GerenciadorTela(largura_mundo=1600, altura_mundo=1200)
        self.gerenciador_eventos = GerenciadorEventos(self.gerenciador_tela)

        self._criar_atores()
        self._setup_eventos()

    def _setup_eventos(self):
        self.gerenciador_eventos.adicionar_fade_in(2000)
        self.gerenciador_eventos.adicionar_espera(1000)
        self.gerenciador_eventos.adicionar_espera(1000)
        self.gerenciador_eventos.adicionar_fade_out(2000)
        self.gerenciador_eventos.adicionar_fade_in(200)
        self.gerenciador_eventos.adicionar_fade_out(200)
        self.gerenciador_eventos.adicionar_fade_in(200)
        self.gerenciador_eventos.adicionar_fade_out(200)

    def _criar_atores(self):
        triangulo_sup = Ator(animacoes={"padrao": Animacao(["triangulo_sup.png"])})
        triangulo_inf = Ator(animacoes={"padrao": Animacao(["triangulo_inf.png"])})

        self.gerenciador_atores.adicionar_ator("triangulo_sup", triangulo_sup)
        self.gerenciador_atores.adicionar_ator("triangulo_inf", triangulo_inf)

    def update(self, dt):
        self.tempo_atual = pygame.time.get_ticks()
        self.gerenciador_eventos.atualizar(self.tempo_atual)
        self.gerenciador_tela.atualizar(self.tempo_atual, dt)
        self.gerenciador_atores.update(dt)

    def draw(self):
        self.gerenciador_atores.draw(self.screen)
        self.placar.draw(self.screen)
        self.gerenciador_eventos.desenhar(self.screen)
        self.gerenciador_tela.desenhar(self.screen)

    def input(self, acao):
        print(f"[ {acao} ]")
        if self.gerenciador_eventos.eventos_ativos() or self.gerenciador_tela.esta_em_fade():
            print("Entrada ignorada: controle travado por evento ou fade.")
            return
        # self.gerenciador_atores.input(acao)
