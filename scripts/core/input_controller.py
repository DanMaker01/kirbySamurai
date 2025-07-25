###########################################
# InputController
###########################################
# Recebe as teclas e retorna os bindings
###########################################
# Modular: Sim
# Finalizada: Não
###########################################
# A Fazer:
# - Definir botões finais
# - Sistema de edição dinâmico
# - Retornar a lista de botões apertados no momento
# --> Isso vai liberar um sistema de empate
###########################################



import pygame
from scripts.core.config import *

class InputController:
    def __init__(self):
        self.key_bindings = {
            # pygame.K_1: ('player1', 'parado'),
            # pygame.K_2: 'load_sequence_player1',
            # pygame.K_3: ('player1', 'movimento'),
            # pygame.K_4: ('player1', 'pos_movimento'),
            # pygame.K_q: ('player2', 'parado'),
            # pygame.K_w: ('player2', 'pre_movimento'),
            # pygame.K_e: ('player2', 'movimento'),
            # pygame.K_r: ('player2', 'pos_movimento'),
            # pygame.K_p: 'toggle_pause',
            pygame.K_LEFT: LEFT,
            pygame.K_RIGHT: RIGHT,
            pygame.K_UP: UP,
            pygame.K_DOWN: DOWN,
            pygame.K_z: CONFIRM,
            pygame.K_x: CANCEL,
            pygame.K_z: P1_HIT,
            pygame.K_p: P2_HIT
        }
        self.pressed_keys = {}  # key -> timestamp

    def process_event(self, event):
        # mudar para um sistema: #?????
        # - QUando você aperta ele modifica uma variável interna
        # - Quando você lê o input ele retorna uma lista do bindings On/Off

        now = pygame.time.get_ticks()

        if event.type == pygame.KEYDOWN:
            key = event.key
            if key not in self.pressed_keys:
                self.pressed_keys[key] = now
            return {
                'event': 'keydown',
                'key': key,
                'binding': self.key_bindings.get(key)
            }

        elif event.type == pygame.KEYUP:
            key = event.key
            if key in self.pressed_keys:
                duration = now - self.pressed_keys[key]
                del self.pressed_keys[key]
            else:
                duration = 0
            return {
                'event': 'keyup',
                'key': key,
                'duration': duration,
                'binding': self.key_bindings.get(key)
            }

        return None
