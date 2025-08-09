
class Gerenciador_Controle:
    """Gerencia o controle, locks, etc."""

    def __init__(self):
        self.input_lock = False        

    def update(self, dt):
        pass

    def draw(self, screen, offset= None):
        pass

    def set_input_lock(self, valor):
        self.input_lock = valor