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
from evento import *
import pygame

class GerenciadorEventos:
    def __init__(self, gerenciador_controle,gerenciador_tela, gerenciador_atores, camera):
        self.fila_eventos = []                           # fila de eventos do roteiro
        self.tempo_pausado = False
        # Referência de cada sub-sistema
        self.gerenciador_tela = gerenciador_tela
        self.gerenciador_atores = gerenciador_atores
        self.gerenciador_controle = gerenciador_controle
        self.camera = camera
        # Lista dos eventos sendo executados agora 
        self.eventos_ativos: list[Evento] = []

    def esta_rodando_evento(self, tipo_evento):
        """
        Verifica se há algum evento ativo do tipo especificado.
        tipo_evento: classe do evento (ex: EventoFade)
        """
        return any(isinstance(evento, tipo_evento) for evento in self.eventos_ativos)

    def _adicionar_evento(self, evento):
        self.fila_eventos.append(evento)
    # ------------------------------------------------------------
    # Tela
    def adicionar_fade_in(self, duracao_ms, callback=None):
        self._adicionar_evento(EventoFade("in", duracao_ms, self.gerenciador_tela, callback))
    def adicionar_fade_out(self, duracao_ms, callback=None):
        self._adicionar_evento(EventoFade("out", duracao_ms, self.gerenciador_tela, callback))
    
    # Camera
    def adicionar_camera_move(self, duracao_ms, x,y, callback=None ):
        self._adicionar_evento(EventoMoverCamera(duracao_ms, self.camera, x,y, callback))
    
    # Atores   
    def adicionar_ator_move(self, duracao_ms,nome, destino_x=0,destino_y=0,callback=None):
        self._adicionar_evento( EventoMoverAtor(duracao_ms,self.gerenciador_atores,nome,destino_x,destino_y, callback) )
    def adicionar_ator_set_visibilidade(self,nome,valor,callback=None):
        self._adicionar_evento( EventoAtorVisibilidade(self.gerenciador_atores,nome,valor,callback) )

    # Controle
    def adicionar_input_lock(self,valor=False,callback=None):
        self._adicionar_evento( EventoInputLock(self.gerenciador_controle,valor,callback) )
    # Jogo
    def adicionar_espera(self, duracao_ms, callback=None):
        self._adicionar_evento(EventoEspera(duracao_ms, callback))

    def adicionar_limpa_eventos(self,callback=None):
        self._adicionar_evento( EventoLimpaEventos(self, callback))
    # ------------------------------------------------------------

    def atualizar(self, tempo_atual):
        # Atualiza todos os eventos ativos (inclusive esperas)
        for evento in self.eventos_ativos[:]:
            evento.atualizar(tempo_atual)
            if evento.concluido:
                # print(evento.__class__, "finalizado em ",tempo_atual)
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
                if evento == None:
                    print("acabaram eventos")
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
    def desenhar_debug(self, tela):
        fonte = pygame.font.SysFont("Consolas", 12) #integrar
        x = 10
        y = 300
        linha = 0

        def desenhar_linha(texto, cor=(200, 200, 200)):
            nonlocal linha
            surf = fonte.render(texto, True, cor)
            tela.blit(surf, (x, y + linha * 20))
            linha += 1

        desenhar_linha("== EVENTOS ATIVOS ==")
        for evento in self.eventos_ativos:
            tipo = evento.__class__.__name__
            restante = f"{evento.duracao - (pygame.time.get_ticks() - evento.inicio)} ms" if evento.inicio else "a iniciar"
            desenhar_linha(f"[ATIVO] {tipo} — restante: {restante}")

        desenhar_linha("")
        desenhar_linha("== FILA DE EVENTOS ==")
        for evento in self.fila_eventos:
            tipo = evento.__class__.__name__
            desenhar_linha(f"[FILA]  {tipo}")
        
    def limpar_eventos(self):
        self.fila_eventos.clear()
        self.eventos_ativos = []