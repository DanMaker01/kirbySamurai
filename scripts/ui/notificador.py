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

    def adicionar_mensagem(self, texto, duracao_ms=2000, pos_x=0, pos_y=0):
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
        self.estado = "entrando"  # "entrando", "mostrando", "saindo"

        self.duracao_entrada = 400
        self.duracao_saida = 600
        self.duracao_mostrar = duracao_total - self.duracao_entrada - self.duracao_saida

    def atualizar_estado(self, tempo_atual):
        decorrido = tempo_atual - self.tempo_inicio

        if self.estado == "entrando" and decorrido >= self.duracao_entrada:
            self.estado = "mostrando"
            self.tempo_inicio = tempo_atual

        elif self.estado == "mostrando" and decorrido >= self.duracao_mostrar:
            self.estado = "saindo"
            self.tempo_inicio = tempo_atual

        elif self.estado == "saindo" and decorrido >= self.duracao_saida:
            return False  # terminou

        return True

    def draw(self, screen, tempo_atual):
        decorrido = tempo_atual - self.tempo_inicio
        alpha = 255
        offset_y = 0
        offset_max = 5  # antes era 30

        if self.estado == "entrando":
            t = min(1.0, decorrido / self.duracao_entrada)
            eased = ease_in_out(t)
            alpha = int(eased * 255)
            offset_y = int((1 - eased) * offset_max)

        elif self.estado == "mostrando":
            alpha = 255
            offset_y = 0

        elif self.estado == "saindo":
            t = min(1.0, decorrido / self.duracao_saida)
            eased = ease_in_out(t)
            alpha = int((1 - eased) * 255)
            offset_y = -int(eased * offset_max)

        surface = self.fonte.render(self.texto, True, (255, 255, 0))
        fundo = pygame.Surface((surface.get_width() + 20, surface.get_height() + 10), pygame.SRCALPHA)
        fundo.fill((0, 0, 0, alpha))

        pos_x = self.x
        pos_y = self.y + offset_y

        screen.blit(fundo, (pos_x - 10, pos_y - 5))

        surface_alpha = surface.copy()
        surface_alpha.set_alpha(alpha)
        screen.blit(surface_alpha, (pos_x, pos_y))
