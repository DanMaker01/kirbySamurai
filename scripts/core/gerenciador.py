
######################################################
# Gerenciador
######################################################
# Orquestra os sistemas modulares
######################################################
# Modular: Não, criar classe de Roteiro, Cena, Etc
# Finalizada: Não
######################################################
# A Fazer: 
# - Sistema de empate (E)
# - Dialogo
# - GerenciadorEscolhas
######################################################
# - Inventario 
# - GerenciadorCena ??? Futuramente
# - Roteiro???? cena já resolve? não! Então Roteiro lê uma variável
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
from scripts.sistemas.gerenciador_variaveis import GerenciadorVariaveis
# UI
from scripts.ui.notificador import Notificador
# Atores #deve sair daqui em breve
from scripts.atores.ator import Ator
######################################################
class Gerenciador:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.tempo_atual = pygame.time.get_ticks()#repete no update

        # Core
        self.notificador = Notificador(self.screen)
        self.memoria = Persistencia()
        self.placar = Placar(y=350)
        self.camera             = Camera(largura_tela=WIDTH, altura_tela=HEIGHT)
        # Subsistemas
        self.gerenciador_atores = Gerenciador_Atores()
        self.gerenciador_som    = Gerenciador_Som()
        self.gerenciador_tela   = GerenciadorTela(iniciar_preto=True)
        self.gerenciador_controle=Gerenciador_Controle()
        self.gerenciador_variaveis = GerenciadorVariaveis()

        self.tempo_largada = -1

        # quase todos gerenciadores serão passados. Passar gerenciador em si? #????
        self.gerenciador_eventos= GerenciadorEventos(self.gerenciador_controle, 
                                                     self.gerenciador_som,
                                                     self.gerenciador_tela, 
                                                     self.gerenciador_atores,
                                                     self.camera)
        #UI
        

        #carregar sons
        self._carregar_som()

        # Preparar cena e roteiro #??? mudar para carregar_cena
        self.reset()

    def _carregar_som(self):
        self.gerenciador_som.carregar_som("ataque1", "audio/094-Attack06.wav")
        self.gerenciador_som.carregar_som("ataque2", "audio/095-Attack07.wav")
        self.gerenciador_som.carregar_som("largada", "audio/056-Right02.wav")
        self.gerenciador_som.carregar_musica("vento", "audio/003-Wind03.wav")
        
    def reset(self):#????
        self._criar_atores()
        self._setup_eventos()

    def _criar_atores(self):
        ##############################################
        bg = Ator(animacoes={
            'padrao': Animacao( ['bg.png'] )})

        triangulo_sup = Ator(pos = (-360,0), animacoes={
            "padrao": Animacao(["triangulo_sup2.png"])})
        
        triangulo_inf = Ator(pos = (360,0), animacoes={
            "padrao": Animacao(["triangulo_inf2.png",])})
        
        
        ##############################################
        y_geral = 150
        player1 = Ator(pos = (40,0+y_geral), animacoes={
            # "parado": Animacao( [f"et0{i}.png" for i in range(6)] ),
            "parado" : Animacao( ["p1_parado.png",] ),
            "ataque": Animacao( ["p1_ataque.png",] ),
            "ataque_fim": Animacao( ["p1_ataque_fim.png",] ),
            })

        player2 =  Ator(pos = (240,30+y_geral), animacoes={
            "parado": Animacao( ["p2_parado.png"] ),
            "ataque": Animacao( ["p2_ataque.png"] ),
            "ataque_fim": Animacao( ["p2_ataque_fim.png"] ),
            })
        
        ##############################################
        largada =  Ator(pos = (WIDTH/2-30,HEIGHT/16), 
                        animacoes={"parado": Animacao( ["largada00.png","largada01.png"] )},
                        visivel=False)
        
        ##############################################
        # adiciona
        self.gerenciador_atores.adicionar_ator('bg', bg)
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
        self.gerenciador_eventos.adicionar_espera(1500)
        self.gerenciador_eventos.adicionar_ator_move(1500,'t1',-360,0) 
        self.gerenciador_eventos.adicionar_ator_move(1500,'t2',360,0) 

        # self.gerenciador_eventos.adicionar_espera(500)

        self.gerenciador_eventos.adicionar_espera(1000)
        self.gerenciador_eventos.adicionar_fade_out(1000)
        
        tempo_random_largada = random.randint(1000, 4000)
        self.gerenciador_eventos.adicionar_espera(tempo_random_largada)
        self.gerenciador_eventos.adicionar_input_lock(False)
        
        
        self.gerenciador_eventos.adicionar_espera(0)
        self.gerenciador_eventos.adicionar_fade_in(0)
        self.gerenciador_eventos.adicionar_ator_set_visibilidade('largada',True,callback=self._salvar_tempo_largada)
        self.gerenciador_eventos.adicionar_som('largada',0.4)
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
        # self.gerenciador_eventos.desenhar_debug(self.screen)
        self.notificador.draw()
        # print("self.camera.pos::\t", self.camera.pos_x, self.camera.pos_y, " -> ",self.camera.objetivo_x, self.camera.objetivo_y)

    def input(self, acao):
        if self.gerenciador_controle.input_lock:
            print(f"[ {acao} ]\t->\tEntrada ignorada: controle travado.")
            return
        
        # necessário?
        self.gerenciador_controle.input_lock = True
        self.gerenciador_eventos.limpar_eventos()

        ator_largada = self.gerenciador_atores.pegar_ator('largada')
        if not ator_largada.get_visivel():
            # Erro de largada, ponto vai para o oponente
            oponente = 'p2' if acao == P1_HIT else 'p1'
            print(f"{acao} ERROU!")
            self.placar.adicionar_pontos(oponente, 1)
            self.reset()
            return

        if acao in (P1_HIT, P2_HIT):
            # Acerto
            # ===================================================
            
            # Config
            # ===================================================
            nome_jogador_atacando    = 'p1' if acao == P1_HIT else 'p2'
            #
            deslocamento = +150 if nome_jogador_atacando == 'p1' else -150
            pos_msg      = (90, 50) if nome_jogador_atacando == 'p1' else (WIDTH - 80, 50)

            # Som de ataque aleatório
            nome_som = "ataque1" if random.randint(0, 1) == 0 else "ataque2"
            
            # ===================================================
            self.gerenciador_eventos.adicionar_espera(1)
            self.gerenciador_eventos.adicionar_som(nome_som)
            self.gerenciador_eventos.adicionar_ator_muda_animacao(nome_jogador_atacando,"ataque")
            self.gerenciador_eventos.adicionar_ator_move_incremento(1,nome_jogador_atacando,deslocamento)
            
            self.gerenciador_eventos.adicionar_espera(200)
            self.gerenciador_eventos.adicionar_ator_move_incremento(500, nome_jogador_atacando,deslocamento/1.5,0)
            self.gerenciador_eventos.adicionar_espera(300)
            self.gerenciador_eventos.adicionar_ator_muda_animacao(nome_jogador_atacando,'ataque_fim')

            self.gerenciador_eventos.adicionar_espera(200)
            self.gerenciador_eventos.adicionar_ator_muda_animacao(nome_jogador_atacando, "parado")

            # self.gerenciador_eventos.adicionar_espera(500)
            print(f"{nome_jogador_atacando.upper()} acertou!")
            self.placar.adicionar_pontos(nome_jogador_atacando, 1)

            tempo_reacao = pygame.time.get_ticks() - self.tempo_largada
            tempo_str = f"{tempo_reacao / 1000:.3f}s"
            self.notificador.adicionar_mensagem(f"{nome_jogador_atacando.upper()} acertou!",  500, *pos_msg)
            self.notificador.adicionar_mensagem(f"{tempo_str}",                 1000, *pos_msg)
            # self.notificador.adicionar_mensagem(f"{tempo_str}", *pos_msg)

            self.gerenciador_eventos.adicionar_espera(2000)
            self.gerenciador_eventos.adicionar_espera(1000)
            self.gerenciador_eventos.adicionar_fade_out(1000, callback=self.reset)
