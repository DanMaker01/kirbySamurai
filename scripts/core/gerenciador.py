
######################################################
# Gerenciador
######################################################
# Orquestra os sistemas modulares
######################################################
# Modular: Não, criar classe de Roteiro, Cena, Etc
# Finalizada: Não
######################################################
# A Fazer: 
# - Inventario 
# - GerenciadorEscolhas
# - Dialogo
# - GerenciadorCena
# - Roteiro???? cena já resolve? não! Então Roteiro lê uma variável
# - Sistema de empate (E)
######################################################
import pygame
import random
# core
from scripts.core.config import *
from scripts.core.placar import Placar
from scripts.core.persistencia import Persistencia
from scripts.core.animacao import Animacao
from scripts.core.evento import *
from scripts.core.camera import Camera
# sub-sistemas
from scripts.sistemas.gerenciador_atores import Gerenciador_Atores
from scripts.sistemas.gerenciador_som import Gerenciador_Som
from scripts.sistemas.gerenciador_eventos import GerenciadorEventos
from scripts.sistemas.gerenciador_tela import GerenciadorTela
from scripts.sistemas.gerenciador_controle import Gerenciador_Controle
# UI
from scripts.ui.notificador import Notificador
# Atores #deve sair daqui em breve
from scripts.atores.ator import Ator
######################################################
class Gerenciador:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.tempo_atual = pygame.time.get_ticks()

        # Core
        self.notificador = Notificador(self.screen)
        self.memoria = Persistencia()
        self.placar = Placar()
        self.camera             = Camera(largura_tela=WIDTH, altura_tela=HEIGHT)
        # Subsistemas
        self.gerenciador_atores = Gerenciador_Atores()
        self.gerenciador_som    = Gerenciador_Som()
        self.gerenciador_tela   = GerenciadorTela(iniciar_preto=True)
        self.gerenciador_controle=Gerenciador_Controle()

        self.tempo_largada = -1

        self.gerenciador_eventos= GerenciadorEventos(self.gerenciador_controle, 
                                                     self.gerenciador_som,
                                                     self.gerenciador_tela, 
                                                     self.gerenciador_atores,
                                                     self.camera)
        #UI
        

        #carregar sons
        self.gerenciador_som.carregar_som("ataque1", "audio/094-Attack06.wav")
        self.gerenciador_som.carregar_som("ataque2", "audio/095-Attack07.wav")
        self.gerenciador_som.carregar_som("largada", "audio/056-Right02.wav")
        self.gerenciador_som.carregar_musica("vento", "audio/003-Wind03.wav")

        # Preparar cena e roteiro
        self.reset()

        
    def reset(self):
        self._criar_atores()
        self._setup_eventos()

    def _criar_atores(self):
        # 
        triangulo_sup = Ator(pos = (-360,0), animacoes={
            "padrao": Animacao(["triangulo_sup2.png"])})
        
        triangulo_inf = Ator(pos = (360,0), 
                             animacoes={"padrao": Animacao(["triangulo_inf2.png",])})
        #
        y_geral = 150
        player1 = Ator(pos = (20,20+y_geral), animacoes={
            "parado": Animacao( ["p1_parado.png",] ),
            "ataque": Animacao( ["p1_ataque.png",] )
            })

        player2 =  Ator(pos = (240,30+y_geral), animacoes={
            "parado": Animacao( ["p2_parado.png"] ),
            "ataque": Animacao( ["p2_ataque.png"] )
            })

        largada =  Ator(pos = (WIDTH/2-30,HEIGHT/6), 
                        animacoes={"parado": Animacao( ["largada00.png","largada01.png"] )},
                        visivel=False)
        
        # adiciona
        self.gerenciador_atores.adicionar_ator('p1', player1)
        self.gerenciador_atores.adicionar_ator('p2', player2)
        self.gerenciador_atores.adicionar_ator("t1", triangulo_sup)
        self.gerenciador_atores.adicionar_ator("t2", triangulo_inf)
        self.gerenciador_atores.adicionar_ator("largada", largada)

    def _setup_eventos(self):
        self.gerenciador_som.tocar_musica("vento", loop=True)
        self.gerenciador_eventos.adicionar_espera(0)
        self.gerenciador_eventos.adicionar_input_lock(True)
        
        self.gerenciador_eventos.adicionar_espera(2000)
        self.gerenciador_eventos.adicionar_fade_in(2000)

        self.gerenciador_eventos.adicionar_espera(500)

        self.gerenciador_eventos.adicionar_espera(2000)
        self.gerenciador_eventos.adicionar_ator_move(2000,'t1',-10,0) 
        self.gerenciador_eventos.adicionar_ator_move(2000,'t2',10,0) 
        
        # self.gerenciador_eventos.adicionar_espera(5000)
        # self.gerenciador_eventos.adicionar_espera(5000)
        
        self.gerenciador_eventos.adicionar_espera(1500)
        #
        self.gerenciador_eventos.adicionar_espera(2000)
        self.gerenciador_eventos.adicionar_ator_move(2000,'t1',-360,0) 
        self.gerenciador_eventos.adicionar_ator_move(2000,'t2',360,0) 

        # self.gerenciador_eventos.adicionar_espera(500)

        self.gerenciador_eventos.adicionar_espera(1000)
        self.gerenciador_eventos.adicionar_fade_out(1000)
        
        tempo_random_largada = random.randint(1000, 4000)
        self.gerenciador_eventos.adicionar_espera(tempo_random_largada)
        self.gerenciador_eventos.adicionar_input_lock(False)
        
        
        self.gerenciador_eventos.adicionar_espera(0)
        self.gerenciador_eventos.adicionar_fade_in(0)
        self.gerenciador_eventos.adicionar_ator_set_visibilidade('largada',True,callback=self._salvar_tempo_largada)
        self.gerenciador_eventos.adicionar_som('largada',0.5)
        # self.gerenciador_eventos.adicionar_espera(0,callback=self.gerenciador_som.tocar_som('largada'))
        
        #libera o controle, ativa contador, ...
        self.gerenciador_eventos.adicionar_espera(4000)

        # trava o controle, ninguem reagiu
        self.gerenciador_eventos.adicionar_espera(0)
        self.gerenciador_eventos.adicionar_ator_set_visibilidade('largada',False)
        self.gerenciador_eventos.adicionar_input_lock(True)
        
        self.gerenciador_eventos.adicionar_espera(2000)
        self.gerenciador_eventos.adicionar_fade_out(2000)
        
        self.gerenciador_eventos.adicionar_espera(1000)
        self.gerenciador_eventos.adicionar_limpa_eventos(callback=self.reset)

    def _salvar_tempo_largada(self):
        self.tempo_largada = pygame.time.get_ticks()

    def update(self, dt):
        self.tempo_atual = pygame.time.get_ticks()
        self.gerenciador_eventos.atualizar(self.tempo_atual)
        self.gerenciador_tela.atualizar(self.tempo_atual, dt)
        self.gerenciador_atores.update(dt)
        self.camera.atualizar(dt)
        self.placar.atualizar(dt)
        self.notificador.atualizar()

    def draw(self):
        self.screen.fill((0, 0, 0))  # Preenche a tela com preto (vazio)

        # atualizar aqui???? sim
        # cada classe vai agir dependendo da camera?
        self.gerenciador_atores.draw(self.screen, (-self.camera.pos_x, -self.camera.pos_y)) # deve receber uma defasagem pela câmera
        # self.gerenciador_eventos.desenhar(self.screen) #atualmente não faz nada, retirar???
        self.gerenciador_tela.desenhar(self.screen)
        self.placar.draw(self.screen)
        self.gerenciador_eventos.desenhar_debug(self.screen)
        self.notificador.draw()
        # print("self.camera.pos::\t", self.camera.pos_x, self.camera.pos_y, " -> ",self.camera.objetivo_x, self.camera.objetivo_y)

    def input(self, acao):
        if self.gerenciador_controle.input_lock:
            print(f"[ {acao} ]\t->\tEntrada ignorada: controle travado.")
            return
        self.gerenciador_controle.input_lock = True
        self._ataque(acao) #no momento do input, deve guardar os estados dos bindings no jogo, e o jogo decide quem venceu, pois aí dá pra tratar empates. #??????? (E)

    def _ataque(self, acao):
        self.gerenciador_eventos.limpar_eventos()

        ator_largada = self.gerenciador_atores.pegar_ator('largada')
        if not ator_largada.get_visivel():
            self._registrar_erro(acao)
            return

        if acao == P1_HIT:
            self._registrar_acerto('p1', deslocamento=+150, pos_msg=(20, 50))

        elif acao == P2_HIT:
            self._registrar_acerto('p2', deslocamento=-150, pos_msg=(WIDTH - 120, 50))

    def _registrar_acerto(self, jogador, deslocamento, pos_msg):
        
        r = random.randint(0,1)
        if r==0:
            self.gerenciador_som.tocar_som("ataque1")
        else:
            self.gerenciador_som.tocar_som("ataque2")

        ator = self.gerenciador_atores.pegar_ator(jogador)
        ator.transladar(deslocamento, 0)
        ator.animacoes.trocar("ataque")
        
        print(f"{jogador.upper()} acertou!")
        self.placar.adicionar_pontos(jogador, 1)

        tempo_reacao = pygame.time.get_ticks() - self.tempo_largada
        tempo_str = f"{tempo_reacao / 1000:.3f}s"
        self.notificador.adicionar_mensagem(f"{jogador.upper()} acertou!",  500, *pos_msg)
        self.notificador.adicionar_mensagem(f"{tempo_str}",                 2500, *pos_msg)

        self.gerenciador_eventos.adicionar_espera(2000)
        self.gerenciador_eventos.adicionar_espera(1000)
        self.gerenciador_eventos.adicionar_fade_out(1000, callback=self.reset)
        
        # self.gerenciador_eventos.adicionar_espera(1000, callback=self.reset)

    def _registrar_erro(self, acao):
        oponente = 'p2' if acao == P1_HIT else 'p1'
        print(f"{acao} ERROU!")
        self.placar.adicionar_pontos(oponente, 1)
        self.reset()