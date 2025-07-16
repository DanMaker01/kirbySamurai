import pygame

class Camera:
    def __init__(self, largura_mundo, altura_mundo, largura_tela, altura_tela):
        self.largura_mundo = largura_mundo
        self.altura_mundo = altura_mundo
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela

        self.pos_x = 0
        self.pos_y = 0

        self.vel_x = 0
        self.vel_y = 0

        self.objetivo_x = 0
        self.objetivo_y = 0

        self.suavizacao = 0.1  # fator de suavização (0 = sem suavização)

    def set_posicao(self, x, y):
        self.pos_x = max(0, min(x, self.largura_mundo - self.largura_tela))
        self.pos_y = max(0, min(y, self.altura_mundo - self.altura_tela))

    def mover_para(self, x, y):
        self.objetivo_x = x
        self.objetivo_y = y

    def set_velocidade(self, vel_x, vel_y):
        self.vel_x = vel_x
        self.vel_y = vel_y

    def atualizar(self, dt):
        # Movimento baseado na velocidade
        if self.vel_x != 0 or self.vel_y != 0:
            self.set_posicao(
                self.pos_x + self.vel_x * dt,
                self.pos_y + self.vel_y * dt
            )
        else:
            # Suavização ao mover para um objetivo
            dx = self.objetivo_x - self.pos_x
            dy = self.objetivo_y - self.pos_y
            self.set_posicao(
                self.pos_x + dx * self.suavizacao,
                self.pos_y + dy * self.suavizacao
            )

    def aplicar(self, rect):
        # Retorna um novo retângulo ajustado pela posição da câmera
        return rect.move(-self.pos_x, -self.pos_y)

    def aplicar_pos(self, pos):
        # Ajusta uma posição (x, y) com base na câmera
        return (pos[0] - self.pos_x, pos[1] - self.pos_y)

    def centralizar_em(self, x, y):
        self.mover_para(
            x - self.largura_tela // 2,
            y - self.altura_tela // 2
        )
