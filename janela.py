###########################################
# Janela
###########################################
# Modular: Sim
# Finalizada: Não
###########################################
# A Fazer:
# - Modificações dos parametros por métodos??
# - 
###########################################


import pygame

class Janela:
    def __init__(
        self, 
        x=0, y=0, 
        lar=100, alt=100, 
        cor=(255, 255, 255, 255), 
        margem_sup=10, margem_inf=10, 
        margem_esq=10, margem_dir=10
    ):
        self.pos = pygame.Vector2(x, y)
        self.lar = lar
        self.alt = alt
        self.cor = cor

        self.margens = {
            "sup": margem_sup,
            "inf": margem_inf,
            "esq": margem_esq,
            "dir": margem_dir
        }

        
    def get_rect(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.lar, self.alt)

    def mover_para(self, x, y):
        self.pos.update(x, y)
        self.rect.topleft = (x, y)

    def mudar_tamanho(self, lar, alt):
        self.lar = lar
        self.alt = alt
        self.rect.size = (lar, alt)

    def desenhar(self, surface):
        pygame.draw.rect(surface, self.cor, self.get_rect())

    def obter_area_interna(self):
        """
        Retorna um pygame.Rect representando a área útil (sem margens) da janela.
        """
        return pygame.Rect(
            self.pos.x + self.margens["esq"],
            self.pos.y + self.margens["sup"],
            self.lar - (self.margens["esq"] + self.margens["dir"]),
            self.alt - (self.margens["sup"] + self.margens["inf"])
        )
