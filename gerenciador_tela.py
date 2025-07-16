import pygame
from config import WIDTH, HEIGHT
from camera import Camera
class GerenciadorTela:
    def __init__(self, largura_mundo, altura_mundo):
        self.superficie_fade = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        self.alfa_tela_atual = 0  # alfa fixo atual (aplicado sempre)
        self.fade_em_andamento = False

        self.tipo_fade = None
        self.inicio = None
        self.duracao = 0

        self.camera = Camera(largura_mundo, altura_mundo, WIDTH, HEIGHT)

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

        self.camera.atualizar(dt)

    def desenhar(self, tela):
        if self.alfa_tela_atual > 0:
            self.superficie_fade.fill((0, 0, 0, self.alfa_tela_atual))
            tela.blit(self.superficie_fade, (0, 0))

    def esta_em_fade(self):
        return self.fade_em_andamento
    
     # --- MÉTODOS DE CONTROLE DA CÂMERA ---

    # def set_posicao_camera(self, x, y):
    #     """Define posição da câmera diretamente."""
    #     self.camera.set_posicao(x, y)

    def mover_camera_para(self, x, y):
        """Define posição objetivo para a câmera se mover suavemente."""
        self.camera.mover_para(x, y)

    def set_velocidade_camera(self, vel_x, vel_y):
        """Define velocidade de movimento da câmera."""
        self.camera.set_velocidade(vel_x, vel_y)

    def centralizar_camera_em(self, x, y):
        """Centraliza a câmera em uma posição (x, y)."""
        self.camera.centralizar_em(x, y)

    # def aplicar_camera(self, rect):
    #     """Aplica o deslocamento da câmera em um rect (para desenhar)."""
    #     return self.camera.aplicar(rect)

    # def aplicar_camera_pos(self, pos):
    #     """Aplica o deslocamento da câmera em uma posição (x, y)."""
    #     return self.camera.aplicar_pos(pos)