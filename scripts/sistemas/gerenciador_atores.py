from scripts.atores.ator import Ator
from typing import Dict

class Gerenciador_Atores:
    """Gerencia instâncias de atores."""

    def __init__(self):
        self.atores = {}
        # Importa a classe Ator para que o tipo seja conhecido
        # (já feito na linha 1), mas para dicas de tipo:
        self.atores: Dict[str, Ator] = {}        

    def adicionar_ator(self, nome, ator):
        """Adiciona um ator ao gerenciador."""
        if ator:
            self.atores[nome] = ator

    def update(self, dt):
        """Atualiza todos os atores gerenciados."""
        for ator in self.atores.values():
            ator.update(dt)

    def draw(self, screen, offset= None):
        '''
        O offset é para facilitar o uso de uma câmera externa'''

        for ator in self.atores.values():
            # correção para offset
            ator.draw(screen, offset) 
        pass

    def pegar_ator(self, nome):
        """Retorna o ator com o nome especificado, ou None se não existir."""
        return self.atores.get(nome)