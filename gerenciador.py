
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
from camera import Camera

class Gerenciador:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.tempo_atual = pygame.time.get_ticks()
        self.controle_travado = False

        # Subsistemas
        self.persistencia_placar = Persistencia()
        self.placar = Placar()
        self.gerenciador_atores = Gerenciador_Atores()
        self.gerenciador_som    = Gerenciador_Som()
        self.gerenciador_tela   = GerenciadorTela()
        self.camera             = Camera(largura_tela=WIDTH, altura_tela=HEIGHT)
        self.gerenciador_eventos= GerenciadorEventos(self.gerenciador_tela, self.gerenciador_atores,self.camera)
        # Preparar cena e roteiro

        self._criar_atores()
        self._setup_eventos()

    def _setup_eventos(self):
        # self.gerenciador_eventos.adicionar_camera_move(1,10,0)
        self.gerenciador_eventos.adicionar_fade_in(2000)
        # self.gerenciador_eventos.adicionar_fade_in(1000)
        # self.gerenciador_eventos
        # self.gerenciador_eventos.adicionar_camera_move(1000,100,0)
        # self.gerenciador_eventos.adicionar_camera_move(1000,0,0)
        # self.gerenciador_eventos.adicionar_camera_move(1000,-100,0)
        # self.gerenciador_eventos.adicionar_camera_move(1000,0,0)
        # self.gerenciador_eventos.adicionar_espera(1000)
        self.gerenciador_eventos.adicionar_espera(1000)
        self.gerenciador_eventos.adicionar_ator_move(1000,) <<<<<<<<<<<<<<<<<<<<<<???????
        # self.gerenciador_eventos.adicionar_fade_out(500)

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
        self.camera.atualizar(dt)

    def draw(self):
        self.screen.fill((0, 0, 0))  # Preenche a tela com preto (vazio)

        # atualizar aqui???? sim
        # cada classe vai agir dependendo da camera?
        self.gerenciador_atores.draw(self.screen, (-self.camera.pos_x, -self.camera.pos_y)) # deve receber uma defasagem pela câmera
        # self.gerenciador_eventos.desenhar(self.screen) #atualmente não faz nada, retirar???
        self.gerenciador_tela.desenhar(self.screen)
        self.placar.draw(self.screen)
        print("self.camera.pos::\t", self.camera.pos_x, self.camera.pos_y, " -> ",self.camera.objetivo_x, self.camera.objetivo_y)

    def input(self, acao):
        print(f"[ {acao} ]")
        if self.gerenciador_eventos.eventos_ativos() or self.gerenciador_tela.esta_em_fade():
            print("Entrada ignorada: controle travado por evento ou fade.")
            return
        # self.gerenciador_atores.input(acao)
