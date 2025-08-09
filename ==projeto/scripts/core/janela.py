import pygame

###########################################
# Janela, JanelaSelecionável
###########################################
# Modular: Sim
# Finalizada: Não
###########################################
# A Fazer:
# - Modificações dos parametros por métodos??
# - Get e set Rect
###########################################
# Feito:
# -
# -
# -
# -
###########################################


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

    # Acesso direto às margens (propriedades)
    @property
    def margem_sup(self): return self.margens["sup"]

    @property
    def margem_inf(self): return self.margens["inf"]

    @property
    def margem_esq(self): return self.margens["esq"]

    @property
    def margem_dir(self): return self.margens["dir"]

    def get_rect(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.lar, self.alt)

    def mover_para(self, x, y):
        self.pos.update(x, y)

    def mudar_tamanho(self, lar, alt):
        self.lar = lar
        self.alt = alt

    def desenhar(self, surface):
        pygame.draw.rect(surface, self.cor, self.get_rect())

    def obter_area_interna(self):
        """Retorna um pygame.Rect representando a área útil (sem margens) da janela."""
        return pygame.Rect(
            self.pos.x + self.margem_esq,
            self.pos.y + self.margem_sup,
            self.lar - (self.margem_esq + self.margem_dir),
            self.alt - (self.margem_sup + self.margem_inf)
        )


######################################
# Janela Selecionável
######################################
class JanelaSelecionavel(Janela):
    def __init__(
        self,
        opcoes,
        x=0, y=0,
        lar=100, alt=100,
        cor=(128, 128, 128),
        cor_selecao=(180+20, 180+20, 255),
        fonte=None,
        margem_sup=10, margem_inf=10,
        margem_esq=10, margem_dir=10,
        espaco_entre=8
    ):
        super().__init__(x, y, lar, alt, cor, margem_sup, margem_inf, margem_esq, margem_dir)
        self.opcoes = opcoes
        self.indice_selecionado = 0
        self.cor_selecao = cor_selecao
        self.fonte = fonte or pygame.font.SysFont(None, 28)
        self.espaco_entre = espaco_entre
        self.ajustar_tamanho_para_conter_texto()

    def ajustar_tamanho_para_conter_texto(self):
        """Ajusta lar e alt da janela com base no texto e margens."""
        larguras = []
        alturas = []

        for texto in self.opcoes:
            render = self.fonte.render(texto, True, (0, 0, 0))
            larguras.append(render.get_width())
            alturas.append(render.get_height())

        if larguras and alturas:
            largura_max = max(larguras)
            altura_total = sum(alturas) + self.espaco_entre * (len(self.opcoes) - 1)
        else:
            largura_max = 0
            altura_total = 0

        self.lar = largura_max + self.margem_esq + self.margem_dir
        self.alt = altura_total + self.margem_sup + self.margem_inf

    def desenhar(self, surface):
        super().desenhar(surface)
        area = self.obter_area_interna()

        y = area.top
        for i, texto in enumerate(self.opcoes):
            render = self.fonte.render(texto, True, (0, 0, 0))
            rect_opcao = render.get_rect(topleft=(area.left, y))

            if i == self.indice_selecionado:
                pygame.draw.rect(surface, self.cor_selecao, rect_opcao)

            surface.blit(render, rect_opcao)
            y += render.get_height() + self.espaco_entre

    def avancar(self):
        self.indice_selecionado = (self.indice_selecionado + 1) % len(self.opcoes)

    def voltar(self):
        self.indice_selecionado = (self.indice_selecionado - 1) % len(self.opcoes)

    def selecionar(self):
        return self.opcoes[self.indice_selecionado]

    def set_opcao(self, indice):
        if 0 <= indice < len(self.opcoes):
            self.indice_selecionado = indice
