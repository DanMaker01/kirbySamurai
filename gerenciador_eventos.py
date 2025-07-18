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
        # Lista dos eventos sendo executados agora 
        self.eventos_ativos: list[Evento] = []

    def _adicionar_evento(self, evento):
        self.fila_eventos.append(evento)
    # ------------------------------------------------------------

    def adicionar_fade_in(self, duracao_ms, callback=None):
        self._adicionar_evento(EventoFade("in", duracao_ms, self.gerenciador_tela, callback))

    def adicionar_fade_out(self, duracao_ms, callback=None):
        self._adicionar_evento(EventoFade("out", duracao_ms, self.gerenciador_tela, callback))

    def adicionar_camera_move(self, duracao_ms, x,y, callback=None ):
        self._adicionar_evento(EventoMoverCamera(duracao_ms, self.camera, x,y, callback))
        
    def adicionar_ator_move(self, duracao_ms,nome, destino_x=0,destino_y=0,callback=None):
        self._adicionar_evento( EventoMoverAtor(duracao_ms,self.gerenciador_atores,nome,destino_x,destino_y, callback) )

    def adicionar_espera(self, duracao_ms, callback=None):
        self._adicionar_evento(EventoEspera(duracao_ms, callback))
    # ------------------------------------------------------------

    def atualizar(self, tempo_atual):
        # Atualiza todos os eventos ativos (inclusive esperas)
        for evento in self.eventos_ativos[:]:
            evento.atualizar(tempo_atual)
            if evento.concluido:
                print(evento, "finalizado em ",tempo_atual)
                if evento.callback:
                    evento.callback()
                self.eventos_ativos.remove(evento)

        # Verifica se há algum EventoEspera ainda ativo
        espera_ativa = any(isinstance(e, EventoEspera) for e in self.eventos_ativos)

        # Enquanto houver eventos na fila...
        while self.fila_eventos:
            proximo = self.fila_eventos[0]
            evento:Evento
            # Se é uma espera, só iniciamos se não houver outra ativa
            if isinstance(proximo, EventoEspera):
                if espera_ativa:
                    break  # Espera ativa: não inicia outra
                else:
                    
                    evento = self.fila_eventos.pop(0)
                    evento.iniciar(tempo_atual)
                    self.eventos_ativos.append(evento)
                    break  # Espera recém-iniciada: aguarda ela terminar
            else:
                # Inicia outros eventos imediatamente
                evento =self.fila_eventos.pop(0)
                evento.iniciar(tempo_atual)
                self.eventos_ativos.append(evento)



    def desenhar(self, tela):
        '''
        Atualmente não está fazendo nada. Retirar??????
        '''
        # if self.evento_atual:
        #     self.evento_atual.desenhar(tela)
        pass

    def eventos_ativos(self):
        return bool(self.fila_eventos) or bool(self.eventos_ativos)
