##############################################################################
# Conjuntos dos estados de animação e um sistema de física simples
##############################################################################
# A Fazer:
# - Melhorar o sistema de posicao, unificar, criar get e set posicao. 
# - Pro draw é importante o anima.pos, pro resto é importante o fisica.pos
##############################################################################

from scripts.core.animacao import Animacao

# --------------------------------------------------------------------
class Ator:
    def __init__(self, animacoes=None, pos=(0.0, 0.0), escala=1.0, tintura=(255, 255, 255, 255), visivel=True   ):
        
        # componentes
        self.animacoes = ControladorAnimacoes(animacoes or {}, pos, escala)
        self.fisica = FisicaAtor(pos)

        # específico de arte (deixar aqui????????????)
        self.tintura = tintura

        # propriedades
        self.ativa = True

        # dialogo/colisao/etc ?????? implementar
        # self.interagivel = False #quero manter
        self.set_visivel(visivel)

    def update(self, dt):
        if not self.ativa:
            return

        #pensar nessa ordem (??????????????????)
        self.animacoes.update(dt)
        self.fisica.processar(dt)
        self.animacoes.set_pos(*self.fisica.posicao) #a física vem primeiro, corrigir posicao nas animções

    def draw(self, screen, offset=(0,0)):
        if not self.ativa:
            return
        self.animacoes.draw(screen, tintura=self.tintura, offset=offset)
    
    def set_posicao(self,x,y):
        self.animacoes.pos=(x,y)
        self.fisica.posicao=(x,y)

    def set_visivel(self, is_visible):
        self.animacoes.set_visivel(is_visible)
    
    def get_visivel(self):
        return self.animacoes.visivel
# --------------------------------------------------------------------
# ????? implementar:
# - atualiza_pos (sempre que o ator atualizar)
#
#

class ControladorAnimacoes:
    def __init__(self, animacoes: dict[str, Animacao], pos, escala):
        self.animacoes: dict[str, Animacao] = animacoes
        self.animacao_atual = 0  # índice da lista de chaves
        self.pos = pos # depende da posição dos 
        self.escala = escala
        self.aplicar()
        self.visivel = True

    def aplicar(self):
        '''Aplica posição e escala às animações'''
        
        for anim in self.animacoes.values():
            anim.set_pos(*self.pos)
            anim.set_escala(self.escala)

    def update(self, dt):
        if self.animacoes:
            nome = list(self.animacoes.keys())[self.animacao_atual]
            self.animacoes[nome].update(dt)

    def draw(self, screen, tintura, offset=(0, 0)):
        if self.animacoes and self.visivel:
            nome = list(self.animacoes.keys())[self.animacao_atual]
            anim = self.animacoes[nome]
            if anim.ativa:
                anim.draw(screen, tintura, offset=offset)

    def set_pos(self, x, y):
        self.pos = (x, y)
        self.aplicar()

    def set_escala(self, escala):
        self.escala = escala
        self.aplicar()

    def adicionar(self, nome, animacao):
        if nome in self.animacoes:
            raise ValueError(f"Animação '{nome}' já existe.")
        self.animacoes[nome] = animacao
        self.aplicar()

    def remover(self, nome):
        if nome in self.animacoes:
            del self.animacoes[nome]

    def reset(self):
        for anim in self.animacoes.values():
            anim.reset()

    def stop(self):
        for anim in self.animacoes.values():
            anim.stop()

    def trocar(self, nome):
        if nome in self.animacoes:
            self.animacao_atual = list(self.animacoes.keys()).index(nome)
            self.animacoes[nome].reset()

    def trocar_vel(self, nome, nova_vel):
        if nome in self.animacoes:
            self.animacoes[nome].vel_anima = nova_vel

    def atual_nome(self):
        if not self.animacoes:
            return None
        return list(self.animacoes.keys())[self.animacao_atual]
    
    def set_visivel(self, valor):
        self.visivel = valor

class FisicaAtor:
    def __init__(self, pos):
        self.posicao = pos
        self.vel = (0.0, 0.0)

    def processar(self, dt):
        if self.vel:
            x = self.posicao[0] + self.vel[0] * dt
            y = self.posicao[1] + self.vel[1] * dt
            self.posicao = (x, y)

    def set_vel(self, vel_x, vel_y):
        self.vel = (vel_x, vel_y)


# --------------------------------------------------------------------