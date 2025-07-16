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

#Ações
CONFIRM = 'confirma'
CANCEL = 'cancela'
UP = 'cima'
DOWN = 'baixo'
LEFT = 'esquerda'
RIGHT = 'direita'