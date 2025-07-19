
###########################################
# Persistência
###########################################
# Modular: Sim
# Finalizada: Sim
###########################################
# A Fazer:
# - Multiplos saves?
# - 
###########################################

import json
import os

class Persistencia:
    def __init__(self, nome_arquivo="save.json", endereco_arquivo="."):
        self.nome_arquivo = nome_arquivo
        self.endereco_arquivo = endereco_arquivo

    def _caminho_completo(self):
        return os.path.join(self.endereco_arquivo, self.nome_arquivo)

    def salvar(self, objeto):
        try:
            with open(self._caminho_completo(), 'w', encoding='utf-8') as f:
                json.dump(objeto, f, ensure_ascii=False, indent=4)
            print(f"[✔] Dados salvos em {self._caminho_completo()}")
        except Exception as e:
            print(f"[✖] Erro ao salvar: {e}")

    def carregar(self):
        try:
            with open(self._caminho_completo(), 'r', encoding='utf-8') as f:
                objeto = json.load(f)
            print(f"[✔] Dados carregados de {self._caminho_completo()}")
            return objeto
        except FileNotFoundError:
            print(f"[!] Arquivo não encontrado: {self._caminho_completo()}")
            return None
        except Exception as e:
            print(f"[✖] Erro ao carregar: {e}")
            return None
