import os
import json
from ..config import CACHE_DIR

def garantir_diretorio_existe(diretorio=CACHE_DIR):
    """Garante que o diretório especificado existe."""
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
        print(f"Diretório '{diretorio}' criado com sucesso.")

def carregar_arquivo_json(caminho_arquivo):
    """Carrega dados de um arquivo JSON."""
    try:
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, 'r') as arquivo:
                return json.load(arquivo)
        return []
    except json.JSONDecodeError:
        print(f"Erro ao carregar o arquivo {caminho_arquivo}. Formato JSON inválido.")
        return []
    except Exception as e:
        print(f"Erro ao abrir o arquivo {caminho_arquivo}: {str(e)}")
        return []

def salvar_arquivo_json(caminho_arquivo, dados, indentacao=2):
    """Salva dados em um arquivo JSON."""
    try:
        with open(caminho_arquivo, 'w') as arquivo:
            json.dump(dados, arquivo, indent=indentacao)
        return True
    except Exception as e:
        print(f"Erro ao salvar o arquivo {caminho_arquivo}: {str(e)}")
        return False