
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
from scripts.core.janela import JanelaSelecionavel
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
from scripts.sistemas.gerenciador_janelas import GerenciadorJanelas
# UI
from scripts.ui.notificador import Notificador
# Atores #deve sair daqui em breve
from scripts.atores.ator import Ator
######################################################
class Gerenciador:
    def __init__(self, screen:pygame.Surface, clock):
        self.screen = screen
        self.clock = clock
        self.tempo_atual = pygame.time.get_ticks()#repete no update

        # Core
        self.notificador            = Notificador(self.screen)
        self.memoria                = Persistencia()
        self.placar                 = Placar(y=350,players=2)
        self.camera                 = Camera(largura_tela=WIDTH, altura_tela=HEIGHT)
        # Subsistemas
        self.gerenciador_atores     = Gerenciador_Atores()
        self.gerenciador_som        = Gerenciador_Som()
        self.gerenciador_tela       = GerenciadorTela(iniciar_preto=True)
        self.gerenciador_controle   =Gerenciador_Controle()
        self.gerenciador_variaveis  =GerenciadorVariaveis()
        self.gerenciador_janelas    =GerenciadorJanelas()

        self.tempo_largada = -1     # pq??? parece gambiarra isso aqui
        self.continuar = False
        # quase todos gerenciadores serão passados. Passar gerenciador em si? #????
        self.gerenciador_eventos= GerenciadorEventos(self.gerenciador_controle, 
                                                     self.gerenciador_som,
                                                     self.gerenciador_tela, 
                                                     self.gerenciador_atores,
                                                     self.camera)
    
        # Preparar cena e roteiro #??? mudar para carregar_cena
        self.reset()

    def _carregar_som(self):
        self.gerenciador_som.carregar_musica("vento",   "audio/003-Wind03.wav")
        self.gerenciador_som.carregar_som   ("ataque1", "audio/094-Attack06.wav")
        self.gerenciador_som.carregar_som   ("ataque2", "audio/095-Attack07.wav")
        self.gerenciador_som.carregar_som   ("largada", "audio/056-Right02.wav")
        self.gerenciador_som.carregar_som   ("falta",   "audio/057-Wrong01.wav")
        self.gerenciador_som.carregar_som   ("tick",   "audio/tick.wav")
        
    def reset(self):#???? acho que deveria ser reset cena, deve ser controlado pelo Gerenciador_Cena
        
        if self.placar.diferenca_maior_que(2) and not self.continuar:
            self.gerenciador_janelas.ativar('rematch')
            print("ativou janela")
        
        else:
            self.gerenciador_janelas.resetar()
            self.gerenciador_janelas.adicionar_janela(nome='rematch',
                                                    janela=JanelaSelecionavel( 
                                                        ["Revanche","Continuar","Sair"],
                                                        x=WIDTH/2-WIDTH/8,
                                                        y=20 ),
                                                    ativa=False)
            
            self._carregar_som()
            self._carregar_atores()
            self._carregar_eventos_iniciais()

    def _carregar_atores(self):
        ##############################################
        bg = Ator(animacoes={
            'padrao': Animacao( ['bg.png'] )})

        triangulo_sup = Ator(pos = (-360,0), animacoes={
            "padrao": Animacao(["triangulo_sup2.png"])})
        
        triangulo_inf = Ator(pos = (360,0), animacoes={
            "padrao": Animacao(["triangulo_inf2.png",])})
        ##############################################
        y_geral = 150
        player1 = Ator(pos = (40,20+y_geral), animacoes={
            # "parado": Animacao( [f"et0{i}.png" for i in range(6)] ),
            "parado" : Animacao( ["p1_parado.png",] ),
            "ataque": Animacao( ["p1_ataque.png",] ),
            "ataque_fim": Animacao( ["p1_ataque_fim.png",] ),
            "apanhando": Animacao( ["p1_apanhando.png",] ),
            })

        player2 =  Ator(pos = (240,30+y_geral), animacoes={
            "parado": Animacao( ["p2_parado.png"] ),
            "ataque": Animacao( ["p2_ataque.png"] ),
            "ataque_fim": Animacao( ["p2_ataque_fim.png"] ),
            "apanhando": Animacao( ["p2_apanhando.png"] ),
            })
        ##############################################
        largada =  Ator(pos = (WIDTH/2-30,HEIGHT/16), 
                        animacoes={"parado": Animacao( ["largada00.png","largada01.png"] )},
                        visivel=False)
        
        falta = Ator(animacoes={"parado": Animacao( ["falta00.png", "falta01.png"] )},
                     pos = (WIDTH/2-30,HEIGHT/16 + 60),
                     visivel=False)
        ##############################################
        # adiciona
        self.gerenciador_atores.adicionar_ator('bg', bg)
        self.gerenciador_atores.adicionar_ator('p1', player1)
        self.gerenciador_atores.adicionar_ator('p2', player2)
        self.gerenciador_atores.adicionar_ator("t1", triangulo_sup)
        self.gerenciador_atores.adicionar_ator("t2", triangulo_inf)
        self.gerenciador_atores.adicionar_ator("largada", largada)
        self.gerenciador_atores.adicionar_ator("falta", falta)

    def _carregar_eventos_iniciais(self):
        self.gerenciador_som.tocar_musica("vento", loop=True)
        self.gerenciador_eventos.adicionar_espera()
        self.gerenciador_eventos.adicionar_input_lock(True)
        
        self.gerenciador_eventos.adicionar_espera(2000)
        self.gerenciador_eventos.adicionar_fade_in(2000)

        self.gerenciador_eventos.adicionar_espera(500)

        self.gerenciador_eventos.adicionar_espera(2000)
        self.gerenciador_eventos.adicionar_ator_move(2000,'t1',-10,0) 
        self.gerenciador_eventos.adicionar_ator_move(2000,'t2',10,0) 
        
        self.gerenciador_eventos.adicionar_espera(1500)
        #
        self.gerenciador_eventos.adicionar_espera(1500)
        self.gerenciador_eventos.adicionar_ator_move(1500,'t1',-360,0) 
        self.gerenciador_eventos.adicionar_ator_move(1500,'t2',360,0) 

        self.gerenciador_eventos.adicionar_espera(1000)
        self.gerenciador_eventos.adicionar_fade_out(1000)
        
        tempo_random_largada = random.randint(600, 4500)
        self.gerenciador_eventos.adicionar_espera(tempo_random_largada)
        self.gerenciador_eventos.adicionar_input_lock(False)
        
        self.gerenciador_eventos.adicionar_espera()
        self.gerenciador_eventos.adicionar_fade_in()
        self.gerenciador_eventos.adicionar_ator_set_visibilidade('largada',True,callback=self._salvar_tempo_largada)
        self.gerenciador_eventos.adicionar_som('largada', 0.4)
        
        self.gerenciador_eventos.adicionar_espera(4000)

        # trava o controle, ninguem reagiu
        self.gerenciador_eventos.adicionar_espera()
        self.gerenciador_eventos.adicionar_ator_set_visibilidade('largada',False)
        self.gerenciador_eventos.adicionar_input_lock(True)
        
        self.gerenciador_eventos.adicionar_espera(2000)
        self.gerenciador_eventos.adicionar_fade_out(2000)
        
        self.gerenciador_eventos.adicionar_espera(1000)
        self.gerenciador_eventos.adicionar_limpa_eventos(callback=self.reset)
        pass

    def _salvar_tempo_largada(self):
        self.tempo_largada = pygame.time.get_ticks()

    def update(self, dt):
        self.tempo_atual = pygame.time.get_ticks()
        # if len(self.gerenciador_janelas.listar_ativas()) >= 1:
            
        self.gerenciador_eventos.atualizar(self.tempo_atual)
        self.gerenciador_tela.atualizar(self.tempo_atual, dt)
        self.gerenciador_atores.update(dt)
        self.camera.atualizar(dt)
        self.placar.atualizar(dt)
        self.notificador.atualizar()
        # self.gerenciador_janelas.atualizar()
        # self.menu_rematch = #não tem update, mas se tiver será aqui

    def draw(self):
        # Aqui a ordem importa. O que é desenhando primeiro fica atrás.
        # =======================================================
        # Limpa tela
        self.screen.fill((0, 0, 0))  # Preenche a tela com preto (vazio)
        # =======================================================
        # Desenha Atores e Efeitos de Tela 
        # ???cada classe vai agir dependendo da camera? 
        # print("self.camera.pos::\t", self.camera.pos_x, self.camera.pos_y, " -> ",self.camera.objetivo_x, self.camera.objetivo_y)
        self.gerenciador_atores.draw(self.screen, (-self.camera.pos_x, -self.camera.pos_y)) # deve receber uma defasagem pela câmer
        self.gerenciador_tela.desenhar(self.screen)
        # =======================================================
        # Desenha UI
        self.placar.draw(self.screen)
        self.gerenciador_janelas.desenhar(self.screen)
        self.notificador.draw()
        # =======================================================

    def input(self, acao):
        
        
        nome_janela_ativa = self.gerenciador_janelas.listar_ativas()
        if nome_janela_ativa != []:
            janela_ativa = self.gerenciador_janelas.get(nome_janela_ativa[0])
            if janela_ativa:
                if acao == 'cima' or acao == 'esquerda':
                    janela_ativa.voltar()
                if acao == 'baixo' or acao == 'direita':
                    janela_ativa.avancar()
                if acao in [CONFIRM,P1_HIT, P2_HIT]:
                    resultado = janela_ativa.selecionar()
                    if (resultado) == "Revanche":
                        self.placar.zerar_placar()
                        self.gerenciador_janelas
                        self.gerenciador_eventos.limpar_eventos()
                        self.gerenciador_eventos.adicionar_espera(1000)
                        self.gerenciador_eventos.adicionar_fade_out(1000, callback=self.reset)
                        pass
                    elif resultado == "Continuar":
                        self.continuar = True
                        self.gerenciador_eventos.limpar_eventos()
                        self.gerenciador_eventos.adicionar_espera(1000)
                        self.gerenciador_eventos.adicionar_fade_out(1000, callback=self.reset)
                        pass
                    elif resultado == "Sair":
                        print("...encerrando jogo.")
                        pygame.quit()
                        # sys.exit()
                        pass
                    
                return

        if self.gerenciador_controle.input_lock:
            print(f"[ {acao} ]\t->\tEntrada ignorada: controle travado.")
            self.gerenciador_som.tocar_som('tick', 0.20)
            return

        # necessário?
        self.gerenciador_controle.input_lock = True
        self.gerenciador_eventos.limpar_eventos()

        ator_largada = self.gerenciador_atores.pegar_ator('largada')

        if not ator_largada.get_visivel():
            # Erro de largada, ponto vai para o oponente
            oponente = 'p2' if acao == P1_HIT else 'p1'
            nome_som_falta = "falta"
            # SEUENCIA DE EVENTOS ===================================================
            self.gerenciador_eventos.adicionar_fade_in()
            self.gerenciador_eventos.adicionar_espera(1)
            self.gerenciador_eventos.adicionar_som(nome_som_falta)
            self.gerenciador_eventos.adicionar_ator_set_visibilidade('falta',valor=True)
            
            self.gerenciador_eventos.adicionar_espera(2000)
            
            self.gerenciador_eventos.adicionar_espera(1000)
            self.gerenciador_eventos.adicionar_fade_out(1000, callback=self.reset)           
            # ===================================================
            self.placar.adicionar_pontos(oponente, 1)
            return

        if acao in (P1_HIT, P2_HIT):
            # Acerto
            # ===================================================
            # Config
            nome_jogador_atacando    = 'p1' if acao == P1_HIT else 'p2'
            nome_jogador_morto       = 'p2' if acao == P1_HIT else 'p1'
            # posicionamento e movimento
            deslocamento = +150 if nome_jogador_atacando == 'p1' else -150
            pos_msg      = (90, 50) if nome_jogador_atacando == 'p1' else (WIDTH - 80, 50)
            # Som de ataque aleatório
            nome_som = "ataque1" if random.randint(0, 1) == 0 else "ataque2"
            # SEUENCIA DE EVENTOS ===================================================
            self.gerenciador_eventos.adicionar_espera(1)
            self.gerenciador_eventos.adicionar_som(nome_som)
            self.gerenciador_eventos.adicionar_ator_muda_animacao(nome_jogador_atacando,"ataque")
            self.gerenciador_eventos.adicionar_ator_move_incremento(1,nome_jogador_atacando,deslocamento)
            
            self.gerenciador_eventos.adicionar_espera(200)
            self.gerenciador_eventos.adicionar_ator_move_incremento(500, nome_jogador_atacando,deslocamento/1.5,0)
            self.gerenciador_eventos.adicionar_espera(300)
            self.gerenciador_eventos.adicionar_ator_muda_animacao(nome_jogador_atacando,'ataque_fim')
            self.gerenciador_eventos.adicionar_ator_muda_animacao(nome_jogador_morto,'apanhando')

            self.gerenciador_eventos.adicionar_espera(200)
            self.gerenciador_eventos.adicionar_ator_muda_animacao(nome_jogador_atacando, "parado")

            self.placar.adicionar_pontos(nome_jogador_atacando, 1)

            # Mostrar tempo de reação e Notificar-lo na tela.
            tempo_reacao = pygame.time.get_ticks() - self.tempo_largada
            tempo_str = f"{tempo_reacao / 1000:.3f}s"
            self.notificador.adicionar_mensagem(f"{nome_jogador_atacando.upper()} acertou!",  500, *pos_msg)
            self.notificador.adicionar_mensagem(f"{tempo_str}",                 1000, *pos_msg)

            self.gerenciador_eventos.adicionar_espera(2000)
            
            self.gerenciador_eventos.adicionar_espera(1000)
            self.gerenciador_eventos.adicionar_fade_out(1000, callback=self.reset)
            pass