###########################################
# Evento
###########################################
# Modular: Sim
# Finalizada: Não
###########################################
# A Fazer:
# - Criar as propriedades extras
# - Padronizar os retornos no config
# - InputLock
# - Modificar Variavel
# - 
# - Chamar Diálogo
# - Abrir Opções
# - 
# - 
# - 
# - 
# - 
# - Provavelmente draw não será necessário em nenhum evento
# - 
###########################################
# from config import EV_ABRIR_DIALOGO, EV_
import pygame
from camera import Camera
from gerenciador_tela import GerenciadorTela
##########################################################################
class Evento:
    def __init__(self, duracao_ms, callback=None):
        self.duracao = duracao_ms
        self.callback = callback
        self.inicio = None
        self.concluido = False

    def iniciar(self, tempo_atual):
        self.inicio = tempo_atual
        self.concluido = False
        print("iniciando:\t",self.__class__.__name__, self.duracao, self.inicio)

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
from gerenciador_atores import Gerenciador_Atores
class EventoMoverAtor(Evento):
    def __init__(self, duracao_ms,gerenciador_atores:Gerenciador_Atores, callback=None):
        super().__init__(duracao_ms, callback)
        self.gerenciador_atores = gerenciador_atores
    
    def atualizar(self, tempo_atual):
        # return super().atualizar(tempo_atual)
        pass

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
class EventoMoverCamera(Evento):
    def __init__(self, duracao_ms, camera: Camera, destino_x, destino_y, callback=None):
        super().__init__(duracao_ms, callback)
        self.camera = camera
        self.destino_x = destino_x
        self.destino_y = destino_y
        self.inicio_x = None
        self.inicio_y = None

    def iniciar(self, tempo_atual):
        super().iniciar(tempo_atual)
        # Salva a posição inicial atual da câmera para interpolar
        self.inicio_x = self.camera.pos_x
        self.inicio_y = self.camera.pos_y
        print(self.inicio_x, self.inicio_y," -> ", self.destino_x, self.destino_y)

    def atualizar(self, tempo_atual):
        if self.concluido:
            return

        tempo_passado = tempo_atual - self.inicio
        proporcao = min(1.0, tempo_passado / self.duracao)
        # Interpola linearmente a posição da câmera
        nova_x = self.inicio_x + (self.destino_x - self.inicio_x) * proporcao
        nova_y = self.inicio_y + (self.destino_y - self.inicio_y) * proporcao
        
        # self.camera.set_posicao(nova_x, nova_y)
        self.camera.mover_para(nova_x, nova_y)
        
        print(f"self.camera.pos: ",self.camera.pos_x,self.camera.pos_y )
        
        if proporcao >= 1.0:
            self.concluido = True
            proporcao = 1
            if self.callback:
                self.callback()
