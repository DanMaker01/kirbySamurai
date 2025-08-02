############################################################
# Evento, EventoSom,EventoMoverAtor,EventoLimpaEventos, ...
############################################################
# Modular: Sim
# Finalizada: Não
############################################################
# A Fazer:
# - Criar as propriedades extras
# - Padronizar os retornos no config??? deletar?
# - Set_visivel ? o que? ator?
# - 
# - 
############################################################
# Criar Eventos:
# - Mostrar texto
# - Mostrar opções
# - Mudar variáveis
# - Mudar cena
# - Mudar inventario
# - Piscar tela
# - Chamar menu
# - Parar música
# - 
# - 
############################################################

import pygame
from scripts.core.camera import Camera
from scripts.sistemas.gerenciador_tela import GerenciadorTela
from scripts.sistemas.gerenciador_som import Gerenciador_Som 
from scripts.sistemas.gerenciador_atores import Gerenciador_Atores
from scripts.atores.ator import Ator
from scripts.sistemas.gerenciador_controle import Gerenciador_Controle
# ==============================================================================
# Evento
# ==============================================================================
class Evento:
    def __init__(self, duracao_ms, callback=None):
        if duracao_ms == 0:
            duracao_ms = 1 # para evitar divisões por 0, etc...
        self.duracao = duracao_ms
        self.callback = callback
        self.inicio = None
        self.concluido = False

    def iniciar(self, tempo_atual):
        self.inicio = tempo_atual
        self.concluido = False
        # print(f"iniciando:\t{self.__class__.__name__}\t\t{self.duracao}\t{self.inicio}")

    def atualizar(self, tempo_atual):
        if self.concluido:
            return
        if self.inicio == None:
            self.concluido = True
            return
        if tempo_atual - self.inicio >= self.duracao:
            self.concluido = True

    def desenhar(self, tela):
        pass  # por padrão não desenha nada
# ==============================================================================

# ==============================================================================
# Tipos de Eventos
# ==============================================================================
class EventoSom(Evento):
    def __init__(self, gerenciador_som,nome_som,volume=1.0, callback=None):
        super().__init__(0, callback)
        self.gerenciador_som:Gerenciador_Som = gerenciador_som
        self.nome_som = nome_som
        self.volume = volume
    def iniciar(self, tempo_atual):
        self.gerenciador_som.tocar_som(self.nome_som, volume=self.volume)
        # print(f"tocando:{self.nome_som}, vol={self.volume}")
        # return super().iniciar(tempo_atual)
# ==============================================================================
class EventoInputLock(Evento):
    def __init__(self,gerenciador_controle, valor, callback=None):
        super().__init__(0, callback)
        self.valor = valor
        self.gerenciador_controle:Gerenciador_Controle = gerenciador_controle

    def iniciar(self, tempo_atual):
        super().iniciar(tempo_atual)
        self.gerenciador_controle.set_input_lock(self.valor)
        # self.concluido = True
        pass
        
        # return super().iniciar(tempo_atual)
# ==============================================================================
class EventoEspera(Evento):
    # Apenas espera sem desenhar nada 
    pass
# ==============================================================================
class EventoLimpaEventos(Evento):
    def __init__(self,gerenciador_eventos, callback=None):
        super().__init__(0, callback)
        self.gerenciador_eventos = gerenciador_eventos
    def iniciar(self, tempo_atual):
        super().iniciar(tempo_atual)
        self.gerenciador_eventos.limpar_eventos()
        pass
# ==============================================================================

# =======================
# Ator
# =======================
class EventoAtorAnimacao(Evento):
    def __init__(self, gerenciador_atores:Gerenciador_Atores, nome_ator,nome_animacao, callback=None):
        super().__init__(0, callback)
        self.gerenciador_atores = gerenciador_atores
        self.nome_ator = nome_ator
        self.nome_animacao = nome_animacao
    def iniciar(self,tempo_atual):
        super().iniciar(tempo_atual)
        ator :Ator = self.gerenciador_atores.pegar_ator(self.nome_ator)
        ator.animacoes.trocar(self.nome_animacao)
# ==============================================================================
class EventoAtorVisibilidade(Evento):
    def __init__(self, gerenciador_atores, nome_ator, valor, callback=None):
        super().__init__(0, callback)
        self.valor = valor
        self.gerenciador_atores :Gerenciador_Atores = gerenciador_atores
        self.nome_ator = nome_ator
    def iniciar(self, tempo_atual):
        super().iniciar(tempo_atual)
        ator = self.gerenciador_atores.pegar_ator(self.nome_ator)
        # if ator == None:
        #     print("não achou ator:",self.nome_ator)
        #     return
        ator.set_visivel(self.valor)
        # self.concluido = True
    # ==============================================================================
# ==============================================================================
class EventoMoverAtorPorIncremento(Evento):
    def __init__(self, duracao_ms, gerenciador_atores, nome_ator, delta_x=0, delta_y=0, callback=None):
        super().__init__(duracao_ms, callback)
        self.gerenciador_atores: Gerenciador_Atores = gerenciador_atores
        self.nome_ator = nome_ator
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.inicio_x = None
        self.inicio_y = None
        self.destino_x = None
        self.destino_y = None

    def iniciar(self, tempo_atual):
        super().iniciar(tempo_atual)
        ator: Ator = self.gerenciador_atores.pegar_ator(self.nome_ator)
        if ator is None:
            print('Não achou o ator:', self.nome_ator)
            return

        self.inicio_x, self.inicio_y = ator.fisica.posicao
        self.destino_x = self.inicio_x + self.delta_x
        self.destino_y = self.inicio_y + self.delta_y

        duracao_seg = self.duracao / 1000.0  # ms → s
        vel_x = self.delta_x / duracao_seg
        vel_y = self.delta_y / duracao_seg

        ator.fisica.set_vel(vel_x, vel_y)

    def atualizar(self, tempo_atual):
        if self.concluido:
            return
        if tempo_atual - self.inicio >= self.duracao:
            ator = self.gerenciador_atores.pegar_ator(self.nome_ator)
            ator.fisica.set_vel(0.0, 0.0)
            ator.set_posicao(self.destino_x, self.destino_y)  # Corrige qualquer imprecisão
            self.concluido = True
            if self.callback:
                self.callback()
# ==============================================================================
class EventoMoverAtor(Evento):
    def __init__(self, duracao_ms, gerenciador_atores, nome_ator, destino_x= None, destino_y = None, callback=None):
        super().__init__(duracao_ms, callback)
        self.gerenciador_atores :Gerenciador_Atores= gerenciador_atores
        self.nome_ator = nome_ator
        self.destino_x = destino_x
        self.destino_y = destino_y
        self.inicio_x = None
        self.inicio_y = None

    def iniciar(self, tempo_atual):
        super().iniciar(tempo_atual)
        ator:Ator = self.gerenciador_atores.pegar_ator(self.nome_ator)
        if ator == None:
            print('não achou o ator:',self.nome_ator)
            return
        # ator.fisica.set_vel()
        self.inicio_x, self.inicio_y = ator.fisica.posicao

        if self.destino_x == None:
            self.destino_x = self.inicio_x    

        if self.destino_y == None: 
            self.destino_y = self.inicio_y

        dx = self.destino_x - self.inicio_x
        dy = self.destino_y - self.inicio_y
        
        duracao_seg = self.duracao / 1000.0  # ms → s

        vel_x = dx / duracao_seg
        vel_y = dy / duracao_seg

        ator.fisica.set_vel(vel_x, vel_y)

    def atualizar(self, tempo_atual):
        if self.concluido:
            return
        if tempo_atual - self.inicio >= self.duracao:
            ator = self.gerenciador_atores.pegar_ator(self.nome_ator)
            # print(ator)
            ator.fisica.set_vel(0.0, 0.0)
            ator.set_posicao(self.destino_x, self.destino_y)  # Corrige qualquer imprecisão
            self.concluido = True
            if self.callback:
                self.callback()
# ============================================
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
# ==============================================================================
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
        
        if proporcao >= 1.0:
            self.concluido = True
            proporcao = 1
            if self.callback:
                self.callback()
