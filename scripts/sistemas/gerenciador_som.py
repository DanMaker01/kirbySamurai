##############################################################3
# Gerenciador de Som
##############################################################3
# Modular: Sim
# Finalizada: Sim
##############################################################3
import pygame
class Gerenciador_Som:
    def __init__(self):
        pygame.mixer.init()
        self.sons = {}     # sons simples (efeitos)
        self.musicas = {}  # caminhos de músicas
        self.volume_efeitos = 1.0
        self.volume_musica = 1.0
        self.musica_atual = None
    # ========== CARREGAR AUDIO =====================
    def carregar_som(self, nome, caminho):
        if nome not in self.sons:
            self.sons[nome] = pygame.mixer.Sound(caminho)
            self.sons[nome].set_volume(self.volume_efeitos)
    def carregar_musica(self, nome, caminho):
        if nome not in self.musicas:
            self.musicas[nome] = caminho
    # ========== EXECUÇÃO ====================================
    def tocar_som(self, nome, volume=1.0):
        if nome in self.sons:
            som = self.sons[nome]
            volume = max(0.0, min(volume, 1.0))
            som.set_volume(volume)  # <<< ESSENCIAL
            print("gerenciador som: tocando", nome, "com volume:", volume)
            som.play()
        else:
            print(f"[Som não encontrado]: {nome}")
    def tocar_musica(self, nome, loop=True):
        if nome in self.musicas:
            caminho = self.musicas[nome]
            if self.musica_atual != nome:
                pygame.mixer.music.load(caminho)
                pygame.mixer.music.set_volume(self.volume_musica)
                pygame.mixer.music.play(-1 if loop else 0)
                self.musica_atual = nome
        else:
            print(f"[Música não encontrada]: {nome}")
    def parar_musica(self):
        pygame.mixer.music.stop()
        self.musica_atual = None
    # =========================================================
    def set_volume_efeitos(self, volume):
        self.volume_efeitos = max(0.0, min(volume, 1.0))
        for som in self.sons.values():
            som.set_volume(self.volume_efeitos)
    def set_volume_musica(self, volume):
        self.volume_musica = max(0.0, min(volume, 1.0))
        pygame.mixer.music.set_volume(self.volume_musica)
    # =========================================================
