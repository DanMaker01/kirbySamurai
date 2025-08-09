###############################################################################
# Notificador
###############################################################################
# Classe para fazer pop-up de notiicação na tela
###############################################################################
# Modular: Sim
# Finalizada: Não
###############################################################################
# A fazer:
# - Janela em volta 
# -  
###############################################################################

import pygame
from scripts.core.config import WIDTH, HEIGHT

##########################################################################################
def ease_in_out(t):
    # Função de interpolação suave (ease)
    return t * t * (3 - 2 * t)

##########################################################################################
class Notificador:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20, bold=True)

        self.fila_mensagens = []
        self.mensagem_atual = None

    def adicionar_mensagem(self, texto, duracao_ms=1000, pos_x=0, pos_y=0):
        self.fila_mensagens.append((texto, duracao_ms, pos_x, pos_y))

    def atualizar(self):
        tempo_atual = pygame.time.get_ticks()

        # Atualiza mensagem atual
        if self.mensagem_atual:
            viva = self.mensagem_atual.atualizar_estado(tempo_atual)
            if not viva:
                self.mensagem_atual = None

        # Inicia próxima mensagem da fila
        if not self.mensagem_atual and self.fila_mensagens:
            texto, duracao, x, y = self.fila_mensagens.pop(0)
            self.mensagem_atual = Mensagem(texto, duracao, x, y, self.font, tempo_atual)

    def draw(self):
        if self.mensagem_atual:
            self.mensagem_atual.draw(self.screen, pygame.time.get_ticks())

##########################################################################################
class Mensagem:
    def __init__(self, texto, duracao_total, x, y, fonte, tempo_inicio):
        self.texto = texto
        self.duracao_total = duracao_total
        self.x = x
        self.y = y
        self.fonte = fonte
        self.tempo_inicio = tempo_inicio
        self.estado = "entrando"

        self.duracao_entrada = 200
        self.duracao_saida = 300
        self.duracao_mostrar = duracao_total - self.duracao_entrada - self.duracao_saida

        self.offset_max = 10

        # Pré-renderiza texto e fundo para performance
        self._pre_render()

    def _pre_render(self):
        self.text_surface = self.fonte.render(self.texto, True, (255, 255, 0))
        tw, th = self.text_surface.get_size()
        self.padding = 16

        self.box_width = tw + self.padding * 1.5
        self.box_height = th + self.padding * 1.5

        # Cria fundo arredondado uma vez
        self.box_surface = pygame.Surface((self.box_width, self.box_height), pygame.SRCALPHA)
        fundo_cor = (20, 20, 20, 220)  # Fundo escuro semi-transparente
        pygame.draw.rect(
            self.box_surface,
            fundo_cor,
            (0, 0, self.box_width, self.box_height),
            border_radius=12
        )

    def atualizar_estado(self, tempo_atual):
        decorrido = tempo_atual - self.tempo_inicio

        if self.estado == "entrando" and decorrido >= self.duracao_entrada:
            self.estado = "mostrando"
            self.tempo_inicio = tempo_atual

        elif self.estado == "mostrando" and decorrido >= self.duracao_mostrar:
            self.estado = "saindo"
            self.tempo_inicio = tempo_atual

        elif self.estado == "saindo" and decorrido >= self.duracao_saida:
            return False

        return True

    def draw(self, screen, tempo_atual):
        decorrido = tempo_atual - self.tempo_inicio

        if self.estado == "entrando":
            t = min(1.0, decorrido / self.duracao_entrada)
            eased = ease_in_out(t)
            alpha = int(eased * 255)
            offset_y = int((1 - eased) * self.offset_max)

        elif self.estado == "mostrando":
            alpha = 255
            offset_y = 0

        elif self.estado == "saindo":
            t = min(1.0, decorrido / self.duracao_saida)
            eased = ease_in_out(t)
            alpha = int((1 - eased) * 255)
            offset_y = -int(eased * self.offset_max)

        # Aplica alpha
        box = self.box_surface.copy()
        box.set_alpha(alpha)
        text = self.text_surface.copy()
        text.set_alpha(alpha)

        pos_x = self.x - self.box_width // 2
        pos_y = self.y + offset_y - self.box_height // 2

        screen.blit(box, (pos_x, pos_y))

        # Centraliza o texto dentro da box
        text_rect = text.get_rect(center=(pos_x + self.box_width // 2, pos_y + self.box_height // 2))
        screen.blit(text, text_rect)
