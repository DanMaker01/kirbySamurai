###########################################
# Cena01 - Jogo de Reação
###########################################
# A Fazer:
# - Sistema de empate (E)
# - Definir se o gereciador de atores fica na cena, no gerenciador de cena ou no gerenciador
###########################################
# - 
# - 
###########################################


###########################################
import random
from scripts.core.cena import Cena
from scripts.core.animacao import Animacao
from scripts.core.ator import Ator
from scripts.core.roteiro import Roteiro
from scripts.sistemas.gerenciador_atores import Gerenciador_Atores
from scripts.sistemas.gerenciador_janelas import GerenciadorJanelas, JanelaSelecionavel
# from scripts.sistemas.gerenciador_eventos import GerenciadorEventos
from scripts.sistemas.gerenciador_som import Gerenciador_Som
from scripts.core.placar import Placar
from scripts.ui.notificador import Notificador
# from scripts.sistemas.gerenciador_controle import Gerenciador_Controle
from scripts.core.config import *
from scripts.core.evento import *

class Cena01(Cena):
    # ver e julgar quais sistemas são de Cena e quais são exclusivos de Cena01 #??? Talvez todos de Cena?
    def __init__(self, gerenciador_atores, gerenciador_eventos, gerenciador_som, gerenciador_variaveis, gerenciador_controle,gerenciador_tela, notificador, gerenciador_janelas):
        super().__init__(gerenciador_atores, gerenciador_eventos, gerenciador_som, gerenciador_variaveis)
        self.gerenciador_controle : Gerenciador_Controle= gerenciador_controle
        self.gerenciador_tela     : GerenciadorTela     = gerenciador_tela
        self.notificador          : Notificador         = notificador
        self.gerenciador_janelas  : GerenciadorJanelas = gerenciador_janelas
        self.placar                                     = Placar(350,players=2)
        self.tempo_largada                              = -1

    def _carregar_atores(self):
        # super()._carregar_atores()
        # Plano de fundo
        bg = Ator(animacoes={'padrao': Animacao(['bg.png'])})

        # Triângulos
        triangulo_sup = Ator(pos=(-360, 0), animacoes={'padrao': Animacao(['triangulo_sup2.png'])})
        triangulo_inf = Ator(pos=(360, 0), animacoes={'padrao': Animacao(['triangulo_inf2.png'])})

        # Jogadores
        y_geral = 150
        player1 = Ator(pos=(40, 20 + y_geral), animacoes={
            "parado": Animacao(["p1_parado.png"]),
            "ataque": Animacao(["p1_ataque.png"]),
            "ataque_fim": Animacao(["p1_ataque_fim.png"]),
            "apanhando": Animacao(["p1_apanhando.png"]),
        })

        player2 = Ator(pos=(240, 30 + y_geral), animacoes={
            "parado": Animacao(["p2_parado.png"]),
            "ataque": Animacao(["p2_ataque.png"]),
            "ataque_fim": Animacao(["p2_ataque_fim.png"]),
            "apanhando": Animacao(["p2_apanhando.png"]),
        })

        # Largada e Falta
        largada = Ator(
            pos=(WIDTH / 2 - 30, HEIGHT / 16),
            animacoes={"parado": Animacao(["largada00.png", "largada01.png"])},
            visivel=False
        )

        falta = Ator(
            pos=(WIDTH / 2 - 30, HEIGHT / 16 + 60),
            animacoes={"parado": Animacao(["falta00.png", "falta01.png"])},
            visivel=False
        )

        # Registro
        self.gerenciador_atores : Gerenciador_Atores
        self.gerenciador_atores.adicionar_ator('bg', bg)
        self.gerenciador_atores.adicionar_ator('p1', player1)
        self.gerenciador_atores.adicionar_ator('p2', player2)
        self.gerenciador_atores.adicionar_ator('t1', triangulo_sup)
        self.gerenciador_atores.adicionar_ator('t2', triangulo_inf)
        self.gerenciador_atores.adicionar_ator('largada', largada)
        self.gerenciador_atores.adicionar_ator('falta', falta)
        # print(self.gerenciador_atores.atores)

    def _carregar_som(self):
        # super()._carregar_som()
        self.gerenciador_som : Gerenciador_Som
        self.gerenciador_som.carregar_musica("vento",   "audio/003-Wind03.wav")
        self.gerenciador_som.carregar_som   ("ataque1", "audio/094-Attack06.wav")
        self.gerenciador_som.carregar_som   ("ataque2", "audio/095-Attack07.wav")
        self.gerenciador_som.carregar_som   ("largada", "audio/056-Right02.wav")
        self.gerenciador_som.carregar_som   ("falta",   "audio/057-Wrong01.wav")
        self.gerenciador_som.carregar_som   ("tick",   "audio/tick.wav")
        pass

    def _carregar_roteiros(self):
        # super()._carregar_roteiros()
        # ==================================================================
        # Cria Roteiro Intro, sua primeira pagina
        tempo_random_largada = random.randint(600,4500)
        intro = Roteiro()
        intro.adicionar_pagina(
            condicao=None, 
            lista_eventos=[
                EventoMusica(self.gerenciador_som,'vento', loop=True),
                EventoEspera(),
                EventoInputLock(self.gerenciador_controle,True),
                EventoEspera(2000),
                EventoFade('in',2000,self.gerenciador_tela),
                EventoEspera(500),
                EventoEspera(2000),
                EventoMoverAtor(2000,self.gerenciador_atores,'t1',-10,0),
                EventoMoverAtor(2000,self.gerenciador_atores, 't2',10,0),
                EventoEspera(1500),
                EventoEspera(1500),
                EventoMoverAtor(1500,self.gerenciador_atores, 't1', -360,0),
                EventoMoverAtor(1500,self.gerenciador_atores, 't2', 360,0),
                EventoEspera(1000),
                EventoFade('out',1000,self.gerenciador_tela),
                EventoEspera(tempo_random_largada),
                EventoInputLock(self.gerenciador_controle, False),
                EventoEspera(),
                EventoFade('in',0,self.gerenciador_tela),
                EventoAtorVisibilidade(self.gerenciador_atores, 'largada',True,callback=self._salvar_tempo_largada),
                EventoSom(self.gerenciador_som,'largada',0.3),
                EventoEspera(4000),
                EventoEspera(),
                EventoAtorVisibilidade(self.gerenciador_atores,'largada', False),
                EventoInputLock(self.gerenciador_controle, True),
                EventoEspera(2000),
                EventoFade('out',2000,self.gerenciador_tela),
                EventoEspera(1000),
                EventoLimpaEventos(self.gerenciador_eventos,callback=self.reset)           
        ])
        
        # =================================================
        # Adicionar Roteiros à Cena
        self.adicionar_roteiro('intro',intro)
        # print("Quantos roteiros na cena:",len(self.roteiros))
        # print("condições:",pagina_atual_do_roteiro_intro.condicao)
        pagina_atual_do_roteiro_intro = self.chamar_roteiro('intro')

        # ================================================= 
        # Carregar os eventos na pagina inicial do roteiro, pro gerenciador eventos.
        for evento in pagina_atual_do_roteiro_intro.lista_eventos:
            self.gerenciador_eventos._adicionar_evento(evento)
        # =================================================
        pass


    def input(self, acao): # ajeitandof
        print("input recebido pela Cena01:",acao)

        if self.gerenciador_controle.input_lock:
            self.gerenciador_som.tocar_som('tick',volume=0.10) #imediatamente, não criar evento
            return
        
        # necessário?
        self.gerenciador_controle.input_lock = True
        self.gerenciador_eventos.limpar_eventos()
        # necessário?

        # se o ator 'largada' não estiver visivel, então:
        # ataque antes da hora, queimou largada
        if not self.gerenciador_atores.pegar_ator('largada').get_visivel():
            # Erro de largada, ponto vai para o oponente
            oponente = 'p2' if acao == P1_HIT else 'p1'
            nome_som_falta = "falta"
            # SEUENCIA DE EVENTOS ===================================================
            self.gerenciador_eventos.adicionar_espera()
            self.gerenciador_eventos.adicionar_fade_in()
            self.gerenciador_eventos.adicionar_som(nome_som_falta,volume=0.5)
            self.gerenciador_eventos.adicionar_ator_set_visibilidade('falta',valor=True)
            
            self.gerenciador_eventos.adicionar_espera(2000)
            
            self.gerenciador_eventos.adicionar_espera(1000)
            self.gerenciador_eventos.adicionar_fade_out(1000, callback=self.reset)
            self.placar.adicionar_pontos(oponente,1)
                

            if self.placar.diferenca_maior_que(1):
                # self.gerenciador_eventos.adicionar_espera(1000)
                # self.gerenciador_eventos.adicionar_fade_out(1000)
                self.gerenciador_eventos.adicionar_espera(callback=self._mostrar_janela)
                self.gerenciador_eventos.adicionar_limpa_eventos()
                # return
                
                # self.gerenciador_eventos.adicionar_espera(10, callback=self.gerenciador_eventos.limpar_eventos())
            else:
                pass    
                

            return
        else:
            # se o ator 'largada' estiver visivel, então:
            if acao in (P1_HIT, P2_HIT):
                nome_jogador_atacando    = 'p1' if acao == P1_HIT else 'p2'
                nome_jogador_morto       = 'p2' if acao == P1_HIT else 'p1'
                # posicionamento e movimento
                deslocamento = +150 if nome_jogador_atacando == 'p1' else -150
                pos_msg      = (90, 50) if nome_jogador_atacando == 'p1' else (WIDTH - 80, 50)
                # Som de ataque aleatório
                nome_som = "ataque1" if random.randint(0, 1) == 0 else "ataque2"
                # SEUENCIA DE EVENTOS ===================================================
                self.gerenciador_eventos.adicionar_espera()
                self.gerenciador_eventos.adicionar_som(nome_som,volume=0.5)
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
                tempo_reacao = pygame.time.get_ticks() - self.mostrar_tempo_largada()
                
                print(pygame.time.get_ticks())
                # print(self.tempo_atual)
                tempo_str = f"{tempo_reacao / 1000:.3f}s"
                self.notificador.adicionar_mensagem(f"{nome_jogador_atacando.upper()} acertou!",  500, *pos_msg)
                self.notificador.adicionar_mensagem(f"{tempo_str}",                 1000, *pos_msg)

                self.gerenciador_eventos.adicionar_espera(1000)
                self.gerenciador_eventos.adicionar_espera()
                self.gerenciador_eventos.adicionar_ator_set_visibilidade('largada',False)
                self.gerenciador_eventos.adicionar_espera(1000)
                

                if self.placar.diferenca_maior_que(1):
                    self.gerenciador_eventos.adicionar_espera(1000)
                    # self.gerenciador_eventos.adicionar_espera(1000)
                    self.gerenciador_eventos.adicionar_fade_out(1000,callback=self._mostrar_janela)
                    # self.gerenciador_eventos.adicionar_espera(1000,callback=self.gerenciador_janelas.adicionar_janela('rematch',janela_rematch,ativa=False))
                    # self.gerenciador_eventos.adicionar_espera(1000)
                    # self.gerenciador_eventos.adicionar_espera(1000,callback=self.gerenciador_janelas.ativar('rematch'))
                    # self.gerenciador_janelas.adicionar_janela('rematch',
                    #                                             JanelaSelecionavel(["Continuar","Revanche","Sair"], x=130,y=10),
                    #                                             ativa=True)
                    
                    # self.gerenciador_eventos.adicionar_fade_out(1000, callback=self.gerenciador_janelas.adicionar_janela('rematch',JanelaSelecionavel(['Revanche',"Continuar","Sair"],120,20),ativa=True))
                    # self.gerenciador_eventos.adicionar_espera(10, callback=self.gerenciador_eventos.limpar_eventos())
                else:
                    self.gerenciador_eventos.adicionar_espera(1000)
                    self.gerenciador_eventos.adicionar_fade_out(1000, callback=self.reset)
                    # self.gerenciador_janelas.adicionar_janela('rematch',
                

    def _mostrar_janela(self):
        janela_rematch = JanelaSelecionavel(["Continuar","Revanche","Sair"],
                                            x=135,y=135)                                                                                  
        self.gerenciador_janelas.adicionar_janela('rematch',janela_rematch,ativa=True)
    def _salvar_tempo_largada(self):
        self.tempo_largada = pygame.time.get_ticks()
        print("salvou tempo largada:", self.tempo_largada)

    def reset(self):
        # Lógica de reset da cena
        self.carregar_tudo()

    def atualizar(self,dt):
        super().atualizar(dt) #não tirar
        self.placar.atualizar(dt)
        self.notificador.atualizar()
        

    def draw(self,screen, offset):
        super().draw(screen,offset)
        self.gerenciador_atores.draw(screen,offset)
        self.placar.draw(screen)
        self.notificador.draw()

    def mostrar_tempo_largada(self):
        return self.tempo_largada