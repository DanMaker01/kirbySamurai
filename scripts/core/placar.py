###########################################
# Placar
###########################################
# Modular: Sim
# Finalizada: Não
###########################################
# A Fazer:
# - Generalizar para N players
# -
###########################################
import pygame

class Placar:
    def __init__(self):
        self.pontuacao = {
            'p1': 0,
            'p2': 0
        }
        #pro draw
        self.font = pygame.font.SysFont(None, 30)

    def adicionar_pontos(self, time, pontos):
        if time in self.pontuacao:
            self.pontuacao[time] += pontos

    def zerar_placar(self):
        for time in self.pontuacao:
            self.pontuacao[time] = 0

    def mostrar_pontuacao(self, time):
        return self.pontuacao.get(time)

    def draw(self,screen):
            
        score_text = f"{self.mostrar_pontuacao('p1')} x {self.mostrar_pontuacao('p2')}"
        text_surface = self.font.render(score_text, True, (255, 255, 255))
        screen.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2, 20))