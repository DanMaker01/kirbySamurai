###########################################
# Config/Definições
###########################################
# Modular: Sim
# Finalizada: Não
###########################################
# A Fazer:
# - padronizar os retornos dos eventos
#
###########################################

import pygame

# Janela
WIDTH, HEIGHT = 360, 640

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)


# Fonte
pygame.font.init()
FONT_LARGE = pygame.font.SysFont(None, 36)
FONT_SMALL = pygame.font.SysFont(None, 24)

# Padronização dos nomes das Ações
CONFIRM = 'confirma'
CANCEL = 'cancela'
UP = 'cima'
DOWN = 'baixo'
LEFT = 'esquerda'
RIGHT = 'direita'
P1_HIT = 'p1_hit'
P2_HIT = 'p2_hit'

KEY_BINDINGS = {
    pygame.K_LEFT:  LEFT,
    pygame.K_RIGHT: RIGHT,
    pygame.K_UP:    UP,
    pygame.K_DOWN:  DOWN,

    # pygame.K_z:     CONFIRM,
    pygame.K_RETURN:CONFIRM,
    
    pygame.K_x:     CANCEL,
    
    pygame.K_z:     P1_HIT,
    pygame.K_p:     P2_HIT,
}