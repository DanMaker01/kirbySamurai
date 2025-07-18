###########################################
# Gerenciador_Eventos
###########################################
# Modular: Não
# Finalizada: Não
###########################################
# Ordena e supervisiona a fila de eventos 
###########################################
# A Fazer:
# - Gerenciar totalmente os eventos
# - Retorna acoes para o Gerenciador
# - Apenas eventos de Wait podem esperar
# - eventos de fade não precisam ser esperados e não travam os controles
# - 
###########################################
from evento import Evento, EventoEspera, EventoFade, EventoMoverCamera, EventoMoverAtor

class GerenciadorEventos:
    def __init__(self, gerenciador_tela, gerenciador_atores, camera):
        self.fila_eventos = []                           # fila de eventos do roteiro
        self.tempo_pausado = False
        # Referência de cada sub-sistema
        self.gerenciador_tela = gerenciador_tela
        self.gerenciador_atores = gerenciador_atores
        self.camera = camera
        # Referência do evento sendo executado agora 
        self.evento_atual: Evento = None

    def _adicionar_evento(self, evento):
        self.fila_eventos.append(evento)
    # ------------------------------------------------------------

    def adicionar_fade_in(self, duracao_ms, callback=None):
        self._adicionar_evento(EventoFade("in", duracao_ms, self.gerenciador_tela, callback))

    def adicionar_fade_out(self, duracao_ms, callback=None):
        self._adicionar_evento(EventoFade("out", duracao_ms, self.gerenciador_tela, callback))

    def adicionar_camera_move(self, duracao_ms, x,y, callback=None ):
        self._adicionar_evento(EventoMoverCamera(duracao_ms, self.camera, x,y, callback))
        
    def adicionar_ator_move(self, duracao_ms, x=0,y=0,vel_x=0, vel_y=0, callback=None):
        self._adicionar_evento( EventoMoverAtor(duracao_ms,,self.gerenciador_atores, callback) )

    def adicionar_espera(self, duracao_ms, callback=None):
        self._adicionar_evento(EventoEspera(duracao_ms, callback))
    # ------------------------------------------------------------

    def atualizar(self, tempo_atual):
        if not self.evento_atual and self.fila_eventos:
            self.evento_atual = self.fila_eventos.pop(0)
            self.evento_atual.iniciar(tempo_atual)

        if self.evento_atual:
            self.evento_atual.atualizar(tempo_atual)
            if self.evento_atual.concluido:
                if self.evento_atual.callback:
                    self.evento_atual.callback()
                self.evento_atual = None

    def desenhar(self, tela):
        '''
        Atualmente não está fazendo nada. Retirar??????
        '''
        if self.evento_atual:
            self.evento_atual.desenhar(tela)

    def eventos_ativos(self):
        return self.evento_atual is not None or bool(self.fila_eventos)
