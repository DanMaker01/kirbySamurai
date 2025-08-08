# ====================================================
# Cena (base) (classe abstrata)
# ====================================================
# Modular: Sim
# Finalizada: Não
# ====================================================
# À fazer:
# - Preciso gerenciador_atores, eventos e som?
# - Atores - ok
# - Eventos - ok
# - Som #???
# - 
# - 
# ====================================================
# Feito:
# - 
# - 
# ====================================================
import pygame
from scripts.core.roteiro import Roteiro
from scripts.sistemas.gerenciador_atores import Gerenciador_Atores
from scripts.sistemas.gerenciador_eventos import GerenciadorEventos

class Cena:
    def __init__(self, gerenciador_atores, gerenciador_eventos, gerenciador_som, gerenciador_variaveis):
        self.gerenciador_atores = gerenciador_atores
        self.gerenciador_eventos = gerenciador_eventos
        self.gerenciador_som = gerenciador_som
        self.gerenciador_variaveis = gerenciador_variaveis

        self.roteiros = {}  # nome -> Roteiro

    def _carregar_atores(self):
        # print("método abstrato necessário, deve ser implementado pela classe filha.)
        pass

    def _carregar_som(self):
        # print("método abstrato necessário, deve ser implementado pela classe filha.)       
        pass

    def _carregar_roteiros(self):
        # print("método abstrato necessário, deve ser implementado pela classe filha.)
        pass

    # def _carregar_eventos_iniciais(self): # excluir, Roteiro o fará.
    #     # print("método abstrato necessário, deve ser implementado pela classe filha.)
    #     pass

    def input(self, acao):
        # print("métod abstrato necessário, deve ser implementado pela classe filho.")
        pass

    def carregar_tudo(self):
        print("carregar tudo")
        self._carregar_atores()
        self._carregar_som()
        self._carregar_roteiros()
        # self._carregar_eventos_iniciais() #provavelmente vai sair

    def adicionar_roteiro(self, nome, roteiro: Roteiro):
        self.roteiros[nome] = roteiro

    def chamar_roteiro(self, nome_roteiro):
        print("chamar roteiro:",nome_roteiro)
        roteiro : Roteiro = self.roteiros.get(nome_roteiro)
        if not roteiro:
            print(f"[Cena] Roteiro '{nome_roteiro}' não encontrado.")
            return
        print("roteiro:",roteiro, "chamado.")

        pagina = roteiro.descobrir_qual_pagina_deve_ser_rodada(self.gerenciador_variaveis)
        # print("pagina a ser :",pagina)
        if pagina:
            # pagina.executar(self.gerenciador_eventos)
            return pagina
        else:
            print(f"[Cena] Nenhuma página válida para o roteiro '{nome_roteiro}'.")

    def atualizar(self, dt):
        # isso aqui é evidencia de que a gerenciador atores e gerenciador eventos devem ficar dentro da Cena
        self.gerenciador_atores : Gerenciador_Atores
        self.gerenciador_eventos : GerenciadorEventos

        # print("ok")
        self.gerenciador_eventos.atualizar(pygame.time.get_ticks())
        self.gerenciador_atores.update(dt)
        
    def draw(self, screen, offset): 
        # método abstrato necessário, draw deve ser implementado pela classe filha.
        pass