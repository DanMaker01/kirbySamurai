import pygame

class Placar:
    def __init__(self):
        self.pontuacao = {
            'p1': 0,
            'p2': 0
        }
        self.font = pygame.font.SysFont(None, 30)
        self._on_modified = None
        self._blink = False
        self._blink_duration = 2.0  # segundos
        self._blink_elapsed = 0.0   # tempo acumulado do blink

    def set_on_modified(self, callback):
        self._on_modified = callback

    def _notify_modified(self):
        if self._on_modified:
            self._on_modified(self.pontuacao)
        self._blink = True
        self._blink_elapsed = 0.0

    def adicionar_pontos(self, time, pontos):
        if time in self.pontuacao:
            self.pontuacao[time] += pontos
            self._notify_modified()

    def zerar_placar(self):
        for time in self.pontuacao:
            self.pontuacao[time] = 0
        self._notify_modified()

    def mostrar_pontuacao(self, time):
        return self.pontuacao.get(time)

    def atualizar(self, dt):
        if self._blink:
            self._blink_elapsed += dt
            if self._blink_elapsed >= self._blink_duration:
                self._blink = False

    def draw(self, screen):
        score_text = f"{self.mostrar_pontuacao('p1')} x {self.mostrar_pontuacao('p2')}"
        
        if self._blink:
            # Pisca a cada 200ms
            blink_on = int(self._blink_elapsed * 5) % 2 == 0
            color = (255, 0, 0) if blink_on else (255, 255, 255)
        else:
            color = (255, 255, 255)

        text_surface = self.font.render(score_text, True, color)
        screen.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2, 20))
