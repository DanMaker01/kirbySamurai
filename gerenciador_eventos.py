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


from evento import Evento, EventoEspera, EventoFade

class GerenciadorEventos:
    def __init__(self):
        self.eventos = []
        self.tempo_pausado = False

    def adicionar_evento(self, evento, tempo_atual):
        evento.iniciar(tempo_atual)
        self.eventos.append(evento)

    def atualizar(self, tempo_atual):
        if not self.eventos:
            return

        evento_atual = self.eventos[0]
        resultado = evento_atual.atualizar(tempo_atual)

        if isinstance(evento_atual, EventoEspera):
            self.tempo_pausado = not evento_atual.concluido
        else:
            self.tempo_pausado = False

        if evento_atual.concluido:
            self.eventos.pop(0)

        return resultado

    def eventos_ativos(self):
        return len(self.eventos) > 0

    def limpar_eventos(self):
        self.eventos.clear()
        self.tempo_pausado = False
