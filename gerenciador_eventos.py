###########################################
# Gerenciador_Eventos
###########################################
# Modular: Não
# Finalizada: Não
###########################################
# A Fazer:
# - Gerenciar totalmente os eventos
# - Retorna acoes para o Gerenciador
# - Apenas eventos de Wait podem esperar
# - eventos de fade não precisam ser esperados e não travam os controles
# - 
###########################################
from evento import EventoEspera, EventoFade

class GerenciadorEventos:
    def __init__(self, gerenciador_tela):
        self.eventos = []
        self.tempo_pausado = False
        self.gerenciador_tela = gerenciador_tela
        self.evento_atual = None

    def adicionar_fade_in(self, duracao_ms, callback=None):
        self.adicionar_evento(EventoFade("in", duracao_ms, self.gerenciador_tela, callback))

    def adicionar_fade_out(self, duracao_ms, callback=None):
        self.adicionar_evento(EventoFade("out", duracao_ms, self.gerenciador_tela, callback))


    def adicionar_evento(self, evento):
        self.eventos.append(evento)

    def adicionar_espera(self, duracao_ms, callback=None):
        self.adicionar_evento(EventoEspera(duracao_ms, callback))

    def atualizar(self, tempo_atual):
        if not self.evento_atual and self.eventos:
            self.evento_atual = self.eventos.pop(0)
            self.evento_atual.iniciar(tempo_atual)

        if self.evento_atual:
            self.evento_atual.atualizar(tempo_atual)
            if self.evento_atual.concluido:
                if self.evento_atual.callback:
                    self.evento_atual.callback()
                self.evento_atual = None

    def desenhar(self, tela):
        if self.evento_atual:
            self.evento_atual.desenhar(tela)

    def eventos_ativos(self):
        return self.evento_atual is not None or bool(self.eventos)
