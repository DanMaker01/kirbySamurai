# ===========================================
# Gerenciador de Cenas
# ===========================================
# Responsabilidades:
# - Cuidar do gerenciador de eventos
# - Cuidar do gerenciador dos Atores?
# - 
# ===========================================
# A Fazer:
# - 
# - Definir se o gereciador de atores fica na cena, no gerenciador de cena ou no gerenciador
# - 
# ===========================================
# Possibilidades:
# - 
# - 
# 
# ===========================================

# from scripts.core.roteiro import Roteiro
from scripts.core.cena import Cena
from scripts.sistemas.gerenciador_atores import Gerenciador_Atores
from scripts.sistemas.gerenciador_eventos import GerenciadorEventos

class Gerenciador_Cenas:
    def __init__(self, gerenciador_atores, gerenciador_som,gerenciador_eventos):
        self.gerenciador_atores = gerenciador_atores
        self.gerenciador_som = gerenciador_som
        self.gerenciador_eventos = gerenciador_eventos
        self.cenas = {}               # nome -> Cena
        self.cena_atual_nome = None
        self.cena_atual = None

    def registrar_cena(self, nome, cena):
        if nome in self.cenas:
            print(f"[AVISO] Cena '{nome}' já registrada. Sobrescrevendo.")
        self.cenas[nome] = cena

    def executar_cena(self, nome):
        cena : Cena = self.cenas.get(nome)
        if not cena:
            print(f"[Cena] Cena '{nome}' não registrada.")
            return

        self.cena_atual_nome = nome
        self.cena_atual = cena
        # print("nome cena:", nome)
        # # print("executar cena:", cena)
        # # print(cena.roteiros)
        
        # # print("Ev ativos:",self.gerenciador_eventos.eventos_ativos)
        print("roteiros encontrados:",self.cena_atual.roteiros)
        pass        
        
    


    def chamar_roteiro(self, nome_roteiro): # ??? implementar mais
        if not self.cena_atual:
            print("[Cena] Nenhuma cena ativa.")
            return

        pagina_condicionada = self.cena_atual.chamar_roteiro(nome_roteiro)
        if pagina_condicionada:
            print("pagina condicionada:")
            print(pagina_condicionada)
        else:
            print("Não há nenhuma pagina neste roteiro:",nome_roteiro)

    def reiniciar_cena(self):
        if self.cena_atual:
            self.cena_atual.carregar_tudo()

    # def resetar_cena(self):
    #     self.cena_atual_nome = None
    #     self.cena_atual = None
    #     self.cenas.clear()

    def update(self, dt):
        # self.cena_atual: Cena
        self.cena_atual.atualizar(dt)
        # self.gerenciador_eventos.atualizar(dt)
        # self.gerenciador_atores.update(dt)

    def is_esperando(self):
        # return self.gerenciador_eventos.is_esperando()
        pass

    def is_em_fade(self):
        # return self.gerenciador_eventos.is_em_fade()
        pass
    
    def draw(self, screen, camera_offset):
        self.cena_atual.draw(screen,camera_offset)
        # self.gerenciador_atores.draw(screen, camera_offset)
        # for ator in self.gerenciador_atores.atores:
            # print("ATOR:",ator)

    def input(self, acao): 
        # parece que preciso dessas dependencias, ver se realmente devem estar aqui
        # ???
        # - gerenciador_janelas
        # - placar
        # - gerenciador_eventos
        # - gerenciador_controle ??? provavelmente não precisa desse
        # - gerenciador_som
        # - gerenciador_atores
        # - notificador
        if self.cena_atual:
            self.cena_atual.input(acao)

        pass
