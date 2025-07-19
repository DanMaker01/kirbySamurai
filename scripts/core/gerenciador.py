
######################################################
# Gerenciador
######################################################
# Orquestra os sistemas modulares
######################################################
# Modular: Não
# Finalizada: Não
######################################################
# A Fazer: 
# - Inventario 
# - GerenciadorVariaveis
# - GerenciadorEscolhas
# - Dialogo
# - GerenciadorCena
# - Roteiro???? cena já resolve?
######################################################

import pygame
import random
# sub-sistemas
from scripts.sistemas.gerenciador_atores import Gerenciador_Atores
from scripts.sistemas.gerenciador_som import Gerenciador_Som
from scripts.sistemas.gerenciador_eventos import GerenciadorEventos
from scripts.sistemas.gerenciador_tela import GerenciadorTela
from scripts.sistemas.gerenciador_controle import Gerenciador_Controle
#
from scripts.core.config import *
from scripts.core.placar import Placar
from scripts.core.persistencia import Persistencia
from scripts.core.animacao import Animacao
from scripts.core.evento import *
from scripts.core.camera import Camera
#
from scripts.atores.ator import Ator

######################################################
class Gerenciador:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.tempo_atual = pygame.time.get_ticks()

        # Subsistemas
        self.persistencia_placar = Persistencia()
        self.placar = Placar()
        self.gerenciador_atores = Gerenciador_Atores()
        self.gerenciador_som    = Gerenciador_Som()
        self.gerenciador_tela   = GerenciadorTela()
        self.gerenciador_controle=Gerenciador_Controle()
        self.camera             = Camera(largura_tela=WIDTH, altura_tela=HEIGHT)

        self.gerenciador_eventos= GerenciadorEventos(self.gerenciador_controle, 
                                                     self.gerenciador_tela, 
                                                     self.gerenciador_atores,
                                                     self.camera)
        # Preparar cena e roteiro
        self.reset()
        
    def reset(self):
        self._criar_atores()
        self._setup_eventos()

    def _criar_atores(self):
        # 
        triangulo_sup = Ator(pos = (-360,0), animacoes={
            "padrao": Animacao(["triangulo_sup2.png"])})
        
        triangulo_inf = Ator(pos = (360,0), 
                             animacoes={"padrao": Animacao(["triangulo_inf2.png",])})
        #
        y_geral = 150
        player1 = Ator(pos = (20,20+y_geral), animacoes={
            "parado": Animacao( ["p1_parado.png"] ),
            "ataque": Animacao( ["p1_ataque.png"] )
            })

        player2 =  Ator(pos = (240,30+y_geral), animacoes={
            "parado": Animacao( ["p2_parado.png"] ),
            "ataque": Animacao( ["p2_ataque.png"] )
            })

        largada =  Ator(pos = (WIDTH/2-30,HEIGHT/6), 
                        animacoes={"parado": Animacao( ["largada00.png","largada01.png"] )},
                        visivel=False)
        
        # adiciona
        self.gerenciador_atores.adicionar_ator('p1', player1)
        self.gerenciador_atores.adicionar_ator('p2', player2)
        self.gerenciador_atores.adicionar_ator("t1", triangulo_sup)
        self.gerenciador_atores.adicionar_ator("t2", triangulo_inf)
        self.gerenciador_atores.adicionar_ator("largada", largada)

    def _setup_eventos(self):
        self.gerenciador_eventos.adicionar_espera(0)
        self.gerenciador_eventos.adicionar_input_lock(True)
        
        self.gerenciador_eventos.adicionar_espera(2000)
        self.gerenciador_eventos.adicionar_fade_in(2000)

        self.gerenciador_eventos.adicionar_espera(1000)

        self.gerenciador_eventos.adicionar_espera(3000)
        self.gerenciador_eventos.adicionar_ator_move(3000,'t1',-10,0) 
        self.gerenciador_eventos.adicionar_ator_move(3000,'t2',10,0) 
        
        # self.gerenciador_eventos.adicionar_espera(5000)
        # self.gerenciador_eventos.adicionar_espera(5000)
        
        self.gerenciador_eventos.adicionar_espera(2000)
        #
        self.gerenciador_eventos.adicionar_espera(3000)
        self.gerenciador_eventos.adicionar_ator_move(3000,'t1',-360,0) 
        self.gerenciador_eventos.adicionar_ator_move(3000,'t2',360,0) 

        self.gerenciador_eventos.adicionar_espera(500)

        self.gerenciador_eventos.adicionar_espera(3000)
        self.gerenciador_eventos.adicionar_fade_out(3000)
        
        tempo_random_largada = random.randint(2000, 4000)
        self.gerenciador_eventos.adicionar_espera(tempo_random_largada)
        self.gerenciador_eventos.adicionar_input_lock(False)
        
        self.gerenciador_eventos.adicionar_espera(0)
        self.gerenciador_eventos.adicionar_fade_in(0)
        self.gerenciador_eventos.adicionar_ator_set_visibilidade('largada',True)
        
        
        #libera o controle, ativa contador, ...
        self.gerenciador_eventos.adicionar_espera(4000)

        # trava o controle, ninguem reagiu
        self.gerenciador_eventos.adicionar_espera(0)
        self.gerenciador_eventos.adicionar_ator_set_visibilidade('largada',False)
        self.gerenciador_eventos.adicionar_input_lock(True)
        
        self.gerenciador_eventos.adicionar_espera(2000)
        self.gerenciador_eventos.adicionar_fade_out(2000)
        
        self.gerenciador_eventos.adicionar_espera(1000)
        self.gerenciador_eventos.adicionar_limpa_eventos(callback=self.reset)

    def update(self, dt):
        self.tempo_atual = pygame.time.get_ticks()
        self.gerenciador_eventos.atualizar(self.tempo_atual)
        self.gerenciador_tela.atualizar(self.tempo_atual, dt)
        self.gerenciador_atores.update(dt)
        self.camera.atualizar(dt)
        self.placar.atualizar(dt)

    def draw(self):
        self.screen.fill((0, 0, 0))  # Preenche a tela com preto (vazio)

        # atualizar aqui???? sim
        # cada classe vai agir dependendo da camera?
        self.gerenciador_atores.draw(self.screen, (-self.camera.pos_x, -self.camera.pos_y)) # deve receber uma defasagem pela câmera
        # self.gerenciador_eventos.desenhar(self.screen) #atualmente não faz nada, retirar???
        self.gerenciador_tela.desenhar(self.screen)
        self.placar.draw(self.screen)
        # self.gerenciador_eventos.desenhar_debug(self.screen)
        # print("self.camera.pos::\t", self.camera.pos_x, self.camera.pos_y, " -> ",self.camera.objetivo_x, self.camera.objetivo_y)

    def input(self, acao):
        print(f"[ {acao} ]")
        if self.gerenciador_controle.input_lock:
            print("Entrada ignorada: controle travado.")
            return
        self._ataque(acao)

    def _ataque(self, acao):
        if acao == P1_HIT:
            ator_largada = self.gerenciador_atores.pegar_ator('largada')
            if ator_largada.get_visivel():
                ator_p1 = self.gerenciador_atores.pegar_ator('p1')
                ator_p1.transladar(80,0)
                ator_p1.animacoes.trocar("ataque")
                print("P1 acertou!!!!!!!!!!!!")
                self.placar.adicionar_pontos('p1',1)
                self.gerenciador_eventos.limpar_eventos()
                self.gerenciador_eventos.adicionar_espera(1000)
                self.gerenciador_eventos.adicionar_espera(1000)
                self.gerenciador_eventos.adicionar_fade_out(1000, callback=self.reset)
                # self.gerenciador_eventos.adicionar_espera(1000, callback=self.reset)
                
                # self.reset()

            else:
                print("P1 errou!!!!!!!!!!!!!")
                self.placar.adicionar_pontos('p2',1)
                self.gerenciador_eventos.limpar_eventos()
                self.reset()
        if acao == P2_HIT:
            ator_largada = self.gerenciador_atores.pegar_ator('largada')
            if ator_largada.get_visivel():
                ator_p2 = self.gerenciador_atores.pegar_ator('p2')
                ator_p2.transladar(-80,0)
                ator_p2.animacoes.trocar("ataque")
                print("P2 acertou!!!!!!!!!!!!")
                self.placar.adicionar_pontos('p2',1)
                self.gerenciador_eventos.limpar_eventos()
                self.gerenciador_eventos.adicionar_espera(1000)
                self.gerenciador_eventos.adicionar_espera(1000)
                self.gerenciador_eventos.adicionar_fade_out(1000, callback=self.reset)
                # self.reset()

            else:
                print("P2 errou!!!!!!!!!!!!!")
                self.placar.adicionar_pontos('p1',1)
                self.gerenciador_eventos.limpar_eventos()
                self.reset()
