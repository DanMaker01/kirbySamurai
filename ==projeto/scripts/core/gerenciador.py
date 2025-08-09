
######################################################
# Gerenciador
######################################################
# Orquestra os sistemas modulares
######################################################
# Modular: Não.
# Finalizada: Não
######################################################
# A Fazer: 
# - Definir se o gereciador de atores fica na cena, no gerenciador de cena ou no gerenciador
# - Definir Responsabilidades do: Gerenciador_Cena, Gerenciador e Cenas.
# - Finalizar parte de Roteiro e chamada de paginas, testar condições
######################################################
# Pensar me implementar:
# - Inventario 
# - 
######################################################
import pygame
# core
from scripts.core.config                    import *
from scripts.core.evento                    import *
from scripts.core.persistencia              import Persistencia
from scripts.core.camera                    import Camera
from scripts.core.janela                    import Janela, JanelaSelecionavel
# sub-sistemas
from scripts.sistemas.gerenciador_controle  import Gerenciador_Controle
from scripts.sistemas.gerenciador_som       import Gerenciador_Som
from scripts.sistemas.gerenciador_variaveis import GerenciadorVariaveis
from scripts.sistemas.gerenciador_janelas   import GerenciadorJanelas
from scripts.sistemas.gerenciador_cenas     import Gerenciador_Cenas
from scripts.sistemas.gerenciador_eventos   import GerenciadorEventos
from scripts.sistemas.gerenciador_atores    import Gerenciador_Atores
from scripts.sistemas.gerenciador_tela      import GerenciadorTela
from scripts.cenas.cena01                   import Cena01
# UI
from scripts.ui.notificador                 import Notificador #tem que ficar aqui???
######################################################

######################################################
class Gerenciador:
    # def __init__(self, screen:pygame.Surface, clock):
    def __init__(self, screen:pygame.Surface):
        # ======================================================
        self.screen                 = screen
        # self.clock                  = clock
        
        self.tempo_atual            = pygame.time.get_ticks()#repete no update
        # ======================================================
        # Core
        self.memoria                = Persistencia()
        self.notificador            = Notificador(self.screen)
        self.camera                 = Camera(largura_tela=WIDTH, altura_tela=HEIGHT)
        # ======================================================
        # Subsistemas
        self.gerenciador_controle   = Gerenciador_Controle()
        self.gerenciador_som        = Gerenciador_Som()
        self.gerenciador_tela       = GerenciadorTela(iniciar_preto=True)
        self.gerenciador_janelas    = GerenciadorJanelas()
        self.gerenciador_variaveis  = GerenciadorVariaveis()
        self.gerenciador_atores     = Gerenciador_Atores() # passar pra dentro de cenas??? deixar aqui? o Ger_Evt necessita, ficará travado
        # ======================================================
        # Cria no gerenciador. 
        # quase todos gerenciadores serão passados. Passar gerenciador em si? #????
        self.gerenciador_eventos    = GerenciadorEventos(self.gerenciador_controle, 
                                                         self.gerenciador_som,
                                                         self.gerenciador_tela, 
                                                         self.gerenciador_atores,
                                                         self.camera)
        # ======================================================
        # Gerenciador Cenas deve ter parametros G_Eventos, Camera, ...  #???
        self.gerenciador_cenas      = Gerenciador_Cenas(self.gerenciador_atores,
                                                        
                                                        self.gerenciador_som,
                                                        self.gerenciador_eventos)
        # ======================================================
        self.gerenciador_cenas.registrar_cena('principal',Cena01(self.gerenciador_atores,
                                                                 self.gerenciador_eventos,
                                                                 self.gerenciador_som,
                                                                 self.gerenciador_variaveis,
                                                                 self.gerenciador_controle,
                                                                 self.gerenciador_tela,
                                                                 self.notificador,
                                                                 self.gerenciador_janelas))
        self.gerenciador_cenas.executar_cena('principal')
        self.reset()
        # ======================================================

    def reset(self):
        self.gerenciador_cenas.reiniciar_cena()

    def update(self, dt):
        self.tempo_atual = pygame.time.get_ticks()
        # if len(self.gerenciador_janelas.listar_ativas()) >= 1:
        
        # self.gerenciador_eventos.atualizar(self.tempo_atual) #??? vai p/ gerenciador_cenas
        # self.gerenciador_atores.update(dt) #??? vai para gerenciador_cenas
        self.gerenciador_cenas.update(dt)
        self.gerenciador_tela.atualizar(self.tempo_atual, dt)
        self.camera.atualizar(dt)       #??? vai ficar?
        
        # self.notificador.atualizar()    #??? vai ficar?
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
        self.gerenciador_cenas.draw(self.screen, (-self.camera.pos_x, -self.camera.pos_y)) # deve receber uma defasagem pela câmer
        self.gerenciador_tela.desenhar(self.screen)
        # =======================================================
        # Desenha UI
        
        self.gerenciador_janelas.desenhar(self.screen)
        # self.notificador.draw()
        # =======================================================

    def input(self, acao): #mover pra Cena ??? Acho que sim. Sim!

        
        # Handle active window input
        janela_ativa : JanelaSelecionavel = self.gerenciador_janelas.get('rematch')
        

        if not janela_ativa:
            self.gerenciador_cenas.input(acao)
            return
        else:
            self.gerenciador_eventos.limpar_eventos()
        
            # Handle navigation
            if acao in ['cima', 'esquerda']:
                janela_ativa.voltar()
            elif acao in ['baixo', 'direita']:
                janela_ativa.avancar()
            elif acao in [CONFIRM, P1_HIT, P2_HIT]:
                resultado = janela_ativa.selecionar()
                print("resultado:", resultado)
                
                # Handle menu actions
                if resultado == "Revanche":
                    self.gerenciador_janelas.resetar()
                    self.gerenciador_eventos.limpar_eventos()
                    self.gerenciador_eventos.adicionar_espera(callback=self.reset)
                    # self.gerenciador_eventos.adicionar_fade_out(1000, callback=self.reset)
                    cena :Cena01 = self.gerenciador_cenas.cena_atual
                    cena.placar.zerar_placar()
                    
                elif resultado == "Continuar":
                    self.gerenciador_janelas.resetar()
                    self.gerenciador_eventos.limpar_eventos()
                    self.gerenciador_eventos.adicionar_espera(callback=self.reset)
                    
                elif resultado == "Sair":
                    self.gerenciador_janelas.resetar()
                    print("Encerrando jogo...")
                    pygame.quit()

        

        return

