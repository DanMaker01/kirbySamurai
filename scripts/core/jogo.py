###########################################
# Jogo
###########################################
# Classe que controla o Loop principal
# Também controla o tamanho da janela, ícone, título
###########################################
# Modular: Sim
# Finalizada: Não
###########################################
# A Fazer:
# - Pensar onde colocar esse clock, melhor jogar para o gerenciador?
# - 
###########################################



import pygame
import sys
from scripts.core.config import *
# from scripts.ui.ui import GameUI
from scripts.core.input_controller import InputController
from scripts.core.gerenciador import Gerenciador

# Sistema Principal
class Jogo:
    def __init__(self):
        pygame.init()
        self.running = False
        self._inicializar_janela()
        self._criar_componentes()

    def _inicializar_janela(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Kirby Samurai")
        pygame.display.set_icon(pygame.Surface((1, 1)))

    def _criar_componentes(self):
        self.clock = pygame.time.Clock() #pra que serve? #???
        self.input_controller = InputController()
        self.gerenciador = Gerenciador(self.screen)

    def rodar(self):
        self.running = True
        print("iniciando jogo...")
        while self.running:
            self.handle_events()
            #loop principal
            self.gerenciador.update( self.clock.get_time() / 1000.0 )
            self.gerenciador.draw()
            pygame.display.flip()

            self.clock.tick(60)
        #finalizar jogo
        self._encerrar()

    #input
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
                self._encerrar()

            result = self.input_controller.process_event(event)
            if result:
                if result['binding'] != None and result['event']=='keydown': # se tiver binding
                    # print(result)
                    self.gerenciador.input(result["binding"])
                    
                # elif result['event']== 'keydown': #para mostrar apenas quando apertar
                #     #sempre que não tiver binding para esta tecla e não tiver largando-a 
                #     print(f"tecla {result['key']} sem função definida.")
                    
    def _encerrar(self):
        print("...encerrando jogo.")
        pygame.quit()
        sys.exit()
