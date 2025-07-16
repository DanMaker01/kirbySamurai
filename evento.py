###########################################
# Evento
###########################################
# Modular: Sim
# Finalizada: Não
###########################################
# A Fazer:
# - Definir mais tipos de eventos e como eles agem
# - Criar as propriedades extras
# - Padronizar os retornos no config
# - InputLock
# - Modificar Variavel
# - Modificar Tela
# - Chamar Diálogo
# - Abrir Opções
# - 
# - 
# - 
# - 
# - 
# - 
# - 
###########################################
# from config import EV_ABRIR_DIALOGO, EV_
import pygame
from gerenciador_tela import GerenciadorTela
##########################################################################
class Evento:
    def __init__(self, duracao_ms, callback=None):
        self.duracao = duracao_ms
        self.callback = callback
        self.inicio = None
        self.concluido = False

    def iniciar(self, tempo_atual):
        print("iniciando:\t",self.__class__.__name__, self.duracao, self.inicio)
        self.inicio = tempo_atual
        self.concluido = False

    def atualizar(self, tempo_atual):
        if self.concluido:
            return
        if tempo_atual - self.inicio >= self.duracao:
            self.concluido = True

    def desenhar(self, tela):
        pass  # por padrão não desenha nada

##########################################################################

class EventoEspera(Evento):
    # Apenas espera sem desenhar nada 
    pass

##########################################################################

class EventoFade(Evento):
    def __init__(self, tipo, duracao_ms, tela: GerenciadorTela, callback=None):
        super().__init__(duracao_ms, callback)
        self.tipo = tipo
        self.tela = tela

    def atualizar(self, tempo_atual):
        if self.concluido:
            return

        tempo_passado = tempo_atual - self.inicio
        proporcao = min(1.0, tempo_passado / self.duracao)

        if self.tipo == "in":
            alfa = int(255 * (1 - proporcao))
        else:
            alfa = int(255 * proporcao)

        self.tela.set_tintura(alfa)

        if proporcao >= 1.0:
            self.concluido = True

    def desenhar(self, tela):
        # Nada — o GerenciadorTela já desenha automaticamente com o alfa atual
        pass



##########################################################################