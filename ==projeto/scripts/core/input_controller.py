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
# - Opcional, sistema de um botão duas funções, lidar com casos em que as duas função são válidas, ordem de prioridade?
###########################################



import pygame
from scripts.core.config import *

class InputController:
    def __init__(self):
        self.key_bindings = KEY_BINDINGS

        
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
            
            # print(key, self.key_bindings.get(key))

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
