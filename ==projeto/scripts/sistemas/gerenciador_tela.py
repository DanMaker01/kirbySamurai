# =======================================================
# Gerenciador de Tela
# =======================================================
# Cuida dos efeitos na tela, como:
# - Fade
# - Coloração
# - Tremor
# - etc (o que seria aqui?)
# =======================================================
# Finalizado: Não
# =======================================================
# - A fazer:
# - Efeito de coloração generalizada
# - Efeito de tremor por tempo
# - Efeitos de partículas
# =======================================================

import pygame
from scripts.core.config import WIDTH, HEIGHT
# from scripts.core.camera import Camera

class GerenciadorTela:
    def __init__(self, iniciar_preto=False):
        # propriedades
        self.tipo_fade = None
        self.superficie_fade = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        self.alfa_tela_atual = 255 if iniciar_preto else 0  # alfa fixo atual (aplicado sempre)
        # fade
        self.fade_em_andamento = False
        # tempo
        self.inicio = None
        self.duracao = 0
        
    def iniciar_fade(self, tipo, duracao_ms, tempo_atual):
        self.tipo_fade = tipo
        self.inicio = tempo_atual
        self.duracao = duracao_ms
        self.fade_em_andamento = True

    def set_tintura(self, alfa):
        self.alfa_tela_atual = max(0, min(255, alfa))  # clamp 0–255

    def atualizar(self, tempo_atual, dt):
        if self.fade_em_andamento and self.tipo_fade:
            tempo_passado = tempo_atual - self.inicio
            proporcao = min(1.0, tempo_passado / self.duracao)

            if self.tipo_fade == "in":
                alfa = int(255 * (1 - proporcao))
            else:
                alfa = int(255 * proporcao)

            self.set_tintura(alfa)

            if proporcao >= 1.0:
                self.fade_em_andamento = False
                self.tipo_fade = None


    def desenhar(self, tela): 
        #será desenhado por cima do jogo, porém antes da UI.
        if self.alfa_tela_atual > 0: 
            self.superficie_fade.fill((0, 0, 0, self.alfa_tela_atual))
            tela.blit(self.superficie_fade, (0, 0))

    def esta_em_fade(self):
        return self.fade_em_andamento
