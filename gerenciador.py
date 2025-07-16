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
from gerenciador_atores import Gerenciador_Atores
from gerenciador_som import Gerenciador_Som
from config import *
from ator import Ator
from animacao import Animacao
import pygame
from evento import *

class Gerenciador:
    def __init__(self, screen, clock):
        self.placar = Placar()
        self.persistencia_placar = Persistencia()
        self.gerenciador_atores = Gerenciador_Atores()
        self.gerenciador_som = Gerenciador_Som()
        #self.gerenciador_eventos = Gerenciador_Eventos()
        #self.gerenciador_tela = Gerenciador_Tela()
        self.clock = clock
        self.controle_travado = False
        self.fila_eventos = []
        self.evento_atual = None
        self._criar_atores()
        self.superficie_fade = pygame.Surface( (WIDTH,HEIGHT) ).convert_alpha()
        self.superficie_fade.fill((0, 0, 0, 0))  # Começa transparente
        self.fade_em_andamento = None  # Evento de fade atual
        self.tempo_atual = pygame.time.get_ticks()
        self.screen = screen
        self._setup_eventos()
        
    def _setup_eventos(self):
        self.adicionar_fade_in(2000)
        self.adicionar_espera(1000)
        # self.adicionar_espera(1000)
        # self.adicionar_espera(1000)
        # self.adicionar_espera(2000)
        # self.adicionar_fade_out(2000)
        

    def _criar_atores(self):
        sprite_triangulo_sup = Animacao(["triangulo_sup.png"])
        sprite_triangulo_inf = Animacao(["triangulo_inf.png"])

        self.gerenciador_atores.adicionar_ator(
            "triangulo_sup", Ator(animacoes={"padrao": sprite_triangulo_sup,
                                             }))

        self.gerenciador_atores.adicionar_ator(
            "triangulo_inf", Ator(animacoes={"padrao": sprite_triangulo_inf,
                                             }))

    def update(self, clock):
        self.tempo_atual = pygame.time.get_ticks()

        if self.evento_atual:
            self.evento_atual.atualizar(self.tempo_atual)
            if self.evento_atual.concluido:

                print("finalizando evento :\t", self.evento_atual,"\n")
                if self.evento_atual.callback:
                    self.evento_atual.callback()
                self.evento_atual = None

        if not self.evento_atual and self.fila_eventos:
            self.evento_atual = self.fila_eventos.pop(0)
            self.evento_atual.iniciar(self.tempo_atual)

        self.gerenciador_atores.update(clock)




    def _processar_fade(self):
        evento = self.fade_em_andamento
        tempo_passado = self.tempo_atual - evento["inicio"]
        proporcao = min(1.0, tempo_passado / evento["duracao"])

        if evento["tipo"] == "fade_in":
            alfa = int(255 * (1 - proporcao))  # de preto (255) até 0
        else:
            alfa = int(255 * proporcao)        # de 0 até preto (255)

        self.superficie_fade.fill((0, 0, 0, alfa))

        if proporcao >= 1.0:
            self.fade_em_andamento = None
            self.eventos.pop(0)
            if evento.get("callback"):
                evento["callback"]()

    def adicionar_espera(self, duracao_ms, callback=None):
        self.fila_eventos.append(EventoEspera(duracao_ms, callback))

    def adicionar_fade_in(self, duracao_ms, callback=None):
        self.fila_eventos.append(EventoFade("in", duracao_ms, self.superficie_fade, callback))

    def adicionar_fade_out(self, duracao_ms, callback=None):
        self.fila_eventos.append(EventoFade("out", duracao_ms, self.superficie_fade, callback))


    def desenhar_fade(self, tela):
        tela.blit(self.superficie_fade, (0, 0))

    def draw(self):
        self.gerenciador_atores.draw(self.screen)
        self.placar.draw(self.screen)

        if self.evento_atual:
            self.evento_atual.desenhar(self.screen)

    def input(self, acao):
        print(f"[ {acao} ]")
        if self.fila_eventos or self.fade_em_andamento:
            print("Entrada ignorada: controle travado por evento.")
            return
        
        # self.gerenciador_atores.input(acao)
    def draw(self):
        self.gerenciador_atores.draw(self.screen)
        self.placar.draw(self.screen)

        if self.evento_atual:
            self.evento_atual.desenhar(self.screen)
