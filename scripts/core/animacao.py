

import pygame

# @ implementar spritesheets
# @ implementar escala nas animações, não no Ator
# @ alterar o indice a qualquer momento

class Animacao: # cada animação deve ter sua escala, o ator tem a escala dele tbm, que gerencia a de todas animações
    def __init__(self, imagens=None, pos=(0, 0), vel_anima=0.1, loop=True, escala=1.0):
        """
        imagens: lista de caminhos ou Surfaces
        pos: posição inicial (x, y)
        escala: fator de escala
        vel_anima: segundos entre frames (ex: 0.1 = 10 fps)
        loop: se a animação reinicia após terminar
        """
        self.pos = pos
        self.escala = escala #tem que ter para cada animação, e uma geral no ator
        self.vel_anima = vel_anima
        self.loop = loop
        self.tempo_acumulado = 0
        self.indice_atual = 0
        self.ativa = True

        self.sprites = []
        # Store original images 
        self.path = 'sprites/'
        if imagens is not None:
            self.original_images = [self._carregar_imagem(self.path + img if isinstance(img, str) else img) for img in imagens]
            self.sprites = []
            self._gerar_sprites()

    # #@implementar direito, tá bugado o escalar
    # def carregar_spritesheet(self, caminho_spritesheet, num_colunas, num_linhas, indice_ini, indice_fin, escala=1):
    #     """
    #     Carrega uma spritesheet e cria sprites a partir dela.

    #     Args:
    #         caminho_spritesheet: Caminho para o arquivo da spritesheet
    #         num_colunas: Número de colunas na spritesheet
    #         num_linhas: Número de linhas na spritesheet
    #         indice_ini: Índice inicial dos sprites a serem carregados
    #         indice_fin: Índice final dos sprites a serem carregados
    #     """
    #     self.original_images = []
    #     self.original_images.clear()
    #     spritesheet = pygame.image.load(caminho_spritesheet).convert_alpha()
    #     largura = spritesheet.get_width() // num_colunas
    #     altura = spritesheet.get_height() // num_linhas
    #     for i in range(indice_ini, indice_fin + 1):
    #         x = (i % num_colunas) * largura
    #         y = (i // num_colunas) * altura
    #         img = spritesheet.subsurface((x, y, largura, altura))
    #         self.original_images.append(img)
    #     _esc = escala
    #     self._gerar_sprites(_esc)
    
    def _carregar_imagem(self, imagem):
        if isinstance(imagem, str):
            return pygame.image.load(imagem).convert_alpha()
        else:
            print("caminho inválido ou imagem não carregada corretamente:", imagem)
        return imagem.convert_alpha()

    def _gerar_sprites(self, escala=1.0):
        self.sprites.clear()
        for img in self.original_images:
            if escala != 1.0:
                w, h = img.get_size()
                img = pygame.transform.scale(img, (int(w * escala), int(h * escala)))

            sprite = pygame.sprite.Sprite()
            sprite.image = img
            sprite.rect = img.get_rect(topleft=self.pos)
            self.sprites.append(sprite)

    def set_escala(self, nova_escala: float):
        """Altera a escala da animação em tempo de execução"""
        self.escala = nova_escala
        self._gerar_sprites(nova_escala)

    def set_pos(self, x, y):
        self.pos = (x, y)
        for sprite in self.sprites:
            sprite.rect.topleft = self.pos

    def update(self, dt):
        if not self.ativa or len(self.sprites) <= 1:
            return

        self.tempo_acumulado += dt
        if self.tempo_acumulado >= self.vel_anima:
            self.tempo_acumulado = 0
            self.avanca_sprite()

    def avanca_sprite(self):
        self.indice_atual += 1
        if self.indice_atual >= len(self.sprites):
            if self.loop:
                self.indice_atual = 0
            else:
                self.indice_atual = len(self.sprites) - 1
                self.ativa = False

    def draw(self, screen, tintura = (255,255,255,255), offset= (0,0)):
        if self.sprites:
            sprite = self.sprites[self.indice_atual]
            # Cria uma cópia da imagem original
            colored_image = sprite.image.copy()
            # Aplica a cor multiplicando os canais (RGB), mantendo a transparência
            colored_image.fill(tintura, special_flags=pygame.BLEND_RGBA_MULT)  # aplica tom avermelhado
            x_off = sprite.rect.x -offset[0]
            y_off = sprite.rect.y -offset[1]
            
            screen.blit(colored_image, (x_off,y_off))

    def reset(self):
        self.indice_atual = 0
        self.tempo_acumulado = 0
        self.ativa = True

    def stop(self):
        self.ativa = False
        self.indice_atual = len(self.sprites) - 1 if self.sprites else 0

    def start(self):
        self.ativa = True #redundante???????/
        self.reset()
