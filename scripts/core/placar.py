#####################################
# Placar
#####################################
# A Fazer:
# - Adicionar no dicionário o numero de players
# -
# -
#####################################
# A Fazer:
# -
# -
#####################################
import pygame

class Placar:
    def __init__(self, y=20, players=1): 
        self.pontuacao = {}
        for i in range(players):
            self.pontuacao[f'p{i+1}'] = 0

        self.y = y
        self.font = pygame.font.SysFont(None, 30)
        self._on_modified = None
        self._blink = False
        self._blink_duration = 3.0  # segundos
        self._blink_elapsed = 0.0   # tempo acumulado do blink


    def adicionar_jogador(self, nome):
        if nome not in self.pontuacao:
            self.pontuacao[nome] = 0

    def set_on_modified(self, callback):
        self._on_modified = callback

    def _notify_modified(self):
        if self._on_modified:
            self._on_modified(self.pontuacao)
        self._blink = True
        self._blink_elapsed = 0.0

    def adicionar_pontos(self, jogador, pontos):
        if jogador not in self.pontuacao:
            self.pontuacao[jogador] = 0
        self.pontuacao[jogador] += pontos
        self._notify_modified()

    def zerar_placar(self):
        for jogador in self.pontuacao:
            self.pontuacao[jogador] = 0
        self._notify_modified()

    def mostrar_pontuacao(self, jogador):
        return self.pontuacao.get(jogador, 0)

    def mostrar_quem_esta_vencendo(self):
        if not self.pontuacao:
            return None

        maior_pontuacao = float('-inf')
        vencedores = []

        for jogador, pontos in self.pontuacao.items():
            if pontos > maior_pontuacao:
                maior_pontuacao = pontos
                vencedores = [jogador]
            elif pontos == maior_pontuacao:
                vencedores.append(jogador)

        if len(vencedores) == 1:
            return vencedores[0]
        else:
            return 'empate'
        
    def diferenca_maior_que(self, valor):
        if len(self.pontuacao) < 2:
            return False  # diferença não é significativa com 0 ou 1 jogador

        pontuacoes = list(self.pontuacao.values())
        diferenca = max(pontuacoes) - min(pontuacoes)
        return diferenca > valor


    def atualizar(self, dt):
        if self._blink:
            self._blink_elapsed += dt
            if self._blink_elapsed >= self._blink_duration:
                self._blink = False

    def draw(self, screen):
        # Exibir placar de cada jogador
        linhas = []
        for jogador in sorted(self.pontuacao.keys()):
            pontos = self.pontuacao[jogador]
            linhas.append(f"{jogador}: {pontos}")

        # # Exibir quem está vencendo
        # vencedor = self.mostrar_quem_esta_vencendo()
        # if vencedor == 'empate':
        #     linhas.append("EMPATE!")
        # elif vencedor:
        #     linhas.append(f"{vencedor.upper()} vencendo")

        # Renderizar cada linha do placar
        for i, texto in enumerate(linhas):
            if self._blink:
                blink_on = int(self._blink_elapsed * 5) % 2 == 0
                color = (255, 0, 0) if blink_on else (255, 255, 255)
            else:
                color = (255, 255, 255)

            surf = self.font.render(texto, True, color)
            x = screen.get_width() // 2 - surf.get_width() // 2
            y = self.y + i * 25
            screen.blit(surf, (x, y))
