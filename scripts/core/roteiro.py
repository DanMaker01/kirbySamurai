
# #################################################################
# Roteiro
# #################################################################
# Modular: Sim
# Finalizada: Não
# #################################################################
# A Fazer:
# - 
# - Verificar se descobrir_pg_sera_ativa está bom
# - 
##################################################################
import operator
import re
from scripts.core.pagina import Pagina
class Roteiro:
    def __init__(self):
        self.lista_paginas = [] #vir com padrão

    def adicionar_pagina(self, condicao=None, lista_eventos=None):
        self.lista_paginas.append(Pagina(condicao, lista_eventos))

    def remover_pagina(self, condicao):
        self.lista_paginas = [p for p in self.lista_paginas if p.condicao != condicao]

    def get_pagina(self, condicao):
        for pagina in self.lista_paginas:
            if pagina.condicao == condicao:
                return pagina
        return None

    def descobrir_qual_pagina_deve_ser_rodada(self, variaveis):
        """
        Avalia condições tipo 'vida>=10' com base nas variáveis fornecidas.
        Retorna a última página cuja condição é satisfeita.
        """
        pagina_escolhida = None
        for pagina in self.lista_paginas:
            pagina:Pagina
            if self._avaliar_condicao(pagina.condicao, variaveis):
                pagina_escolhida = pagina
        return pagina_escolhida

    def _avaliar_condicao(self, condicao, variaveis):
        """
        Avalia uma expressão do tipo 'var>=10' usando operadores seguros.
        """
        if condicao == 'padrao':
            return True

        # Expressões suportadas: ==, !=, >=, <=, >, <
        operadores = {
            '==': operator.eq,
            '!=': operator.ne,
            '>=': operator.ge,
            '<=': operator.le,
            '>': operator.gt,
            '<': operator.lt,
        }

        # Regex para dividir: var operador valor
        match = re.match(r'^\s*(\w+)\s*(==|!=|>=|<=|=|<|>)\s*(-?\w+)\s*$', condicao)
        if not match:
            print(f"Condição malformada: {condicao}")
            return False

        var, op_str, val_str = match.groups()

        # Converte valor (int, float, ou string bool)
        val = self._interpretar_valor(val_str)
        var_val = variaveis.get(var, None)

        if var_val is None:
            return False  # variável não definida

        try:
            return operadores[op_str](var_val, val)
        except Exception:
            return False

    def _interpretar_valor(self, val_str):
        """Converte string para int, float ou bool automaticamente."""
        if val_str.lower() == 'true':
            return True
        elif val_str.lower() == 'false':
            return False
        try:
            if '.' in val_str:
                return float(val_str)
            else:
                return int(val_str)
        except ValueError:
            return val_str  # trata como string literal
